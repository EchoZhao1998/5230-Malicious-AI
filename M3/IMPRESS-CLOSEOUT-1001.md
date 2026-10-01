# 🏁 IMPRESS half of M3 — CLOSE-OUT (1 Oct 2026, revised same day)

**Status: the measuring is finished. What is left is ~1 hour of housekeeping, then slides.**
No more GPU on this workstream. Every number below was recomputed on 1 Oct from the executed
notebooks' own output tables or from the archived PNGs, not copied from prose.

> **Revised 1 Oct (afternoon)** after Echo's eye test: §2 adds the reference parameters, §3 is new
> (what the visible noise actually is), §5 is the full slide plan. Two earlier statements were
> wrong and are corrected in §6: *"eps 16 is invisible"* and *"L∞ 60 = L2 noise piling into spots"*.

---

## 1 · The two runs that ARE the result (both Colab, n = 10, same pinned faces)

| run | notebook | what it answers | raw data |
|---|---|---|---|
| `run_0925_0152` | `M3/Dark_Tyro_M3_0925_colab.ipynb` (cells 1–9 executed) | **four wash arms** on ONE shared protect stage | Drive `FIT5230_M3/run_0925_0152/` |
| `sweep_0927_0210` | `M3/Dark_Tyro_M3_sweep_0927_Colab.ipynb` (all cells executed, no errors) | **shield sweep**: can PhotoGuard be made strong enough to be measured? | Drive `FIT5230_M3/sweep_0927_0210/` |

Kaggle runs of 19–20 Sep are **supporting evidence** (the reproducibility finding), not the
headline. Colab is canonical because the brief requires a Colab link.
All four arms share one protect stage (`ssim_adv` 0.521), so **the four-arm table is fully matched.**

---

## 2 · Our shield vs the reference shield — say this on the slide

| | attack | budget (`eps`) | stride (`step`) | effort (iterations × gradient repeats) |
|---|---|---|---|---|
| PhotoGuard, simple (encoder) attack | L∞ | 0.06 ≈ **8 grey levels per pixel max** | 0.01 | 1000 |
| PhotoGuard, complex (diffusion) attack | L2 | **16** | 1 | **200 × 10** |
| IMPRESS script default (`pg_mask_diff_helen.py`) | L2 | 16 | 1 | 200 × 10 — a copy of PhotoGuard's complex attack |
| **Ours (M2 and M3)** | L2 | 16 (64, 256 in the sweep) | 1 (4 in the sweep) | **40 × 2 = 1/25 of the reference effort** |

Checked against both repos' code on 1 Oct. **Why 1/25:** ~77 min per image at 200 × 10 on a free
T4 (HANDOVER, 16 Aug) → ~13 h for ten faces. **Not re-run** — stopping rule.

**What the knobs mean:** `eps` = the fence (largest total change allowed). `step` = stride length
per iteration. `iterations × repeats` = how many strides, and how carefully each direction is
chosen. Real strength = how far the noise actually travelled and how well-aimed it is. At step 1
× 40 iterations it never reached the fence, so `eps` did nothing (16 ≡ 32, measured 9 Sep); at
step 4 it reaches the fence by eps ≈ 64 and saturates (64 ≡ 256 in size, measured 19 Sep).

---

## 3 · ⭐ What the visible noise actually is (measured 1 Oct, zero GPU)

Echo's eye test: noise is **clearly visible** at eps16/step1, eps16/step8, eps64/step4, eps256/step4.
The difference image `protected − original` (×5) shows **two different things**:

| component | where | eps 16 → eps 256 (max change, grey levels) | source |
|---|---|---|---|
| **smooth glow + hard seam** | around the head, along the face edge | **35 → 35** and **56 → 56** — unchanged | **IMPRESS's save step** |
| **fine speckle** | inside the face | **48 → 97** and **57 → 122** — doubles | **PhotoGuard's noise** |

At eps 16 the smooth part dominates (L2 2133 vs 1341; 5715 vs 2501). So **at the M2 setting, most
of what you can see is not PhotoGuard.** At eps 256 PhotoGuard's own speckle is visible on the face.

