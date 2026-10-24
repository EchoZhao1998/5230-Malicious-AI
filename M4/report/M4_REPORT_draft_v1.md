# Attacking and Defending Image Immunisation: A Semester of Adversarial Gameplay on PhotoGuard and ESD-x

**Wanting Zhao, 35507071** · FIT5230 Malicious AI, Milestone 4 · Team Dark.Tyro (Theme 2, Text-to-Image, Dark side)

<!-- DRAFT v1 · 24 Oct 2026 · every number traces to a file named in the % SOURCE comments.
     Markdown is the drafting format; the submitted PDF comes from the IEEEtran template
     (\documentclass[journal,transmag]{IEEEtran}). [ECHO: …] = a line only you can write. -->

---

## Abstract

PhotoGuard protects a photo from AI editing by adding a small adversarial perturbation (a "shield"). IMPRESS removes the shield with a 100-iteration optimisation loop (a "wash"). Over the semester I attacked PhotoGuard through IMPRESS. I also attacked another team's concept-erasure defence (ESD-x). This report has four parts: a weekly log of my strategy, a recap of the system, and two new demos built after M3. In the enhancement demo, a few denoising steps of Stable Diffusion inside our M2 mask (version D) replaced IMPRESS's optimisation loop. It did 62% less photo damage than IMPRESS and ran about 93× faster per face. But it missed the bar I set before the run: it did 19% more damage than our own masked wash. In the role-reversal demo I defended PhotoGuard with a detector for washed photos. The pre-registered detector flagged nothing. The data instead showed that IMPRESS-washed photos have about 9× the VAE round-trip error of clean photos, so all ten separate from all fifty clean photos. Because I chose that direction after seeing the data, I report it as an observation, not a result. The masked washes were invisible to the same feature.

**Index Terms** — adversarial purification, diffusion models, image immunisation, PhotoGuard, IMPRESS, concept erasure.

---

## I. Introduction

Image editors built on diffusion models, such as Stable Diffusion inpainting [6], can turn one real photo into a convincing fake in seconds. PhotoGuard [1] is a defence: it adds a perturbation that misleads the editor's image encoder, so edits of a protected photo come out garbled. IMPRESS [2] is an attack on that defence. It finds a nearby image that Stable Diffusion's own autoencoder (VAE) reconstructs consistently, which removes the shield. IMPRESS was our baseline paper. PhotoGuard was the obstacle.

Our team was registered on the Dark (attack) side of Theme 2. Across M1–M3 the group pipeline was *protect → wash → edit → score*, on ten fixed faces from the Helen dataset, with one editor, one prompt and one mask. Two scores were used throughout:

- **Photo damage** = LPIPS [7] between the washed photo and the clean photo. Lower is better. It has zero run-to-run noise.
- **Recovery** `R_pipe = (SSIM_washed − SSIM_protected) / (1 − SSIM_protected)`. Each SSIM [8] compares an edit with the edit of the clean photo. Higher is better. Its measured run-to-run noise is about ±3 percentage points (pp).

My individual M3 strategy was aimed at Light team #14 (Cyber Ninjas), whose project erases the Van Gogh style from Stable Diffusion with ESD-x [3].

**Contributions of this report.** (1) A condensed Week 2–12 strategy log (§III). (2) An unconstrained-enhancement demo that swaps IMPRESS's optimisation loop for masked diffusion purification (§IV-A). (3) A role-reversal outline with a washed-photo detector as its demo (§IV-B). (4) A reflection on how my background shaped these choices (§IV-C). Both demos have a pass/fail rule that was written before the run, and both failed it. I report them as measured results.

---

## II. System Recap (M1–M3)

**What is ours and what is IMPRESS's.** IMPRESS's algorithm (`impress.py`, about 25 lines) is theirs, and we left it unmodified. Our work: the eleven repairs needed to run the 2023 code in 2026, the scoring harness, and one method change. In M2 I added a **mask**: wash only the region the editor *keeps*, and put the protected pixels back in the region it repaints. This came from a measurement. During an edit, the kept region moves 4–7 grey levels and the repainted region moves 86–96. The editor also blanks the repainted region before it reads the photo, so washing that region is wasted.

