# FIT5230 Project — Handover / Context Doc

> ## ⭐ CURRENT STATE — 6 Sep 2026. Read this box, then skip to what you need.
>
> **The project is about IMPRESS. Nothing else is live.** QF, the theme-fit argument and the
> three-tier "Gauntlet" below are **closed or parked** — kept as history, not as work.
>
> | | |
> |---|---|
> | **M1** | ✅ submitted 28 Aug. `M1/submittion/` — the Ed post PDF and the notebook, exactly as sent. Per Jessie: M1 only needed a notebook that visibly differs from the reference, which the **eleven repairs** table bought. No results row in the rubric. |
> | **M1 result** | `R_pipe` **+5.2%** at `(40,2)`, **−1.2%** at `(200,2)`, at LPIPS **0.15** — nine times what the shield cost to apply. The wash is weak *and* expensive. |
> | **M2** | 🔨 in progress, due **18 Sep**. `M2/Dark_Tyro_M2.ipynb` = the M1 notebook **+16 lines**. Plan in `M2/M2-PLAN.md`. |
> | **M2 method** | **Wash only the region that survives the edit.** `purified_v2 = mask·purified_impress + (1−mask)·protected`, where **white mask = preserved by the editor** (checked: 4–7 levels changed inside vs 86–96 outside). Four arms, including **N = no wash**, the origin any real attack must beat. |
>
> **The measurement behind it** (from M1's own archive, no new GPU time): PhotoGuard puts
> **3–6× more perturbation inside the inpainting mask** than outside (1.33–2.64 vs 0.47 levels),
> because that is the only region the editor regenerates. **IMPRESS pays uniformly** — 5.00
> levels of damage outside the mask, buying nothing. Restricting the output to the mask cuts
> fidelity damage **61–63%** and lifts SSIM vs clean from **0.75 → 0.93**.
>
> **Smoke run 5 Sep — plumbing passed, and half the claim is already banked.** Masking fires
> exactly where specified (~0.2 levels changed inside the mask, ~4.8 outside). **LPIPS 0.160 ->
> 0.037, SSIM vs clean 0.749 -> 0.937.** That half does not depend on the iteration count. It
> puts our own purifier **inside the LPIPS <= 0.10 budget we publish for challengers** — at M1
> it cost 0.15 and broke our own rule. `R_pipe` is still open and needs the real run.
>
> **Noise floor MEASURED 5 Sep** (two runs, identical settings): **`R_pipe` ±2-4 pp; fidelity
> exactly reproducible.** fp16 shifts the protected image 0.1 levels; the editor amplifies it to
> ~11 levels (~100x) — the same sensitivity PhotoGuard exploits. **Trust orderings and signs,
> never magnitudes.** The A→C gap (9-14 pp) is 3-6x the noise, so that ordering is real.
>
> **Repair 12 (6 Sep).** `A3` compared images by upsampling the 512×512 protected image to the
> photograph's native size, then scoring the interpolation. **Always resample toward the smaller
> image.** The notebook now archives `clean512/` — the tensor the pipeline actually conditioned
> on — so this cannot recur.
>
> **Tried and rejected (report it, do not repeat it):** the FFT-targeted low-pass filter. Band
> measured, cutoff swept f = 0.40 → 0.95; **every cutoff removed more real detail than shield**,
> because at `pg_eps = 16` the shield is ~1 grey level — quieter than the photo's own grain.
>
> **The standing rule, learned the hard way twice: complexity is not neutral.** M2 *Engagement*
> is 2% and M3 *Peer Engagement* is 3%. A notebook nobody runs forfeits both. Keep it short.
>
> ⚠️ **Paths below this box are from before the 6 Sep reorganisation.** `README.md` is the
> current map. **The reasoning below is still valid — only the file paths moved.**

## Who / what
- Unit: **FIT5230 Malicious AI** (50% of unit). Team **"Dark.Tyro"** = Echo Zhao (lead) + Nissa Colidea.
- Theme 2 (Text-to-Image), **Dark / attack** side. Hardware: **free Colab T4 (single GPU)**. Visual-only pipeline.
- I'm a green Data Science student; explain simply, use metaphors. 26 of 50 marks are **individual** — contributions must be distinguishable.

## The project in one line
We **attack images protected by PhotoGuard** (a defense that adds invisible noise so AI editors garble edits). We *remove* that protection so editing works again — proving the shield is fragile.

## Decision locked: Path A
- **Baseline = IMPRESS** (NeurIPS 2023) — an attack paper *with runnable code + replicable metrics*. Satisfies the lecturer's "baseline must have code + metrics."
- **Target/shield = PhotoGuard** (kept as what we attack).
- **Our contribution = a cohesive purification system** + a **quantitative attack-success metric** the baseline lacks.
- **Individual angles:** Echo = FFT "keen observation" low-pass filter (surgical, wins on fidelity). Nissa = model-mismatch attack (different VAE).

## Theme fit — SETTLED, stop re-litigating (checked 16 Aug)

Recurring worry: *"our theme is Text-to-**Image**, but we work on image **editing** — are we off-theme?"* Answer: no, and here is the evidence, so this doesn't need reopening.

1. **Theme 2's own sample papers are Safe Latent Diffusion and InstructPix2Pix.** InstructPix2Pix is an *image editing* model (image + instruction → edited image), not txt2img sampling. The lecturer has therefore already scoped editing into Theme 2 — and PhotoGuard exists specifically to obstruct InstructPix2Pix and SD inpainting. We attack a pipeline built on a listed sample model.
2. **The theme's risk statement is literally our threat model:** *"posing risks when exploited by malicious actors to generate realistic fake images."* We are the malicious actor; PhotoGuard is the obstacle; purification is how we get through.
3. **Theme 2 Dark, second bullet, word for word:** *"If your selected paper focuses on enhancing the security, robustness, or trustworthiness of TTI models, you should design an attack technique to evaluate and potentially bypass the defence mechanism proposed in the selected paper."*

**The one honest weakness.** On a purely technical reading this also fits Theme 1 (Adversarial ML on Gen AI) — stripping an adversarial perturbation *is* adversarial ML, and in our experiments the prompt is close to a fixed constant, so the "text" half does little work. It doesn't bite (we're registered in Theme 2; no rubric row scores theme purity), but it means **the risk is framing, not substance.** Mitigation applied 16 Aug: the Ed post now leads with the **TTI editing pipeline** as the attack surface and demotes PhotoGuard to "the lock on the door", with an explicit scope note citing InstructPix2Pix as a Theme 2 sample paper.

