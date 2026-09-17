import json, pathlib

C = []
def md(s): C.append({'cell_type':'markdown','metadata':{},'source':s.strip('\n').splitlines(keepends=True)})
def code(s): C.append({'cell_type':'code','execution_count':None,'metadata':{},'outputs':[],
                       'source':s.strip('\n').splitlines(keepends=True)})

md(r'''
# 🧪 The Tyro Wash Test — Track A starter

**Team Dark.Tyro · FIT5230 Theme 2 (Text-to-Image), Dark side**

> **Protect 10 faces so our purifier cannot wash the protection off — without wrecking the photographs.**

### Three cells. You only edit one.

1. **Setup** — installs, and loads the image pack.
2. **`protect()`** ← **the only cell you change.**
3. **Run** — protects all 10, checks your perceptual cost, writes the zip to send us.

Leave everything at its defaults and you already have a valid entry. Then change one number and
it is *your* entry. You never need to read our attack code, and you do not have to tell us how
your shield works — our purifier never inspects the perturbation.

### How you are scored — two axes, both published

| axis | meaning | you want |
|---|---|---|
| **`R_pipe`** | how much of the editing pipeline our wash restored. 1.0 = we stripped you completely, 0 = your shield held | **low** |
| **LPIPS(protected, clean)** | how much of the photograph you destroyed to get there | **low**, and **≤ 0.10** to be ranked |

Two axes, because with robustness alone the winning move is trivial: perturb until the picture is
noise. Nothing can be washed off a ruined photo — but nothing can be **edited** either, so that
"defence" defeats its own purpose. It lands in the top-right corner of the plot, in public.

**Round 1 closes 18 September 2026.** Past the date? Send it anyway — we score late entries and
report them in our Milestone 3 presentation.
''')

code(r'''
#@title 1 · Setup — installs, GPU check, and the image pack  (~60 s on a fresh Colab)
import subprocess, sys, importlib.util, os, time, pathlib, zipfile
for mod, pkg in {'diffusers': 'diffusers', 'lpips': 'lpips'}.items():
    if importlib.util.find_spec(mod) is None:
        subprocess.run(f'{sys.executable} -m pip install -q {pkg}', shell=True, check=False)

import torch, numpy as np
from PIL import Image

DEV = 'cuda' if torch.cuda.is_available() else 'cpu'
ALLOW_SLOW_CPU = False          # route C on CPU is ~4 min per image. Set True only if you must.
print('device:', DEV, '|', torch.cuda.get_device_name(0) if DEV == 'cuda' else 'CPU only')
if DEV == 'cpu':
    print('  -> routes "none" and "noise" work fine. For "photoguard": Runtime > Change runtime type > T4 GPU.')

# --- the image pack -------------------------------------------------------------------
PACK = pathlib.Path('tyro_wash_test_trackA')
OUT  = pathlib.Path('my_submission')

if not (PACK / 'clean').is_dir():
    z = pathlib.Path('tyro_wash_test_trackA.zip')
    if not z.exists():
        try:
            from google.colab import files
            print('\nUpload tyro_wash_test_trackA.zip (the pack we sent you):')
            z = pathlib.Path(next(iter(files.upload())))
        except ImportError:
            raise SystemExit('Put tyro_wash_test_trackA.zip in this folder and re-run.')
    zipfile.ZipFile(z).extractall('.')
    print(f'unpacked {z.name}')

assert (PACK / 'clean').is_dir(), f'no clean/ folder under {PACK.resolve()}'
NAMES = sorted(os.listdir(PACK / 'clean'))
OUT.mkdir(exist_ok=True)
print(f'\n{len(NAMES)} images ready in {PACK}/clean  (masks in {PACK}/mask)')
print('your output ->', OUT.resolve())
''')

md(r'''
---
## The reference shield — 30 seconds of theory, then the code

Stable Diffusion never sees your photograph. It first squeezes the image through a VAE encoder
into a small latent code, and edits *that*. So the cheapest sabotage is to make the encoder read
the wrong thing.

> The editor reads a **summary** of your photo, not the photo. This attack rewrites the summary —
> nudging pixels, invisibly, until the encoder describes a flat grey rectangle instead of a face.
> The editor then confidently repaints something that was never there.

It is projected gradient descent with every pixel held inside an `EPS`-sized box, so the change
stays subtle. **`EPS` is your main dial:** bigger = harder to wash off, and more visible.

*You can skip the next cell entirely — just run it.*
''')

