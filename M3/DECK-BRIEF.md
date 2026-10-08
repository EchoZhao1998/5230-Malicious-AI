# M3 deck — assembly brief (8 Oct 2026)
Presentation in the tutorial, **15 min**, M3 due 22 Oct. Solo: Echo presents every section.
Plan **≈ 12 min spoken + 3 min buffer** (accommodation). Scripts at ~110 words/min.
Rules (Echo's, 13 Sep): **title = the claim** in one plain sentence · one picture + at most two numbers per
slide · plain English, no metaphors · no internal names (R_pipe, arms, pg_eps) on slides.

## The brief's three sections → our slides
| § | brief asks | time | marks it feeds | content |
|---|---|---:|---|---|
| A | outcomes + progress since M2 | 3:00 | Framework 5 | IMPRESS: the wash, trained and watched |
| B | ideas tested on other teams' targets | 2:00 | Peer Engagement 3 | what we ran on Cyber Ninjas' target |
| C | one distinct strategy, why it worked/failed, reaction, lessons, role | ≤10:00 (plan 7:00) | Design 4 · Critical 5 · Role 2 | ESD-x: keen observation |

## A · IMPRESS (3 min) — ⚠ script needs rewriting
Old script in `IMPRESS-CLOSEOUT-1001.md` §5 tells the shield-sweep story. 8 Oct handover: rebuild around training.
| # | title (claim) | picture | source |
|---|---|---|---|
| A1 | PhotoGuard protects photos with noise; IMPRESS washes it off. We made the wash gentler. | pipeline diagram (**to build**) | — |
| A2 | In M3 we trained the wash and watched the edit converge onto the clean target. | `M3_training/REPORT_part2/fig4_training_progress_one_face.png` | Part 2 |
| A3 | Longer washing recovers more; our masked wash does the least damage to the photo. | `M3_training/REPORT_part2/fig2_iteration_curve.png` | Part 2 |
| backup | Why only these shield settings | `figures/slides/fig2_shield_sweep_two_panels.png` | sweep_0927 |
Numbers: C = 68% less photo damage than IMPRESS (A), 58% less than B · B's recovery gain is suggestive only (2 of 10 faces).

## B · On Cyber Ninjas' target (2 min) — the experiments
| # | title (claim) | picture | source |
|---|---|---|---|
| B1 | We tested the ESD authors' Van Gogh erasure against unmodified SD v1-4 on 12 ways of asking. | two-model rule as a 4-row table (**type on slide**) | T1 notebook md cell |
| B2 | No way of asking brought Van Gogh back; a neighbouring painter was unaffected. | `esd_attrack/figures/esdx_all_routes.png` | T1 + T2 |

## C · Individual strategy: keen observation (7 min)
| # | title (claim) | picture | rubric row |
|---|---|---|---|
| C1 | Their test set had no other alphabets, and their own leetspeak argument gave us the control. | quote of their case 5 + the rule | Design 4 |
| C2 | We posted the prediction before measuring it. | Ed screenshot (**to take**) | Design / Critical |
| C3 | The prediction was wrong: the base model reads 梵高 as a place, not a painter. | `esd_attrack/figures/esdx_t1_alphabet_base_seed0.png` | Critical 5 |
| C4 | Measured against its own floor, the erased model looked like it kept 99%; on a fixed reference it keeps none. | two numbers: 99% → −4% (**type on slide**) | Critical 5 |
| C5 | The score says erased, but the swirling sky survives when you describe it. | `esd_attrack/figures/esdx_slide_strip_seed6.png` | Critical 5 |
| C6 | Why it failed, what would improve it, and how they reacted. | text, 3 short blocks | Critical 5 |
| C7 | What I did: design, both runs, all posts — a one-person project. | timeline 16 Sep → 8 Oct | Role 2 |
All C numbers and wording: `esd_attrack/RESULT-1008-T2.md` (+ `RESULT-1002-crossscript.md`).
Limitation to say once (C6): the authors' weights differ from our base copy outside the erased layers (other/attn2 = 0.81).

## Still to do before assembling
1. Post `esd_attrack/ESDx-T2-reply.md` on Ed (closes the promise). Screenshot the thread for C2.
2. Upload the executed T2 notebook to Colab with outputs; share as Viewer.
3. Rewrite the A script around the training figures.
4. Moodle PDF with **four** Colab links: IMPRESS Part 1, Part 2, ESD-x test 1, ESD-x test 2.
