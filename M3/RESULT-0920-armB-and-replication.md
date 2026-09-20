# 🏁 RESULT — arm B, and the replication that reframes the gate

**20 Sep 2026.** Closes the last GPU item on the IMPRESS/Tyro workstream.
Sources: `REPORT_run_0920_0600/` (arm B, `impress-m3-0920_armB.ipynb`),
`REPORT_run_0919_2319/` (N·A·C + six-row shield sweep, `impress-m3-0920_r1.ipynb`),
`REPORT_run_0919_0406/` (first n=10 gate run).
Everything below is **measured**. Nothing is extrapolated except where labelled.

---

## 1 · Arm B — the paper's own budget buys nothing

`pur_iters=1000`, shield fixed at (40, 2), eps 16, step 1, ten pinned images.

| arm | pur_iters | R_pipe (mean) | LPIPS(purified, clean) |
|---|---:|---:|---:|
| N_no_wash | — | 0.00 | 0.0342 |
| A_impress_100 | 100 | +0.58 | 0.1846 |
| **B_impress_1000** | **1000** | **−1.60** | **0.1435** |
| C_tyro_masked | 100 (masked) | +1.58 | 0.0596 |

**IMPRESS at ten times the compute is not stronger than IMPRESS at a tenth of it.** The
gap A→B is 2.2 pp, inside the measured ±2–4 pp `R_pipe` noise band (5 Sep), so the claim
that holds is *"10x compute, no measurable gain"* — **not** *"1000 iterations is worse"*.

This is the control the plan asked for, and it does its job: the M1/M2 baseline can no
longer be dismissed as a crippled version of IMPRESS run at 1/10 budget.

### What is safe to quote, and what is not
- **Not safe: any `R_pipe` comparison.** All four arms have **0 engaged images**. By the
  gate's own rule, `R_pipe` has no meaning when the shield never cleared the seed floor.
- **Safe: LPIPS.** Fidelity noise is measured at zero (5 Sep). **C costs 0.0596 against
  B's 0.1435 and A's 0.1846** — the masked wash does under half the perceptual damage of
  either IMPRESS setting, at A's compute. That is the strongest honest statement the
  four-arm table supports, and it is on the axis where the measurement is clean.

### ⚠️ B is not matched to N·A·C
B ran in its own session with its own protect stage: `ssim_adv` **0.5313** against
**0.5203** for N·A·C. The four arms above span two runs. Either state that wherever the
table appears, or re-run B inside the clean pass. See §2 for why the size of that
mismatch is now a known quantity rather than a worry.

### Cost, measured
| stage | 100 iters | 1000 iters |
|---|---:|---:|
| protect (fresh, 10 images) | 33.6 min | 33.7 min |
| purify | 14.7 min | **139.4 min** |
| generate | 4.9 min | 5.0 min |
| metric | 1.4 min | 1.5 min |
| **arm total** | 21.5 min* | **179.8 min** |

\* with protect resumed (0.3 min). Wall clock for the B session on a Kaggle T4:
**3 h 17 min**, of which ~17 min is setup (clone, pip, dataset, SD weights).
Purification scales **9.5x for 10x the iterations** — near-linear, no surprises.

The `M3-IMPRESS-LOCKED.md` §7 estimate of ~90 min was from an uncalibrated cost model in
cell 4. The real figure is **2 h 20 min for the wash alone**. Correct that line.

---

## 2 · ⭐ Three runs, one setting — the shield cannot reproduce its own engagement

Three independent runs at **identical settings on identical hardware** (eps 16, step 1,
Kaggle T4, seed 0). `ssim_adv` per image:

