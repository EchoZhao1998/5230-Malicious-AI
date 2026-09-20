# 🔒 LOCKED — the IMPRESS / Tyro half of M3

> ## ✅ CLOSED 19 Sep 2026. The `pg_eps = 256` run is done; the stopping rule fired.
> **Result: 2 engaged + 1 indeterminate of 10 (three-state gate) at 3.5x the fidelity budget, 4/10 images over LPIPS 0.10. Criterion not
> met, and the engaged subset is biased toward easy gates — so the four arms stay at the M2
> setting.** Full write-up: **`M3/RESULT-0919-FINAL-shield.md`**. No further GPU on this
> workstream. Everything from here to 13 Oct belongs to the ESD-x bypass.

**Locked 19 Sep 2026.** Supersedes §1 of `M3-PLAN.md`. Covers the **5 + 5 marks** (Framework
Progress, Colab hygiene) only. The ESD-x bypass (the 11) is a separate workstream in its own chat.

**Stopping rule, agreed before starting: ONE more GPU run. Whatever it returns, the notebook work
is finished and the write-up begins.**

---

## 0 · What is already measured and will not be re-run

| run | setting | engaged | median margin above floor |
|---|---|---:|---:|
| `run_0919_0406` N arm | eps 16, step 1 (the M2 setting) | 1/10 | +0.0752 |
| sweep | eps 16, step 2 / 4 / 8 | 1/10 each | — |
| probe | **eps 64, step 4** | **2/10** | **+0.0314** |

Plus, zero GPU: perturbation size for all of the above, and (cell 7f) shield LPIPS for all of them.

## 1 · ⭐ The finding — and it is about the baseline paper, not about our wash

**`pg_eps` is live after all, and the 9 Sep "inert" result was conditional.** At `step_size = 1`
the optimiser never reached the L2 ball, so 16 and 32 looked identical. At `step_size = 4` it does
reach it: raising eps 16 → 64 grew the perturbation by **+21% median L2** and cut `ssim_adv` by
**0.045 median** against the M2 setting. The knob works. It was mislabelled, not dead.

But the knob is not enough, and the shape of the shortfall is the result:

- 4x the reference budget moves engagement **1/10 → 2/10** (4/10 counting the two within 0.012).
- Median margin above the floor halves, **0.0752 → 0.0314**, but does not close.
- Linear extrapolation on the measured slope puts **5/10 engagement at `pg_eps` ≈ 650 — roughly
  40x the reference default.**
- At only 4x, L-inf already reaches **96 levels median (74–123)** out of 255. The shield is no
  longer invisible.

> **The evaluation's sensitivity floor sits above the defence's usable range.** IMPRESS's published
> metric only registers PhotoGuard once PhotoGuard is strong enough to be seen — and a protection
> you can see has already failed at being a protection.

That is a falsifiable statement about a NeurIPS 2023 evaluation platform, measured at n=10 across a
2.5x range of editor stability, with the mechanism (L2-ball clipping vs optimiser convergence)
separated by direct measurement. **It is worth more than a better `R_pipe`.**

## 2 · The one remaining run
**`pg_eps = 256`, `pg_step_size = 4`** — change `_EPS` in cell 7e and re-run it. Cost: one setting.

Three points (16 / 64 / 256) turn a two-point line into a measured curve, so the "≈40x" claim
becomes an extrapolation from data rather than from one gradient.

**Two-axis success, both required:**
1. **≥ 5 of 10 engaged**, and
2. **shield LPIPS ≤ 0.10** — our own published challenger budget, measured by cell 7f.

| outcome | what happens next |
|---|---|
| both met | run cell 7 (four arms) at that setting. **That table is the M3 result.** |
| engaged but **over** LPIPS budget | **do not use it.** Report the curve and the budget crossing — that IS the sensitivity-floor finding, with the crossing point measured |
| neither | same write-up, one fewer data point |

**In two of the three outcomes the deliverable is identical.** That is why this is the last run.

## 3 · ⛔ Explicitly not doing
- **`attack_type = linf`.** Dropped. `pg_eps` is the live lever; adding a second geometry opens a
  branch we have no budget to finish, and the finding does not need it.
- Any further `pg_step_size` work. Settled: it re-randomises, it does not steer, and past step 4 it
  only raises L-inf.
- A new method, a new metric, rebuilding arm B, reviving the CLIP proxy.
- Re-running the four arms at the M2 setting "for completeness". They exist; the gate explains them.

## 4 · What ships (the 5 Colab-hygiene marks)
One clean top-to-bottom run committed **with outputs**, by **19 Oct**. Cells in order, no dead ends:
pinned ten + floors → shield sweep → perturbation diagnostic → fidelity → four arms → gate →
figures. Markdown narrates problem → method → result → limitation. Delete nothing, but move
superseded cells out rather than leaving them unrun.

## 5 · Calendar (revised — ahead of `M3-PLAN.md`)
| week | this workstream |
|---|---|
| 21–27 Sep | the eps 256 run · cell 7f · **write the finding up while it is fresh** |
| 28 Sep – 12 Oct | **nothing.** All time to the ESD-x bypass (the 11 marks) |
| 13–19 Oct | clean end-to-end run committed with outputs |
| 20–21 Oct | buffer only |

**The point of locking: this half is worth 10 of 25 marks and it is now 90% done. Everything from
28 Sep belongs to the 11-mark row.**

---

## 6 · Cell hygiene — merge AFTER the last run, not before

The investigation cells accumulated one question at a time, which was right while the answer to
each decided the next. For the shipped notebook they collapse into two, because there were only
ever two questions:

