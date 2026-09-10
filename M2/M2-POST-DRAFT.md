# M2 — Dark.Tyro: a cheaper wash, and a metric that cannot see the shield

**Team Dark.Tyro** · Echo Zhao · Nissa Corlidea
**Theme 2 (Text-to-Image) · Dark / attack side** · Milestone 2, 18 September 2026

**In short.** Four lines of arithmetic make IMPRESS's purifier **four times cheaper** at the same
attack strength. Testing that claim properly, we found IMPRESS's own evaluation metric cannot
detect PhotoGuard at PhotoGuard's own settings — and that the paper's documented way to
strengthen the shield does not strengthen it. Our challenge, the **Tyro Wash Test**, is open.

---

## 1 · The change

M1 ported IMPRESS to 2026 and measured it: `R_pipe = +5.2%` at a cost of `LPIPS 0.15` — nine
times what the shield it removes cost to apply. A solvent that damages the photo more than the
protection did is not a usable attack.

The inpainting mask splits the photo in two. Inside the white mask (~30% of pixels) the editor
**preserves** the image — 4–7 grey levels change. Outside it, the editor **repaints from
scratch** — 86–96 levels. IMPRESS scrubs both equally, so ~70% of its cost buys nothing.

```python
purified_v2 = mask * purified_impress + (1 - mask) * protected
```

Wash only the region that survives into the output. The mask edge is feathered by 3 px, because
a hard seam is itself an artefact and a detector signature.

> Repainting three walls and keeping the fourth. Sanding all four isn't thorough — it's damage
> to the one wall you meant to keep.

The mask is an **input** to the editing pipeline we are about to run, not privileged knowledge
of the defence — PhotoGuard's own scripts are named `pg_mask_*` for the same reason.

## 2 · Result

Four arms, one shield setting, same faces, same seed, **n = 2 images**.

| arm | wash | `R_pipe` % ↑ | LPIPS vs clean ↓ |
|---|---|---|---|
| **N** | none — the origin | 0.00 | **0.018** |
| **A** | IMPRESS, 100 iters — the M1 baseline | 4.75 | 0.150 |
| **B** | IMPRESS, 1000 iters — the paper's own budget | 9.41 | 0.109 |
| **C** | **ours** — IMPRESS 100 iters, mask-restricted | 7.05 | **0.039** |

C runs at A's compute for **26% of A's perceptual cost**. `R_pipe` moves +2.3 pp, which is inside
our measured noise, so we do not claim it.

> **The claim: the same attack strength to within our measured noise, at a quarter of the
> perceptual cost.** A cost claim, not a strength claim.

Arm N is what makes the table honest: it skips purification entirely, so it sits at `R_pipe = 0`
by construction. Anything below or right of N did more harm than not attacking at all.

## 3 · Three controls, and what they cost us

**Null 1 — the seed floor.** Edit the *clean* image twice with two different seeds. Nothing is
protected, so any difference is the generator's own variance.
**Null 2 — random noise at matched L2.** Any difference is structure, not size.

SSIM against the seed-0 clean edit; **lower = more disturbed**:

| image | seed floor | **real shield** | random, same L2 |
|---|---|---|---|
| 1233476865_1 | **0.472** | 0.584 | 0.737 |
| 1525918600_1 | **0.415** | 0.610 | 0.921 |

PhotoGuard **beats random noise at identical L2** — the shield is genuinely structured, and we
report that as a positive finding about PhotoGuard. But **changing the seed disturbs the edit
more than the shield does.** The shield moves the image 0.5–0.9 grey levels. `1 − ssim_adv`, the
denominator of `R_pipe`, is mostly generative variance. CLIPScore agrees independently: the seed
gap is 2.19 points and neither image's protection clears it.

**Control 3 — we tried to fix this by doubling the shield.** At `pg_eps = 32`, twice the paper's
setting, the perturbation did not change: L2 2645.8 → 2641.6 and 1860.4 → 1841.1, damage 0.73 →
0.72 levels. The protect stage really re-ran. At `pg_iters=40, pg_step_size=1` the L2 ball is
never reached, so **`pg_eps` never binds — the documented strength knob is inert on this code
path.**

That gave us a free third measurement of our own noise. With the shield physically unchanged,
fidelity reproduced (A 0.1501→0.1495, C 0.0391→0.0381) while `R_pipe` moved **A +2.3, B +2.3,
C −1.1 pp** — changing sign between arms. That is the ±2–4 pp noise floor, not a result. It is
also why we decline to read the arm ordering.

