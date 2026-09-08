# Trial Log — reading the IMPRESS × PhotoGuard results
*Thread A · 20 Aug 2026 (Week 4) · source read directly from `AAAAAAsuka/Impress` @ main*

This file answers three questions: **is the 3-panel figure a fair comparison, what does
each knob actually do, and which trial ships to Ed.**

---

## 1 · Verdict first

**The `pg_iters=200, grad_reps=2` trial is not a failure. It is your first interpretable
result, and it should be the M1 headline figure** — subject to one re-run (§5).

What the three images show:

| panel | what happened |
|---|---|
| **CLEAN** | face preserved, background regenerated into a plausible scene. The pipeline behaving normally. |
| **PROTECTED** | the face is a **detached oval with crazed, cracked skin**, floating over an aerial landscape. The generator could not read the face, so it painted a scene that does not connect to it. **The shield worked.** |
| **PURIFIED** | boy re-integrated — neck, hoodie, headphones, coherent body. **The shield was stripped.** |

Clean → broken → restored. That is the entire M1 story in three pictures, and Trial #1
(`pg_iters=40, grad_reps=2`) did not have it.

> Why it may have *felt* like a failure: the PROTECTED panel contains the most convincing
> *airplane* of the three. If you were asking "did the prompt work?", protected looks like
> the winner. But that is the wrong question — see §4.

---

## 2 · Is the comparison fair? **Yes.** (verified in source)

This was the thing that could have sunk the figure, so it was checked line by line in
`pg_generate.py`.

```python
def test_image(image_dir, image_name, mask, save_dir, model, device, seed):
    np.random.seed(seed=seed); torch.manual_seed(seed); torch.cuda.manual_seed(seed)
    diff_image = model(prompt=args.prompt, image=image, mask_image=mask, eta=1,
                       num_inference_steps=args.test_diff_steps,
                       guidance_scale=args.test_guidance).images[0]
```

The RNG is **re-seeded immediately before each of the three generations**, with the same
`--manual_seed` (default 0), the same mask, the same prompt, the same guidance and the same
step count. So the initial noise and the whole sampling trajectory are byte-identical
across clean / protected / purified.

**Therefore every visible difference between the three panels is caused by the input image
alone.** That is exactly the controlled experiment you want, and it is worth one sentence in
the Ed post — most teams cannot say it.

### Which region is protected — worth knowing, it explains the pictures

Helen's mask is **inverted** (`ImageOps.invert`), then:

- `mask == 1` → the region the model **regenerates** (here: the background)
- `mask == 0` → the region the model **keeps and reads as context** (here: the face)
- the adversarial gradient is multiplied by `(1 - cur_mask)` → **the noise is written onto
  the face**, the part that is preserved
- `recover_image(..., background=True)` then puts original pixels back in the generated
  region and adversarial pixels in the context region

So PhotoGuard is not defacing the output. It is **poisoning the only part of the image the
model is allowed to look at.** Metaphor: it does not smash the painting, it smudges the
label the restorer reads before deciding what to paint. Everything downstream then goes
wrong — which is precisely the cracked-skin floating head you saw.

---

## 3 · TWO NEW BUGS (numbers 7 and 8 — extra "Initial Customization" evidence for M1)

### 🔴 Bug 7 — the purified folder name carries **no `pg_*` parameters**

`pg_mask_pur_helen.py`, line ~37:

```python
save_dir_pur = f"../helen_face/pur_eps{args.pur_eps}_pur_iters{args.pur_iters}" \
               f"_pur_lr{args.pur_lr}_pur_alpha{args.pur_alpha}_pur_noise{args.pur_noise}/"
```

Compare the protected folder, which *does* encode them:

```python
adv_dir = f"../helen_face/adv_{attack_type}_eps{pg_eps}_step{pg_step_size}" \
          f"_iter{pg_iters}grad_reps{pg_grad_reps}_eta{pg_eta}..."
```

All three of your trials used identical `pur_*` settings
(`0.1 / 100 / 0.005 / 0.01 / 0.05`). **So all three wrote their purified images into one and
the same folder, silently overwriting each other.** There is no skip-if-exists guard in the
purify stage, and `pg_generate.py` and `pg_metric.py` both read that folder blind.

Consequences, in order of nastiness:

1. **If you ever ran 8a (protect) at a new strength and then jumped to 8c (generate) without
   re-running 8b (purify), your PURIFIED panel is stale — it belongs to a different trial.**
   This alone could produce a "poor result" that is really a bookkeeping error.
