# Tyro Wash Test — Track A image pack

**Dark.Tyro** · FIT5230 Theme 2 (Text-to-Image), Dark side · Milestone 1

> **Your task: protect these 10 faces so our purifier cannot wash the protection off —
> without wrecking the photographs.**

---

## What is in here

| | |
|---|---|
| `clean/` | 10 face photographs, **512 × 512 RGB PNG** |
| `mask/` | the matching inpainting masks, same filenames, same size |
| `manifest.json` | filenames, original resolutions, checksums |
| `check_submission.py` | run this on your output before you send it |

Source: the Helen face subset released with PhotoGuard and reused by IMPRESS. We take
`sorted(os.listdir(clean))[:10]` — the same selection rule our notebook uses, so these are
literally the images our published results were computed on.

## ⚠️ Why 512 × 512, and why you should not resize

The originals are 2736×3582, 4000×3000 and so on. Every IMPRESS entry point does exactly this
before touching an image:

```python
Image.open(path).convert('RGB').resize((512, 512))   # PIL default resample = BICUBIC
```

So the 512×512 file in `clean/` **is the tensor the pipeline actually conditions on** — not a
convenience thumbnail. We publish it rather than the original on purpose: if you protect a
full-resolution photo and we downsample it afterwards, the resize destroys part of your
perturbation and we would be measuring interpolation instead of your defence. That mistake
cost us a whole afternoon of diagnostics, so we are not going to make you repeat it.

**Protect these files as they are. Do not upsample, resize, re-crop or re-encode as JPEG.**

## How to submit

Return **10 PNGs, 512 × 512, exactly these filenames.** That is the whole interface.

You do not have to tell us how you protected them. PhotoGuard at any strength, Glaze, Mist,
diffusion-based watermarking, or something you invented — our purifier never inspects the
perturbation, so it makes no difference to us.

```bash
python check_submission.py  path/to/your_protected_folder
```

Checks filenames, size and mode, prints SSIM/PSNR against our clean images, and — if you have
`torch` and `lpips` installed — your LPIPS and whether you are inside the ranking budget.

## How you will be scored

Two axes, both published, as one scatter plot:

| axis | meaning | you want |
|---|---|---|
| **`R_pipe` = (SSIM_pur − SSIM_adv) / (1 − SSIM_adv)** | how much of the editing pipeline our wash restored. 1.0 = fully stripped, 0 = your shield held | **low** |
| **LPIPS(protected, clean)** | how much of the photograph you destroyed to achieve it | **low** |

**Why two axes.** With robustness alone the winning move is trivial: perturb until the image
is visible noise. Nothing can be washed off a ruined photo — but nothing can be *edited*
either, so that "defence" defeats its own purpose. A shield that wins by wrecking the picture
lands in the top-right corner of the plot, in public.

**Ranking budget: LPIPS(protected, clean) ≤ 0.10.** The number is taken from `pur_eps = 0.1`,
the LPIPS allowance in IMPRESS's own objective — though in fairness that is a soft hinge
weighted at `pur_alpha = 0.01`, not a hard cap, so treat it as an anchor rather than a
symmetry claim.

**Here is the calibration, measured on `1233476865_1.png` from this pack**, so you can see how
much room you actually have:

| image | SSIM vs clean | PSNR | mean abs. difference |
|---|---|---|---|
| PhotoGuard, `pg_iters=40, grad_reps=2, eps=16` | 0.9888 | 38.6 dB | 0.93 levels |
| PhotoGuard, `pg_iters=200, grad_reps=2, eps=16` | 0.9773 | 37.4 dB | 1.30 levels |
| **our IMPRESS purifier's output** | **0.7790** | **31.3 dB** | **5.24 levels** |
| crude uniform noise, ±25 levels | 0.4635 | 25.2 dB | 11.8 levels |

Two things to read off that table. First, the reference defence is genuinely subtle — about
one grey level — so the budget is **generous**: you have room for a far more aggressive shield
than PhotoGuard and will still be ranked. Second, **our purifier moves the image roughly four
times further than the shield it removes.** We are not hiding that; it is the most interesting
weakness in our own attack, and if your shield forces us to spend even more, say so — that is
a result in your favour and we will publish it.

Over-budget entries are still plotted and discussed, just not ranked.

**Engagement gate.** If your shield does not measurably damage the edit, `R_pipe` becomes a
ratio of two near-zero numbers and means nothing. We report it only when
SSIM(edited-protected, edited-clean) ≤ 0.85. Otherwise we report **"shield did not engage"**
and show you what we measured, rather than printing a flattering number.

## What we commit to

- **Every outcome is published, including ours losing.** Our purifier is deliberately blind.
  If your protection defeats it, that is a real result about IMPRESS and we report it as one.
- Results appear in our **Milestone 2 post, 18 September**. Submissions close then.

## No protection code yet? Start here

Our Colab has a working PhotoGuard protector you can run in one cell against this exact
folder. Change one parameter and you have an entry. You are welcome to beat us with our own
starter kit — that is the point of publishing it.

---

*Questions, or to submit: reply on our Ed thread.*
