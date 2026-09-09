# M2 — Dark.Tyro: a stronger wash, and the metric that could not see it

**Team Dark.Tyro** · Echo Zhao · Nissa Corlidea
**Theme 2 (Text-to-Image) · Dark / attack side** · Milestone 2, 18 September 2026

---

## TL;DR

We made IMPRESS's purifier **four times cheaper** at the same attack strength, using four lines
of arithmetic. Then we ran two controls the original paper never ran, and found that
**IMPRESS's own evaluation metric cannot detect PhotoGuard at PhotoGuard's own settings** —
the pipeline's re-run noise is larger than the shield's signal. We report both, because the
second one limits what we are allowed to claim about the first.

Our challenge, **the Tyro Wash Test**, is open now. Entry cost is one notebook cell.

---

## 1 · The change: four lines

M1 ported IMPRESS to 2026 (eleven repairs) and measured it honestly: `R_pipe = +5.2%` at a cost
of `LPIPS 0.15` — roughly **nine times** what the shield it removes cost to apply. A solvent
that damages the photograph more than the protection did is not yet a usable attack.

**The observation.** An inpainting mask splits the photo into two regions the editor treats
completely differently. Inside the white mask (~30% of pixels) the editor **preserves** the
image — we measured 4–7 grey levels of change. Outside it, the editor **regenerates from
scratch** — 86–96 levels.

IMPRESS pays the same everywhere. So about **70% of its fidelity cost is spent scrubbing pixels
the editor throws away and repaints.**

**The method, in full:**

```python
purified_v2 = mask * purified_impress + (1 - mask) * protected
```

Keep IMPRESS's work where the edit survives; restore the original pixels where the editor
repaints anyway. The mask is feathered by 3 px, because a hard seam is itself a high-frequency
artefact and an obvious detector signature.

> Repainting three walls of a room and keeping the fourth. Sanding all four is not thorough —
> it is wasted effort that damages the one wall you meant to keep.

**Why this is not cheating.** The attacker holds the mask; it is an *input* to the editing
pipeline they are about to run, not privileged knowledge of the defence. PhotoGuard's own
scripts are named `pg_mask_*` for the same reason. We use knowledge of **our own edit**, not of
the shield.

**Why it might have failed.** The black region is discarded as *output*, but the whole image is
still encoded as *conditioning* — a shield left there can still steer what gets generated. That
was the honest risk, and the table below is what tested it.

---

## 2 · The result: same strength, a quarter of the cost

Four arms, one shield setting (`pg_iters=40, grad_reps=2, pg_eps=16`), same faces, same seed.
**n = 2 images.** Every number below is measured, not estimated.

| arm | wash | `R_pipe` % ↑ | LPIPS vs clean ↓ | SSIM vs clean | damage |
|---|---|---|---|---|---|
| **N** | none (the origin) | 0.00 | **0.018** | 0.988 | 0.73 levels |
| **A** | IMPRESS, 100 iters — *the M1 baseline* | 4.75 | 0.150 | 0.758 | 5.04 levels |
| **B** | IMPRESS, 1000 iters — *the paper's own budget* | 9.41 | 0.109 | 0.794 | 4.76 levels |
| **C** | **ours** — IMPRESS 100 iters, mask-restricted | 7.05 | **0.039** | **0.937** | 1.84 levels |

**C runs at A's compute.** Against A it costs **0.039 instead of 0.150 LPIPS — 26% of the
price** — while `R_pipe` moves +2.3 pp, which is *inside* our own measured noise band and which
we therefore do not claim as an improvement.

> **The claim: the same attack strength to within our measured noise, at a quarter of the
> perceptual cost.** A cost claim, not a strength claim.

**Arm N is why the table is honest.** It skips purification entirely and edits the protected
image, so it sits at `R_pipe = 0` by construction, at the shield's own LPIPS. Any arm below or
to the right of N did more harm than not attacking at all — a real possibility for a purifier,
and one that comparing washes only against each other can never reveal.

*(figure: `m2_tradeoff.png` — a stronger wash moves UP and LEFT)*

---

## 3 · The controls, and what they cost us

Before claiming `R_pipe` had improved, we asked whether `R_pipe` measures anything. Two nulls,
neither of which appears in the IMPRESS paper.

**Null 1 — the seed floor.** Edit the *clean* image twice with two different seeds. Nothing is
protected; any difference is the generator's own variance.

**Null 2 — random noise at matched L2.** Replace PhotoGuard's shield with random noise of
identical magnitude. Any difference is structure, not size.

SSIM against the seed-0 clean edit — **lower means the edit was disturbed more:**

| image | seed floor (null 1) | **real shield** | random, same L2 (null 2) |
|---|---|---|---|
| 1233476865_1 | **0.472** | 0.584 | 0.737 |
| 1525918600_1 | **0.415** | 0.610 | 0.921 |

Two things follow, and they point in opposite directions:

1. **PhotoGuard beats random noise at identical L2.** The shield is genuinely *structured*, not
   merely a perturbation. That is a positive finding about PhotoGuard and we report it as one.
2. **But changing the random seed disturbs the edit more than the shield does.** The shield
   moves the image only 0.5–0.9 grey levels. So `1 − ssim_adv` — the denominator of `R_pipe` —
   is dominated by ordinary generative variance, not by protection.

