# Thread map — Dark.Tyro working structure
*Set up 20 Aug 2026. One conversation per thread. Paste the kickoff block into a new chat.*

Split by **what each conversation has to hold in its head**, not by topic. A thread is a
working memory: a chat that has spent an hour debugging notebook cells is a bad place to
have a careful conceptual discussion.

| thread | holds | status | deadline |
|---|---|---|---|
| **A · Read the results** | the 3 trials, the images, the parameters, metric-vs-perception | ✅ **done 20 Aug** → `M1/TRIAL-LOG.md`, `GLOSSARY.md` | — |
| **B · Ship M1** | submission notebook + Ed post | ✅ **notebook built & executed 22 Aug** → `M1/Dark_Tyro_M1_FINAL.ipynb`. Assembly only left, see `M1/M1-CHECKLIST.md` | **28 Aug** |
| **C · IMPRESS internals & M2** | the paper's mechanics, why purification underperforms | ⬜ **next** | 18 Sep |
| **D · IMPRESS × QF fusion** | two threat models, one system, a joint metric | ⬜ | 2 Nov (M4) |

B depends on A. C and D are parallel and unhurried. **C is the natural piece to hand Nissa**
— it is self-contained reading plus a written summary, needs no GPU, and blocks nothing.

---

## Kickoff block — Thread C · IMPRESS internals & M2  ⟵ START HERE NEXT

> Read `HANDOVER.md`, then `M1/RESULT-INTERPRETATION.md`. This is **Thread C**, due 18 Sep.
> M1 is built — do not rebuild it, do not reopen the baseline decision.
>
> **The question C exists to answer: why does IMPRESS recover so little at the reference
> settings?** Our measured `R_pipe` is +5.2% at 80 gradient-units and −1.2% at 400.
>
> **The lead:** a bare VAE round-trip changes an image by **4.28** levels; everything
> purification did amounts to **4.75**. Purification's whole effect is about the size of just
> passing the image through the autoencoder. `M2_diagnostics.ipynb` has the measurement — and
> a table of which earlier readings were **voided** by a resolution mismatch. Read that table
> before quoting anything from it.
>
> **Job 0, before any new measurement:** archive a **512×512 copy of the clean image** — the
> tensor the pipeline actually conditioned on — beside the originals. `clean/` currently holds
> full-resolution Helen photos (2736×3582, 4000×3000) while `protected/` and `purified/` are
> 512×512, so every clean-vs-other comparison silently measured interpolation. Fix the archive
> contract in `run_config` and the whole diagnostic line becomes trustworthy.
>
> **Then, in order:**
> 1. Read `pg_mask_pur_helen.py` line by line. What does `pur_alpha` actually weight? Is the
>    anchor strong enough to matter at 0.01? Does `pur_noise=0.05` get removed again?
> 2. Sweep `pur_eps` 0.1 → 0.3 and `pur_iters` 100 → 300 on **one** configuration. Does the
>    purifier move further than the round-trip floor?
> 3. Sweep **`pg_eps` 16 → 24 → 32** — the untouched lever, and the one that raises the
>    shield's ceiling. `pg_iters` saturates; `pg_eps` does not.
> 4. Then ≥ 5 faces, LPIPS beside SSIM, and the CLIPScore edit-success rate.
>
> **Nissa's angle lives here too:** model-mismatch purification — does protection computed
> against one autoencoder survive a different one? Self-contained, no dependency on 1–4.
>
> Constraints: **Kaggle GPU T4 x2, never the P100** (`sm_60`, no kernels in current torch).
> Persist results the moment they exist — see repair 11 and the persistence cell.

## Kickoff block — Thread D · IMPRESS × QF fusion (M4)

> Read `HANDOVER.md` §"QF's real home" and `QF_Attack_Tyro.ipynb`. This is **Thread D**, for
> the individual IEEE report due 2 Nov. Worth **9%** across two M4 rows.
>
> A TTI editing pipeline has **two** inputs: an image and a prompt. Everything in M1–M3
> attacks the image side. PhotoGuard, Glaze and Mist all guard pixels; **nobody guards the
> prompt.**
>
> 1. **"Unconstrained System Enhancement & Feasibility" (4%)** — the two-flank attack: strip
>    the image shield *and* perturb the text side. `QF_Attack_Tyro.ipynb` is the feasibility
>    demo the rubric asks for.
> 2. **"Adversarial Role-Reversal Strategy & Demo" (5%)** — having run a text-side attack
>    makes the text-side *defence* concrete: normalise prompts before encoding, reject
>    embeddings far from any in-vocabulary neighbour, or ensemble two text encoders and refuse
>    when they disagree. The first is about ten lines.
>
> Needs a joint metric that covers both flanks. Do not start this before M2 ships.
