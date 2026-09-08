# M2 — "Show of Force" · due 18 Sep 2026

Rewritten 6 Sep. **The deliverable is a wash that is measurably stronger than M1's, and a
notebook short enough that another team will actually run it.**

## The method, in one sentence

**Wash only the region that survives into the output.** Keep IMPRESS's output inside the white
mask — the part the editor *preserves* — and restore the original pixels in the black region,
which the editor repaints from scratch.

```
purified_v2 = mask * purified_impress + (1 - mask) * protected
```

### Why — measured on M1's own archived run, before any new GPU time

| | inside the mask (30% of pixels) | outside it (70%) |
|---|---|---|
| PhotoGuard's shield | 1.33 – 2.64 levels | **0.47 levels** |
| IMPRESS's damage | 5.12 levels | **5.00 levels** |

PhotoGuard concentrates its budget **3–6× more densely inside the mask** — sensibly, since that
is the only region an inpainting editor regenerates. **IMPRESS pays uniformly**, so ~70% of the
damage it does buys nothing.

**Effect of the fix, already measured:** fidelity damage **−61 to −63%**, SSIM vs clean
**0.75 → 0.93**.

> You are about to repaint three walls and keep the fourth. Sanding all four is not thorough —
> it is wasted effort that damages the one wall you meant to keep.

## The three arms

| arm | wash | role |
|---|---|---|
| **N** | **none — edit the protected image** | **the origin.** `R_pipe = 0` by construction, LPIPS = the shield's own cost. **Any arm that lands below or right of N did more harm than not attacking at all.** Comparing washes only to each other can never reveal that. |
| A | IMPRESS `pur_iters=100` | the M1 baseline — without it there is no "stronger" |
| B | IMPRESS `pur_iters=1000` | the honest control: the budget the paper's own script uses, which M1 did not |
| C | **IMPRESS `pur_iters=100`, mask-restricted** | ours, at A's compute cost |

Shield fixed at `(40, 2)`. Every arm reports **`R_pipe`** (up is better) **and LPIPS vs clean**
(down is better) — the same two-axis scoreboard we hold challengers to. **A stronger wash moves
up and to the left.** A number that only goes up is a trade we failed to report.

**B matters even if C wins.** If B alone explains the gain, our M1 number was a budget artefact
and we say so in the post. Publishing the control that could embarrass us is what makes the rest
credible.

## Why this shape fits the rubric

Technical depth **3%** · Engagement **2%** · Description **2%** · Documentation **1%**.
**Only 2 of 8 marks are for results.** Three are for the code being *"beyond basic
implementation"*, and two depend on other people having interacted with us.

- **Technical depth** — a method derived from a measurement we made, not a knob we turned.
- **Documentation** — the notebook is M1 **+16 lines of code**. The diff *is* the contribution.
- **Engagement** — a short notebook gets run; a clever one does not. **This is the reason to
  keep the code small, and it is worth more marks than any extra diagnostic.**

## Engagement — starts the week of 8 Sep, not the 17th

1. **Publish the Track A pack** (`M2/challenge/tyro_wash_test_trackA/`). Built, zero GPU cost,
   and the M1 post gave **no close date** — add one. Suggest **15 Sep**.
2. **Read every Theme 2 Light M1 post**, wash one team's shield, post the numbers. That is the
   brief's "which aspect of the other team are you targeting" row.
3. Reply substantively to two other teams.

## Sequence

| when | what | who |
|---|---|---|
| wk of 8 Sep | publish Track A + close date; read Light posts | Echo |
| | run arms A and C (same cost, ~1 h) | Echo |
| wk of 15 Sep | run arm B (10× the purify stage only) | Echo |
| | wash one Light team's shield, post numbers | Echo |
| | draft Ed post §results and §documentation | **Nissa** |
| 17 Sep | figure, read-through, Moodle PDF | both |

Critical path runs through Echo — solo-resilient. Nissa's piece blocks nothing.

## Dropped, and why saying so is free marks

- **The FFT-targeted filter.** Tried and it does not work. We measured PhotoGuard's band and
  swept a Butterworth cutoff from f = 0.40 to 0.95; **every cutoff removed more real detail than
  shield**, because at `pg_eps = 16` the shield is ~1 grey level — quieter than the photograph's
  own grain. Reported as Limitation 5. It is what pointed us at the mask.
- **A0.5 / A0.6 / A0.7 diagnostics.** Internal debugging, not a deliverable. Their one durable
  output — FIX 12, the resolution bug — is baked into the notebook as the `clean512/` archive.
- **`pg_eps` sweep** → M3. **CLIPScore `R_edit`** → built, not run; only if time allows.

## The rule that keeps this on track

**Check the rubric before starting any investigation.** M1 nearly lost a week to three
diagnostics that overturned each other, six days before a milestone whose rubric had no results
row. And now the sharper version: **complexity is not neutral — it costs engagement marks.**
