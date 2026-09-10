# M1 interactive challenge — "The Tyro Wash Test"
*Dark.Tyro · drafted 23 Aug 2026 · built on what `M1/Dark_Tyro_M1_FINAL.ipynb` actually produces*

Rubric row this buys: **Challenge Design Quality 0.5%** — *"thoughtfully crafted, original,
and non-trivial."* It also sets up **M2 Engagement 2%** and **M3 Peer Engagement 3%**, which
are worth ten times more and depend on other teams *actually attempting* it.

- **Part 1** is paste-ready for the Ed post.
- **Part 2** is private ops — what we must generate, what it costs, what we never publish.
- **Part 3** is the trim, if the week runs short.

---
---

# PART 1 — paste into the Ed post

## 🧪 The Tyro Wash Test

Our attack is a **solvent, not a lock-pick.** IMPRESS purification takes a protected image and
optimises it until it is self-consistent under a Stable Diffusion autoencoder. It never asks
*how* the perturbation got there — so it does not care whether your shield is PhotoGuard,
Glaze, Mist, or something you invented last week.

That is the claim we want you to break. **Two tracks. Enter either, or both.**

---

### Track A — "Build a shield we can't wash off"

**What we give you.** In our Colab: 10 clean faces at 512×512, their inpainting masks, and a
working PhotoGuard protector you can run in one cell. If you have no protection code of your
own yet, that cell **is** your starter kit — change one parameter and you have an entry.

**What you send back.** Ten PNGs, 512×512, **same filenames as ours**. That is the entire
interface. How you protected them is your business and you do not have to tell us.

**What we do with it.** We run our IMPRESS-based purifier over your images, edit clean,
protected and purified with an identical prompt, seed and mask, and report **two numbers**:

| axis | what it means | you want it |
|---|---|---|
| **`R_pipe`** = (SSIM_pur − SSIM_adv) / (1 − SSIM_adv) | how much of the editing pipeline our wash restored. 1.0 = we fully stripped you, 0 = your shield held | **low** |
| **Perceptual cost** = LPIPS(protected, clean) | how much of the photograph you destroyed to get there | **low** |

**Both axes are published, as one scatter plot.** This matters, because with robustness alone
there is a degenerate winner: crank the perturbation until the image is visible noise.
Nothing can be washed off a photo that is already ruined — but nothing can be *edited* either,
so that "defence" defeats its own purpose. **A shield that wins by wrecking the picture will
appear as a dot in the top-right corner, and we will say so.**

**The budget, and the calibration behind it.** We rank only submissions with
**LPIPS(protected, clean) ≤ 0.10**. The number comes from `pur_eps = 0.1`, the LPIPS allowance
in IMPRESS's own objective — in fairness a *soft hinge* weighted at `pur_alpha = 0.01`, not a
hard cap, so treat it as an anchor rather than a symmetry claim.

Measured on `1233476865_1.png` from the pack, so you can see the room you have:

| image | SSIM vs clean | PSNR | mean abs. diff |
|---|---|---|---|
| PhotoGuard `(40, 2)`, eps 16 | 0.9888 | 38.6 dB | 0.93 levels |
| PhotoGuard `(200, 2)`, eps 16 | 0.9773 | 37.4 dB | 1.30 levels |
| **our purifier's output** | **0.7790** | **31.3 dB** | **5.24 levels** |
| crude uniform noise ±25 | 0.4635 | 25.2 dB | 11.8 levels |

The reference defence costs about **one grey level**, so the budget is generous — you may build
a far more aggressive shield than PhotoGuard and still be ranked. And note the third row:
**our purifier moves the image roughly four times further than the shield it removes.** We
publish that rather than hide it; if your shield forces us to spend more still, that is a
result in your favour. Over-budget entries are plotted and discussed, just not ranked.

**Engagement gate — measured, and corrected in public.**

If your shield does not measurably disturb the edit, `R_pipe` is a ratio of two near-zero
numbers and means nothing. We originally published a threshold of **0.85**. That number was a
guess made before we measured anything, and it was wrong.