code(r'''
#@title 2 · The PhotoGuard encoder attack (route "photoguard"). Loads a VAE once, ~10 s per image after.
VAE_ID = 'stable-diffusion-v1-5/stable-diffusion-inpainting'   # the SAME VAE our scorer's editor uses
_vae = None

def _get_vae():
    global _vae
    if _vae is None:
        from diffusers import AutoencoderKL
        try:
            _vae = AutoencoderKL.from_pretrained(VAE_ID, subfolder='vae')
            print('vae:', VAE_ID)
        except Exception as e:
            print(f'!! could not load {VAE_ID}: {e}')
            print('!! falling back to stabilityai/sd-vae-ft-mse -- a DIFFERENT autoencoder from the')
            print('!! one our scorer edits with, so your shield becomes a cross-model attack.')
            print('!! Tell us if you submit from this path; we will report it as such.')
            _vae = AutoencoderKL.from_pretrained('stabilityai/sd-vae-ft-mse')
        _vae = _vae.to(DEV).eval().requires_grad_(False)
    return _vae

def photoguard_encoder(img, eps_levels=4, step_levels=1, iters=100):
    """PGD on the VAE encoder, dragging the latent toward the latent of flat grey.
       eps_levels / step_levels are in 0-255 grey levels: EPS=16 means never move a pixel
       more than 16 of 255 -- about 6%, and invisible on a photograph."""
    if DEV == 'cpu' and not ALLOW_SLOW_CPU:
        raise RuntimeError('Route "photoguard" on CPU is ~4 MIN PER IMAGE (~45 min for the pack).\n'
                           '  -> Runtime > Change runtime type > T4 GPU, then re-run from the top.\n'
                           '  -> or set ALLOW_SLOW_CPU = True in cell 1 if you really want to wait.')
    vae = _get_vae()
    x0  = (torch.from_numpy(np.asarray(img.convert('RGB'), np.float32))
           .permute(2, 0, 1)[None].to(DEV) / 127.5 - 1.0)
    eps, step = eps_levels / 127.5, step_levels / 127.5
    with torch.no_grad():
        target = vae.encode(torch.zeros_like(x0)).latent_dist.mean      # grey = 0 in [-1, 1]
    x = x0.clone()
    for _ in range(iters):
        x.requires_grad_(True)
        loss = (vae.encode(x).latent_dist.mean - target).norm()
        g    = torch.autograd.grad(loss, x)[0]
        x    = (x.detach() - step * g.sign()).clamp(x0 - eps, x0 + eps).clamp(-1, 1)
    a = ((x[0].permute(1, 2, 0).cpu().numpy() + 1) * 127.5).round().clip(0, 255)
    return Image.fromarray(a.astype(np.uint8))

print('ready')
''')

md(r'''
---
## ✏️ 3 · YOUR ENTRY — the only cell you have to change

`protect()` takes one clean 512×512 image and its mask, and returns your protected image, same
size, same mode. Nothing else cares how you do it.

**The mask is given to you because it is given to us too** — it is an input to the editing
pipeline, not secret knowledge. White = the region the editor keeps. Black = the region it
repaints from scratch. Use it or ignore it.
''')

code(r'''
#@title protect()  <-- EDIT THIS
SHIELD = 'photoguard'      #@param ['none', 'noise', 'photoguard']
EPS    = 3                 #@param {type:'integer'}
# EPS is in grey levels, and it bites harder than it looks: it is a per-pixel CEILING and PGD
# pushes most pixels to it, so cost climbs faster than EPS. Measured on this pack (route
# "photoguard"): EPS 3 -> LPIPS ~0.07 (ranked) · EPS 4 -> 0.104 (over by 0.004) · EPS 16 -> 0.415.
# Per-image LPIPS at EPS=4 ranged 0.039 to 0.152 -- a 4x spread at identical settings, so read
# the mean printed by cell 4 rather than trusting one face.

def protect(img, mask):
    """img: PIL RGB 512x512 (clean).  mask: PIL RGB 512x512.  returns: PIL RGB 512x512."""

    # route "none" -- no shield. The control: proves the interface works, in seconds, no GPU.
    if SHIELD == 'none':
        return img

    # route "noise" -- random perturbation. No GPU, no model. A real (weak) baseline, and it
    # asks a fair question: at matched perceptual cost, does STRUCTURED beat RANDOM?
    if SHIELD == 'noise':
        a = np.asarray(img, np.float32)
        a = a + np.random.default_rng(0).normal(0, EPS / 8, a.shape)
        return Image.fromarray(a.clip(0, 255).astype(np.uint8))

    # route "photoguard" -- the encoder attack above. Needs a GPU. ~10 s/image.
    if SHIELD == 'photoguard':
        return photoguard_encoder(img, eps_levels=EPS)

    raise ValueError(SHIELD)

print(f'shield = {SHIELD}, eps = {EPS} levels')

# ----------------------------------------------------------------------------------------
# Ideas, if you want to go past the reference shield:
#   * spend the budget INSIDE the white mask -- the only region the editor keeps
#   * aim the encoder at a target that is not grey (another face, pure texture)
#   * make it wash-resistant: re-run the attack on a JPEG'd / blurred copy each step
#   * randomise across steps so no single fixed filter can subtract it
# ----------------------------------------------------------------------------------------
''')

