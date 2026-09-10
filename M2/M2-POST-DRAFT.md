# M2 — Dark.Tyro: a cheaper wash, and a metric that cannot see the shield

**Team Dark.Tyro** · Echo Zhao · Nissa Corlidea
**Theme 2 (Text-to-Image) · Dark / attack side** · Milestone 2, 18 September 2026

**In short.** Four lines of arithmetic make IMPRESS's purifier **four times cheaper**, at no
measurable loss of attack strength. Testing that properly, we found IMPRESS's own evaluation
metric cannot detect PhotoGuard at PhotoGuard's own settings — and that the documented way to
strengthen the shield does nothing. Our challenge, the **Tyro Wash Test**, is open.

---

## 1 · The change

M1's port of IMPRESS scored `R_pipe = +5.2%` at a cost of `LPIPS 0.15` — nine times what the
shield it removes cost to apply. A solvent that damages the photo more than the protection did
is not usable.

The inpainting mask splits the photo in two. Inside the white mask (~30% of pixels) the editor
**preserves** the image — 4–7 grey levels change. Outside, it **repaints from scratch** — 86–96
levels. IMPRESS scrubs both equally, so ~70% of its cost buys nothing.

```python
purified_v2 = mask * purified_impress + (1 - mask) * protected
```

Wash only the region that survives into the output. The edge is feathered 3 px, because a hard
seam is itself an artefact and a detector signature.

> Repainting three walls and keeping the fourth. Sanding all four isn't thorough — it's damage
> to the one wall you meant to keep.

## 2 · Result

Four arms, one shield setting, same faces, same seed, **n = 2 images**.

| arm | wash | `R_pipe` % ↑ | LPIPS vs clean ↓ |
|---|---|---|---|
| **N** | none — the origin | 0.00 | **0.018** |
| **A** | IMPRESS, 100 iters — the M1 baseline | 4.75 | 0.150 |
| **B** | IMPRESS, 1000 iters — the paper's budget | 9.41 | 0.109 |
| **C** | **ours** — IMPRESS 100 iters, mask-restricted | 7.05 | **0.039** |

C runs at A's compute for **26% of A's perceptual cost**. Its `R_pipe` sits 2.3 pp above A —
inside our measured noise, so we claim no gain in strength.

> **No measurable change in attack strength, at one quarter of the perceptual cost.**
> A cost claim, not a strength claim.

Arm N makes the table honest: it skips purification, so `R_pipe = 0` by construction. Anything
below or right of N did more harm than not attacking.

## 3 · Three controls

**Null 1 — the seed floor:** edit the clean image twice with different seeds; nothing is
protected, so the difference is generator variance.
**Null 2 — matched random noise:** random noise at the shield's exact L2, so any difference is
structure rather than size.

SSIM against the seed-0 clean edit; **lower = more disturbed**:

| image | seed floor | **real shield** | random, same L2 |
|---|---|---|---|
| 1233476865_1 | **0.472** | 0.584 | 0.737 |
| 1525918600_1 | **0.415** | 0.610 | 0.921 |

Read each row twice:

1. **shield vs random** — 0.584 < 0.737, 0.610 < 0.921. The shield beats matched noise, so it is
   genuinely structured: a positive finding about PhotoGuard.
2. **shield vs seed floor** — 0.584 > 0.472, 0.610 > 0.415. But a seed change disturbs the edit
   *more* than the shield does, so `R_pipe`'s denominator is mostly generator variance.

CLIPScore agrees: the seed gap is 2.19 points and neither image clears it — on one it is
*negative*, the protected edit matching the prompt better than the clean one.

**Control 3 — we doubled the shield.** At `pg_eps = 32`, protect stage genuinely re-run, the
perturbation was unchanged: L2 2645.8 → 2641.6 and 1860.4 → 1841.1, damage 0.73 → 0.72 levels.
At `pg_iters=40, pg_step_size=1` the L2 ball is never reached, so **`pg_eps` never binds — the
documented strength knob is inert on this code path.**

**⭐ The finding.** `pg_metric.py`'s SSIM is IMPRESS's *own* evaluation metric, and at the paper's
own settings **it cannot detect PhotoGuard**: re-run noise exceeds the shield's signal, and the
documented way to raise that signal does nothing. Three controls the paper never ran.

Fidelity survives all of it, because it never invokes the editor — which is why it reproduces to
four decimals.

---

## 4 · The challenge is open — the Tyro Wash Test

**Build a shield we can't wash off.** We give you 10 clean 512×512 faces and their masks. Either
tune the PhotoGuard protector we ship — one cell, one parameter — or replace `protect()` with
your own. Send back 10 PNGs using our filenames. You never have to say how you made them: our
purifier never inspects the perturbation.

- 📦 `tyro_wash_test_trackA.zip` — images, masks, `check_submission.py`, `seed_floor_10.json`
- 📓 starter notebook: **[LINK]**

| axis | measures | better |
|---|---|---|
| `R_pipe` | how much of the edit our wash restores | lower |
| `LPIPS(protected, clean)` | how much your shield damages the photo | lower |

**Both published, as one scatter plot** — because one axis alone has a degenerate winner:
perturb until the photo is noise and nothing can be washed off it, but nothing can be edited
either. That entry lands top-right, in public.

**Ranking budget: LPIPS ≤ 0.10**, the allowance our own purifier gets (`pur_eps = 0.1`). Our
reference entry sits at **0.0665**. Over-budget entries are plotted, not ranked.

**When we report a number.** We first published a gate of SSIM ≤ 0.85, then measured the seed
floor on all ten images: it runs **0.285–0.707**, so 0.85 would have passed everything — our own
shield included. Corrected:

> We report `R_pipe` for an image only when SSIM(edited-protected, edited-clean) is **below that
> image's seed floor** (`seed_floor_10.json`). Otherwise: **"shield did not engage"**, plus the
> number we measured.

Floors vary 2.5×, so the images are not equally hard — the editor's doing, not ours. **We rank on
how many of the ten engaged**, per image, never a single mean.

**Every outcome gets published, including ours losing. Send by 15 September**; results in our
18 September post.

---

## 5 · Limitations

1. **n = 2, and `R_pipe` is unstable for the reason the defence exists.** Per-image `R_pipe`
   disagrees in *sign* (−10.5% and +18.8% on arm A); fp16 kernel choice alone shifts the
   protected image 0.1 of a grey level, which the editor amplifies ~100× into ~11 levels of
   output. Read orderings, never magnitudes.
2. **No stronger shield was tested — this knob cannot produce one.** The lever that does bind
   (`pg_step_size`, or the attack type) is M3.
3. **The mask is an input, not a discovery.** True of any inpainting attacker, but it does not
   transfer to whole-image protections such as Glaze.
4. **A frequency-targeted filter failed.** Butterworth cutoffs f = 0.40–0.95: the perturbation is
   quieter than the photo's own fine detail, so every cutoff cost more detail than shield. It is
   what pointed us at the mask.

## Code

Kaggle, GPU T4 ×2, Internet ON, top to bottom. Each notebook has a smoke mode: the full pipeline
at reduced iterations, so a broken path fails in four minutes, not forty.

- `Dark_Tyro_M2.ipynb` — the attack. M1 plus four lines; the diff *is* the contribution.
- `challenge/Tyro_Wash_Test_STARTER.ipynb` — the defence starter. One function to edit.
- `Tyro_M2_diagnostics.ipynb` — the three controls above.

**Provenance:** the IMPRESS algorithm is unmodified. The eleven repairs, the harness, the
four-line mask restriction and the controls are ours.
