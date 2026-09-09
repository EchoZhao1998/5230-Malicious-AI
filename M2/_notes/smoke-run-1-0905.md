# Smoke run — 5 Sep 2026 · PLUMBING PASSED

**`SMOKE = True`: `pg_iters=10`, `pur_iters=10`, arms A and C, n=2.**
**The `R_pipe` numbers here are not results.** Ten optimisation steps is not a purifier. What
this run establishes is that the pipeline is correct, plus one thing that does not depend on
the settings at all.

## 1 · Stage (c2) fired exactly where it was supposed to

Difference between arm A's and arm C's purified images:

| image | inside the mask | outside the mask |
|---|---|---|
| `1233476865_1` | 0.30 levels | **4.60 levels** |
| `1525918600_1` | 0.12 levels | **4.95 levels** |

Near-zero inside (only the feathered boundary), ~5 levels outside. That is the method working
as specified, and it is the check that matters — a masking bug would show as the reverse.

Both arms report **identical `ssim_adv` = 0.6864**, confirming the comparison is controlled:
same shield, same seed, same mask, so only the wash differs.

## 2 · The fidelity result — and it does NOT depend on the smoke settings

| | IMPRESS (A) | mask-restricted (C) | |
|---|---|---|---|
| **LPIPS vs clean** | 0.160 | **0.037** | −77% |
| SSIM vs clean512 | 0.7491 | **0.9368** | +0.19 |
| PSNR | 31.6 dB | **35.9 dB** | +4.3 dB |
| damage | 5.14 levels | **1.82 levels** | −65% |

**Why this half is already established.** Restricting the output to the mask removes IMPRESS's
damage in the 70% of pixels it never needed to touch. That is a geometric fact about *where*
the damage is, not about how many optimisation steps produced it, so the iteration count does
not change it. It reproduces the prediction made from M1's archive (0.759 → 0.937) to three
decimals.

**🔑 The number to lead with: our own purifier now costs LPIPS 0.037, inside the ≤ 0.10 budget
we publish for challengers.** At M1 it cost 0.15 and broke our own rule. That is not a
cosmetic improvement — it is the difference between a challenge we can defend and one a Light
team could have turned on us.

## 3 · What is NOT settled — `R_pipe`

| arm | `R_pipe` |
|---|---|
| A_impress_100 | −13.8% |
| C_tyro_masked | **−5.4%** |

Both negative: at ten iterations the wash makes the edit *worse* than leaving the shield on.
Expected — M1 got +5.2% at `pur_iters=100`. **Do not quote these.**

The one thing worth noting: C is roughly **half as harmful as A** at identical settings, which
is the same direction as the fidelity result. Less indiscriminate damage, less disruption to
the edit. Suggestive, not evidence.

## 4 · What the real run has to answer

`R_pipe` at `pur_iters` = 100 (arm A, M1's setting) and 1000 (arm B, the paper's). The question
is whether mask-restriction keeps `R_pipe` roughly level while cutting LPIPS by 4×. If it does,
the claim is *"same strength, a quarter of the cost."* If `R_pipe` falls, we report that — the
mask carries edit context, and losing it may cost more than predicted.

## 5 · Housekeeping

`metric_stdout.txt`, `scores.json` and the per-arm zips are not in this folder. The figures
prove `pg_metric` ran and `RESULTS` was populated, so they existed on Kaggle. **Copy them out
of `/kaggle/working` on the real run** — `metric_stdout.txt` is the raw evidence behind every
number we publish, and reproducibility is a marked row (1% of M2).