2. Trials 1–3 are not archived. There is no folder on disk that says which purification
   belongs to which protection.
3. `pg_metric.py` builds its file list from that folder, so the reported numbers inherit
   the ambiguity.

**Fix** — one line before running 8b, and it becomes a stamped, reproducible artefact:

```python
# Bug 7 fix: stamp the protection strength into the purified folder name.
PG_TAG = f"iter{PG_ITERS}grad{PG_GRAD_REPS}eps{PG_EPS}"
!sed -i "s|_pur_noise{args.pur_noise}/\"|_pur_noise{args.pur_noise}_$PG_TAG/\"|" \
    pg_mask_pur_helen.py pg_generate.py pg_metric.py
```

(Simplest robust alternative if sed feels fragile: after 8b, `shutil.move` the `pur_...`
folder to `pur_..._{PG_TAG}` and pass an explicit `--pur_dir`. Either way, **stamp it**.)

### 🟠 Bug 8 — the bridge cell grabs an arbitrary folder

Notebook cell 8a-bridge:

```python
src = glob.glob('/content/helen_face/adv_l2_*')[0]     # ← [0] of an UNSORTED glob
```

With one trial on disk this is correct. With three trials on disk, `[0]` is whichever the
filesystem hands back first — so you can bridge trial 1's protected images into trial 3's
purification run and never be told. Same class of failure as bug 7.

**Fix:** build the path from the parameter variables instead of globbing.

### 🟡 Bug 9 (notebook hygiene, not upstream)

Cell 13 hard-codes `adv_diff_*iter40grad_reps2*`. After running trial 3 it still displays
**trial 1's** protected panel. The notebook as it stands on disk cannot show you what you
think it is showing you.

**Fix:** one `PARAMS` dict at the top of the notebook, every cell f-strings from it. This is
also the single biggest readability win for the Ed submission.

---

## 4 · The measurement trap: two different questions wearing one word

You have two candidate scores and they **disagree on this trial**. That disagreement is a
finding, not a bug — but it has to be named before a Light team names it for you.

| question | what answers it | on your trial |
|---|---|---|
| **Q1 · Did the shield break the edit?** | `pg_metric.py`: SSIM/PSNR/VIF of the *edited protected* image against the *edited clean* image | protected should score **low**, purified **high**. This is the attack story. |
| **Q2 · Does the output match the prompt?** | CLIPScore(edited image, "a person in an airplane") → your `R` | protected may score **highest** — it has the most airplane-like background |

Both are legitimate; they measure different things. PhotoGuard can leave a scene that is
*on-prompt but incoherent* — a beautiful aerial view with a broken face pasted on it.

> Metaphor: Q1 asks "did the forger's copy come out looking like the real thing?" Q2 asks
> "does the copy at least depict what was ordered?" A forger can deliver a recognisable
> airplane and still have produced an obvious fake.

**⚠️ A subtlety that will bite:** the Ed post §4 currently says *"Fidelity — SSIM/PSNR vs the
original photo."* But `pg_metric.py` computes SSIM **against the clean *edit***, not against
the original photograph:

```python
clean_image = load_image(diff_dir_clean, image_name)   # the EDITED clean image
image_quality_metrics(clean_image, adv_image, adv_score_dict)
image_quality_metrics(clean_image, pur_image, pur_score_dict)
```

Two different quantities, both called "SSIM". Fix the wording in the Ed post (Thread B) or
a marker will read the sentence and the table as contradicting each other.

**Recommended reporting for M1:** lead with Q1 (`pg_metric` numbers + the visual panel),
introduce `R` as the *added* contribution with its guard rail, and spend two sentences on
the divergence. That divergence is free M2 technical-depth material.

---

## 5 · What the knobs actually do — and the finding that changes your M2 plan

### 🔑 `pg_iters` saturates. `pg_eps` is the real lever.

Read `super_l2` in `pg_mask_diff_helen.py`:

```python
grad_normalized = grad.detach() / (grad_norm + 1e-10)   # unit-length direction
X_adv = X_adv - grad_normalized * actual_step_size      # step_size = 1  → each step moves L2 = 1.0
d_x_norm = torch.renorm(d_x, p=2, dim=0, maxnorm=eps)   # project back into the radius-16 L2 ball
```

Each PGD step moves the image a distance of **exactly `pg_step_size` = 1.0** in L2, and the
result is then projected back inside a ball of radius `pg_eps` = 16.

**So from the centre you hit the wall of the ball after ~16 steps. Everything after that is
walking around on the surface, not further out.**