**Table I — The canonical M3 result** (n = 10 faces, shield at L2, eps 16, step 1, 40 × 2 iterations; one shared protect stage).
<!-- % SOURCE: HANDOVER 8 Oct box; M3/M3_training/REPORT_part1, REPORT_part2 -->

| Version | Wash iterations | Photo damage (LPIPS) ↓ | Recovery (pp) ↑ |
|---|---:|---:|---:|
| N · no wash | 0 | 0.034 | 0.0 |
| A · IMPRESS | 100 | 0.185 | +0.2 |
| B · IMPRESS | 1000 | 0.143 | +4.9* |
| **C · A + our mask** | 100 | **0.060** | +0.9 |

\*B's gain clears the ±3 pp band, but two of ten faces carry it (+29, +25 pp; median +3.0). It is suggestive, not established.

C does **68% less photo damage than A at the same compute**, and 58% less than B at a tenth of B's compute. Its recovery is inside the noise of A's, but 3.9 pp below B. So the honest claim is a trade-off: **B gives the most recovery, and C gives the least photo damage.** The shield was weak in every run. It was noticed on 0 of 10 faces in this run, because at 40 × 2 iterations it ran at 1/25 of PhotoGuard's reference effort (200 × 10).

**ESD-x attack (individual, M3).** I tested whether Cyber Ninjas' erasure could be bypassed through routes it was not trained on: the name in five other scripts, painting titles, and a description without the name. I scored each route on the erased model and on the unmodified SD v1-4, against one fixed reference. **No route brought Van Gogh back.** The non-Latin names were NO SIGNAL, because the unmodified model never draws Van Gogh from them. The description and title-plus-description routes were erased (−4% and 27% kept). A Gauguin control kept 105%, so the erasure is specific. One limit of the score: by eye, on one seed, the erased model still paints a swirling starry sky. <!-- % SOURCE: M3/esd_attrack/RESULT-1008-T2.md -->

---

## III. Weekly Strategy Log (Weeks 2–12)

*Each entry gives the strategy, the edge it was meant to buy, and what changed. The full diary is kept separately.* <!-- % SOURCE: Admin/Echo-M4-Strategy-Log.md -->

**Week 2 (3–9 Aug) · Own the plan.** I registered Dark early to secure the Theme 2 slot, set up the shared Drive, and read PhotoGuard end to end before writing any code. *Edge:* the strategy-lead role, where 26 of 50 marks are individual. *Adapted:* compute was not the bottleneck; coordination was.

**Week 3 (10–16 Aug) · Choose the baseline by running it.** I ran both candidates (IMPRESS and QF) on a T4 instead of comparing abstracts. I also asked the lecturer for the requirements in writing. *Edge:* certainty that our comparison numbers would exist. *Adapted:* QF attacks the prompt, not the protected image, so I moved it to Related Work. I built a quantitative recovery score, because IMPRESS judges edits by eye.

**Week 4 (17–23 Aug) · Make provenance a defence.** I read `impress.py` line by line and wrote one sentence on what is theirs and what is ours. I designed the M1 challenge with two scoring axes. *Edge:* a single-axis challenge has a lazy winner (perturb until the photo is noise), so scoring robustness *and* cost closes that move.

**Week 5 (24–30 Aug) · Publish the negative.** M1 scored +5.2% on one image and −1.2% on the other, and I published both. *Edge:* an early honest negative makes later claims believable. *Adapted:* my wash cost LPIPS 0.15, nine times the shield it removed. That broke my own published budget and led directly to the mask.

**Week 6 (31 Aug–6 Sep) · Small enough to defend.** I turned the cost problem into a four-line method, the mask, backed by a measurement. I added a null arm (no wash) as the floor. *Adapted:* the smoke run showed my mask polarity was backwards. I now verify by measurement, never by intuition.

