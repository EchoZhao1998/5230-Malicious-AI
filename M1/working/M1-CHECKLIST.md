# M1 — what is left, and nothing else
*Dark.Tyro · 22 Aug 2026 · six days to the 28th*

**M1 is 2%. Its rubric has no row for results.** It has five rows: Baseline Justification
0.5 · Problem Statement 0.5 · Challenge Design 0.5 · Initial Customization & Setup 0.4 ·
Clarity 0.1. The setup row is bought by the ten repairs and a pipeline that demonstrably
runs. **You already have that.**

Everything else this week was M2 work wearing an M1 costume. It is parked in
`M2_diagnostics.ipynb` and does not need another minute before the 28th.

---

## The submission is two things

1. **`M1/Dark_Tyro_M1_FINAL.ipynb`** — 21 cells, frozen. Setup, ten repairs, the sweep,
   `R_pipe`, the 3-panel figure, a save check. Nothing else.
2. **The Ed post** — `M1/M1_Ed_Post_DRAFT.md`, plus a link to the notebook, plus the link
   pasted into a PDF/txt on the Moodle M1 page.

That is the whole deliverable.

---

## Remaining work, in order

| # | task | owner | time | status |
|---|---|---|---|---|
| — | Ed post §1 and §2 | Nissa | — | ✅ **done** |
| 1 | Run `Dark_Tyro_M1_FINAL.ipynb` on Kaggle — **Accelerator: GPU T4 x2, NOT P100** — `CONFIGS = [(40,2),(200,2)]`, download the zips | Echo | ~30 min | ⬜ |
| 2 | Paste Nissa's §1/§2 into `M1_Ed_Post_DRAFT.md`, check the `‹CHECK›` correction survived | Echo | 15 min | ⬜ |
| 3 | Drop the 3-panel figure into §4 | Echo | 10 min | ⬜ |
| 4 | Tier 3 pack (`TIER3-SPEC.md`) — **run B4 first** | Echo | ~2 h | ⬜ |
| 5 | Share link "anyone with the link", tested logged out | Echo | 5 min | ⬜ |
| 6 | Post to Ed, then submit the URL on Moodle | Echo | 15 min | ⬜ |

**Critical path: about half a day of your time.** Nissa's half is in.

## 🛑 Kaggle accelerator: T4, not P100

The P100 is compute capability **6.0 (`sm_60`)**, and current PyTorch wheels ship kernels only
for `sm_70` and above. Everything loads, then the first CUDA op dies with *"no kernel image is
available for execution on the device"*. Nothing in the notebook can fix that — **change the
accelerator.** Cell 1 now detects it and stops you before the wait.

T4 is roughly 2.2× slower here, so `(40,2)+(200,2)` is ~31 min rather than ~17. Still under
2% of your weekly quota.

## Explicitly NOT before the 28th

- Why purification underperforms — the whole A0.5 / A0.6 / A0.7 line
- Re-running anything at higher `pur_eps` or `pur_iters`
- `pg_eps` sweep · ≥ 5 faces · LPIPS · CLIPScore edit-success rate
- The frequency analysis and the fidelity-vs-success chart

All of it is real work. **None of it is marked on the 28th.**

---

## If someone asks "does your attack work?"

> At the reference settings, barely — about 11% recovery at the weakest shield and nothing
> measurable at 400 gradient-units. We know that, we can show the measurement, and finding
> out *why* is what M2 is for.

That is a complete and defensible answer. M1 asks whether you can justify a baseline, state a
problem, design a challenge, and get a 2023 codebase running in 2026. **You can, and you did.**

## Does the IMPRESS baseline still stand? Yes.

It clones, patches, runs end to end, and produces images plus metrics on two different free
platforms. That is what "the baseline is viable" means, and it was settled on 21 Aug.

A purification attack that recovers little **at one set of reference settings** is a result
about those settings, not evidence the code is broken. Nothing found this week touched the
pipeline — the resolution mismatch that voided the diagnostics was in the *analysis scripts*,
comparing full-resolution originals against 512×512 outputs. `pg_metric.py` compares the
pipeline's own 512×512 outputs to each other and was never affected.

**Do not reopen the baseline decision.** The escape hatch, if compute ever became impossible,
was always *a smaller experiment, never a different paper*.