md(r'''
---
## 4 · Run it, check it, pack it

One cell: protects all 10, prints the same LPIPS we will compute, and writes the zip to send us.
Over the budget? You are still plotted and discussed — just not ranked.
''')

code(r'''
#@title Protect all 10 -> self-check -> zip
import lpips
BUDGET = 0.10
net = lpips.LPIPS(net='alex').to(DEV).eval()      # must match the scorer: alex, not vgg
_t = lambda a: (torch.from_numpy(np.asarray(a, np.float32).transpose(2, 0, 1)[None]).to(DEV) / 127.5 - 1)

t0, vals = time.time(), []
print(f'  {"image":<24}{"LPIPS":>9}')
for i, n in enumerate(NAMES, 1):
    img  = Image.open(PACK / 'clean' / n).convert('RGB')
    mask = Image.open(PACK / 'mask'  / n).convert('RGB')
    out  = protect(img, mask)
    assert out.size == (512, 512), f'{n}: protect() returned {out.size}, must be (512, 512)'
    out.convert('RGB').save(OUT / n)
    with torch.no_grad():
        l = float(net(_t(out), _t(img)).item())
    vals.append(l)
    print(f'  {n:<24}{l:>9.4f}   [{i:>2}/{len(NAMES)}] {time.time()-t0:5.0f}s', flush=True)

m = float(np.mean(vals))
print(f'\n  mean LPIPS = {m:.4f}   budget = {BUDGET}   ({(time.time()-t0)/60:.1f} min total)')
print('  -> INSIDE the budget. You will be ranked.' if m <= BUDGET else
      '  -> OVER the budget. Plotted and discussed, but not ranked. Lower EPS.')

zp = pathlib.Path('tyro_wash_test_submission.zip')
with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in NAMES: z.write(OUT / n, n)
print(f'\n  packed -> {zp.resolve()} ({zp.stat().st_size/1e6:.1f} MB). Send us this file.')
''')

md(r'''
---
## What happens next

We run our IMPRESS-based purifier over your 10 images, then edit **clean**, **protected** and
**purified** with an identical prompt, seed and mask, and publish both axes as one scatter plot
with your dot labelled.

**Every outcome gets published, including ours losing.** Our purifier is deliberately *blind* — it
never inspects your perturbation, so if your shield defeats it, that is a real result about IMPRESS
and we will report it as one.

### One honest guard rail: a shield can be too quiet to measure

If your shield does not measurably disturb the edit, `R_pipe` becomes a ratio of two near-zero
numbers. We then report **"shield did not engage"** and show you what we measured, rather than
printing a flattering ratio.

The bar is in the pack as **`seed_floor_10.json`** — one number per image, measured as how far
apart two *innocent* edits of the same clean photo land with no protection anywhere. It runs from
**0.285 to 0.707** across the ten, so the images are not equally hard; that is the editor, not a
design choice. We rank on **how many of the ten engaged** and publish per-image numbers, never a
single mean over ten images of unequal difficulty.

**We apply this to ourselves first, and it stings:** our own PhotoGuard reference sits at
0.584 / 0.610 — *above* several of those floors. A quiet shield is a genuine failure mode, not a
scoring trick.

### Calibration — measured on this pack, so you can see the room you have

| | LPIPS vs clean (mean of 10) | ranked? |
|---|---|---|
| **your** route "noise", EPS 16 | 0.019 | yes |
| **your** route "photoguard", EPS 3 *(default)* | ~0.07 | yes |
| **your** route "photoguard", EPS 4 | 0.104 | no — over by 0.004 |
| **your** route "photoguard", EPS 16 | 0.415 | no — far over |
| *our shield, for scale* (IMPRESS L2 attack — **not** the same attack as above) | 0.017 | — |
| *our baseline purifier's output* | 0.150 | — |
| *our M2 masked purifier's output* | **0.038** | — |

Read three things off that. **The budget is generous:** our own shield spends 0.017, six times
under the cap, so you may build something far more aggressive than PhotoGuard and still be ranked.
**Our attack costs more than the shield it removes** — 0.150 against 0.017 for the baseline. And
**our M2 method cuts that to 0.038**, a 74% reduction, which is the result we are defending. If
your shield forces us to spend more again, say so: that is a result in your favour and we publish
it.

**The budget is an anchor, not a cliff.** We rank on the mean of your ten, and an entry a hair
over is still plotted, discussed and written up — we are not excluding a real defence over 0.004.

---

*Questions, or to submit: reply on our Ed thread.*
''')

nb = {'cells': C, 'metadata': {'accelerator': 'GPU', 'colab': {'provenance': []},
      'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
      'language_info': {'name': 'python'}}, 'nbformat': 4, 'nbformat_minor': 0}

p = pathlib.Path.home() / 'mnt/5230-Assignment/M2/challenge/Tyro_Wash_Test_STARTER.ipynb'
p.write_text(json.dumps(nb, indent=1, ensure_ascii=False))
print('wrote', p, len(C), 'cells')
