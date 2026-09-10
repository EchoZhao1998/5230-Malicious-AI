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

## What's left — 9 Sep, gate CLOSED

1. ~~The gate.~~ **DONE and negative.** `pg_eps = 32` (`0909_SMOKE_ESP32/`) produces the *same
   perturbation as 16, to within 1%* — L2 2645.8→2641.6 and 1860.4→1841.1, damage 0.73→0.72
   levels. `pg_eps` is **not the binding constraint** at `pg_iters=40, pg_step_size=1`; the L2
   ball is never reached. `ssim_adv = 0.571`, still far above the 0.42–0.47 seed floor.
   **⛔ Do not run `pg_eps = 64` — same knob, same answer.** The untested lever is
   `pg_step_size`, and that is M3.
   *This is a better result than the one we wanted:* the paper's documented way to strengthen
   the shield does not strengthen it, and we can show that in one table.
   ⚠️ At eps 32 arm A appears to beat C by 1.14 pp. That is **inside the 2–4 pp noise floor** —
   the shield did not change between runs, so any R_pipe movement is noise by definition.
   Fidelity still favours C ~4x at both settings (0.039 / 0.038 vs 0.150 / 0.150).

2. **Publish the challenge** — no GPU, everything built. `challenge/tyro_wash_test_trackA.zip`
   exists as of 9 Sep. Needs only a public Colab link for the starter notebook.
   Say **"send by 15 Sep, results in the 18 Sep post"** — the M1 post already promised 18 Sep.

3. **Finish the post.** Draft is `M2-POST-DRAFT.md`, already updated with the eps-32 table.

**Not doing:** n = 10, re-running arm B, Track B (deferred to M3), any new features.
Only 2 of M2's 8 marks are for results; three are for the code being readable and run by others.

## Folders

| | |
|---|---|
| `run_0907_pgeps16/` | the evidence — four arms, all stages, `scores.json` |
| `figures/` | the panel, the trade-off chart, the all-stages comparison |
| `challenge/` | spec, starter notebook, the 10-image pack, our reference entry |
| `_notes/` | superseded plans, smoke runs, the deferred Track B spec. **History only.** |