We have since measured the **seed floor**: how far apart two *innocent* edits of the same clean
image land, with no protection anywhere in the loop. Across the ten pack images it runs from
**0.285 to 0.707**. So 0.85 would have passed all ten trivially — and it would have passed our
own PhotoGuard reference (0.584 / 0.610), which we have separately shown is indistinguishable
from the generator's own randomness.

> **The gate, corrected:** we report `R_pipe` for an image only when
> SSIM(edited-protected, edited-clean) falls **below the seed floor for that image**. Otherwise
> we report **"shield did not engage"** and show you the number we measured.

The ten floors ship with the pack as `seed_floor_10.json`:

| image | seed floor | | image | seed floor |
|---|---|---|---|---|
| 2167874246_1 | 0.285 | | 2061993362_1 | 0.436 |
| 221629697_1 | 0.316 | | 1233476865_1 | 0.472 |
| 2139626906_1 | 0.317 | | 178046512_1 | 0.480 |
| 2099073485_1 | 0.376 | | 181707205_1 | 0.562 |
| 1525918600_1 | 0.415 | | 1961032923_1 | 0.707 |

**The images are not equally hard, and that is not our choice — it is the editor.** On
`1961032923_1` the editor is stable across seeds, so a shield only has to push below 0.707. On
`2167874246_1` it must get under 0.285. A 2.5x range. **We therefore rank on how many of the ten
images engaged, and publish per-image numbers — never a single mean over ten images of unequal
difficulty.**

---

### Track B — "Find the fingerprint"

Washing a photo leaves a trace. IMPRESS optimises for autoencoder self-consistency, and we
have measured that axis ourselves: clean images sit at round-trip inconsistency **0.0071**,
protected at **0.0204**. So *"is purification detectable?"* is already answered — **yes.**

The question we actually want answered is the harder one:

> **Does a detector that catches one purifier still catch a different one?**

| | |
|---|---|
| **Calibration set** | 12 images, 4 clean / 4 protected / 4 purified, **labels given.** Fit anything you like |
| **Evaluation set** | 30 images, 10 / 10 / 10, labels withheld. The purified ten come from **more than one purifier setting** — we will not say which, or how many |
| **Submit** | one predicted label per evaluation image |
| **Score** | 3×3 confusion matrix + balanced accuracy on **both** sets (chance = 33.3%) |
| **Headline** | the **generalisation gap** = balanced_acc(calibration) − balanced_acc(evaluation) |

A small gap means you found something real about what purification does to an image, and we
will build our M2 purifier to defeat it. A large gap means detection does not transfer — which
is a result about the *defence*, not about you.

---

### What we commit to

- **Every outcome gets published, including ours losing.** Our purifier is deliberately
  *blind* — it never inspects your perturbation. If a protection defeats it, that is a real
  result about IMPRESS and we will report it as one, not quietly drop it.
- **Ground truth for Track B, our own detector, and a read of the error patterns** — released
  **after** the deadline. We are not publishing the answer key before the exam.
- **Submissions close 18 September** (our Milestone 2 post), where all results appear.

### What we are not telling you yet

Our own detection accuracy, which statistic our detector uses, and which evaluation images
came from which purifier setting. That is the ordinary shape of a challenge, not evasion.

**Reply here or DM us for the image pack and the submission folder.**

---
---

# PART 2 — private ops notes (never publish this part)

## What must be generated before posting

Everything below comes out of `Dark_Tyro_M1_FINAL.ipynb` unchanged — the archive already
writes `clean/ protected/ purified/ edit_clean/ edit_protected/ edit_purified/ params.json`
per configuration tag.

| pack | contents | how |
|---|---|---|
| **Track A** | 10 clean 512×512 faces + 10 masks | ✅ **BUILT 23 Aug — `M1/tyro_wash_test_trackA/` + `.zip`. No GPU run was needed.** |
| **Track B** | 14 clean · 14 protected · 14 purified (7 from each of two purifier settings) | one protect pass at `(40, 2)`, then **purify twice** — `pur_eps = 0.1` and `pur_eps = 0.3` |

### 🔑 Vary the *purifier*, not the shield

The earlier spec said the purified ten come from "two configurations", meaning two *shield*
strengths. **Change it to two purifier settings.** Two reasons:

