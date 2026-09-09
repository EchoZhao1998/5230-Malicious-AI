# Rehearsing the Tyro Wash Test — private notes

*Written 8 Sep 2026. Not for publication. The question this answers: **is the challenge
manageable and doable for another team?** You find out by being that team for an hour.*

---

## The thing to understand first

**The expensive side of this challenge is ours, not theirs.**

| | who pays | cost |
|---|---|---|
| produce 10 protected PNGs | **the challenger** | seconds (no GPU) to ~5 min (free Colab T4) |
| purify + edit + score them | **us** | ~35 min of Kaggle T4 per entry |

So "too complicated for another team" is almost certainly **not** the risk. Their interface is
ten files in, ten files out; they never open `Dark_Tyro_M2.ipynb`. The real risks are the three
below, and the rehearsal is designed to find them.

| risk | what it looks like | rehearsal step |
|---|---|---|
| **R1 · the shield never engages** | our scorer prints *"shield did not engage"* for the reference PhotoGuard entry. Every honest entrant gets no score, so nobody plays. **This is the live one — see `Tyro_M2_diagnostics.ipynb` D2.** | Level 2 |
| **R2 · entry takes too long** | route C runs 30+ min on a free Colab and people give up halfway | Level 1 |
| **R3 · the interface bites** | filename mismatch, wrong size, self-check crashes on a machine without skimage | Level 0 |

---

## Level 0 — 5 minutes, on your Mac, no GPU. Do this today.

Open `Tyro_Wash_Test_STARTER.ipynb`, set `PACK` to `tyro_wash_test_trackA`, and run it twice:

1. `SHIELD = 'none'` — the control. Confirms filenames, sizes, the zip, and that LPIPS reads
   exactly 0.0000 for an unmodified submission.
2. `SHIELD = 'noise'`, `EPS = 16` — confirms the self-check reports **inside** the budget
   (should land near LPIPS 0.019, the same perceptual price as PhotoGuard).

**Verdict you are looking for:** both runs finish in under a minute and `check_submission.py`
says *"submission looks valid"*. That closes R3.

> Already verified on this pack, 8 Sep: route `none` → 10 images in 0.7 s, LPIPS 0.0000.
> Route `noise` at EPS = 16 → 10 images in 0.5 s, 1.6 grey levels, LPIPS ≈ 0.019.

## Level 1 — RUN 8 Sep. Found two bugs, both now fixed.

Ran on the Mac, CPU only, `SHIELD='photoguard'`, `EPS=16`, all 10 images.

| what happened | why it matters | fix applied |
|---|---|---|
| **43.4 min** (4 min/image) | on CPU. A T4 does the same in ~2 min. A challenger who misses the GPU note quits halfway. | route C now **refuses to run on CPU** unless `ALLOW_SLOW_CPU=True`, and says how long it would take |
| **LPIPS 0.43** — four times over our own 0.10 budget | `EPS=16` was the default. Measured: it moves 8.7 grey levels, ~550x the L2 of our own reference shield. We would have shipped a starter whose default entry is unrankable. | default is now **`EPS = 4`** (LPIPS 0.053), with the measured calibration table printed beside it |

**The two-axis design worked exactly as intended.** Echo's own entry scored as the degenerate
"wreck the photo" answer, and the LPIPS axis caught it before anyone saw it. Worth saying in the
post: *we ran our own challenge first and our own first entry failed the budget.*

## Level 1 (re-run) — 15 minutes, free Colab T4. Do this before you post.

Same notebook, `SHIELD = 'photoguard'`, `EPS = 16`. Watch the per-image timer.

**The number you are collecting is the sentence you put in the Ed post:** *"the reference
shield takes about N minutes for all ten on a free Colab T4."* People decide whether to enter
on that sentence.

- under 10 min → post it as written
- 10–20 min → post it, and say so plainly
- over 20 min → **cut the pack to five images.** Ten images is not worth losing entrants over;
  five is still a scatter plot. `manifest.json` and `check_submission.py` both derive their
  file list from `clean/`, so deleting five pairs is the whole change.

## Level 2 — ~40 min Kaggle T4. The one that actually decides things.

**Run `Tyro_M2_diagnostics.ipynb` D2 first.** It is 4 minutes and it answers R1 directly on
images you already have, without touching the challenge at all.

- **If D2 says the shield clears both nulls** → the challenge is sound. Score your own Level 1
  submission through arm C on 3 images as a plumbing check, then publish.
- **If D2 says the shield is indistinguishable from a seed change** → **do not publish the
  challenge as written.** The reference entry cannot be scored, so no entrant can be either.

  The fix is small and it is the same fix M2 needs anyway: raise `EPS` in the starter until the
  shield engages (try 32, then 64 — 32 costs LPIPS ≈ 0.08 as noise, less as PhotoGuard, so
  there is room under the 0.10 cap), and publish **that** as the reference setting. Then the
  starter's default entry is one that demonstrably survives being scored, which is exactly the
  worked example the challenge was missing.

---

## Three things to change in the post regardless

1. **Add the close date.** The M1 post gave none. **15 September.** Already written into the
   starter notebook's last cell.
2. **Ship one worked example dot.** Publish the reference PhotoGuard entry's own two numbers on
   the scatter, labelled *"reference entry — beat this"*. A challenge with a visible target gets
   entered; an empty plot does not.
3. **Hold Track B back.** It is a second, unrelated task (detection, not defence). Two tracks do
   not double participation, they halve it on each. Track B is better as an M3 post, where
   *Peer Engagement* is worth 3% and you will have the M2 result to hang it on.

## Bugs already fixed while rehearsing (8 Sep)

- `check_submission.py` scored LPIPS with **vgg** while our scorer (`Dark_Tyro_M2.ipynb` cell 8)
  uses **alex**. Different nets, different numbers, one published 0.10 budget — a challenger
  could self-check as inside and be ranked outside. Checker now uses `alex`.
- Without `scikit-image` the checker printed a silent column of `nan` for SSIM. It now says why
  and what to install.
