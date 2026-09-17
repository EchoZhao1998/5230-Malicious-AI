# Review — `Tyro_Wash_Test_STARTER.ipynb`
*15 Sep 2026. Checked against `CHALLENGE-SPEC.md`, the pack README, `M2_Ed_Post_V8.md` and the
canonical cold-run numbers. The mechanics are sound; the published numbers are not.*

The code runs and the interface is right (`protect()` is the only socket, the assert on size is
the right guard, `net='alex'` matches the scorer, the LPIPS input scaling matches `Dark_Tyro_M2`).
Everything below is either a stale number or an adoption blocker.

---

## A · Must fix before this is re-published

### A1 · The close date contradicts the spec
Cell 11: **"Submissions close 15 September 2026."**
`CHALLENGE-SPEC.md` and the pack README: **18 September.**
Pick one. See §D for why the answer is probably *neither*.

### A2 · "our own purifier's output | 0.12" is stale, and it sells you short
Canonical cold-run LPIPS: **A 0.150 · B 0.108 · C 0.038.** `0.12` is no arm.
Worse, the prose beside it — *"our purifier damages the photograph more than the shield it
removes"* — is **no longer true of your own M2 method.** C is 0.038. The V8 post's headline is
**74% less damage**, and this notebook is quietly publishing the pre-M2 version of your result.

Fix: name the arms.
| row | LPIPS vs clean |
|---|---|
| IMPRESS baseline (arm A, 100 iters) | 0.150 |
| IMPRESS at the paper's budget (arm B, 1000) | 0.108 |
| **our M2 masked purifier (arm C)** | **0.038** |

### A3 · Two different things are both called "PhotoGuard"
The calibration table mixes two implementations with no label:
- rows 1–3 = **this notebook's L∞ encoder attack**, `EPS` in grey levels → 0.07 / 0.104 / 0.415
- your scorer's shield = **IMPRESS's L2 `pg_mask_diff_helen.py`** at `(40,2)`, eps 16 → ~0.017

The prose *"the reference defence spends about one grey level and lands at 0.019"* refers to the
second one, **which is not a row in the table.** A careful reader lines the sentence up against
row 1 (0.07), the arithmetic fails, and they stop trusting the rest of the page.

Fix: label each row with its implementation, and add the IMPRESS shield as its own row.

### A4 · The "fair fight" claim in cell 7 is arithmetically wrong
> *"sigma = EPS/8 is not arbitrary: at EPS=16 it costs LPIPS ~0.019, the SAME perceptual price as
> the PhotoGuard reference below."*

The PhotoGuard reference *below* is the encoder attack, whose default `EPS = 3` costs **~0.07** —
**3.7× more**, not the same. The matched-cost claim only holds against the **IMPRESS** shield.
Say which one, or drop the word "same".

---

## B · Should fix — fairness and adoption

### B1 · The VAE fallback chain is a trap
```python
for mid in ['runwayml/stable-diffusion-inpainting',        # DELETED from HF — your own FIX 1
            'stable-diffusion-v1-5/stable-diffusion-inpainting',
            'stabilityai/sd-vae-ft-mse']:                  # a DIFFERENT VAE
```
- Entry 1 always fails. It is the dead repo you already patched out of IMPRESS.
- `except Exception: continue` swallows everything, so an HF auth failure looks identical to a
  missing repo and the team has no idea why it took 30 s.
- **Entry 3 is a different autoencoder from the one your scorer's editor uses.** A team that
  silently lands there builds its shield against the wrong encoder and scores badly because of
  *your fallback order*, not their design. That is an unfair result you would have to publish.

Fix: pin `stable-diffusion-v1-5/stable-diffusion-inpainting`, drop `runwayml`, print the exception,
and if the `sd-vae-ft-mse` fallback is ever used, **warn loudly that the shield is now
cross-model** — a real finding, but not the fight they signed up for.

### B2 · There is no way to get the image pack into Colab
Cell 3: *"Unzip `tyro_wash_test_trackA.zip` next to this notebook."* On Colab there is no "next
to this notebook". You promised an entry cost of one cell; step zero is currently a manual upload
with no instructions. Add `google.colab.files.upload()` or a direct `!wget` of the zip.

---

## C · The gap that matters most

**`seed_floor_10.json` ships in the pack and the starter never touches it.**

A team can clear the LPIPS budget in five minutes and have no idea their shield will not engage.
Their entry then comes back **"shield did not engage"** — which reads as your scoring being
evasive rather than their shield being quiet, and it is the single most likely way this challenge
generates bad feeling instead of a result.

And you have never measured whether the starter's own shield engages. **Your IMPRESS shield at
`(40,2)` sat at `ssim_adv = 0.5624`, above the 0.42 / 0.47 floors — it did not engage.** The
encoder attack here is a *different* attack (L∞, latent-toward-grey, 100 steps), so it may well
bite harder. Nobody knows.

> **If the default route C does not engage, every entry returns no `R_pipe` and the challenge
> yields nothing.** Measure it before inviting another team.

**And this is free work.** The starter's `photoguard_encoder` is the **L∞ path** named as the
fallback in `M3/M3-PLAN.md` §1.1. One run answers both questions: *does the starter engage?* and
*does L∞ give us a detectable shield for M3?* Same hour of T4, two deliverables.

---

## D · The strategic call on the date

Their M2 is also due 18 Sep. Nobody is spending the last 72 hours on someone else's challenge.
**Expect zero submissions by 18 Sep — and that is not a failure.**

*"Submissions closed, nobody entered"* is a dead end. A standing invitation with a date is an
open loop, and the open loop is what M3's 5-mark row pays for.

**Recommended: round 1 closes 18 Sep (results in the M2 post, even if the result is "no entries
yet"), round 2 closes ~10 Oct, results presented in the M3 talk.** Say it in the M2 post.

---

## E · Minor
- `ALLOW_SLOW_CPU` is read in cell 5 but defined in cell 7. It survives only because
  `globals().get(..., False)` defaults false. Move the default into cell 5.
- The LPIPS budget is checked on the **mean of ten** here, while engagement ranking is explicitly
  **per-image** everywhere else. Not a contradiction — but say so in one line, or a reader will
  call it one. Publish per-image LPIPS too; it already prints.
