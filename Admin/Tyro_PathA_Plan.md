# Tyro — FIT5230 Theme 2 (Attack) — Path A Plan

**Decision:** Baseline = **IMPRESS** (attack paper, NeurIPS 2023, has code + replicable metrics).
Target/shield = **PhotoGuard**. Our contribution = a **cohesive purification system** on top.

This satisfies both of the lecturer's options at once: we adopt an *attack paper with runnable code as the baseline*, while keeping PhotoGuard as the thing we attack.

- IMPRESS paper: https://arxiv.org/abs/2310.19248
- IMPRESS code: https://github.com/AAAAAAsuka/Impress
- PhotoGuard (defense): https://arxiv.org/abs/2302.06588 · https://github.com/MadryLab/photoguard

---

## Why IMPRESS fits us (checked against the repo)

The repo has a **ready-made PhotoGuard track** — we don't build the baseline from scratch:

| Step | Script | What it does |
|---|---|---|
| Add shield | `pg_mask_diff_helen.py` | Puts PhotoGuard noise on face images |
| Baseline attack | `pg_mask_pur_helen.py` | IMPRESS purification (removes the noise) |
| Edit | `pg_generate.py` | Runs the malicious edit on clean/protected/purified |
| **Metrics** | `pg_metric.py` | Replicable numbers — the "replicable baseline" the lecturer wants |

Two gifts that save us days:

1. **Pre-made PhotoGuard data** (Helen faces) is downloadable from the repo's Google Drive — we can skip generating protected images.
2. **The PhotoGuard track needs NO fine-tuning.** (Only the *Glaze* track needs 4-GPU fine-tuning — we ignore it.) So it runs on **free Colab T4**, our exact hardware limit.

---

## What we get free vs. what we build (our novelty)

- **Free (baseline):** PhotoGuard shield + IMPRESS purification + metrics harness.
- **We build (the "cohesive system of attacks"):** one tunable pipeline —
  **JPEG → blur → downscale/upscale → DiffPure** — plugged into the same `pg_metric.py` harness, compared head-to-head against IMPRESS.
  This is one system with shared knobs, not four separate hacks — exactly what the lecturer asked for.
- **Individual extensions (26/50 marks are individual):**
  - **Echo** — FFT "keen observation" attack: compare frequency spectra of protected vs. clean, then a *surgical low-pass filter*. Sells on fidelity (removes noise, keeps the face sharp).
  - **Nissa** — model-mismatch attack: purify against a *different VAE* than PhotoGuard targeted.

---

## Compute feasibility (Colab T4 only)

- Stable Diffusion **2.1-base**, fp16, xformers — fits in T4's 15 GB.
- No fine-tuning on the PhotoGuard track → the heavy cost is gone.
- IMPRESS purification is a ~1000-iteration optimization *per image* → run on a **small subset (10–20 faces)** for the demo, not the whole set.
- Our own pipeline (JPEG/blur/upscale) is near-instant — cheap to sweep many settings.

**Main risk:** the repo's `requirements.txt` is 2023-era (old `diffusers`/`torch`). On today's Colab this can cause dependency conflicts.
**Mitigation:** install in a fresh venv with their pinned versions; if a script breaks, patch the one deprecated call rather than upgrading everything. Budget half a day for setup friction.

---

## Milestones (mapped to unit deadlines)

- **M1 — 28 Aug (2%, Ed post + own Colab):** clone IMPRESS, download PhotoGuard data, get `pg_mask_diff_test.sh` to run end-to-end on ~5 faces. Screenshot protected vs. purified vs. edited. Post to Ed.
- **M2 — 18 Sep (8%):** our purification system (JPEG→blur→upscale→DiffPure) integrated + first comparison table vs. IMPRESS baseline.
- **M3 — 22 Oct (25%, presentation):** full results, individual angles (Echo FFT / Nissa VAE) shown as separate contributions.
- **M4 — 2 Nov (15%, IEEE report):** written up, individually.

---

## Role split (solo-resilient)

- **Echo (lead):** owns the IMPRESS baseline + shared metric harness + FFT extension. Everything critical runs through Echo, so the project stands even if support is thin.
- **Nissa:** owns the VAE-mismatch extension + report sections. Bounded, independent piece — nice if delivered, not load-bearing.

---

## Immediate next step (M1)

1. Open a Colab (T4), `git clone` IMPRESS, `pip install -r requirements.txt`.
2. Download the PhotoGuard Helen-face data (repo Google Drive link).
3. Run `bash scripts/new/pg_mask_diff_test.sh` on a tiny subset.
4. Save 3 images (protected / purified / edited) for the Ed post.