**⭐ The finding.** `pg_metric.py`'s SSIM is IMPRESS's *own* evaluation metric. At the paper's own
settings it cannot detect PhotoGuard, because the pipeline's re-run noise exceeds the signal —
and the documented way to raise that signal does nothing. Three controls the paper never ran.

The fidelity result is untouched by all of this: it compares purified images to the clean photo
and never invokes the editor, which is why it reproduces to four decimals.

---

## 4 · The challenge is open — the Tyro Wash Test

**Build a shield we can't wash off.**

We give you 10 clean 512×512 faces, their masks, and a working PhotoGuard protector in one cell.
You edit **one function**. You send back 10 PNGs with our filenames. That is the whole interface —
you never have to tell us how you protected them, because our purifier never inspects the
perturbation.

- 📦 `tyro_wash_test_trackA.zip` — images, masks, `check_submission.py`, `seed_floor_10.json`
- 📓 starter notebook: **[LINK]**

**Two axes, both published as one scatter plot:** `R_pipe` (how much of the pipeline our wash
restored — you want it low) and **LPIPS(protected, clean)** (how much of the photo you destroyed
— also low). One axis alone has a degenerate winner: perturb until the image is noise and nothing
can be washed off it, but nothing can be edited either. That entry lands top-right, in public.

**Ranking budget: LPIPS ≤ 0.10** — the same perceptual allowance our own purifier gets
(`pur_eps = 0.1`). Our reference entry sits at **0.0665**; PhotoGuard's default costs about one
grey level, so the budget is generous. Over-budget entries are plotted and discussed, not ranked.

**Engagement gate — measured, and corrected in public.** We first published a threshold of 0.85.
That was a guess. We have since measured the seed floor on all ten images: it runs from **0.285
to 0.707**. 0.85 would have passed all ten trivially, including our own shield at 0.584 / 0.610 —
the one section 3 shows is indistinguishable from noise. So:

> We report `R_pipe` for an image only when SSIM(edited-protected, edited-clean) is **below that
> image's seed floor**, shipped in `seed_floor_10.json`. Otherwise: "shield did not engage", plus
> the number we measured.

The floors vary 2.5×, so the images are not equally hard — that is the editor, not our choice.
**We rank on how many of the ten engaged**, and publish per-image numbers, never a single mean.

**Every outcome gets published, including ours losing.** **Send by 15 September**; results appear
in our 18 September post. Reply here or DM us.

---

## 5 · Limitations

1. **n = 2 images.** Per-image `R_pipe` disagrees in *sign* (−10.5% and +18.8% on arm A).
   Between-image spread ~30 pp; between-arm 1–4 pp. Read orderings, never magnitudes.
2. **We have not tested a stronger shield — we showed this knob can't produce one.** `pg_eps` 16
   and 32 give the same perturbation. Finding the lever that binds (`pg_step_size`, or the attack
   type) is M3.
3. **The mask is an input, not a discovery.** True of any inpainting attacker, but it does not
   transfer to whole-image protections like Glaze, where there is no mask. We claim nothing there.
4. **`R_pipe` is unstable for the reason the defence exists.** fp16 kernel choice shifts the
   protected image by 0.1 of a grey level; the editor amplifies that into ~11 levels of output,
   roughly 100×. Fidelity is reported as a point, `R_pipe` as a range.
5. **A frequency-targeted filter was tried and failed.** Butterworth cutoffs from f = 0.40 to
   0.95: at this shield strength the perturbation is quieter than the photograph's own fine
   detail, so every cutoff removed more detail than shield. It is what pointed us at the mask.

## Code

Runs top to bottom on Kaggle (GPU T4 ×2, Internet ON). Each notebook ships a smoke mode that
exercises the full pipeline at reduced iterations, so a broken path fails in four minutes not forty.

| notebook | what it is |
|---|---|
| `Dark_Tyro_M2.ipynb` | the attack — M1 plus four lines. The diff *is* the contribution. |
| `challenge/Tyro_Wash_Test_STARTER.ipynb` | the defence starter. One function to edit. |
| `Tyro_M2_diagnostics.ipynb` | the three controls above. |

**Provenance:** the IMPRESS algorithm is unmodified. The eleven repairs, the measurement harness,
the four-line mask restriction and the controls are ours.