| image | 0406 | 2319 | 0600 | range | floor | verdicts |
|---|---:|---:|---:|---:|---:|---|
| 1233476865 | 0.5018 | 0.5534 | 0.5718 | **0.0700** | 0.4721 | blind · blind · blind |
| 181707205 | 0.6453 | 0.5915 | 0.6258 | 0.0538 | 0.5620 | blind · blind · blind |
| 2167874246 | 0.4346 | 0.4118 | 0.4600 | 0.0482 | 0.2849 | blind · blind · blind |
| 2061993362 | 0.4656 | 0.5047 | 0.5004 | 0.0391 | 0.4360 | blind · blind · blind |
| 1525918600 | 0.6372 | 0.6373 | 0.6710 | 0.0338 | 0.4149 | blind · blind · blind |
| **1961032923** | 0.6966 | 0.7160 | 0.7029 | 0.0194 | 0.7067 | **ENGAGED · indet · indet** |
| 221629697 | 0.5178 | 0.5241 | 0.5050 | 0.0191 | 0.3159 | blind · blind · blind |
| 2099073485 | 0.5401 | 0.5335 | 0.5525 | 0.0190 | 0.3757 | blind · blind · blind |
| 2139626906 | 0.3837 | 0.3808 | 0.3660 | 0.0177 | 0.3165 | blind · blind · blind |
| 178046512 | 0.5370 | 0.5477 | 0.5496 | 0.0126 | 0.4800 | blind · blind · blind |

**Median range 0.0266 · max 0.0700 · median per-image SD 0.0147.**

`1961032923` is the **only image that has ever engaged in this project**, and it engages
in **one run out of three**. The 1/10 headline was never a measurement; it was a coin.

### Where the variance comes from — isolated by direct comparison
Comparing the archived PNGs of `run_0919_0406` against `run_0919_2319`:

- **`edit_clean` is byte-identical on all ten images.** The editor is fully deterministic
  at a fixed seed. It contributes nothing.
- **`protected` differs on all ten images**, by ~0.3 grey levels mean, **L2 ≈ 850**.

The shield's own perturbation at this setting is L2 **2 600–6 400**. So roughly
**a quarter to a third of what PhotoGuard produces is run-to-run noise from its own
optimiser**, and that noise propagates through a deterministic editor into `ssim_adv`
swings of up to 0.07.

> The defence is not a fixed object being measured by a noisy test. It is a noisy object,
> and the noise is a third of its own size.

### Consequence for `DRIFT`
`DRIFT = 0.010` was calibrated from **cross-platform** spread (~0.004 each side, Colab vs
Kaggle). The **same-platform, same-setting** spread is ~0.027 — about 2.7x wider. The
band was measuring the wrong thing.

**Widening the band costs nothing.** Re-scored at `DRIFT = 0.027`:

| setting | at 0.010 | at 0.027 |
|---|---|---|
| eps 64, step 4 | 2 engaged | **2 engaged**, 4 indeterminate |
| eps 256, step 4 | 1 engaged, 4 indet | **1 engaged**, 5 indeterminate |

Engagement never exceeds 2/10 either way. So the honest band is free, and it upgrades the
claim from *"the shield barely engages"* to:

> **The shield cannot reproduce its own engagement between two identical runs.** The
> evaluation's sensitivity floor does not merely sit above the defence's usable range — it
> sits above the defence's own run-to-run variance.

Same rule, fourth application: *a difference smaller than the measurement's own spread is
not a difference.* Applied to `R_pipe` (±2–4 pp), to the step sweep (17x drift), to the
gate (three-state), and now to the shield itself.

**Floors are still not re-measured.** They are published with the challenge and the
scoring runbook depends on them. Widening the uncertainty band is the honest response;
moving a public artefact is not.

---

## 3 · Notebook state — three fixes before the clean pass

Both `impress-m3-0920_r1.ipynb` and `impress-m3-0920_armB.ipynb` ran clean: no failed
arms, no NaNs, all cells executed, only torchvision `pretrained` deprecation warnings.
Three things to fix, all small:

1. **`SHIELD_GRID` breaks cell 11 when cell 10 is skipped.** The arm-B notebook commented
   out cell 10 (correctly — no sweep needed) and cell 11 died with
   `NameError: SHIELD_GRID`. A traceback in the submitted notebook costs Colab-hygiene
   marks. **Fix:** move `SHIELD_GRID` into cell 4, or guard cell 11 with
   `if 'SHIELD_GRID' in globals()`.