**The argument that doesn't depend on theme fit at all:** QF makes a *terrible* adversarial game. The defence against a 5-character prompt suffix is input sanitisation — ~10 lines, complete, one round and the game is over. PhotoGuard-vs-purification is a genuine arms race (strengthen perturbation → widen filter → randomise band → go adaptive → EOT → mismatched VAE). This assignment scores four milestones of back-and-forth: M2 *Engagement* 2% + M3 *Peer Engagement* 3%. Pick the fight that lasts.

### Why NOT the other options
- **QF (Query-Free Adversarial Attack, arXiv:2303.16378)** — Nissa's find. Attacks the **CLIP text encoder** (perturbs the *prompt*). Wrong axis for M1–M3: **no protected asset in its threat model**, so it shares no evaluation harness with `pg_metric.py`. **BUT — see "QF's real home" below. It is not dead, it moved.**
- **JPEG-bypass paper (arXiv:2304.02234)** — no official code / no replicable metrics, so not a valid baseline. The JPEG attack itself is one line → our simplest ablation and Tier 1 of the challenge.

## Key links
- IMPRESS paper https://arxiv.org/abs/2310.19248 · code https://github.com/AAAAAAsuka/Impress
- PhotoGuard (defense) https://arxiv.org/abs/2302.06588 · code https://github.com/MadryLab/photoguard
- QF (related work / M4 material) https://arxiv.org/abs/2303.16378

---

# ⭐ THE BIG UNLOCK (16 Aug): PhotoGuard has a *cheap* attack

PhotoGuard ships **two** attacks and we were only using the expensive one.

| | cost/image on free T4 | what it does |
|---|---|---|
| **Diffusion attack** (`pg_mask_diff_helen.py`) | ~77 min *(⚠️ that was `(200,10)`, the grid's most expensive corner. Measured on a T4: `(40,2)` = 12.5 min and `(200,2)` = 38.5 min for 2 images)* | backprops through the whole diffusion process |
| **Encoder attack** (PGD on the VAE encoder) | **~30 s** | drags the latent toward a grey target |

The encoder attack produces a shield of the same frequency character. **Editing is also cheap (~10 s).** So the entire clean → protect → purify → edit → measure loop runs in **~15 min on a blank runtime**.

**Why this mattered:** the bottleneck was never compute, it was *iteration latency*. At 77 min/image you get one experiment per evening. At 30 s you get dozens per hour. The general move: when a pipeline is too slow to iterate on, look for a cheaper variant of the **expensive stage** rather than cutting scope.

**Caveat to state in writing:** encoder attack ≠ diffusion attack. It is cheaper *and weaker*. Standalone numbers are **directional only**; M2/M3 headline figures must come from the real IMPRESS diffusion run.

---

# Current files (project folder + Google Drive) — reorganised 16 Aug

> ⚠️ **This table predates 22 Aug — superseded.** The current file map is in
> "22 Aug session → Decision 1" at the end of this file.
> **`M1/Dark_Tyro_M1_FINAL.ipynb` is the submission.**

| path | what it is |
|---|---|
| `Tyro_Analysis_Toolkit.ipynb` | **the main workhorse.** `MODE` switch — see below. |
| `QF_Attack_Tyro.ipynb` | self-contained QF test bench. M4 material, not M1–M3. |
| `HANDOVER.md` | this file. |
| `Nissa-Handoff-Message.md` | copy-paste update for Nissa. |
| `M1/M1_Ed_Post_DRAFT.md` | rubric-aligned Ed post draft. `[[placeholders]]` to fill. |
| `M1/IMPRESS_PhotoGuard_first_trial.ipynb` | the real IMPRESS pipeline, all 2023 rot patched. Slow, authoritative. |
| `M1/toolkit_test_png/` | source faces for the standalone toolkit run. |
| `Admin/Echo-M4-Strategy-Log.md` | Echo's private weekly strategy diary (3% of M4). |
| `Admin/FIT5230 Assignment & Milestones 2026.pdf` | the brief. |
| `Tyro-Tracker.xlsx` | shared task tracker. |

**Note on `M1/toolkit_test_png/`:** those PNGs are 3–5 MB each. The toolkit resizes to `IMG_SIZE` (512) on load, so size doesn't matter for correctness — but set `SOURCE_DIR` to that folder, or copy them into `/content/source_faces`.

## `Tyro_Analysis_Toolkit.ipynb` — the MODE switch

```python
MODE = "standalone"   # builds everything itself on a blank T4, ~15 min, no IMPRESS
MODE = "impress"      # reads folders the real IMPRESS run already wrote
```

Both modes write **the same folder contract**, so every analysis cell downstream is mode-agnostic. Standalone mode is the **fast development loop**; IMPRESS mode produces the numbers we cite.

Standalone mode builds: PhotoGuard encoder attack → four purifiers (JPEG q65 · Gaussian blur · Butterworth FFT low-pass · **IMPRESS-lite**) → SD 1.5 img2img edits (fixed seed) → all metrics.

**IMPRESS-lite** reimplements the baseline's actual objective in ~15 lines:

    min ‖D(E(x′)) − x′‖² + λ‖x′ − x_prot‖²

i.e. make the image self-consistent under a VAE round-trip (which erases the shield) while staying close to the protected input (which stops the optimiser wandering off). It exists so standalone comparisons are against the baseline's **real idea**, not a straw man. **Do not report it as "IMPRESS's performance"** — it is one fixed λ and fewer steps. Call it "the baseline objective at reduced budget."

## What we measure now (this is the M2 contribution)

IMPRESS reports image-fidelity numbers (VIF/SSIM/PSNR) but judges whether the **edit** succeeded **by eye**. That gap is why we could not compare purifiers. Added:

**Attack success** — CLIPScore(edited image, edit prompt), judged by `openai/clip-vit-base-patch32`, deliberately **not** SD's own ViT-L/14 (don't let the chef grade the dish). Reduced to one number:

    R = (S_purified − S_protected) / (S_clean − S_protected)

`R = 1.0` → editor fully restored. `R = 0` → shield held.

**Guard rail baked into the notebook:** when protection efficacy `P = S_clean − S_protected` sits in the noise, `R` is a ratio of two near-zero numbers and means **nothing**. The cell refuses to print it and tells you to strengthen the shield. This is exactly the Trial #1 situation — don't override it.

**Fidelity** — SSIM/PSNR vs the original photo. Plotted against attack success as a scatter (one y-axis, never twin axes). That chart is the M2/M3 headline figure.

**Frequency signature** — radial power spectrum locates the band PhotoGuard injects into → gives (a) the surgical filter spec and (b) a detector.

---

# M1 challenge design: the three-tier "Tyro Gauntlet"

Dark teams must **mirror** the PDF's Light-worded examples ("can you break our defense" → "can you defend against our attack").

