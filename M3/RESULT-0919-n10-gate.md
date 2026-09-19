# n=10 gate run — `run_0919_0406` · 19 Sep 2026

Shield `(40, 2)`, `attack_type=l2`, `pg_step_size=1`, `pg_eps=16`. N arm only, ten pinned images.

## Headline: 1 of 10 engaged — and that 1 should be read as 0

| image | ssim_adv | floor | margin |
|---|---:|---:|---:|
| 1961032923 | 0.6966 | 0.7067 | **−0.0101 ENGAGED** |
| 2061993362 | 0.4656 | 0.4360 | +0.0296 |
| 1233476865 | 0.5018 | 0.4721 | +0.0297 |
| 178046512 | 0.5370 | 0.4800 | +0.0570 |
| 2139626906 | 0.3837 | 0.3165 | +0.0672 |
| 181707205 | 0.6453 | 0.5620 | +0.0833 |
| 2167874246 | 0.4346 | 0.2849 | +0.1497 |
| 2099073485 | 0.5401 | 0.3757 | +0.1644 |
| 221629697 | 0.5178 | 0.3159 | +0.2019 |
| 1525918600 | 0.6372 | 0.4149 | +0.2223 |

Median margin **+0.075**. Mean **+0.100**.

**The single engagement is inside the error bars and must not be reported as a success.** Its
margin is 0.0101, while the same shield drifts **0.0032–0.0037** between runs on identical images
(see replication below), and each floor was measured from **one** seed pair, so the floor carries
its own unquantified error. Report as **"0–1 of 10, with the one indeterminate"**, never as 1/10.

## ⭐ The engaged image engaged because its gate was easy, not because the shield worked
`1961032923` has the **highest floor in the set (0.7067)** and the **second-highest `ssim_adv`
(0.6966)**. A high floor means the editor barely changes between seeds on that image, so the bar
*"disturb it more than a seed change does"* is a low bar in absolute terms. The shield did not do
better there; the test was easier there.

> Ten rooms of different loudness. The whistle was heard in the quietest room, by a hair. That is a
> fact about the room.

**Generalisable: when a per-image gate passes on exactly one image, check whether that image has
the easiest gate before crediting the method.**

## The floor and the shield are not independent
`corr(floor, ssim_adv) = +0.783`. Images whose edits are seed-stable are also images the shield
cannot move. Both are measuring the same underlying thing — how far the output is determined by
the prompt and mask rather than by the input pixels. So the gate partly cancels its own difficulty,
and **the margin, not `ssim_adv`, is the quantity to sweep against.**

## ✅ Replication — the protect stage is reproducible
The two M2 images, re-run on different hardware (M2: Colab cold run 14 Sep · M3: 19 Sep) as part of
a ten-image set rather than a two-image set:

| image | M2 `ssim_adv` | M3 `ssim_adv` | Δ |
|---|---:|---:|---:|
| 1233476865 | 0.5055 | 0.5018 | −0.0037 |
| 1525918600 | 0.6404 | 0.6372 | −0.0032 |

**Agreement to 3 decimals.** M2's numbers were not a fluke of n=2, and the ±2–4 pp `R_pipe` noise
measured on 5 Sep is downstream amplification, not instability in the shield itself.

## What this buys, and what it costs
**Buys:** M2's central limitation is now measured at n=10 across floors spanning 2.5×, not argued
from two images. *"The shield does not engage"* is no longer a caveat — it is the result, and it
is the strongest thing in the notebook.

**Costs:** nothing yet. No `R_pipe` from this run is quotable, and none was claimed — the N arm is
0.00 by construction.

## ⭐ The sweep now has a number, not a hope
`pg_step_size` must reduce `ssim_adv` by:

| target | required drop |
|---|---:|
| 3 of 10 engage | **0.030** |
| **5 of 10 engage** | **0.067** |
| 8 of 10 engage | 0.164 |
| 10 of 10 engage | 0.222 |

**Success criterion for the sweep: a drop of ≥ 0.067, i.e. ≥ 5 of 10 engaged.** Below 0.030 the
setting is indistinguishable from `pg_step_size=1` and should be discarded, not reported as partial
progress. Sweep `2 → 4 → 8`, stop at the first setting that clears, and do not sweep past it.

If no L2 setting clears, switch `attack_type` to `linf` (the challenge starter's L∞ `eps`
demonstrably binds). If neither clears, the M3 finding is
*"the L2 branch of this implementation cannot produce an engaging shield at any setting, measured
across ten images spanning a 2.5× range of editor stability"* — a measured negative at a stated
setting, which is what M1 and M2 were credited for.
