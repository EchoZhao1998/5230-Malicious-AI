# FIT5230 Malicious AI — Team Plan

**Team:** Echo Zhao + Nissa Colidea
**Team name:** Tyro
**Theme:** 2 — Text-to-Image
**Side:** Dark (attack)
**Compute:** Free Colab (T4)
**Hard constraint:** the pipeline must be 100% visual — no audio at any stage.
**Google Drive:** https://drive.google.com/drive/folders/1bqjIVx3N73YOzQnK_Al2MUGx9Pzo0X9d?usp=sharing


> ### ✅ Feasibility confirmed — 6 Aug 2026
> Smoke test passed 3/3 on free Colab. Free T4 obtained; InstructPix2Pix loaded in **55s** using 2.2 GB of 15 GB; one image edit took **6.1s**; PSNR measurement verified. Whole test: 5.3 minutes.
>
> **Implication:** a 50-image, two-condition experiment costs ~10 minutes of GPU against a 15–30 GPU-hour weekly budget. **Compute is not our constraint. Calendar time is.**
>
> Working versions to pin: `torch 2.11.0+cu128`, `diffusers 0.39.0`, `transformers 5.13.1`.

---

## 1. The project in one paragraph

Artists and photographers now use tools that add **invisible noise** to an image so that AI editors (Stable Diffusion, InstructPix2Pix) choke when someone tries to edit it. Think of it as an **invisible tripwire baked into the pixels**. The best-known one is **PhotoGuard** (MIT, ICML 2023). Our job as the Dark team is to prove the tripwire is flimsy: we build a **purification pipeline** that quietly wipes the protection off an image, then edits it as if the protection was never there.

The punchline that makes this a good project: **saving the image as a JPEG is already a partial attack.** We escalate from there.

---

## 2. Why this project and not something else

| Requirement | How this project satisfies it |
|---|---|
| Free Colab T4 only | InstructPix2Pix is SD-1.5 sized. Zero model training required — inference only. |
| No audio | Images in, images out. |
| Beginner-safe | The attack is image processing (compress, blur, resize), not novel ML research. |
| Convincing demo | Every result is a before/after image grid. Instantly readable on a slide. |
| Non-trivial | The naive version works in a day; the strong version is genuinely open research. |
| Nothing unethical to generate | Test edits are benign ("make it winter", "turn the car red"). No NSFW, no real people needed. |
| Live research area | There is a March 2026 paper on exactly this. We are not doing something stale. |

---

## 3. The technical pipeline

```
  clean image
      │
      ├──► [DEFENSE] PhotoGuard-style immunization
      │      PGD attack on the VAE encoder → imperceptible noise
      │                    │
      │                    ▼
      │            protected image
      │                    │
      │        ┌───────────┴───────────┐
      │        │                       │
      │        ▼                       ▼
      │   InstructPix2Pix       [OUR ATTACK] purify
      │   "make it winter"       JPEG / blur / upscale / DiffPure
      │        │                       │
      │        ▼                       ▼
      │   ✅ garbled output      purified image
      │   (defense works)               │
      │                                 ▼
      │                         InstructPix2Pix
      │                          "make it winter"
      │                                 │
      │                                 ▼
      └──────────────────────► ❌ clean edit (we win)
```

**Three numbers we measure every time:**

1. **Edit success** — CLIP similarity between the output image and the edit instruction. Higher = our attack worked.
2. **Image fidelity** — LPIPS / PSNR against the original. Proves we didn't just destroy the image to beat the defense.
3. **Perceptibility** — is the purified image still visually clean to a human?

The whole point is the **trade-off curve** between 2 and 1. A purification that works but leaves a smeary mess is not a real attack. That nuance is where the technical-depth marks live.

---

## 4. The escalation ladder

Do not try to build the final thing now. Each milestone is one rung.

| Rung | Milestone | What we build | Effort |
|---|---|---|---|
| **0** | M1 (28 Aug) | Get InstructPix2Pix running. Immunize one image. Show the edit fails. Show JPEG-75 partly un-fails it. | 1 weekend |
| **1** | M2 (18 Sep) | Systematic sweep: JPEG quality, Gaussian blur, bit-depth reduction, **upscale→downscale**. Plot the trade-off curve over ~50 images. Release it as runnable base code. | 2 weeks |
| **2** | M3 (22 Oct) | **DiffPure**: add noise at timestep *t*, denoise with SD. Kills the adversarial signal, keeps the semantics. Plus **model-mismatch transfer** — attack an editor the defender never anticipated. | 4 weeks |