> Metaphor: `pg_eps` is the length of the dog's leash. `pg_iters` is how long the dog runs.
> After the first few seconds the leash is taut, and running longer does not get the dog
> one inch further from the post — it only lets it find a *better spot along the arc*.

That reframes your three trials:

| trial | leash | running time | direction quality | value |
|---|---|---|---|---|
| 1 · `iters=40, grad_reps=2` | 16 | saturated | noisy (2 samples) | plumbing check |
| 2 · `iters=40, grad_reps=10` | 16 | saturated | good (10 samples) | **best value for money** |
| 3 · `iters=200, grad_reps=2` | 16 | saturated ×12 over | noisy (2 samples) | **~5× the compute on the one lever that had already run out** |

Trial 3 gave the best-looking picture, but mostly because 200 refinement steps eventually
found a good direction *despite* the noisy gradient. Trial 2 should get there for a fraction
of the cost. **This is exactly the kind of "keen observation" the M3 rubric rewards, and it
was invisible from outside the source.**

### Levers ranked by shield-strength per GPU-minute

| rank | knob | what it changes | cost | note |
|---|---|---|---|---|
| **1** | `--pg_eps` 16 → 24 → 32 | the **size of the ball** — the actual ceiling on shield strength | **free** | the untouched lever. `type=int`, so integers only |
| **2** | `--pg_grad_reps` 2 → 10 | averages 10 stochastic gradients instead of 2 → a truer direction (this is EOT) | **linear**, ×5 | the paper's setting |
| **3** | `--diff_steps` 4 → 8 | how much of the diffusion process the attack unrolls and backprops through | **linear**, and it is the expensive one | changes folder names — must match across 8a→8d |
| **4** | `--pg_iters` 200 → 40 | steps taken inside the ball | linear | **saturates ~16–40. Going higher is near-free of benefit.** |

### How visible does a bigger `eps` get?

`eps` is an L2 budget on the **whole tensor**, but the gradient is masked, so the entire
budget is spent inside the face region. If the face is ~15% of a 512×512×3 image:

| `pg_eps` | RMS perturbation in the face region |
|---|---|
| 16 (current) | ≈ 5.9 / 255 |
| 24 | ≈ 8.9 / 255 |
| 32 | ≈ 11.9 / 255 |

Around 8–12/255 the noise starts becoming visible as texture — which is itself the
**protection-strength sweep** already on your M2 list. You now have a principled axis to
sweep along, and a fidelity cost to plot against it.

### ⚠️ Trap: `--attack_type=linf` is currently a no-op

`super_linf` clamps to `X ± eps` with images in `[-1, 1]` — a range of width 2. With
`pg_eps=16` the constraint never binds, so the perturbation is **effectively unbounded**.
If you ever run linf, use `pg_eps ≈ 0.06` (= 8/127.5)… except `pg_eps` is declared `int`,
so you must change its type first. **For now: stay on `l2`, and say so in writing.**

---

## 6 · Recommended action before Ed (28 Aug)

1. **Fix bug 7 first** (stamp `pg_*` into the purified folder name). Everything below is
   untrustworthy until this is done.
2. **Re-run trial 3's chain end-to-end in one session** — 8a → bridge → 8b → 8c → 8d, no
   skipped stages — so the three panels are provably from one parameter set. This is the
   figure that ships.
3. **If GPU time allows, add one run at `--pg_eps=24 --pg_iters=40 --pg_grad_reps=10`.**
   Cheaper than trial 3 and, per §5, should produce a *stronger* shield. If it does, that
   single comparison is the most interesting sentence in your Ed post.
4. Record `pg_metric.py` output for the shipped run. With 1 image `std` prints `nan`; run
   ≥2 images so the number is reportable.
5. Hand §3 and §4 to Thread B — bugs 7/8/9 join the "six fixes" list (now nine), and the
   SSIM wording in §4 of the Ed post needs correcting.

---

## 7 · Still open

- **Is `R` even computable here?** Needs `S_clean − S_protected` to be meaningfully
  positive. Given §4, it may be near zero or negative on this trial. Compute it before
  promising it as the headline.
- **How much of the face damage is the shield vs. VAE round-trip loss?** The clean panel
  also passes through the VAE. Worth a control: encode/decode the clean image with no
  attack and look at it. Cheap, and it pre-empts an obvious challenge.
- The `10 * (cur_masked_image - image_nat).norm(p=2)` term in `compute_grad` is **not in
  PhotoGuard's original loss** — IMPRESS's copy adds it. Worth confirming against the
  PhotoGuard repo before describing the shield in the report. → Thread C.