**Week 7 (7–13 Sep) · Attack my own instrument.** I added a seed floor, a random-noise null, and a re-run at double strength. *Edge:* the editor's seed-to-seed variation disturbs the edit more than the shield does. That is a finding about the baseline's test, and it is worth more than another point of recovery. *Adapted:* `pg_eps` is inert at step 1, and my published SSIM gate (0.85) passed everything. I published the correction.

**Week 8 (14–20 Sep) · Budget by rubric weight.** I submitted M2 three days early and read the M3 rubric line by line. Only 5 of 25 marks reward "the attack got better", while 11 reward the individual strategy. I pre-decided a cut ("if the challenge pack is not public by Monday, ESD-x moves to M3"), and it fired. *Adapted:* my own gate, run on my own M2 images, showed the shield never engaged. Nissa had contributed nothing since M1, so I emailed the tutor and planned the rest of the unit as solo work.

**Mid-semester break (21–27 Sep) · One question per session.** I moved the canonical runs to Colab, the platform the brief accepts. I split the work so each notebook answers one question and survives a disconnect. *Adapted:* our shield ran at 1/25 of the reference effort, and I stated that as a limitation before anyone else could.

**Week 9 (28 Sep–4 Oct) · A falsifiable prediction, then the test.** I posted my cross-script prediction on Cyber Ninjas' thread *before* running it, then ran the test. The prediction was refuted, and I conceded publicly, crediting their argument. On 4 Oct I reframed the IMPRESS half around *training the attack* (loss curve and checkpoints) rather than more shield sweeps. *Edge:* a demo a marker can see.

**Week 10 (5–11 Oct) · Make the failure informative.** The tutor confirmed that a failed attack earns marks if the failure is explained. So my second ESD-x test was designed to explain: a fixed reference, fresh seeds, and a Gauguin control. *Adapted:* re-reading test 1 showed its "99% survives" was an artefact of the reference; the true figure is 0–14%.

**Week 11 (12–18 Oct) · Feedback is a map.** My M2 mark (6.3/8) lost points for explaining *what* but not *why*. I added mechanisms read from the source code, with no new GPU runs. I also stated plainly that no team had attacked us, instead of implying a back-and-forth that did not happen.

**Week 12 (19–25 Oct) · Scripts as a coordination protocol.** We rehearsed on Zoom, exchanged written scripts, and Nissa ran the slides from cues in my script. After M3, I built both M4 demos. The quick test caught a data-leakage bug before the full run.

---

## IV. Adversarial Gameplay

### A. Unconstrained System Enhancement: Masked Diffusion Purification

**Idea.** IMPRESS removes the shield by *optimisation*: 100 gradient steps per photo, each passing through the VAE. A diffusion model already knows how to remove Gaussian noise. So the shield can be removed by *denoising* instead:

1. encode the protected photo and add a small amount of noise (strength 0.1 = the first 10% of a 50-step schedule);
2. let Stable Diffusion denoise it for the matching 5 steps, with an empty prompt;
3. keep the result only inside our M2 mask, as in C.

The added noise drowns the shield, and the denoiser has no reason to put it back. This is DiffPure [4] applied to photos, and the same mechanism as AudioPure [5] from the Week 8 workshop. It is also the Week 3 *denoised smoothing* defence [11] turned around: a denoiser placed in front of the editor, used by the attacker. It needs no gradients and no per-image optimisation.

**Why it would be a significant improvement.** In a real attack, cost per photo decides scale. A wash that takes 1 s instead of 107 s turns a per-photo effort into a batch job.

**Demo.** `M4/Dark_Tyro_M4_demos.ipynb`, Part A. It uses the M3 pipeline unchanged, the same ten faces, and the same shield and editor, then adds version D at strengths 0.1 and 0.2. **Stopping rule, written before the run:** success means D's damage ≤ C's, with recovery within 3 pp of C, at a lower wash time than A. One session, two strengths; if it failed, the table is the result.