If rung 2 stalls, rung 1 with a good analysis still scores well. Build the safety net first.

---

## 5. Individual strategies (this is where the marks are)

M3 gives **11% assessed on you personally** and M4 gives 15% individually. You each need **one distinct move you own end-to-end**. Do not blend the work.

**Echo — "Keen observation" → the frequency attack.**
Adversarial perturbations live in high spatial frequencies. Run an FFT on protected vs. clean images, show visually *where* the protection hides, then build a **targeted low-pass filter** that removes exactly that band and nothing else. This beats blunt JPEG on the fidelity metric because it's surgical rather than destructive. It's an analysis-led strategy — perfect for the "critical analysis" rubric line, and it doesn't require heavy engineering.

**Teammate — "Blindsiding" → the model-mismatch attack.**
Light teams will tune their defense against whatever editor we publish in M2. Their protection is generated against a *specific* VAE. Quietly build the attack against a **different** editor/VAE and reveal it at M3. The 2026 literature shows protections collapse under model mismatch — so this is a documented, defensible strategy, not a cheap trick. It's the more code-heavy of the two.

> The rubric literally names *"blindsiding, deception, or keen observation"* as valid strategies. Planned deception is **sanctioned and rewarded** here. Publish a deliberately modest version of the attack in M2; keep the strong version in reserve for M3.

---

## 6. Timeline

| When | What | Owner |
|---|---|---|
| **This week (by ~13 Aug)** | Check the team slots spreadsheet. Agree team name. **Email the tutor.** | Echo |
| | Start the weekly strategy log (M4 needs Weeks 2–12) | Both, separately |
| **By 20 Aug** | InstructPix2Pix running in Colab. One successful edit. | Teammate |
| | Read PhotoGuard + Hönig 2024. Draft the M1 post. | Echo |
| **28 Aug** | **M1 due (2%)** — Ed post + Colab link + Moodle PDF | Echo posts |
| Sep W1–W2 | Purification sweep + metrics code | Teammate |
| | Read other teams' M1 posts, leave 2–3 substantive replies | Echo |
| **18 Sep** | **M2 due (8%)** — results, demos, base code, target declared | Both |
| Sep–Oct | Attack a Light team's published defense. Log everything: what worked, what they did about it. | Both |
| Oct W1–W2 | DiffPure + individual strategies | Split |
| Oct W3 | Slides + rehearse to 15:00 with a timer | Echo leads |
| **22 Oct** | **M3 due (25%)** — presentation + final Colab | Both present |
| Late Oct | Write M4 in Overleaf (IEEE Transactions template) | Each alone |
| **2 Nov** | **M4 due (15%)** — individual report | Each alone |

**Immediate blocking deadline:** the tutor email, by end of Week 4. Themes cap at 10 Light + 10 Dark. Miss it and you get randomly assigned — quite possibly to the audio theme, which does not work for us.

---

## 7. Division of labour

**Echo (lead — research & strategy):** paper reading, problem framing, all Ed forum posts, engagement with other teams, presentation narrative, experimental design, deciding what to measure.

**Teammate (implementation):** the Colab notebook, making it reproducible, running experiments, metrics/plots, dependency wrangling.

**Both, separately:** your own weekly log, your own M3 strategy, your own M4 report. These cannot be shared — they're individually marked.

Rule of thumb: **Echo decides what to test and why. Teammate makes it run.** If you find yourself both editing the same notebook cell, something has gone wrong.

---

## 8. How to use Claude (me)

- **Paper decoder.** Paste a paper or a link — I'll explain it in plain language and tell you which two or three equations actually matter. Ask me anything, however basic.
- **Code drafter.** I'll write the Colab cells; your teammate debugs and runs them on the GPU. Faster than writing from scratch.
- **Red team.** Before you publish anything, I'll play the Light team and try to break your attack — so you find the hole before they do.
- **Writer.** Forum posts, slide outlines, and the IEEE LaTeX report.
- **Log nag.** I can set up a weekly reminder that asks you what you did, so the M4 log writes itself instead of being reconstructed in November.

