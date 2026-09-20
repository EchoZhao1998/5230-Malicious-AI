# 🏁 FINAL — the shield investigation, closed 19 Sep 2026

Five runs, one question: **can PhotoGuard, in IMPRESS's own implementation, be made strong enough
for IMPRESS's own metric to detect it, without becoming visible?**
Ten pinned images, floors spanning 2.5x, N arm only. **The wash was never changed.**

## The whole result in one table

| setting | engaged /10 | median margin above floor | median shield LPIPS | images over the 0.10 budget |
|---|---:|---:|---:|---:|
| **eps 16, step 1** *(the M2 setting)* | **1** | +0.0752 | **0.0272** | 0 |
| eps 16, step 2 | 1 | — | 0.0513 | 1 |
| eps 16, step 4 | 1 | — | 0.0600 | 1 |
| eps 16, step 8 | 1 | — | 0.0654 | 1 |
| eps 64, step 4 | 2 | +0.0314 | 0.0968 | 4 |
| **eps 256, step 4** | **3** | +0.0268 | **0.0955** | **4** |

**Engagement 1 → 3 of 10 costs 3.5x the shield's perceptual budget**, landing the median at
**0.0955 against our published ceiling of 0.10**, with **4 of 10 images already over it** and the
worst at 0.178.

> A protection you can see has already failed at being a protection. This implementation's shield
> becomes detectable by its own metric only as it becomes visible — **the evaluation's sensitivity
> floor sits above the defence's usable range.**

## Three things now settled, each by varying the thing in question

**1 · `pg_step_size` re-randomises; it does not steer.** Spread across settings is 17x the
run-to-run drift, **0 of 10 images monotonic**, engagement flat. Past step 4 it only raises L-inf
(61 → 102 levels median) and LPIPS (0.027 → 0.065). Cost up, effect flat.

**2 · `pg_eps` is live at step 4, inert at step 1, and exhausted by 64.**
16 → 64: **+21% L2.** 64 → 256: **+0.1% L2.** The ball binds somewhere between 16 and 64 and the
optimiser converges by 64. The 9 Sep "inert" finding was conditional on `step_size = 1`, exactly as
that note recorded — which is the only reason it was recoverable.

**3 · Past saturation, more budget changes direction, not size.** From eps 64 to 256 the
perturbation does not grow at all, yet `ssim_adv` still falls 0.016 median and one more image
engages. The extra budget buys a different perturbation of the same size — the same re-randomising
behaviour seen in the step sweep, now isolated from any change in magnitude.

## ⛔ Why we are NOT running the four arms at eps 256 — and it is not only the stopping rule
The locked criterion was **≥5 of 10 engaged AND median LPIPS ≤ 0.10**. We got 3 of 10. But there is
a stronger reason than the threshold:

**The three engaged images are `1233476865` (floor 0.4721), `178046512` (0.4800) and `1961032923`
(0.7067) — three of the four HIGHEST floors in the set.** Engagement is still tracking *gate
difficulty*, not shield strength. An `R_pipe` measured on that subset would be measured on images
selected for having the easiest gates, which is a biased sample by construction — the same defect
as M2's n=2, with an extra image and a nicer story.

**Generalisable: a subset selected by the test's own difficulty is not a sample you can report a
mean over.** Reporting it would undo the entire point of building the gate.

## What ships for M3
- **The claim:** at n=10, across floors spanning 2.5x, PhotoGuard as implemented in IMPRESS does not
  clear its own evaluation metric's noise floor at any setting reachable within the fidelity budget
  IMPRESS's own users would accept. Engagement rises to 3/10 only at 3.5x fidelity cost, with 40%
  of images over budget.
- **The two figures:** engagement vs setting, and shield LPIPS vs setting. Both axes, always — the
  rule the Tyro Wash Test holds challengers to, applied here to the shield itself.
- **The four-arm table stays at the M2 setting**, reported with the gate that explains it. No new
  run, no new method, no new metric.

## Provenance
`probe_eps256.csv` · `probe_eps64.csv` · `sweep_pg_step_size.csv` · `perturbation_size.csv` ·
`shield_fidelity.csv` · gate + per-image from `run_0919_0406`. Narrative in
`RESULT-0919-n10-gate.md` and `RESULT-0919-step-sweep.md`; plan in `M3-IMPRESS-LOCKED.md`.

---

## ⚠️ Revision 19 Sep (later) — the headline is **2 engaged + 1 indeterminate**, not 3

The clean run moves to **Colab**; the published seed floors were measured on a **Kaggle T4**
(10 Sep). Cross-platform drift on `ssim_adv` is measured at **~0.004** (M2 Colab vs M3 Kaggle on the
two shared images), so a margin inside roughly ±0.010 is not a decision.

The merged notebook therefore uses a **three-state gate** — `ENGAGED` / `INDETERMINATE` / `BLIND` —
with `DRIFT = 0.010`. Re-scoring the eps 256 data:

| | old 2-state | **three-state** |
|---|---|---|
| eps 256, step 4 | 3 engaged | **2 engaged · 1 indeterminate · 7 blind** |

The image that moves is **`178046512`**, margin **−0.0062** — smaller than the drift, and it had
already flipped sign between the eps 64 and eps 256 runs (+0.0059 → −0.0062). It was never a
decision; the old gate just had no way to say so.

**Report the curve as 1 → 1 → 2 engaged, with an indeterminate band, never as 1 → 2 → 3.** The
conclusion is unchanged and now survives the platform switch:
*the evaluation's sensitivity floor sits above the defence's usable range.*

> Same rule, third application: **a difference smaller than the measurement's own spread is not a
> difference.** We applied it to `R_pipe` (±2–4 pp), then to the shield sweep (17x drift), now to
> the gate itself. Each time it cost a number we would have liked and bought a claim that holds.

Floors are **not** re-measured: they are published with the challenge and the scoring runbook
depends on them. Changing a public artefact to make our own number look better is the move we would
criticise in another team.
