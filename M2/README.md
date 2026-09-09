# M2 — Dark.Tyro · due 18 Sep 2026

**Start here. This is the only M2 document you need.** `_notes/` is history, not reading.

## The three notebooks

| notebook | what it is | who runs it |
|---|---|---|
| **`Dark_Tyro_M2.ipynb`** | **the attack.** M1 + 16 lines. The 16 lines are the contribution. | us |
| **`challenge/Tyro_Wash_Test_STARTER.ipynb`** | **the defence starter** we hand other teams. One `protect()` function. | them |
| **`Tyro_M2_diagnostics.ipynb`** | **the controls.** Checks our own measurement is valid. Not a defence tool. | us |

## The method, in one line

```
purified_v2 = mask · purified_impress + (1 − mask) · protected
```

Wash only where the editor **keeps** the pixels. Outside the mask the editor repaints from
scratch, so IMPRESS's damage there buys nothing.

> Repainting three walls and keeping the fourth. Sanding all four isn't thorough — it's damage
> to the one wall you meant to keep.

## What we know (all measured, n = 2, `pg_eps = 16`, shield `(40, 2)`)

**✅ The fidelity result — solid, reproducible to four decimals.**

| | IMPRESS (A) | ours (C) |
|---|---|---|
| LPIPS vs clean | 0.150 | **0.039** |
| SSIM vs clean | 0.758 | **0.937** |
| damage | 5.04 levels | **1.84 levels** |

Same compute. It reproduces exactly because it is geometry — it never touches the editor.

**❌ `R_pipe` — has no valid denominator at these settings.** Two controls say so:

| | seed floor | REAL shield | random, same L2 |
|---|---|---|---|
| img 1 | **0.472** | 0.584 | 0.737 |
| img 2 | **0.415** | 0.610 | 0.921 |

*(SSIM vs the seed-0 clean edit; lower = more disturbed)*

- PhotoGuard **beats random noise** at identical L2 → the shield is genuinely structured.
- But **changing the random seed disturbs the edit more than the shield does.** The shield moves
  the image only 0.5–0.9 grey levels. `1 − ssim_adv` is mostly generative variance.
- CLIPScore agrees independently: seed floor 2.19 pts, and neither image's protection efficacy
  clears it. On one image it is **negative** — the protected edit matched the prompt *better*.

**⭐ The finding worth leading with:** `pg_metric.py`'s SSIM is *IMPRESS's own* evaluation metric,
and it cannot detect PhotoGuard at the paper's own settings, because the pipeline's re-run noise
exceeds the signal. Two controls the paper never ran show it.

## The claim for the post

> Same attack strength to within our measured noise, **at a quarter of the perceptual cost.**

A **cost** claim, not a strength claim. It survives whatever happens next.

## What's left

1. **The gate — ~15 min.** Re-run at `pg_eps = 32`, then `64`. Recipe in `Tyro_M2_diagnostics.ipynb`
   section **D3**: one `N_no_wash` arm in `Dark_Tyro_M2.ipynb`, then point D2 at the new folder.
   Looking for `ssim_adv` to fall clearly **below** the ~0.42–0.47 seed floor.
   - **clears it** → re-run the four arms there (~40 min) and `R_pipe` becomes real
   - **doesn't** → run nothing more; publish the finding + fidelity
2. **Publish the challenge** (no GPU, everything built). Close date **15 Sep**. Reference entry is
   already banked: `challenge/my_submission/` at `EPS=3`, LPIPS **0.0665**, inside our own budget.
3. **Write the post.** Structure: the 16-line diff → fidelity → **the controls** → the challenge →
   limitations.

**Not doing:** n = 10, re-running arm B, Track B (deferred to M3), any new features.
Only 2 of M2's 8 marks are for results; three are for the code being readable and run by others.

## Folders

| | |
|---|---|
| `run_0907_pgeps16/` | the evidence — four arms, all stages, `scores.json` |
| `figures/` | the panel, the trade-off chart, the all-stages comparison |
| `challenge/` | spec, starter notebook, the 10-image pack, our reference entry |
| `_notes/` | superseded plans, smoke runs, the deferred Track B spec. **History only.** |
