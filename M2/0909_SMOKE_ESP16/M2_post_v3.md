# M2 — Dark.Tyro: wash less, keep the same result

**Team Dark.Tyro** · Echo Zhao · Nissa Corlidea

**Theme 2 (Text-to-Image) · Dark / attack side** · Milestone 2

**In short.** Four lines of code reduced photo damage by **74%**, with the same measured attack
effect. Our **Tyro Wash Test** is open: edit one function to enter.

---

## 1 · Code and how to run it

Run the notebooks from top to bottom on Colab or Kaggle with two T4 GPUs and Internet access. Smoke mode
checks the setup in about four minutes.

- `Dark_Tyro_M2.ipynb`
- `challenge/Tyro_Wash_Test_STARTER.ipynb` — starter code for defenders
- `Tyro_M2_diagnostics.ipynb` — Metric checks(optional for you)

The key change line is:

```python
purified_v2 = mask * purified_impress + (1 - mask) * protected
```

This keeps the washed pixels inside the mask and the protected pixels outside it.

---

## 2 · Understanding of the Work Pipeline

```text
clean photo
    ↓  PROTECT — PhotoGuard adds a small pattern
protected photo
    ↓  PURIFY — IMPRESS washes away the pattern
purified photo
    ↓  EDIT — Stable Diffusion inpainting uses a mask and prompt
edited photo
    ↓  MEASURE — score edit recovery and photo quality
two results
```

**PhotoGuard** (arXiv:2302.06588) protects a photo with a small, invisible pattern that disrupts AI
editing.

**IMPRESS** (arXiv:2310.19248, `github.com/AAAAAAsuka/Impress`) adjusts the protected photo until
the model's autoencoder accepts it again. This removes much of the protection. Our Dark-side task
is to improve this attack.

A full-image wash can also remove real photo detail. A useful attack should restore editing while
preserving the photo.

---

## 3 · What we changed

Inpainting keeps one region of a photo and repaints another. On a brightness scale that measures how light or dark each pixel is, the kept region changes - `mask * purified_impress` - by only 4–7 levels, while the repainted region - `(1 - mask) * protected` - changes by 86–96.

IMPRESS washes the full image. We restrict the wash to the region that survives the edit, saving
detail in the rest of the photo. The code above blends the washed and protected images with a soft
mask edge.

---

## 4 · What we measure

| Metric | Meaning | Better result |
|---|---|---|
| **`R_pipe`** | Share of the editing pipeline restored, measured across the gap between fully protected and unprotected edits | Higher for our attack |
| **`LPIPS`** | Perceptual difference from the clean photo; 0 means identical | Lower |

We report both metrics together. `R_pipe` measures attack effect, while LPIPS measures photo
quality. Together, they reward effective washes that preserve the image.

---

## 5 · Results

We tested four versions with one shield setting, the same faces and the same seed (**n = 2
images**). Version N is the starting point with no wash.

| Version | Wash | `R_pipe` % ↑ | LPIPS vs clean ↓ |
|---|---|---:|---:|
| **N** | Starting point: no wash | 0.00 | **0.018** |
| **A** | IMPRESS, 100 iterations: M1 baseline | 4.75 | 0.150 |
| **B** | IMPRESS, 1000 iterations: paper budget | 9.41 | 0.109 |
| **C** | **Ours:** IMPRESS, 100 iterations, mask only | 7.05 | **0.039** |

*(Attached: `m2_tradeoff.png`, which plots all four versions, and `m2_panel.png`, which shows the
clean, protected, purified and edited images.)*

C uses the same compute as A and causes **74% less photo damage**.

### How to read the recovery score

C scores 2.3 `R_pipe` points above A. Repeating the same experiment shifts `R_pipe` by ±2–4 points,
so these two recovery scores are effectively the same. The strongest finding is the large drop in
LPIPS.

---

## 6 · A useful metric check

We tested `R_pipe` against the generator's normal variation. We edited each clean photo twice and
changed only the random seed. Lower SSIM means a larger change.

| Image | Different seed | PhotoGuard shield |
|---|---:|---:|
| 1233476865_1 | **0.472** | 0.584 |
| 1525918600_1 | **0.415** | 0.610 |

At these settings, changing the seed affects the edit more than PhotoGuard. This means `R_pipe`
includes some generator variation. Doubling the shield-strength setting also produced the same
result, which shows that the setting is inactive on this code path.

Our challenge scorer therefore checks that each shield registers before reporting its score. This
supports strong confidence in the photo-damage result and cautious reading of the recovery result.
The full test is in `Tyro_M2_diagnostics.ipynb`.

---

## 7 · Tyro Wash Test

**Build a shield that resists our wash.** Entry requires one function: `protect()`.

### What you get

- 📦 `tyro_wash_test_trackA.zip` (3.6 MB): 10 clean 512 × 512 faces, masks and
  `check_submission.py`
- 📓 Starter notebook: **[COLAB LINK]**, ready for a free Colab T4

### What you do

Open the starter notebook and edit `protect()`. You can tune the included PhotoGuard protector or
replace it with your own method.

Submit 10 PNG files at 512 × 512 using the original filenames. Your method stays private because
our purifier scores only the images. Any defence method is welcome.

### How we score it

We publish every entry using two metrics:

- **`R_pipe`**: how much of the edit our wash restores; lower is better for defenders
- **`LPIPS`**: how much the shield changes the photo; lower is better

To qualify for ranking, keep LPIPS below **0.10**. Our shield scores **0.0665**. We will still plot
entries above the limit.

`check_submission.py` reports both metrics and flags shields that are too subtle to register. It
uses the same check as our final scorer. This replaces our M1 fixed rule of SSIM ≤ 0.85, which our
tests showed was too loose.

**Interaction.** We will publish every result in a follow-up, including entries
that beat ours. Reply to this post if the pack needs a fix, and we will update it the ASAP.