**Mechanism (from the code, consistent with the measurement):** the attack fills the region the
editor will repaint with grey (`masked_image = image * (mask < 0.5)`), then
`recover_image(..., background=True)` pastes the original back with the **unbinarised** mask, so
grey bleeds in wherever the mask edge is soft. On a dark background, grey reads as a bright glow.

**Scope:** measured on 2 faces (`1233476865`, `2139626906`) from `M3/_archive/raw_kaggle_0919_0920/` (Kaggle, same
code). Figure: `M3/figures/slides/fig4_what_the_visible_noise_is.png`.

**Consequences — be precise:**
- **The main finding is unaffected.** The glow sits mostly in the region the editor repaints and
  is identical across settings; the engagement counts come from the edits.
- **Shield LPIPS includes the glow.** So "0.027 at eps 16" is NOT "invisible" and NOT "PhotoGuard
  alone". Call it *"the protected image as IMPRESS's pipeline produces it"*. The **rise** from
  0.027 to 0.096 is the shield getting stronger, since the glow is constant.
- **Do not quote L2 or L∞ as "the shield's size".** They include the glow. On 6/10 faces the
  measured L2 exceeds what PhotoGuard's L2 budget (16 × 127.5 = 2040) plus rounding can produce.
- **Four-arm LPIPS comparisons stay valid**: every arm starts from the same protected image, so
  the glow is in all of them equally (N = 0.034 is that floor).

---

## 4 · The numbers for the slides

### Four arms (`run_0925_0152`, shield (40,2), eps 16, step 1)
| arm | wash | R_pipe % | LPIPS vs original |
|---|---|---:|---:|
| N — no wash | — | 0.00 | 0.034 |
| A — IMPRESS | 100 iters | −1.08 | 0.185 |
| B — IMPRESS | 1000 iters (paper budget) | −0.22 | 0.144 |
| **C — ours (masked)** | 100 iters, masked | +1.33 | **0.060** |

- R_pipe: all four inside the measured ±2–4 pp noise band → **no R_pipe claim, for anyone.**
- LPIPS: C does **68% less damage than A, 59% less than B**.
- B = 10× A's compute, **no measurable gain** (purify 139 vs 15 min, Kaggle-measured).

### Shield sweep (`sweep_0927_0210`)
| setting | noticed (band 0.010) | noticed at wide band 0.027 | **noticed AND within LPIPS 0.10** | shield LPIPS median | over budget |
|---|---:|---:|---:|---:|---:|
| eps 16, step 1 (M2) | 1 | 0 | **1** | 0.027 | 0/10 |
| eps 64, step 4 | 2 | 2 | **1** | 0.096 | 3/10 |
| eps 256, step 4 | 1 | 1 | **0** | 0.098 | 3/10 |

The one face noticed at every setting (`1961032923`) costs LPIPS 0.18 at eps 64/256.

### Reproducibility (Kaggle, 3 identical runs, `RESULT-0920` §2)
The only face ever noticed at the M2 setting was noticed in **1 run of 3**.

---

## 5 · The 3-minute IMPRESS segment (rubric bullet 1: "key outcomes … progress since M2")