- **Tier 1** — survive `save(quality=65)`. Deliberately trivial, ~5 min to attempt.
- **Tier 2** — survive the full purification cascade.
- **Tier 3** — detection: 30 unlabelled images (10 clean / 10 protected / 10 purified), sort them.

**Why tiered:** M1's challenge mark is only 0.5%, but M2 *Engagement* (2%) and M3 *Peer Engagement* (3%) depend on other teams **actually attempting** it. A clever challenge nobody tries costs 5%, not 0.5%. Tier 1 is engagement insurance.

**⚠️ Run section B4 (the private detection answer key) BEFORE publishing Tier 3.** We promise to post our own accuracy and return ground-truth labels. If a one-number threshold already separates our purified images from clean ones, tighten the filter first — otherwise we hand a Light team a free win. Knowing the answer to our own riddle is *keen observation* in the M3 rubric's sense: **we choose the difficulty rather than discover it.**

---

# QF's real home: M4, not M1–M3

Off-axis as a baseline, but it maps onto two M4 rows worth **9%**:

- **"Unconstrained System Enhancement & Feasibility" (4%)** — the no-limits idea is a **two-flank attack**: strip the image-side shield *and* perturb the text side. PhotoGuard, Glaze and Mist all guard the **pixels**. **Nobody guards the prompt.** `QF_Attack_Tyro.ipynb` is the feasibility demo the rubric asks for.
- **"Adversarial Role-Reversal Strategy & Demo" (5%)** — having run a text-side attack makes the text-side *defence* concrete: normalise prompts before encoding, reject embeddings far from any in-vocabulary neighbourhood, or ensemble two text encoders and refuse when they disagree. First one is ~10 lines.

**General lesson: check the individual rubric before discarding a paper.** M4 rewards breadth that M1–M3 penalise.

---

# Colab setup for the REAL IMPRESS run (single T4) — working recipe

```python
# 1. GPU on: Runtime > Change runtime type > T4 GPU. Verify:
!nvidia-smi

# 2. Clone + install
!git clone https://github.com/AAAAAAsuka/Impress.git
%cd Impress
!pip install -r requirements.txt
!pip install sewar          # missing from requirements, needed by pg_metric.py

# 3. Hugging Face login (SD model download)
from huggingface_hub import notebook_login; notebook_login()

# 4. FIX the 2023 code (runwayml repo was DELETED from HF):
!sed -i 's|runwayml/stable-diffusion-inpainting|stable-diffusion-v1-5/stable-diffusion-inpainting|g' *.py
!sed -i '/revision="fp16",/d' *.py       # mirror has no fp16 branch; torch_dtype handles fp16

# 5. Data (PhotoGuard/Helen faces only — we do NOT need Glaze/wikiart)
!pip install gdown
!gdown 16xISe7M_DlSqM2Zf2lWI4JJXcdsDEPsl   # -> helen_face_dataset.zip
%cd /content
!unzip -q /content/Impress/helen_face_dataset.zip -d /content/
!ls /content/helen_face                    # must show: clean  mask
```

## The six fixes required to make IMPRESS run at all
*(these are our M1 "Initial Customization" evidence — 0.4%. Other teams hit these in week 6.)*
> **Now ten repairs + two extensions** — bugs 7–9 were found 20 Aug, fix 10 on 22 Aug.
> The current list lives in `M1/Dark_Tyro_M1.ipynb` (title cell) and Ed post §4.

1. **Dead model repo** — `runwayml/stable-diffusion-inpainting` removed from HF; repointed to the `stable-diffusion-v1-5` mirror.
2. **No fp16 branch** on the mirror — strip `revision="fp16"`, let `torch_dtype` handle it.
3. **Undeclared dependency** — `sewar` imported by `pg_metric.py`, absent from `requirements.txt`.
4. **Four-GPU assumption** — `scripts/new/pg_mask_diff_test.sh` shards across 4 devices. Run stages directly with `--device="cuda:0" --parallel_index=-1`.
5. **Broken folder contract** — protect writes `adv_<params>/`, purify reads `adapt_adv_<params>/`. Copy across (notebook cell 8a-bridge).
6. **Silent parameter mismatch** — `pg_generate.py` defaults `--diff_steps=50` but protect used `4`. **Pass `--diff_steps=4` to 8c AND 8d.** All folder names are built from the params, so `pg_iters`, `pg_grad_reps`, `diff_steps`, `pur_iters` **must be identical across 8a→8d** or the chain breaks silently.

## IMPRESS output folder map (under `/content/helen_face/`)
- `adv_<params>/` = PhotoGuard-protected inputs (from 8a)
- `adapt_adv_<params>/` = copy of the above (bridge, for 8b)
- `pur_<params>/` = IMPRESS-purified inputs (from 8b)
- `clean_diff/` = **edited clean** · `adv_diff_<params>/` = **edited protected** · `pur_diff_<params>/` = **edited purified** (from 8c) ← the 3-way story panel
- `result/<prompt>/...` + `pg_metric.py` stdout = VIF / SSIM / PSNR
- **Colab is ephemeral — copy outputs to Drive or they're lost on reset.**

**`Tyro_Analysis_Toolkit.ipynb` in `impress` mode reads these folders and must run in the SAME runtime**, or you must copy the folders to Drive and repoint `ROOT`.

---

# Status

## Is IMPRESS manageable? — SETTLED 21 Aug, do not reopen

Recurring worry: *"we cannot run the model smoothly — should we drop IMPRESS?"* **No.**

**The evidence closed it.** On Kaggle, `[done] iter40_grad2_eps16 (4.9 min)` — a complete
clean → protect → purify → edit → measure chain on 2 images in under five minutes. That is
not a struggling pipeline. The 77-minute figure that caused the alarm was for `(200, 10)`
specifically, which TRIAL-LOG §5 shows is the wasteful corner of the grid.

**The friction was setup cost, not operating cost, and it is now paid:**

| what hurt | status |
|---|---|
| 6 bugs of 2023 rot (dead HF repo, fp16 branch, `sewar`, 4-GPU, folder contract, `diff_steps`) | fixed permanently |
| 3 bugs Thread A found (7 · purified folder name, 8 · glob, 9 · hard-coded display) | fixed permanently |
| NumPy 2 `np.float64(...)` breaking `ast.literal_eval` on the metric output | fixed permanently |
| Colab free quota | replaced by Kaggle, 30 GPU-h/week on a P100 |
| chasing `pg_iters=200` | strategy error, now understood — `pg_eps` is the lever |

**None of these recur, and all of them are M1 evidence.** The nine fixes ARE the "Initial
Customization & Setup" row. Other teams meet them in week 6 with no time left.