CLIPScore agrees independently: the seed-to-seed gap is **2.19 points**, and neither image's
protection efficacy clears it. On one image it is **negative** — the protected edit matched the
prompt *better* than the clean one did.

**⭐ The finding we think matters most.** `pg_metric.py`'s SSIM is *IMPRESS's own* evaluation
metric. At the paper's own settings it **cannot detect PhotoGuard**, because the pipeline's
re-run noise exceeds the signal. Two controls the paper never ran are enough to show it.

**What this costs us:** we do not quote `R_pipe` as evidence of a stronger attack. The fidelity
result is untouched by any of it, because it compares purified images to the clean photograph
and never invokes the editor at all — which is also why it reproduces to four decimals.

---

## 4 · The challenge is open — the Tyro Wash Test

**Track A: build a shield we can't wash off.**

We give you 10 clean 512×512 faces, their inpainting masks, and a working PhotoGuard protector
you can run in one cell. You edit **one function**. You send back 10 PNGs with our filenames.
That is the entire interface — you never have to tell us how you protected them, because our
purifier never inspects the perturbation.

- 📦 pack: `tyro_wash_test_trackA.zip` (10 clean + 10 masks + manifest + `check_submission.py`)
- 📓 starter notebook: **[LINK — paste Colab URL here]**

**We score two axes and publish both, as one scatter plot.**

| axis | meaning | you want |
|---|---|---|
| `R_pipe` | how much of the editing pipeline our wash restored | **low** |
| LPIPS(protected, clean) | how much of the photograph you destroyed to get there | **low** |

One axis has a degenerate winner: perturb until the image is noise, and nothing can be washed
off it — but nothing can be *edited* either, so that "defence" defeats its own purpose. A shield
that wins by wrecking the picture lands in the top-right corner, in public.

**Ranking budget: LPIPS ≤ 0.10** — the same perceptual allowance our own purifier gets
(`pur_eps = 0.1`). The shield may spend exactly what the attack is allowed to spend. For
calibration, our own reference entry sits at **LPIPS 0.0665**, and PhotoGuard's default shield
costs about **one grey level**, so the budget is generous. Over-budget entries are plotted and
discussed, just not ranked.

**Engagement gate — and section 3 is why we mean it.** If your shield does not measurably
disturb the edit, `R_pipe` is a ratio of two near-zero numbers. We report it only when
SSIM(edited-protected, edited-clean) ≤ 0.85; otherwise we report **"shield did not engage"** and
show you what we actually measured. We have just published a section demonstrating that this
happened to *our own* baseline, so this is not a formality.

**Every outcome gets published, including ours losing.** If a protection defeats our purifier,
that is a real result about IMPRESS and we report it as one.

**Send by 15 September** to be included in the results. Reply on this thread or DM us.

---

## 5 · Limitations

Stated plainly, because a claim we cannot evidence costs more than a modest result.

1. **n = 2 images.** Per-image `R_pipe` disagrees in *sign* across the two (−10.5% and +18.8%
   for arm A). Between-image spread is ~30 pp; between-arm spread is 1–4 pp. Read the orderings,
   never the magnitudes.
2. **One shield setting.** `pg_eps = 16` only. Section 3 shows this is precisely the setting at
   which the metric goes blind, so **`pg_eps` is the first thing we test next**, not a footnote.
3. **The mask is an input, not a discovery.** Our method needs to know which region will be
   edited. Always true of an inpainting attacker — but it does **not** transfer to whole-image
   protections such as Glaze, where there is no mask. We claim nothing there.
4. **The two axes have very different noise, and we measured it.** Re-running one configuration
   on identical hardware: LPIPS and SSIM-vs-clean reproduce **exactly**; `R_pipe` moves 2–4 pp.
   The cause is worth stating — fp16 kernel selection shifts the protected image by 0.1 of a
   grey level, which the editor amplifies into ~11 levels of output, roughly 100×. **Our metric
   is unstable for exactly the reason the defence exists.**
5. **A frequency-targeted filter was tried and failed.** We measured PhotoGuard's band and swept
   a Butterworth cutoff from f = 0.40 to 0.95. At `pg_eps = 16` the shield is quieter than the
   photograph's own fine detail, so every cutoff removed more real detail than shield. Reported
   because a negative result at a stated setting is still a measurement — and because it is what
   pointed us at the mask instead.

---

## Code

Everything runs top-to-bottom on Kaggle (GPU T4 ×2, Internet ON). Each notebook ships with a
smoke mode that exercises the full pipeline at reduced iteration counts, so a broken path fails
in four minutes instead of forty.

| notebook | what it is |
|---|---|
| `Dark_Tyro_M2.ipynb` | the attack — M1 plus four lines. The diff *is* the contribution. |
| `challenge/Tyro_Wash_Test_STARTER.ipynb` | the defence starter for challengers. One function to edit. |
| `Tyro_M2_diagnostics.ipynb` | the two controls in section 3. Point it at a run folder; edit one line. |

**Baseline provenance:** the IMPRESS algorithm is unmodified. The eleven repairs, the measurement
harness, the four-line mask restriction, and the two controls are ours.