**Fits the brief:** bullet 1 = this segment (~3 min). Bullet 2 (~2 min, other teams' targets) and
bullet 3 (individual strategy) = ESD-x, built in the other chat. Nothing about IMPRESS goes there.

**Design rules — the slides must work even with no voice at all:**
- **Title = the claim**, one plain sentence. Reading only the four titles tells the whole story.
- One picture per slide + at most two big numbers. No `R_pipe` / `ssim_adv` / `pg_eps` on a slide.
- Ours = blue, everything else = grey (the figures already do this).
- Footer on slides 2–4: *"n = 10 faces · SD inpainting editor · one prompt · PhotoGuard as run in IMPRESS's code"*.
- Script below is **~310 words ≈ 2 min 50 s at an unhurried 110 words/min**, written to be read
  verbatim from notes or recorded as a voice-over, whichever the accommodation allows.

### The logic — Why → How → So what
| | slide | time | the one idea |
|---|---|---|---|
| **Context** | 1 · What we attack, what M1 and M2 built | 0:00–0:50 | the attack + our M2 change + our M2 test |
| **Why** (M3) | 2 · We ran our own test on our own result | 0:50–1:35 | M2's score was measuring a shield that mostly wasn't working |
| **How** (M3) | 3 · Can the shield be made strong enough to notice? | 1:35–2:20 | stronger costs the photo, not noticed more |
| **So what** (M3) | 4 · Judge the wash by the photo, not the broken metric | 2:20–3:00 | our wash: ⅓ of IMPRESS's photo damage, same cost |

---

### Slide 1 — **"PhotoGuard protects photos with noise; IMPRESS washes it off. We made the wash gentler."**
**Picture:** a two-row pipeline. Row 1: photo → *+ PhotoGuard noise* → AI editor → broken edit.
Row 2: protected photo → *wash* → AI editor → normal edit. Under it, a timeline strip:
**M1** reproduce IMPRESS vs PhotoGuard · **M2** masked wash + seed-noise test · **M3** test ourselves.
*(Not built yet — a simple diagram; the faces from `fig4` can be the photo thumbnails.)*

> **Script (≈ 85 words):** PhotoGuard adds noise to a photo so that AI image editors produce a
> broken edit. IMPRESS, published at NeurIPS 2023, is an attack: it washes that noise off. In
> Milestone 1, we got IMPRESS running against PhotoGuard on a free Colab GPU, which needed eleven
> code repairs. In Milestone 2, we made one change: wash only the part of the photo the editor
> keeps. We also published a test: a shield only counts if it changes the edit more than
> re-rolling the random seed does.

### Slide 2 — **"In M3 we ran our own test on our own result: the shield beat seed noise on 1 face in 10."**
**Picture:** `figures/slides/fig1_gate_M2_setting.png`. **Big number:** **1 / 10**.

> **Script (≈ 70 words):** In Milestone 3, we applied that test to ourselves, on ten faces instead
> of two. At our Milestone 2 setting, the shield beat seed noise on only one face in ten, and that
> face did not repeat across identical runs. So our Milestone 2 recovery score was measuring a
> shield that mostly was not working. That is our main progress since Milestone 2: we now know
> which of our numbers mean something.

### Slide 3 — **"Making the shield stronger costs the photo more, but is not noticed more."**
**Picture:** `figures/slides/fig2_shield_sweep_two_panels.png`. **Big numbers:** **1 · 1 · 0** (noticed within budget).

> **Script (≈ 75 words):** So we made the shield stronger, at three strengths. It was noticed on
> one, then two, then one face out of ten. Counting only faces where the photo stayed inside our
> damage budget: one, one, and zero. A stronger shield damages the photo more, without being
> noticed more. One limit we state openly: our shield used one twenty-fifth of the reference
> number of iterations, because the full setting needs about thirteen hours of GPU time.

### Slide 4 — **"On the measure that works, our wash does about one-third of IMPRESS's photo damage."**
**Picture:** `figures/slides/fig3_four_arms_photo_damage.png`. **Big numbers:** **0.060 vs 0.185**.

> **Script (≈ 80 words):** On recovery scores, every wash, including ours, sits inside measurement
> noise, so we claim no winner there. On photo damage, which we can measure cleanly, our masked
> wash does about one-third of IMPRESS's damage at the same cost. IMPRESS at ten times the compute
> gains nothing measurable. Our takeaway: at the shield strength we could afford, this attack's
> success cannot be judged by its own metric. Judge it by what it does to the photo.

### Backup slides (not presented; for Q&A only)
- **B1 · "What you see on a protected photo is mostly IMPRESS's save step"** — `fig4`. For the
  question *"isn't PhotoGuard supposed to be invisible?"*
- **B2 · Parameter table** from §2 — for *"did you use the paper's settings?"*
- **B3 · Four-arm table with recovery scores** from §4 — for *"what were the R_pipe numbers?"*

### Wording check — every sentence above maps to a measured number
| sentence | source |
|---|---|
| "eleven code repairs" | HANDOVER §"Repairs: now ELEVEN" (22 Aug) |
| "1 face in 10", "did not repeat" | `sweep_0927_0210` row (16,1); Kaggle 3 identical runs, `RESULT-0920` §2 |
| "one, two, one" / "one, one, zero" | §4 sweep table |
| "one twenty-fifth", "thirteen hours" | §2 (40×2 vs 200×10; ~77 min/image × 10) |
| "inside measurement noise" | ±2–4 pp band vs R_pipe −1.08 … +1.33 |
| "about one-third", "same cost" | LPIPS 0.060 / 0.185 = 0.32; A and C both 100 iterations |
| "ten times the compute gains nothing measurable" | B −0.22 vs A −1.08, inside noise; LPIPS not worse |

### ⛔ Claims that must NOT appear (each one was nearly made)
| don't say | because | say instead |
|---|---|---|
| "Our wash removes more protection than IMPRESS" | R_pipe +1.33 vs −1.08 is inside noise | "No wash wins on recovery; ours wins on photo damage" |
| "1000 iterations is worse than 100" | inside noise | "10× compute, no measurable gain" |
| "The shield is invisible at eps 16" | eye test + fig 4: visible, mostly from IMPRESS's save step | "The protected image as IMPRESS produces it" |
| "PhotoGuard's noise is X grey levels / L2 Y" | L2/L∞ include the save-step glow | quote LPIPS, or the speckle max from §3 |
| "PhotoGuard doesn't work" | 1/25 effort, one editor, one prompt, IMPRESS's code | "In IMPRESS's benchmark at an affordable budget…" |
| any `ssim_adv` 0.521 next to a seed floor | pg_metric convention, +0.019 off | floors compare to `ssim_pair` (0.539) |
| FSIM, or screenshot of four-arm cell 8 | FSIM is 0.0 everywhere; cell 8 prints "N_no_wash STRONGER and CHEAPER" (noise) | — |

---

## 6 · Corrections made on 1 Oct (so nobody re-uses the old wording)
1. **"eps 16 is invisible (LPIPS 0.027)" — WRONG.** Low LPIPS is not invisibility; the eye test
   and fig 4 show visible artifacts, mostly IMPRESS's save step.
2. **"L∞ 60 at eps 16 means L2 noise piles into visible spots" — WRONG.** The largest changes at
   eps 16 are in the smooth save-step glow (max 35–56), not PhotoGuard speckle.
3. **"Shield LPIPS 0.099 at eps 256"** → the median is **0.098** (0.09845 rounded).

---

## 7 · Close-out checklist (~1 h, zero GPU)

1. **[Colab, 10 min] Tidy the hosted four-arm notebook.** Cells 10–13 never ran. Replace 10–12
   with ONE markdown cell pointing to the sweep notebook; delete or move 13. Under cell 8 add:
   *"R_pipe differences here are inside the ±2–4 pp noise band; the verdict lines are not
   findings."* Do not re-run. File → Download → overwrite the local copy.
2. **[Colab, 5 min] Add one markdown cell to the sweep notebook's Limitations:** our shield runs at
   40 × 2 vs the reference 200 × 10; shield LPIPS includes IMPRESS's save-step glow (§3).
3. **[5 min] Check both share links open WITH outputs** in a private window.
4. **[5 min] Copy `REPORT_sweep_0927_0210.zip` from Drive → `M3/results/`** and unzip.
5. ~~**[5 min] Archive superseded notebooks**~~ **done 1 Oct (folder clean-up)** — → `M3/_archive/`: `Dark_Tyro_M3.ipynb` (20 Sep),
   `Dark_Tyro_M3_sweep.ipynb` (unexecuted), `impress-m3-0920_*.ipynb` (Kaggle). Nothing deleted.
6. **[30 min] Draft slides 1–4 + backups B1–B3** from §5; build the slide-1 diagram. Polish design in 13–19 Oct, not now.
7. **[5 min] Commit** — `git add M3 HANDOVER.md Admin && git commit -m "close IMPRESS (Colab canonical) + slide figures"`.

**Done when:** both links open with outputs, no unexecuted cell in either, slides 1–4 exist in
draft, commit pushed. After that IMPRESS is touched only for the 13–19 Oct rehearsal.