**Why pivoting would be strictly worse:** no alternative clears the lecturer's bar (JPEG-bypass
has no code; QF is off-axis with no protected asset). The Ed post is written around IMPRESS.
The nine fixes would be thrown away. Eight days to M1.

**The tripwire, so the worry has a home.** If compute ever becomes genuinely unaffordable, the
escape hatch is **a smaller experiment, never a different paper** — fall back to
`Tyro_Analysis_Toolkit.ipynb` in `standalone` mode (PhotoGuard's *encoder* attack, ~30 s/image)
for the fidelity-vs-success chart, and cite the diffusion-attack runs as a limited subset with
the "directional only" caveat. That insurance policy is already built. Use it before
reconsidering the baseline.

---

**20 Aug (Thread A) — THE TRIAL IS INTERPRETABLE NOW. `pg_iters=200 grad_reps=2` ships.**
Full reasoning in `M1/TRIAL-LOG.md`. Headlines:

- **The 3-panel comparison is provably controlled.** `pg_generate.py` re-seeds numpy + torch
  immediately before each of the three generations, same mask, same prompt → every visible
  difference is caused by the input image alone. Say this in the Ed post.
- **Clean → broken → restored is present.** Protected = detached, crazed-skin floating head;
  purified = coherent re-integrated person. That IS the attack story; earlier reading of it
  as "poor performance" was wrong.
- **Three new repo bugs (7, 8, 9)** — the "six fixes" list is now **nine**. Bug 7 is the big
  one: the purified folder name encodes **no `pg_*` params**, so every trial silently
  overwrote the last. Fix it before trusting any purified output.
- **🔑 `pg_iters` saturates; `pg_eps` is the real lever.** Each PGD step moves L2 = 1.0 and
  is projected back into a ball of radius `pg_eps=16` → the budget is spent after ~16 steps.
  `pg_iters=200` bought almost nothing for 5× the compute. Untouched lever: `--pg_eps`.
- **Two metrics disagree, and that's a finding.** `pg_metric` SSIM is measured against the
  **clean edit**, not the original photo (the Ed post §4 says otherwise — fix it). CLIPScore
  may rank the *protected* edit highest because its background is the most airplane-like.
  Own the divergence in writing before a Light team finds it.
- **`--attack_type=linf` is currently a no-op** at `pg_eps=16` on `[-1,1]` images. Stay on `l2`.

**Trial #1 (IMPRESS, diffusion attack) — PASSED, but not interpretable.**
End-to-end pipeline runs and produces images + metrics. All six fixes verified. **However:** light settings (`pg_iters=40`, `grad_reps=2`) on 1 image, so (a) `pg_metric` prints `nan` for std, and (b) the shield is too weak to block editing at all — the protected edit still succeeded, so there is no attack story yet. **Numbers are NOT interpretable at these settings. Do not report them.**

**16 Aug — measurement + standalone bench built.** CLIP restoration-rate metric, FFT band analysis, surgical Butterworth filter, private detection answer key, standalone mode, IMPRESS-lite, QF test bench, M1 Ed post draft.

## Verification notes (methodology worth reusing)
- FFT band-onset detection recovered `f = 0.453` against a synthetic shield injected at `0.45`. SSIM 0.27 → 0.74 after filtering.
- **Residue can go negative.** Over-filtering removes the image's own detail — an unnaturally *smooth* image is as detectable as a noisy one. So the surgical filter has a **floor as well as a ceiling**: tune toward *matching clean*, not toward maximum stripping.
- Attack/purifier logic was tested against a tiny stand-in autoencoder. **A randomly-initialised mock gives false failures** — its self-consistency fixed point is flat grey, which coincides with the attack target, so the two objectives collapse into one. Train the mock to reconstruct first, then the test is valid. *General lesson: a control that accidentally agrees with your hypothesis returns a confident wrong answer.*
- Confirmed independently that protected images have higher VAE round-trip inconsistency (0.0204) than clean ones (0.0071) — **this is the premise IMPRESS rests on**, and it is also the detection signal in Tier 3.

---

# Next steps

**Before M1 (28 Aug):**
1. Run `Tyro_Analysis_Toolkit.ipynb` in standalone mode on ~5 faces → get the story panel + the fidelity-vs-success chart.
2. Run section **B4** privately, tune `f_c` so our purified images are **< 1.5 σ** from clean.
3. Fill the `[[placeholders]]` in `M1_Ed_Post_DRAFT.md`, insert the 3-panel figure, **set the Colab link to "anyone with the link can view"** (most common way to lose these marks).
4. Post to Ed **and** submit the link via a PDF/txt to the Moodle M1 page — the Ed post alone is not the submission.

**For M2 (18 Sep):**
5. Raise the real IMPRESS run toward `pg_iters=200 pg_grad_reps=10` on **≥5 faces** so the shield actually blocks editing (~77 min/image → budget overnight runs, or Colab Pro / uni GPU).
6. Re-derive `onset_f` at full protection strength — **the band will move.**
7. Populate the fidelity-vs-success chart with every purifier: JPEG, blur, upscale, FFT low-pass, IMPRESS, IMPRESS-lite.

**Open improvements identified (ranked by marks-per-hour):**
- Add **LPIPS** alongside SSIM — SSIM is a weak perceptual proxy.
- **Cascade purifier**: cheap filters first, expensive purification only on images that resist. Matches the rubric's word *"practical."*
- **Blind operation**: IMPRESS assumes you know the image is protected. Add a detector front-end (VAE round-trip inconsistency) and purify only when it fires — shares all its code with Tier 3.
- **Protection-strength sweep**: find where purification starts to fail. Negative results are fine.

## Deadlines
- M1 **28 Aug** (2%) · M2 **18 Sep** (8%) · M3 **22 Oct** (25%, presentation, 11% individual) · M4 **2 Nov** (15%, individual IEEE report, Overleaf IEEE Transactions template).

## Working style
- Nissa may be a passive teammate → keep the plan **solo-resilient** (critical path runs through Echo: metric, frequency analysis, challenge design, Ed post).
- Files: `/Users/ez_us/Documents/5230/5230-Assignment` + shared Google Drive.

---

# Working structure (from 20 Aug) — four threads

See **`THREADS.md`** for paste-ready kickoff blocks.

| thread | holds | status |
|---|---|---|
| **A · Read the results** | the 3 trials, parameters, metric-vs-perception | ✅ done → `M1/TRIAL-LOG.md`, `GLOSSARY.md` |
| **B · Ship M1** | notebook cleanup + Ed post | ⬜ next · **28 Aug** |
| **C · IMPRESS internals & M2 roadmap** | mechanics, where the headroom is | ⬜ · 18 Sep · *natural piece for Nissa* |
| **D · IMPRESS × QF fusion** | two threat models, one system, joint metric | ⬜ · 2 Nov (M4) |

## Immediate queue (Thread B)

1. Fix **bug 7** (stamp `pg_*` into the purified folder name) — everything else is
   untrustworthy until this is done.
2. Re-run trial 3's chain **end-to-end in one session** (8a → bridge → 8b → 8c → 8d) on
   **≥2 images** so `pg_metric` prints a real `std` instead of `nan`.
3. Optional but high-value: one run at `--pg_eps=24 --pg_iters=40 --pg_grad_reps=10`.
   Cheaper than trial 3 and should be *stronger*. If it is, that comparison is the most
   interesting sentence in the Ed post.
4. Rebuild the notebook around a single `PARAMS` dict; kill every hard-coded glob.
5. Fix the Ed post: SSIM wording (§4), nine fixes not six, replace the stale
   "shield too weak" caveat, add the controlled-comparison sentence, insert the figure.

## Reference files added 20 Aug

| path | what it is |
|---|---|
| `M1/TRIAL-LOG.md` | the verdict, the three new bugs, the parameter analysis, the re-run plan |
| `GLOSSARY.md` | SSIM/VIF/PSNR/LPIPS/CLIPScore/`R`, every `pg_*` and `pur_*` flag, folder-name decoder |
| `THREADS.md` | thread map + kickoff blocks for B, C, D |



# 22 Aug session (Week 5, Sat) — Thread B · **M1 IS BUILT AND RUNS**

Read `M1/RESULT-INTERPRETATION.md` first — it is the tutorial on what our numbers mean, and
it is written so Nissa can read it cold. `M1/M1-CHECKLIST.md` is what is left to submit.

## ✅ Status: the submission artifact exists and executed end to end

`M1/Dark_Tyro_M1_FINAL.ipynb`, run on a **Kaggle T4**, 22 Aug:

| config | wall clock | archived |
|---|---|---|
| `iter40_grad2_eps16` | 12.5 min | 23 MB zip |
| `iter200_grad2_eps16` | 38.5 min | 23 MB zip |

Both configurations completed, both archived and zipped, the 3-panel figure rendered, and
cell 12 confirmed the output. **This is a working submission.**

## The result

```
config  units  metric      adv       pur    recovery
 40:2      80    psnr   14.5712   17.1335    +2.5623
 40:2      80    ssim    0.5921    0.6131    +0.0210
 40:2      80    vifp    0.2209    0.2268    +0.0059
200:2     400    psnr   13.7992   14.0264    +0.2272
200:2     400    ssim    0.5198    0.5143    -0.0055
200:2     400    vifp    0.1545    0.1666    +0.0120
```

`R_pipe = (pur − adv)/(1 − adv)`: **40:2 = +5.2 %**, **200:2 = −1.2 %**.

**Sign test** — 40:2 all three metrics agree (real movement); 200:2 they disagree (inside the
noise). That is the whole statistical claim and it is defensible at n = 2.

**Replicated.** An earlier run on different hardware gave +10.8% and +2.7% — different
magnitudes, identical structure. The 2× spread in magnitude IS the noise level at n = 2, and
it is why we never rank the two configurations against each other.

## 🔑 The most valuable thing we found: the metric and the figure disagree

The **figure** shows the story in `200:2` — protected is a detached, crazed face floating over
an aerial view; purified is a coherent boy back in a seat. Clean → broken → restored.
The **numbers** say `200:2` recovered nothing.

Both are right. `pg_metric`'s SSIM asks *"is the purified edit pixel-aligned with the clean
edit?"* The purified image is a **different plausible edit**, not a pixel-copy, and SSIM
scores that as a miss. **This is precisely why we built the CLIPScore edit-success metric**
(Ed post §4 item 11) — and our own figure is now the evidence that it needed building.

**Lead with this in M3.** "Our metric and our eyes disagreed, we worked out why, and it
justified the second metric we added" beats any clean number.

## What is parked, and where

`M2_diagnostics.ipynb` (project root) holds A0.5 / A0.6 / A0.7 and a table of which readings
were **voided** by a resolution mismatch — `clean/` holds full-resolution Helen originals
(2736×3582, 4000×3000) while `protected/`+`purified/` are 512×512, so any clean-vs-other
comparison measured interpolation. **That fault was in the analysis scripts, never in the
pipeline;** `pg_metric` compares the pipeline's own 512×512 outputs and is unaffected.

**The one measurement that survived:** a bare VAE round-trip changes an image by **4.28**
levels; everything purification did amounts to **4.75**. Purification's whole effect is about
the size of passing the image through the autoencoder. **That is the M2 thread.**
**M2 fix to make this measurable:** archive a 512×512 copy of the clean image — the tensor the
pipeline actually conditioned on — and compare against that.

## Repairs: now ELEVEN

Repair 11 (22 Aug): **the Kaggle P100 no longer works.** It is compute capability 6.0
(`sm_60`); current PyTorch wheels ship `sm_70`+ only. Everything loads, then the first CUDA op
dies with *"no kernel image is available for execution on the device"*. **Use GPU T4 x2.**
Cell 1 now compares `torch.cuda.get_device_capability()` against `torch.cuda.get_arch_list()`
and stops before the long wait; cell 9 asserts on it. Full list in
`fit5230-colab-kaggle-traps` (project memory) and the notebook's title cell.

## Decision 1 — the notebook split

| file | what it is |
|---|---|
| **`M1/Dark_Tyro_M1_FINAL.ipynb`** | **the submission.** 21 cells: setup, eleven repairs, sweep, `R_pipe`, figure, save check. Frozen. |
| `M2_diagnostics.ipynb` | A0.5/A0.6/A0.7, parked, with the voided readings marked |
| `Tyro_Analysis_Toolkit.ipynb` | **keep** — standalone mode, IMPRESS-lite, purifier cascade, and **B4** (never publish B4) |
| `M1/Tyro_Sweep.ipynb`, `patch_cell*.py` | superseded, pre-merge record only |
| `M1/A05_standalone.ipynb`, `A06_regional.ipynb`, `A07_vae_control.ipynb` | one-cell diagnostics, no GPU needed for A0.5/A0.6 |

**Why the M1 notebook is small:** M1's rubric has **no row for results**. Baseline
justification 0.5 · problem statement 0.5 · challenge design 0.5 · setup 0.4 · clarity 0.1.
The setup row is bought by the repairs and a pipeline that demonstrably runs. Everything
answering *why the attack underperforms* is M2 technical depth and was moved out.

## Decision 2 — Tier 3 reframed: disclose detectability, do not hide it

v1 promised "our accuracy as the bar to beat" — announced before we knew we could clear it,
with no good outcome, and one purifier means one fingerprint and one threshold.
Now: a **labelled 12-image calibration set** + an **unlabelled 30-image evaluation set** whose
purified ten come from **two** configurations (announced as plural, never specified); score is
balanced accuracy on both; the headline is the **generalisation gap** between them; ground
truth and our own detector published **after** the deadline.
Tier 2 is rescoped to the cheap purifiers — it was advertising a cascade whose IMPRESS stage
recovers ≈ 0. Full spec: `M1/TIER3-SPEC.md`.
**The principle:** *design a challenge so every possible outcome is a result you are content
to publish.*

## Decision 3 — corrections carried into the Ed post

1. `pg_metric`'s SSIM is measured against the **edited clean image**, not the original photo.
2. "77 minutes per image" was the grid's most expensive corner quoted as the general cost —
   replaced with measured timings plus the saturation finding.
3. The stale "shield too weak, numbers not interpretable" caveat is gone.
4. §4's "two extensions" is now "two instruments we built, and have not yet run".

---

## ⛔ Left before 28 Aug

1. **Confirm the Kaggle zips are downloaded or the version committed.** `/kaggle/working` is
   discarded otherwise. 46 MB, two files.
2. Paste Nissa's §1 and §2 into `M1_Ed_Post_DRAFT.md` (**done by Nissa 22 Aug**); check the
   `‹CHECK›` correction survived.
3. `sweep_grid.png` into Ed post §4.
4. Tier 3 pack — **run B4 first** (step 0 of `TIER3-SPEC.md`).
5. Share link "anyone with the link", tested from a logged-out browser.
6. Post to Ed, then the URL into a PDF/txt on the **Moodle M1 page**.

## Process lesson from this session, worth keeping

Three diagnostics ran in a row, each overturning the last, six days before a **2%** milestone
whose rubric has no results row. Echo stopped it. **Check the rubric before starting an
investigation — curiosity about a result is not the same as work the deadline requires.**

---


## What was done

1. **`M1/Dark_Tyro_M1.ipynb` built — this is the single notebook that ships to Ed.**
2. **Tier 3 redesigned.** Spec in `M1/TIER3-SPEC.md`.
3. **Ed post rewritten to v2.** `M1/M1_Ed_Post_DRAFT.md`, with a change log at the bottom.

---

## Decision 1 — one merged notebook, and what is now superseded

`M1/Dark_Tyro_M1.ipynb` = `Tyro_Sweep.ipynb` backbone with `patch_cell.py` and
`patch_cell2.py` **folded in**, plus Part A (CLIP restoration rate `R`) and Part B (FFT
frequency signature) rewritten against the sweep's archive contract.

**Why merged, not linked:** Ed post §4 claims two extensions. A marker following the single
notebook link must find them there. A claim the artifact cannot evidence costs more than the
0.4% row it was meant to buy. It also puts Echo's individual contribution in the same
artifact as the group pipeline, which matters when 26 of 50 marks are individual.

| file | status |
|---|---|
| `M1/Dark_Tyro_M1.ipynb` | **the submission.** Keep current. |
| `M1/Tyro_Sweep.ipynb` | superseded — kept only as the pre-merge record |
| `M1/patch_cell.py`, `patch_cell2.py` | superseded — folded into cell 8 |
| `Tyro_Analysis_Toolkit.ipynb` | **keep.** Still the home of standalone mode, IMPRESS-lite, the purifier cascade, and **B4** |

**Structural changes beyond a copy-paste merge:**

- Patch cells folded in. A submission notebook must not contain "paste this as a new cell".
- Every stage is archived under a parameter-stamped tag with a `params.json` — the other
  half of the bug-7 fix. Images are archived **before** metrics are parsed, so a parse
  failure can no longer discard a completed run.
- `EDIT_PROMPT = PARAMS['prompt']` — **bound, not copied.** If the two ever diverge, every
  `R` is meaningless while still printing a plausible number. This was a known trap; it is
  now structurally impossible.
- Parts A and B discover archived runs by globbing `tyro_results/` for complete folder sets,
  so they run on saved results from a previous session. Run cells 1 and 6, then jump to A.
- `run_config` catches `torch.cuda.OutOfMemoryError` per configuration — one dead cell of the
  grid no longer costs the whole grid.
- **B4 is NOT in the notebook.** Checklist item added to the Ed post.

## Decision 2 — `(200, 10)` is out of the grid, and that is the stronger story

It **OOMs on 16 GB** (T4 and P100). Recorded as **fix 10**; the fixes list is now
**ten repairs + two extensions**.

Three responses, and the choice matters:

1. ✅ **Omit it and say why.** `pg_iters` saturates — each PGD step moves exactly
   `pg_step_size` in L2 and is projected back into the `pg_eps` ball, so the budget is spent
   after ~16 steps. `(200, 10)` is 5× the compute of `(40, 10)` on the lever that had
   already run out. **A reasoned-out cell reads better than a missing one.**
2. `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` — already set in cell 1. Free; fixes it
   if the cause is fragmentation rather than true capacity. Worth one attempt.
3. ❌ `diff_steps` 4 → 2. Halves peak memory but changes the attack **and every folder name**.
   **A grid where one point used a different attack is not a grid.** Only acceptable if
   applied to all four configurations.

> General lesson worth keeping: when a resource limit blocks one cell of an experiment, check
> whether your own analysis already predicted that cell was uninformative. Here it did, which
> converted a compute failure into a parameter-selection result.

## Decision 3 — Tier 3: stop hiding the detectability problem, make it the question

**The trap in the v1 design.** It promised *"we will publish our own accuracy on this exact
set as the bar to beat."* That is a bar announced before we knew we could clear it, and it
has no good outcome: high accuracy advertises that our purified images are trivially
detectable (the attack half-fails); low accuracy looks like we cannot analyse our own output.
Worse, all 10 purified images came from one purifier configuration — one fingerprint, one
threshold, done.

**The reframe.** We already know purification leaves a trace: IMPRESS optimises for VAE
round-trip self-consistency, and we measured the axis ourselves (clean 0.0071, protected
0.0204). So *"is it detectable?"* is answered — yes. **The open question is whether a
detector that catches one purifier catches a different one.** If it does not, detection is a
defence you must retune whenever the attacker changes a parameter.

**The mechanics** (full spec in `M1/TIER3-SPEC.md`):

| | |
|---|---|
| calibration set | 12 images, 4/4/4, **labels given** — fit whatever you like |
| evaluation set | 30 images, 10/10/10, labels withheld; the purified ten come from **two configurations**, announced as plural, never specified |
| score | 3×3 confusion matrix + balanced accuracy (chance 33.3%) on **both** sets |
| headline | **generalisation gap** = balanced_acc(calibration) − balanced_acc(evaluation) |
| our commitment | ground truth, our own detector, and a read of the error patterns — **after** the deadline, not before |

**Why every outcome is now publishable.** Small gap → someone found something real about
purification, and it becomes our M2 detector-aware purifier spec. Large gap → detection does
not transfer, which is a result about the defence, not about us. Nobody wins by tuning one
threshold, because the evaluation set has more than one fingerprint in it.

**The principle, stated so it survives to M3 and M4:** *design the challenge so that every
possible outcome is a result you are content to publish.* Disclosing a weakness as a designed
research axis removes the only thing an opponent can catch you on — and it is honest, which
matters more.

**What we still do not disclose, legitimately:** our measured detection accuracy, which
statistic our detector uses, the `f_c` we settle on, and which images came from which
purifier. Those are held until after the deadline. That is the ordinary order of a
challenge — you do not publish the answer key before the exam.

## Decision 4 — three factual corrections to the Ed post

1. **"SSIM/PSNR vs the original photo" was wrong.** `pg_metric.py` compares the *edited*
   images against the *edited clean* image. Two different quantities in this project are
   called SSIM; §4 now reports both and labels which is which.
2. **"77 minutes per image" was the most expensive corner of the grid quoted as the general
   cost.** Replaced with measured timings plus the saturation finding — which is a stronger
   claim, because it turns a compute complaint into a result about which knob is real.
   Flagged `‹CHECK›` in §2 for Nissa to carry through.
3. **The stale "shield too weak, numbers not interpretable" caveat is gone.** True of trial 1,
   not of `(200, 2)`. Replaced with two scope notes that are accurate now: the SSIM ambiguity
   and the sample size.

## Finding — the FFT onset rule is method-dependent (new, 22 Aug)

Verified by rebuilding the synthetic test: a shield injected at `f = 0.45`.

| rule | flat (white) reference spectrum | photograph-like 1/f^1.5 spectrum |
|---|---|---|
| **half-peak** (what we had) | 0.453 ✅ | **0.708 ❌** |
| **first sustained crossing of the 3σ noise floor** (added) | fails | **0.453 ✅** |

**Why.** A photograph's spectrum falls off like 1/f, so the shield's *relative* contribution
keeps growing toward Nyquist. The difference curve therefore rises monotonically inside the
band, and "half of peak" lands well inside it rather than at its edge.

The earlier verification note (*"recovered f = 0.453 against a shield injected at 0.45"*) was
run against a flatter reference, which is why the fault did not show. **A control that
happens to agree with your hypothesis returns a confident wrong answer** — the same lesson as
the randomly-initialised mock autoencoder.

**What the notebook does now:** reports **both** numbers as a *range* and tells you to sweep
`f_c` between them, choosing the value whose spectrum best matches clean. It no longer quotes
a single derived cutoff, which would be a precision claim we cannot support.

**Also added: a B2 guard rail**, matching A2's. If the protected spectrum is not measurably
above clean at any frequency, `half` goes negative, every bin clears it, `argmax` returns bin
0, and the cell reports a confident cutoff of `f = 0.003` — which would low-pass the photo
into a grey rectangle. It now refuses and tells you to raise `pg_eps`. Verified against a
no-shield negative control.

---

## ⭐ THE RESULT (added later on 22 Aug, from Echo's FigJam run log)

Full reading in **`M1/RESULTS-READ.md`**. Every recovery figure in the FigJam reproduces
exactly from the adv/pur pairs — the transcription is clean.

`R_pipe = (pur − adv) / (1 − adv)` on `pg_metric` SSIM:

| config | units | SSIM adv | SSIM pur | **R_pipe** | three-metric sign test |
|---|---|---|---|---|---|
| 40:2 | 80 | 0.5494 | 0.5979 | **+10.8 %** | psnr + · ssim + · vifp + → **real** |
| 40:10 | 400 | 0.6138 | 0.6087 | −1.3 % | signs disagree → **noise** |
| 200:2 | 400 | 0.5357 | 0.5482 | +2.7 % | signs disagree → **noise** |

**Say exactly this and no more:** IMPRESS recovers ~11% of the shield's damage at the weakest
protection setting and **nothing measurable at 400 grad-units**, with two independent
allocations agreeing there. **The equal-compute question is answered: neither.** More steps
(`200:2`) and better steps (`40:10`) both collapse — past the threshold, how the shield spent
its budget stops mattering. Two allocations landing on the same answer is a replication.

**Do NOT say** "the shield worked and we stripped it" — that was Ed post §4 and it is now
corrected. **Do not rank** 40:10 against 200:2; their `adv` SSIMs are not even monotone in
shield strength at n = 2.

**How to read a small sample, as a reusable rule:** never trust one metric on two images;
trust whether three independent metrics agree on the **sign**. Agreement = something real
moved. Disagreement = inside the noise — **and saying so is a result.** M1's rubric has no
"your attack works" row.

### Two things called R — keep them apart

| name | what it is | status |
|---|---|---|
| **`R_pipe`** | SSIM ratio from `pg_metric` (vs the *edited clean* image). "Did the pipeline behave normally?" | **computable now, no CLIP** — this is the Kaggle number |
| **`R_edit`** (was just `R`) | CLIPScore ratio. "Does the output match the prompt?" | **not yet run** |

Publishing one under the other's definition is a claim–evidence mismatch. That is now the
third time this project has nearly given two quantities the same name (cf. the two SSIMs).

### The open question, and the test that settles it

Near-zero recovery has two explanations `pg_metric` **cannot** separate, because it only ever
looks at the *edited* images:

| | means | M2 looks like |
|---|---|---|
| (a) purification barely moved the pixels | our attack did not really run — a settings finding | tune `pur_eps` / `pur_iters` |
| (b) it moved and the shield survived | a real property of PhotoGuard's **diffusion** attack | the most interesting thing in the project |

> Recovery near zero is a patient who did not get better. Before concluding the drug does not
> work, check they swallowed it.

**Cell A0.5 in `Dark_Tyro_M1.ipynb` decides this. No GPU, ~30 s, uses the archived inputs.**
It reports a **movement ratio** — how far purification travelled as a fraction of how far the
shield travelled. `< 0.15` = the medicine stayed in the bottle (raise `pur_eps` 0.1→0.3 and
`pur_iters` 100→300 on **one** config first). `≈ 1` and moving toward the original = the
attack ran and lost, which is publishable.

**Second test, ~10 GPU-min:** VAE round-trip inconsistency on clean / protected / purified.
The 0.0071-vs-0.0204 gap was measured against PhotoGuard's **encoder** attack; these runs used
the **diffusion** attack. If the gap has collapsed, IMPRESS's premise does not hold here — a
strong M2/M4 finding, not a setback.

### Caveat this forces onto the saturation claim

Both 400-unit points hitting ≈ 0 is *consistent* with `pg_iters` saturating, but equally
consistent with "both shields simply won". **This experiment cannot separate them, and the Ed
post no longer claims it does.** `pg_eps` remains completely untested and is the M2 priority.

---

## ⛔ Blocking M1 submission (28 Aug)

1. **Run cell A0.5** on the archived inputs. No GPU. It decides how §4 is written.
2. **Locate the raw `tyro_results/` folders.** The numbers are recovered from FigJam, but
   A0.5, Part A and Part B all need the actual image folders (`clean`, `protected`,
   `purified`, `edit_*`).
3. **Look again at the 3-panel figure.** In the FigJam log the edited-protected images look
   far less damaged than TRIAL-LOG's "crazed-skin floating head" description. If the visual
   gap is smaller than we remembered, the caption has to match what a marker will see.
4. **Run B4** (step 0 of `TIER3-SPEC.md`) before building the Tier-3 pack.
5. **Nissa: Ed post §1 and §2**, carrying the `‹CHECK›` corrections.

## Not blocking, ranked by marks-per-hour

- One run at `--pg_eps=24 --pg_iters=40 --pg_grad_reps=10`. Cheaper than `(200, 2)` and per
  the saturation analysis should be *stronger*. If it is, that single comparison is the most
  interesting sentence in the Ed post.
- Re-run the shipped configuration on ≥ 5 faces.
- Sweep `f_c` between the two onset estimates and pick the least-detectable value.

## Original task list for this session (all three addressed)

1. ~~Refine and combine the notebook; confirm one can serve as the submission.~~ → Decision 1
2. ~~Finish the Ed post draft; polish a challenge others can attempt without exposing that
   our output may be easy to detect.~~ → Decisions 3 and 4. Note the answer turned out to be
   the opposite of hiding it.
3. ~~Update `HANDOVER.md`.~~ → this section

## Note on where results live
Echo logs Kaggle run output in **FigJam**, not the project folder. Ask for the FigJam board
rather than searching the filesystem — but the raw `tyro_results/` image folders are still
needed for A0.5 and Parts A/B.



---

# 23 Aug 2026 — ⭐ THE BASELINE CLAIM (settled; use this wording everywhere)

*Supersedes looser phrasings such as "our attack method is IMPRESS, which we revised."
Cite this section in the Ed post, the M3 slides and the M4 report.*

## 1. What is theirs, what is ours — state it precisely

**The algorithm is unmodified. Everything around it is ours.** `impress.py` is 25 lines and
not one of them was touched — **and that is the point.** A repaired reference implementation
is only useful as a baseline if it is still the reference.

| component | ours? | where |
|---|---|---|
| the purification objective `‖D(E(X_p)) − X_p‖² + α·max(LPIPS(X_p,X_adv) − ε, 0)` | ❌ theirs, untouched | `impress.py` |
| a runnable 2026 port (eleven repairs) | ✅ | cells 1–7 |
| single-GPU harness, parameter-stamped archive, live heartbeat | ✅ | cell 8 |
| **`R_pipe`** — a restoration rate the paper has no equivalent of | ✅ | cell 10 |
| the controlled 3-panel comparison (same seed/mask/prompt) | ✅ | cell 11 |

**Say "we did not change the algorithm" out loud.** It sounds modest and is the stronger
claim: it means our numbers are about IMPRESS, not about our edit of IMPRESS. When a Light
team says *"you just ran their code"*, the reply is: the code is theirs, the **measurement**
is ours, and the measurement is what M2 is for.

## 2. The verifiable gap — paper's ambition vs shipped code

IMPRESS abstract, **verbatim** (arXiv:2310.19248, confirmed 23 Aug):

> "IMPRESS ... offers a comprehensive evaluation of several contemporary protection methods,
> and **can be used as an evaluation platform for future protection methods.**"

The released code does not deliver that. It ships **two method-specific pipelines with two
hardcoded folder contracts and no generic entry point**:

```
glaze_pur.py           <- reads ../wikiart/.../trans/...          (Glaze's layout)
pg_mask_pur_helen.py   <- reads ../helen_face/adapt_adv_<pg params>/  (PhotoGuard's layout)
```

Nothing in the repo accepts *"here is a protected image, evaluate it."* Backed by a
`git clone` and two `ls` commands — a claim we can demonstrate live.

**Our M2 contribution, in one line:** *build the generic entry point the paper's claim
implies — one interface that accepts any protected image, plus a two-axis scoreboard
(robustness × perceptual cost) to report it on.*

This converts our position from "we invented something" to **"we complete what the authors
proposed but only partly delivered"** — far easier to defend under questioning, and it earns
the *Baseline Justification* row directly.

## 3. ⚠️ Framing risk: we are Dark, not a neutral benchmark

"We built an evaluation platform for protection methods" is a **Light-sounding** sentence.
Theme 2 Dark requires *"design an attack technique to evaluate and potentially bypass the
defence mechanism."* Keep the platform framing, fix the emphasis — **attacker first**:

> A purification attack that works *without knowing which protection it is removing* is more
> dangerous than one tuned to a single shield. PhotoGuard, Glaze and Mist all assume the
> attacker must be tailored to them. IMPRESS's objective needs no such knowledge — it only
> asks the image to be self-consistent under an autoencoder. We take the authors at their
> word that this generalises, and build the open harness that tests it. That our attack
> doubles as the benchmark for every protection method **is the threat**, not a neutral
> service: one solvent, and every shield in the theme is measured by how long it survives
> contact with it.

> **Metaphor to reuse:** a locksmith who can open every brand of lock is not a neutral
> testing lab. He *becomes* the standard by which locks are rated — and he is still a burglar.

## 4. IMPRESS is a stain remover, not a lock-pick

The fact that dissolves the "should we restrict challengers to PhotoGuard?" question:
`impress()` takes a protected image and optimises it toward VAE self-consistency. **It never
asks how the perturbation got there.** Only the *generation* stage is PhotoGuard-specific —
and in the challenge, the challenger performs that stage, not us. So the challenge is defined
by an **interface**, never by a method. Full design in `M1/CHALLENGE-M1.md`.

## 5. Per-milestone claim

| | claim |
|---|---|
| **M1** | The reference implementation runs in 2026, unmodified in substance, with our measurement on top. PhotoGuard is the *validation case* proving the port is faithful. |
| **M2** | Deliver the generic entry point the paper promised — any protected image in, robustness × cost out. Other teams supply the shields. |
| **M3** | Which shields survived, which did not, and what the pattern says about what protection actually does. |
| **M4** | Echo: the FFT-targeted filter — *keen observation*, the opposite of the blind solvent. The pair is the interesting comparison. |