2. **Cell 10 restores `P['pg_eps']`/`P['pg_step_size']` but leaves `PG` at eps 256,
   step 4.** Re-run cell 7 after cell 10 in the same kernel and all four arms run at
   eps 256 while every label says 16. **Fix:** rebuild `PG` in the same restore line.
3. **Cell 4's cost model is wrong.** `_cost = {100: 1.0, 1000: 10.0}` at 0.6–1.1 min/unit
   predicted 88 min for arm B; it took 180. Recalibrate from the measured table in §1, or
   delete the estimate rather than print a number that is 2x out.

Minor, no action needed: `fsim` is `0.0` with SD `0.0` in every `scores.json`.
`pg_metric`'s FSIM is dead upstream. Harmless — `R_pipe` is SSIM-based — but do not quote it.

---

## 4 · The October clean pass — budget, and the trim

Measured cost of one top-to-bottom Colab run, from §1's stage table:

| content | cost |
|---|---:|
| N + A + C (one shared protect stage) | 83 min |
| arm B | 146 min |
| shield sweep, 6 rows | 208 min |
| shield sweep, 3 rows — (16,1), (64,4), (256,4) | 87 min |
| setup | ~17 min |

- everything, 6-row sweep: **≈ 7.6 h**
- everything, 3-row sweep: **≈ 5.6 h**
- **N·A·C + 3-row sweep, B cited from `run_0920_0600`: ≈ 3.2 h**

Free Colab will not hold 5.6 h, let alone 7.6 h. There is no booking and the free tier
idles out.

### Recommended: the 3.2 h version
Two trims, both already sanctioned by `M3-IMPRESS-LOCKED.md`:

- **Drop the step-size rows** (16,2)/(16,4)/(16,8) from the executed path. §3 declares
  `pg_step_size` settled; §2 asks for three points to make a curve, and (16,1)/(64,4)/(256,4)
  are exactly those three. The dropped rows move to the appendix with their Kaggle outputs
  intact, per §6.
- **Cite arm B from `run_0920_0600`** rather than re-running it. §7's reason for running B
  in the clean pass was that citing it from a *2-image* run would be the table's one soft
  spot. That soft spot is gone: B is n=10. The remaining mismatch — B's own protect
  realisation — is no longer an unknown, it is the quantity measured in §2, and stating it
  is stronger than hiding it.

That is one Colab session, comfortably inside the free tier, and it matches the standing
rule: ship the smallest notebook that carries the claim.

### If arm B must be inside the submitted run
Split across two Colab sessions sharing one `RUN_TAG` (the notebook already supports this:
Drive-mounted `ARCHIVE`, per-arm zips, manual `RUN_TAG` resume). Session 1 = N·A·C +
3-row sweep (~3.2 h); session 2 = B alone (~2.6 h). Outputs from two sessions in one
Colab notebook is normal and defensible; a 5.6 h run that drops at hour 4 is not.

One month of Colab Pro would collapse the whole thing to ~2 h with background execution.
Noted as an option, not a recommendation.

---

## 5 · What ships
- **The claim (unchanged, now stronger):** at n=10, across floors spanning 2.5x,
  PhotoGuard as implemented in IMPRESS does not clear its own evaluation metric's noise
  floor at any setting inside the fidelity budget its own users would accept — and its
  engagement is not reproducible between identical runs.
- **The control:** IMPRESS at its published 1000-iteration budget, n=10, no measurable
  gain over 100 iterations, at 9.5x the compute.
- **The contribution:** the masked wash at A's compute, under half the perceptual cost of
  either IMPRESS setting. Reported on the fidelity axis, where the measurement is clean.
- **The figures:** engagement vs setting, cost vs setting, per-image spread, face grid.
- **No new GPU** beyond the clean pass.