**Table II — Part A result** (run 23 Oct, n = 10). <!-- % SOURCE: REPORT_m4.zip/partA_summary.csv -->

| Version | Photo damage ↓ | Recovery (pp) ↑ | Faces > +3 / < −3 pp | Wash s/face ↓ |
|---|---:|---:|---:|---:|
| N · no wash | 0.034 | 0.0 | — | 0 |
| A · IMPRESS 100 | 0.184 | −5.1 | 2 / 5 | 107.1 |
| C · A + mask | **0.059** | −3.2 | 3 / 4 | 107.1 |
| **D · diffusion 0.1 + mask** | 0.070 | −2.0 | 3 / 5 | **1.15** |
| D · diffusion 0.2 + mask | 0.085 | −5.9 | 3 / 6 | 1.60 |

*[Fig. 1: `figures/figA_damage_recovery.png`. Fig. 2: `figures/figA_examples.png`.]*

**Verdict: FAIL on the damage criterion.** D 0.1 does 19% more photo damage than C (0.070 vs 0.059). It passes the other two checks: recovery is 1.2 pp above C (inside noise), and it is 93× faster than A. Doubling the strength made it worse on both axes (damage +44% vs C). Against the **IMPRESS baseline**, D 0.1 does **62% less photo damage** for about 1% of the wash time, with recovery inside the noise.

**Analysis.**
- *Why D does not beat C.* Denoising regenerates the kept region from the model's prior, so it also changes real detail. C changes the image only as much as IMPRESS's loop needs. More strength means more of the photo is regenerated, which is why 0.2 is worse than 0.1.
- *Recovery tells us nothing here.* All recoveries are negative or inside noise, and one face (221629697) scores −37 pp under A. This is the same weak shield as M3, so recovery has almost nothing to measure. Photo damage and wash time are the reliable axes.
- *Unconstrained version.* Without time or compute limits, I would: run the shield at PhotoGuard's full 200 × 10 so that recovery can actually discriminate; sweep strength finely between 0.05 and 0.1; use more faces, prompts and editors; and add a short IMPRESS-style consistency step after denoising, to recover detail where D loses it.

### B. Role Reversal: Defending PhotoGuard

If I switched sides, I would defend PhotoGuard, our own project's defence. (ESD-x was a different team's defence.) Following the Week 5 workshop's layered anti-deepfake design, no single layer has to hold.

**Strategies (outline).**
1. **Purification-aware shield.** Optimise the shield *through* the wash, averaging over random purifier settings (expectation over transformation [13]). Then the shield is built to survive what the attacker will do to it. Cost: the shield has to differentiate through a purifier.
2. **Spend the budget where the editor reads.** Our M2 finding cuts both ways: the editor blanks the region it repaints, so shield pixels there are wasted. A defender who can predict common edit regions (background, clothing) should concentrate the perturbation in the region the editor keeps.
3. **Make the shield strong enough to engage.** Week 7 and the Week 2 FGS/FGV material [10] point to the same thing: at step size 1 the optimiser never reaches its eps budget, so `pg_eps` is inert. A defender should check step size before raising eps.
4. **Detect washed photos** (the demo below). If removing the shield leaves a fingerprint, a platform can refuse to edit, or flag, a photo that looks washed.
5. **Provenance.** A signed or watermarked original (the Week 5 preventive layer) does not stop the attack, but it makes the washed copy provably not the original.

**Demo: a washed-photo detector** (Part B of the same notebook).

*Feature, from how the attack works.* IMPRESS minimises one number: how much a photo changes on a round trip through the VAE. My hypothesis was that a washed photo would be *more* VAE-consistent than any natural photo, because the attacker leaves the fingerprint of its own objective. The feature is the VAE round-trip error averaged over 32 × 32 patches, taking the **10th-percentile patch**, so that a wash applied only inside the mask can still show up.

