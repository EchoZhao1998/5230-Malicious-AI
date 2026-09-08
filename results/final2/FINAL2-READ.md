# `final2` — reading the Kaggle T4 x2 run
*23 Aug 2026 · supersedes nothing, but it changes what we may claim*

Source: `M1/final2/tyro-m1-final-2.ipynb`, `params.json` identical to `PARAMS` in
`Dark_Tyro_M1_FINAL.ipynb`. 2 images, 2 configurations, 35.9 min wall clock, Tesla T4.

## The numbers

```
config  units  metric      adv      pur   recovery
 40:2      80   psnr   14.3947  17.1470   +2.7523
 40:2      80   ssim    0.5710   0.6063   +0.0353
 40:2      80   vifp    0.2017   0.2215   +0.0198
200:2     400   psnr   13.6939  15.1970   +1.5030
200:2     400   ssim    0.5330   0.5612   +0.0282
200:2     400   vifp    0.1582   0.1747   +0.0165
```

`R_pipe = (pur − adv)/(1 − adv)` on SSIM: **40:2 = +8.23 %**, **200:2 = +6.04 %**.
Three-metric sign test: **both configurations all-positive** — unlike every earlier run.

## Three runs of the same parameters

| run | hardware | 40:2 | 200:2 |
|---|---|---|---|
| first | earlier GPU | +10.8 % | +2.7 % (signs disagree) |
| 22 Aug | Kaggle T4 | +5.2 % | −1.2 % (signs disagree) |
| **final2** | **Kaggle T4 x2** | **+8.23 %** | **+6.04 %** (signs agree) |

## What may and may not be said

- ✅ **`40:2` replicates.** Positive in all three runs, in the range **+5 % to +11 %**.
  Quote the range, never a single figure.
- ❌ **`200:2` is not settled.** It has now been +2.7, −1.2 and +6.04. The sign flips
  between runs. Sign agreement *within* one run answers "did something move in this run",
  not "does it move again next run".
- ⚠️ **The spread is itself the finding.** Same seed, same parameters, different GPU/run →
  about ±5 percentage points. All four IMPRESS scripts call `np.random.seed`,
  `torch.manual_seed` and `torch.cuda.manual_seed`, so the RNG stream *is* fixed. What is
  not fixed is fp16 kernel selection and accumulation order, which differ across GPU model
  and torch build. **At n = 2 images, run-to-run noise is the same size as the effect.**

## Consequence for M2

The cheapest way to make any recovery claim survive is **more faces, not more iterations**:
`N_IMAGES = 5` at the same two configurations is roughly 80 min on a T4. Everything else on
the M2 list (the `pg_eps` sweep, `pur_eps`/`pur_iters`, the VAE round-trip floor) is
uninterpretable until the error bar is smaller than the effect.

Nothing here needs to change before **28 Aug** — M1's rubric has no results row.