What I can't do: run a GPU, post to Ed, or attend your tutorial.

---

## 9. Reference material

**Baseline paper (what we attack):**
Salman et al., *Raising the Cost of Malicious AI-Powered Image Editing* (PhotoGuard), ICML 2023 — [arXiv:2302.06588](https://arxiv.org/abs/2302.06588) · [github.com/MadryLab/photoguard](https://github.com/MadryLab/photoguard)

**Victim editor:**
Brooks et al., *InstructPix2Pix*, CVPR 2023 — [arXiv:2211.09800](https://arxiv.org/abs/2211.09800) · HF model `timbrooks/instruct-pix2pix`

**Our attack's evidence base:**
- Hönig, Rando, Carlini, Tramèr, *Adversarial Perturbations Cannot Reliably Protect Artists From Generative AI*, ICLR 2025 — [arXiv:2406.12027](https://arxiv.org/abs/2406.12027)
- *Purify Once, Edit Freely: Breaking Image Protections under Model Mismatch*, 2026 — [arXiv:2603.13028](https://arxiv.org/abs/2603.13028)
- Nie et al., *DiffPure: Diffusion Models for Adversarial Purification*, ICML 2022 — [arXiv:2205.07460](https://arxiv.org/abs/2205.07460)

**What the Light teams will read (know your enemy):**
- *DiffusionGuard: A Robust Defense Against Malicious Diffusion-based Image Editing* — [arXiv:2410.05694](https://arxiv.org/abs/2410.05694)
- *GuardDoor: Safeguarding Against Malicious Diffusion Editing via Protective Backdoors* — [arXiv:2503.03944](https://arxiv.org/abs/2503.03944)

---

## 10. The M1 challenge to throw down

> **Dark.[TeamName] — The Laundering Service**
>
> You believe your images are protected. We think protection is a rumour.
>
> Post any image you've immunized with any tool you like — PhotoGuard, Glaze, Mist, your own method. We will return it edited, to your instruction, with a fidelity score proving we didn't just blur it into mush.
>
> **You win** if we cannot produce a clean edit while keeping LPIPS below 0.15 against your original.
> **We win** otherwise.
>
> Our notebook, metrics, and purification code are open. Come and check our work.

Concrete, falsifiable, has a scoring rule, and forces Light teams to actually engage with us — which is exactly what the "challenge design quality" and "engagement" marks reward.

---

## 11. Two easy ways to lose marks (don't)

**Colab hygiene — worth 5% at M3.** The rubric demands *pre-rendered execution outputs*: every relevant cell must show its logs, metrics and images **saved in the notebook**, not a clean notebook that "would run if you ran it". Also: no hardcoded local paths, pin your package versions, and write markdown cells that narrate problem → method → result → future work. Treat the notebook as a report that happens to contain code.

**M4 has a part nobody plans for — worth 9%.** Beyond the weekly log, M4 asks for two things that each need a *working demo*:

- **"What would you build with no time or resource constraints?"** (4%) — for us the obvious answer is an **adaptive, purification-aware attack**: instead of purifying after the fact, optimise the attack through Expectation over Transformation so it survives whatever defense the artist applies. Demo = a small code snippet showing the EOT loop, even if you only run it for a few steps.
- **"Switch sides — how would you defend?"** (5%) — as ex-attackers we know exactly why protections fail, so the answer is a defense that doesn't rely on fragile high-frequency noise. Sketch something semantic or backdoor-based (see GuardDoor) and demo the core idea.

Sketch both by early October while the project is fresh. Reconstructing them in the last week is how people lose 9%.

---

## 12. Risks

| Risk | Mitigation |
|---|---|
| Dark slots for Theme 2 already full | Email this week. Fallback: Theme 1 Dark with AdvSticker (visual, no audio). |
| Colab times out mid-experiment | Checkpoint to Google Drive. Keep test sets small (20–50 images). |
| Nobody engages with our challenge | Go to them: attack a Light team's published Colab unprompted and post the result. Engagement marks flow either way. |
| Attack works too easily, looks trivial | That *is* the finding — but strengthen it by adding fidelity constraints and adaptive defenders, so it's a curve, not a yes/no. |
| Uneven contribution | Individual components are graded separately anyway. Keep your own log from Week 2. |