*No leakage.* The threshold was set on 40 held-out clean faces that never appear in the test: flag a photo if its score is below the 5th percentile (0.027), i.e. a 5% false-alarm rate. **Pre-set success rule:** at least 8 of 10 photos flagged for at least one wash.

**Table III — Part B result** (run 23 Oct). <!-- % SOURCE: REPORT_m4.zip/partB_summary.csv, partB_scores.csv -->

| Group | n | Median score | Flagged (pre-set rule) | AUC* |
|---|---:|---:|---:|---:|
| clean, held-out (calibration) | 40 | 0.39 | 2 | — |
| clean, test | 10 | 0.40 | 0 | — |
| protected (N) | 10 | 0.39 | 0 | 0.48 |
| washed · A (IMPRESS) | 10 | **3.57** | 0 | 0.00 |
| washed · C (A + mask) | 10 | 0.40 | 0 | 0.47 |
| washed · D 0.1 | 10 | 0.40 | 0 | 0.51 |
| washed · D 0.2 | 10 | 0.40 | 0 | 0.51 |

\*AUC in the pre-registered direction (lower score = washed). 0.5 = chance. 0.00 means perfectly separated in the *opposite* direction.

*[Fig. 3: `figures/figB_detector_rebuilt.png`, rebuilt from `partB_scores.csv` by `make_figB.py`.]*

**Verdict: FAIL.** The pre-registered detector flagged 0 washed photos.

**Observation, not a pre-registered result.** IMPRESS-washed photos go the other way. Their scores (3.23–4.16) are about 9× the clean median, and every one is above the highest of all 50 clean photos (1.34). Any threshold between 1.34 and 3.23 separates all 10 washed photos from all 50 clean ones. Because I chose that direction after seeing the data, I state it as an observation that a fresh test would need to confirm, with a threshold fixed in advance on new faces.

**Analysis.**
- *Why A goes up, not down.* The most likely cause, untested, is IMPRESS's own start-up step. It adds random noise to the photo (`pur_noise`) and then trains it away, and our M3 training log shows that term is still near its limit after 100 iterations. The VAE cannot reproduce random noise, so the round-trip error rises across the whole photo, even in its most consistent patches.
- *Why C and D are invisible.* The mask puts the protected pixels back over most of the photo, and the 10th-percentile patch falls in that unwashed region. So **our own M2 method already evades this detector.** For the defender, that is the important finding: the cheapest counter-move to a detector is to wash less of the photo.
- *What a defender would do next.* Score only the region an editor is likely to keep, and combine this feature with strategy 1. A shield that survives the wash forces the attacker into a full-photo wash, and a full-photo wash is exactly what this feature sees.
- *Limitation.* The detector assumes the defender has the attacker's VAE. For SD 1.x the VAE is public, but another editor would need its own detector.

### C. Personal Reflection and Background

I came to this unit from data science, not adversarial machine learning. That background shaped my strategy more than any single technique did. I trusted measurements more than explanations. So I added a null arm, a seed floor and a held-out calibration set, I fixed every pass/fail rule before running, and I recomputed numbers from the saved outputs rather than from my own notes. Three of my most useful moments were corrections of my own published claims: the wrong SSIM gate, the reversed mask, and the "99% survives" artefact. Each one came from a control I had added for exactly that purpose.

The weakness was the other half. Early on I did not have the background to judge whether a method was sound. I used AI tools heavily, and in the first weeks they steered me more than I steered them: I received answers I could not check. What changed this was weekly study of PyTorch, CNNs and the Stable Diffusion architecture. Once I understood the VAE, cross-attention and the noise schedule, I could check the AI's suggestions against the code and my own data, and I began to reject some of them. AI use was permitted for this task. My lesson is that a tool's answers are only as useful as my ability to verify them.

Working mostly alone after M1 taught me to plan every deliverable as shippable by one person, and to set stopping rules before open-ended experiments. In the last week, it also taught me that written scripts work as a coordination protocol with a teammate.