1. **It is the question.** Track B asks whether a detector transfers *across purifiers*. Two
   shield strengths do not test that; two purifier settings do.
2. **It is nearly free.** Protecting is the expensive stage; purifying is cheap. One protect
   pass and two purify passes costs barely more than one full chain.

### ⚠️ Track A needed no pipeline run at all

The archive's `clean/` folder holds the **full-resolution** Helen originals (2736×3582,
4000×3000) — it is *not* the 512×512 tensor the model sees. So running `N_IMAGES = 10` through
the GPU chain would not have produced the pack anyway. What was needed is a CPU resize that
matches the pipeline **exactly**:

```python
Image.open(path).convert('RGB').resize((512, 512))   # PIL default resample = BICUBIC (verified)
```

Every IMPRESS entry point — `pg_mask_diff_helen.py:204`, `pg_generate.py:32`,
`pg_mask_pur_helen.py:54` — uses precisely that line, with no `resample` argument and no
aspect-ratio preservation. Verified empirically that PIL's default is BICUBIC, not NEAREST.
File selection is `sorted(os.listdir(clean))[:10]`, the same rule as notebook cell 7, so the
first two are the images our published results were computed on.

**General lesson:** before spending GPU time to produce an artifact, check whether the artifact
is actually an *output* of the computation or just an *input* to it.

### Cost

**Measured:** the full chain at `(40, 2)` on 2 images = **7.2 min** on a Kaggle T4 (final2 run).
**Extrapolated from that** — treat as an estimate, not a measurement:

- protect 14 faces at `(40, 2)` ≈ 35–45 min
- purify 14 faces twice ≈ 15–25 min
- **no edit stage needed for Track B** — detection is on the purified images themselves
- Track A pack needs only `clean/` + masks: **free**

**≈ 1 to 1.5 hours of T4 time.** Under 5% of the weekly Kaggle quota.

## 🛑 Run B4 before publishing Track B

Step 0 of `TIER3-SPEC.md`. If a single one-number threshold already separates our purified
images from clean ones, we are handing a Light team a free win. Tighten first.

**But note the reframe holds:** we no longer promise "our accuracy as the bar to beat", so a
detectable purifier is no longer a disaster — it becomes our M2 detector-aware purifier spec.
B4 now tells us *how hard the challenge is*, not *whether we dare run it*.

> **The principle, kept from the 22 Aug decision:** design the challenge so that every
> possible outcome is a result you are content to publish.

## Never publish

- `Tyro_Analysis_Toolkit.ipynb` **section B4** — the private detection answer key
- our measured detection accuracy, or which statistic the detector uses
- the `f_c` we settle on for the FFT filter (that is Echo's M3/M4 individual angle)
- the mapping from evaluation image → purifier setting

## Why this design earns the rubric row

| rubric word | how it is met |
|---|---|
| **thoughtfully crafted** | two axes, so the degenerate "wreck the photo" answer visibly loses; an engagement gate so a non-functioning shield gets an honest verdict instead of a flattering ratio |
| **original** | the LPIPS budget is set equal to our own purifier's allowance — the shield gets exactly the perceptual budget the attack gets. Symmetric, principled, and not in any paper |
| **non-trivial** | Track B cannot be won by tuning one threshold, because the evaluation set contains more than one fingerprint |
| **engagement** | Track A's entry cost is *one notebook cell*. A Light team with no code at all can still play — that is the insurance for the 5% that depends on participation |

---
---

# PART 3 — the trim, if the week runs short

M1 asks you to **"design and describe"** a challenge. It does not require the image packs to
exist by the 28th.

**Minimum viable version — post Part 1 as written, and ship the packs at M2 (18 Sep).**
The Ed post already says submissions close 18 September, so this is consistent, not a retreat.

If you want *something* live on the 28th, ship **Track A only**: it needs the 10 clean faces
and masks, which the notebook already wrote, and costs **zero extra GPU time.** Track B's
42-image pack then lands with the M2 post, where the Engagement row is actually marked.

**Do not** spend the 28th generating Track B. M1's rubric has no row for it.
