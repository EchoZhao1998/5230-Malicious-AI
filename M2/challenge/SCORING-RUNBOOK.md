# Scoring a Track A submission — runbook
*Written 15 Sep 2026. What to do the day a Light team sends back 10 protected PNGs.*

The whole interaction is: **they replace one stage of our pipeline.** Our chain is
`protect → bridge → purify → (mask) → edit → metric`. A submission means **stage (a) protect is
theirs, not ours.** Everything downstream is unchanged. That is the entire interface, and it is
why the spec only ever asked for filenames.

---

## Step 0 · Validate + budget — ZERO GPU, do this first

```bash
python M2/challenge/tyro_wash_test_trackA/check_submission.py  path/to/their_folder
```
Checks the 10 filenames, 512×512, RGB PNG, and prints SSIM / PSNR / LPIPS vs our `clean/`.

- **Wrong filenames or resized → bounce it back the same day.** Do not silently fix it: a resize
  destroys part of their perturbation and we would be measuring interpolation, not their defence.
- **LPIPS(protected, clean) ≤ 0.10 → ranked.** Above → still plotted and discussed, not ranked.
  We committed to that in public; honour it exactly.

**Never edit their PNGs.** Archive the folder they sent, unmodified, as the provenance record.

---

## Step 1 · Inject their images where PhotoGuard's output would go

`adv_dir()` is rebuilt from `PARAMS` (FIX 8), so the destination is deterministic. Drop their ten
PNGs there and skip stage (a).

Minimal change to `run_arm` — one flag, one branch:

```python
# in ARMS entries:  external_protected='/path/to/their_folder'   (None for our own runs)

# stage (a), replacing the unconditional sh(pg_mask_diff_helen...):
if arm.get('external_protected'):
    os.makedirs(adv_dir(iters, reps), exist_ok=True)
    for f in sorted(glob.glob(f"{arm['external_protected']}/*.png")):
        shutil.copy(f, adv_dir(iters, reps))
    print(f'   [external shield] {len(...)} images copied — protect stage SKIPPED')
else:
    sh(f'pg_mask_diff_helen.py ...')      # unchanged
```

> **Why not just rely on resume?** Stage (a) skips images that already exist, so dropping their
> PNGs in would make PhotoGuard a no-op anyway. **Do not rely on that.** One filename mismatch and
> it quietly protects the missing image with *our* shield, and the table then mixes two defences.
> Skip the stage explicitly.

### ⚠️ Two provenance traps, both of which we have been bitten by before
1. **`adv_dir()`'s folder name encodes OUR pg params** (`adv_l2_eps16_step1_iter40...`). With their
   shield inside, that name is a lie. Write the truth into `params.json`:
   `{'shield': 'EXTERNAL — <team name>, submitted <date>', 'pg_iters': None, 'pg_eps': None}`
   and name the archive folder after the team, not the arm.
2. **A later run of ours with the same params would collide with their images.** Either point
   `ROOT` at a per-submission folder, or delete `adv_dir()` after archiving. Do not leave them there.

---

## Step 2 · `N_IMAGES = 2 → 10`

Non-negotiable — they protected all ten, and the ranking rule is *how many of ten engaged*.
Runtime roughly 5×. `edit_clean` must exist for all ten too (`pg_generate.py` produces it).

---

## Step 3 · The engagement gate — run this BEFORE the wash

`pg_metric` gives `ssim_adv` = SSIM(edited-protected, edited-clean) per image. Compare each to
`seed_floor_10.json`:

| condition | verdict |
|---|---|
| `ssim_adv < seed_floor(image)` | **ENGAGED** — `R_pipe` is meaningful for this image |
| otherwise | **"shield did not engage"** — publish the measured number, no `R_pipe` |

Run the **N arm only** first (no purify stage, so it is cheap). If none of the ten engage, **stop.**
There is nothing left to wash and no honest `R_pipe` to report — and that is itself the result we
promised to publish. Saves an hour of T4 time.

*This is the same gate that caught our own PhotoGuard reference at 0.584 / 0.610. It is not a
courtesy to them; it is what stops us publishing a ratio of two near-zero numbers.*

---

## Step 4 · Run the wash — two arms, not four

| arm | why |
|---|---|
| **N** (no wash) | already run in Step 3. The origin of the chart, and the source of `ssim_adv` |
| **C** (ours, masked, `pur_iters=100`) | the headline: does our M2 method strip *their* shield |
| A (IMPRESS 100, unmasked) | optional. Add it only to say whether the mask still helps on their shield |

**Skip B (1000 iters).** Expensive and already ruled out.
Budget: one T4 session, roughly an hour for N + C on ten images. That is an estimate extrapolated
from 7.2 min / 2 images with our own protect stage included, not a measurement.

---

## Step 5 · Report — per image, never a mean

Publish, per image: `ssim_adv` · its floor · engaged? · `LPIPS(protected, clean)` · `R_pipe`.
Headline = **how many of ten engaged**, plus the scatter (x = LPIPS, y = `R_pipe`) with their dot
beside our PhotoGuard reference.

**Never read an `R_pipe` difference smaller than 4 pp** — that is inside the measured noise floor.
And never compare their numbers to a figure from a different run or platform (4–7 pp drift).

---

## Step 6 · The reply post — this is where the marks actually are

The score is not the deliverable; the **interaction** is. M3's largest individual row (5 marks)
asks *how the target team reacted*, so the post must invite a reaction:

- **Publish it even if their shield beats us.** We committed to that in writing, twice.
- Give them the per-image breakdown, not just a rank — it is useful to them, which is what makes
  a reply likely.
- **End with an open loop**, e.g. *"tell us your setting and we will re-run at (X); if you push
  below the floor on more than N of ten we will say so."* That one sentence is the mechanism that
  manufactures the M3 material.

---

## Step 7 · Record it
Their original zip, our `params.json` with the EXTERNAL marker, the per-image table, and a one-line
memory note. A submission is the only thing in this project whose raw input we cannot regenerate.