[ECHO: one or two sentences in your own voice, e.g. a specific moment from your data-science background, or what you would tell yourself in Week 2.]

---

## V. Limitations and Conclusion

**Limitations.**
1. The shield ran at 1/25 of PhotoGuard's reference effort throughout. Recovery therefore has little to separate, and photo damage is the reliable axis.
2. n = 10 faces, one prompt, one editor, one inpainting mask. The 5% false-alarm rate comes from 40 faces, so it is itself an estimate with wide error bars.
3. D's wash time excludes the one-time model load. IMPRESS's time includes its own.
4. Part B's direction was chosen after seeing the data. ESD-x's motif survival was checked by eye on one seed only.

**Conclusion.** Across the semester, my most useful attacks were on measurements, not on models. Examples: a test that could not see its own defence, an erasure judged against the wrong reference, and a wash that damaged the photo more than the shield did. Both M4 demos missed their pre-set bars. Still, each produced a clear, measured finding. Diffusion purification removes IMPRESS's cost (62% less damage, 93× faster) but not our mask's advantage. And a full-photo wash leaves a VAE fingerprint that a masked wash does not. In game-theory terms, each move here invites a cheap counter-move, so a defender should invest in the layer that is most costly for the attacker to answer: a shield that survives the wash.

---

## References

[1] H. Salman, A. Khaddaj, G. Leclerc, A. Ilyas, and A. Madry, "Raising the cost of malicious AI-powered image editing," in *Proc. ICML*, 2023.
[2] B. Cao, C. Li, T. Wang, J. Jia, B. Li, and J. Chen, "IMPRESS: Evaluating the resilience of imperceptible perturbations against unauthorized data usage in diffusion-based generative AI," in *Proc. NeurIPS*, 2023.
[3] R. Gandikota, J. Materzyńska, J. Fiotto-Kaufman, and D. Bau, "Erasing concepts from diffusion models," in *Proc. ICCV*, 2023.
[4] W. Nie, B. Guo, Y. Huang, C. Xiao, A. Vahdat, and A. Anandkumar, "Diffusion models for adversarial purification," in *Proc. ICML*, 2022.
[5] S. Wu, J. Wang, W. Ping, W. Nie, and C. Xiao, "Defending against adversarial audio via diffusion model," in *Proc. ICLR*, 2023.
[6] R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer, "High-resolution image synthesis with latent diffusion models," in *Proc. CVPR*, 2022.
[7] R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang, "The unreasonable effectiveness of deep features as a perceptual metric," in *Proc. CVPR*, 2018.
[8] Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, "Image quality assessment: From error visibility to structural similarity," *IEEE Trans. Image Process.*, vol. 13, no. 4, pp. 600–612, 2004.
[9] A. Radford *et al.*, "Learning transferable visual models from natural language supervision," in *Proc. ICML*, 2021.
[10] I. J. Goodfellow, J. Shlens, and C. Szegedy, "Explaining and harnessing adversarial examples," in *Proc. ICLR*, 2015.
[11] H. Salman, M. Sun, G. Yang, A. Kapoor, and J. Z. Kolter, "Denoised smoothing: A provable defense for pretrained classifiers," in *Proc. NeurIPS*, 2020.
[12] V. Le, J. Brandt, Z. Lin, L. Bourdev, and T. S. Huang, "Interactive facial feature localization," in *Proc. ECCV*, 2012.
[13] A. Athalye, L. Engstrom, A. Ilyas, and K. Kwok, "Synthesizing robust adversarial examples," in *Proc. ICML*, 2018.
[14] FIT5230 Malicious AI workshop slides, Weeks 2, 3, 5, 8 and 10, Monash University, 2026.

<!-- TODO before LaTeX: [9] CLIP is cited only if the ESD-x scoring sentence names CLIP — add "CLIP ViT-L/14 [9]" in §II or drop [9].
     [12] Helen — cite in §I where "Helen dataset" appears. Check each reference against the paper's own BibTeX. -->