| ship as | merges | asks | GPU |
|---|---|---|---|
| **7A · Shield sweep** | 7s + 7e | across a grid of `(pg_eps, pg_step_size)`, how many of ten engage? | yes |
| **7B · Shield cost** | 7d + 7f | what does each of those shields cost — L2, L∞, LPIPS? | **no** |

7A takes a list of `(eps, step)` pairs with `(16, 1)` as its first row, which removes the hardcoded
`BASELINE` dict and makes the cell self-contained. 7B reads only archived PNGs. Together they give
the two figures the finding needs: **engagement vs setting** and **cost vs setting** — the same
two-axis discipline the Tyro Wash Test holds challengers to, applied to the shield itself.

**⚠️ Do not do this refactor until the `pg_eps = 256` run is finished and its numbers are recorded.**
Rewriting the harness between a measurement and the run that depends on it is how a working result
gets lost to a silent change — the `PG` f-string trap in the sweep was one keystroke away from
exactly that.

**Nothing is deleted.** 7s/7d/7e/7f move to an appendix section at the bottom of the notebook, or
to `M3/_archive/`, with their outputs intact — they are the provenance for the merged table.

---

## 7 · Platform — the clean run goes on COLAB (decided 19 Sep)

All 19 Sep runs (`run_0919_0406`, the sweep, both eps probes) were **Kaggle T4**. The final clean
run will be **Colab**. Two reasons, one of them not optional:

1. **The brief requires it.** M3 submission is *"Link of Google Colab included in a PDF or text file
   to Moodle"*. A Kaggle notebook cannot be the submitted artefact.
2. Colab was already the M2 cold-run platform, so the shipped notebook matches the shipped post.

### ✅ Cross-platform drift is already measured — the conclusions hold
The two M2 images, Colab (14 Sep) vs Kaggle (19 Sep), same shield:

| image | Colab | Kaggle | Δ |
|---|---:|---:|---:|
| 1233476865 | 0.5055 | 0.5018 | −0.0037 |
| 1525918600 | 0.6404 | 0.6372 | −0.0032 |

**~0.004 on `ssim_adv`.** Against median margins of 0.027–0.075, the shield finding is unaffected
by the platform switch. Worth stating in the write-up: it is a free robustness check most teams
will not have.

### ⚠️ But it creates one real methodological wrinkle — fix it in 7A
`seed_floor_10.json` was measured **2026-09-10 on a Kaggle T4**. A Colab run would compare Colab
`ssim_adv` against Kaggle floors — a cross-platform comparison with ~0.004 of drift on each side.

Two margins in the final data sit inside that band: `178046512` at eps 256 is ENGAGED by **0.0062**,
and at eps 64 it was BLIND by **0.0059**. **A platform switch could flip that image, and with it the
headline count 3/10 ↔ 2/10.**

**Fix (zero GPU, ~5 lines, goes into the merged 7A): a three-state gate.**
`ENGAGED` / `BLIND` / **`INDETERMINATE`** for any image whose |margin| < 0.010 — the measured
cross-platform drift on both sides. Report as *"k engaged, m indeterminate, of ten."*

Do **not** re-measure the floors. They are published with the challenge; changing them now would
alter a public artefact and invalidate the scoring runbook. The uncertainty band is the honest
answer and it costs nothing.

> Same reasoning as the seed floor itself, one level up: a difference smaller than the measurement's
> own spread is not a difference. We applied that to `R_pipe`; it applies to the gate too.

### Colab practicalities (all already handled in cell 1, listed so they are not rediscovered)
- `ARCHIVE` goes to Drive on Colab — a disconnect otherwise loses the run.
- Per-arm zip before the next arm starts, so a drop costs one arm.
- Timestamped `RUN_TAG`, so a re-run never overwrites.
- **Not** Kaggle P100 (`sm_60`) if Kaggle is ever used again — cell 1 stops it.
- **✅ PRE-DECIDED 19 Sep: arm B RUNS in the clean pass.** It is the honest control — the paper's
  own 1000-iteration budget — and citing it from a 2-image run while everything else is n=10 would
  be the one soft spot in the table. Cost accepted.

### Execution budget for the clean pass (Colab)
Rough, from the notebook's own cost model: **N + A + C ≈ 30–55 min · arm B alone ≈ 90 min ·
total ≈ 2–2.5 h**, protect stage shared. **Verify before committing the evening:** run arm A first
and time it — B is ten times A's wash, so A's clock gives a real estimate instead of this one.

**You cannot reserve a free Colab GPU.** There is no booking; allocation is best-effort and the
free tier disconnects on idle. What makes the session survive:
- Drive-mounted `ARCHIVE` (cell 1 does this on Colab) — otherwise a disconnect loses everything.
- Per-arm archive + zip before the next arm starts — a drop costs one arm, not the run.
- Timestamped `RUN_TAG` — a resumed run never overwrites a finished one.
- Keep the tab open and the laptop awake; start when GPU demand is low (weekday morning MYT).
- If it drops mid-run: set `RUN_TAG` manually to the interrupted run's tag, then run only the arms
  that did not finish. The archive folder is the record, not the kernel.

**If reliability matters more than the platform label for a rehearsal:** Kaggle gives a predictable
weekly GPU quota and a headless "Save Version / Run All" that executes the whole notebook in the
background — better for a long unattended pass. Colab free has no equivalent on the free tier.
So: **rehearse on Kaggle if needed, but the submitted executed notebook is Colab.**
