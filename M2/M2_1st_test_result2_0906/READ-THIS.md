# Second smoke run — 5 Sep · an accidental REPLICATION, and the most useful thing we have

Identical settings to run 1 (`pg_iters=10`, `pur_iters=10`, arms A and C, n=2). Running the
same configuration twice was not the plan, but it measures something no single run can: **how
much of our result is signal and how much is the pipeline's own noise.**

## The two halves behave completely differently

| | run 1 | run 2 | spread |
|---|---|---|---|
| **LPIPS — A** | 0.160 | 0.160 | **0.000** |
| **LPIPS — C** | 0.037 | 0.037 | **0.000** |
| SSIM(purified, clean) — A | 0.7491 | 0.7491 | **0.0000** |
| SSIM(purified, clean) — C | 0.9368 | 0.9368 | **0.0000** |
| **`R_pipe` — A** | −13.8% | −16.0% | **2.2 pp** |
| **`R_pipe` — C** | −4.5% | −2.2% | **2.3 pp** |

**The fidelity axis is exactly reproducible — to three and four decimal places.** That is the
confirmation that it is *geometry*, not chance: mask-restriction removes IMPRESS's damage in a
fixed set of pixels, so no amount of re-running moves it. The M2 fidelity claim is as solid as
it is going to get.

**The `R_pipe` axis moves by 2-4 percentage points between identical runs.**

## Why `R_pipe` is noisy — and it is the same mechanism we are attacking

Comparing the two runs stage by stage:

| stage | run 1 vs run 2 |
|---|---|
| `edit_clean` | **0.000 levels** — byte-identical |
| `protected` | 0.104 levels |
| `purified` | 0.119 levels |
| **`edit_purified`** | **11.9 levels** |

The editor is perfectly deterministic given identical input (`edit_clean` is byte-identical).
The nondeterminism enters at the *protect* stage — fp16 kernel selection and accumulation order
are not fixed across runs — and it is tiny: **0.1 of a grey level.**

**That 0.1-level difference in the input becomes an 11-level difference in the output. A ~100x
amplification.**

> That amplification *is* PhotoGuard. The whole defence rests on the fact that a diffusion
> pipeline is wildly sensitive to imperceptible input changes — that is how a 1-level
> perturbation ruins an edit. We have just watched the same lever move by accident, from the
> inside. **Our metric is noisy for exactly the reason the attack target exists.**

## What survives the noise

| | run 1 | run 2 |
|---|---|---|
| **A → C gap in `R_pipe`** | **9.3 pp** | **13.8 pp** |

The gap is **3-6x larger than the noise**, and the same sign both times. So *"C is better than
A"* replicates even at settings where neither arm's absolute number means anything. The
**ordering** is robust; the **magnitudes** are not.

## What this changes

1. **We now have a measured error bar: ±2-4 pp on `R_pipe` at n = 2.** `HANDOVER.md` previously
   estimated "about ±5 pp" from a single pair of runs on different hardware. It is now measured
   on identical hardware and identical settings. **Quote this, and never quote an `R_pipe`
   difference smaller than it.**
2. **Report `R_pipe` as a range, not a point**, or raise n. Ten faces would roughly halve it.
3. **The fidelity result needs no error bar at all** — say so, and say why. Being able to
   explain which of your two numbers is noisy and which is not is worth more than either number.

## Still unanswered — and unchanged

Both arms remain **negative**: at ten iterations, washing is worse than leaving the shield on.
That is expected (M1 got **+5.2%** at `pur_iters=100`), but it is why the next run must be the
real one: **`SMOKE = False`, four arms including `N_no_wash`.** Without N there is no way to
tell whether C is winning by attacking well or merely by doing less harm.
