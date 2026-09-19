# `pg_step_size` sweep — 19 Sep 2026

Protect + N arm only, ten pinned images, `attack_type=l2`, `pg_eps=16`, shield `(40, 2)`.
Target was **≥ 5 of 10 engaged**, i.e. a drop in `ssim_adv` of ≥ 0.067.

## Result: the L2 branch does not clear at any swept setting

| `pg_step_size` | engaged | median `ssim_adv` | median drop vs step 1 | drop range |
|---:|---:|---:|---:|---|
| 1 | 1/10 | 0.5274 | — | — |
| 2 | **1/10** | 0.5147 | +0.0052 | −0.025 … +0.081 |
| 4 | **1/10** | 0.5066 | +0.0166 | −0.066 … +0.119 |
| 8 | **1/10** | 0.4882 | −0.0019 | −0.047 … +0.145 |

**Nothing reached +0.067. Nothing reached even +0.030, the discard threshold.** And the engaged
image is `1961032923` at *every* setting — the same highest-floor, easiest-gate image identified in
the n=10 run. **No image ever newly engaged.**

## ⭐ The knob moves the perturbation but not the outcome
This is not a null result from a dead knob, which is what `pg_eps` was.

- Within-image spread of `ssim_adv` across the four settings: **0.0594 mean**, against a measured
  same-setting run-to-run drift of **0.0035**. So step size changes the shield by ~17x the noise.
- But **0 of 10 images are monotonic** in step size, and `corr(log2 step, ssim_adv)` has a median of
  only **−0.109** across images.
- `221629697` falls 0.518 → 0.372 (a large, useful move). `1525918600` *rises* 0.637 → 0.664 over
  the same range. Same knob, opposite directions, same image set.

> Turning the knob is like re-shuffling a deck rather than stacking it. The cards land somewhere
> different every time; none of the arrangements is better.

**Generalisable: a knob that changes the output without changing the outcome is a knob that
re-randomises rather than one that steers. Distinguish the two before sweeping further —
"it did something" is not "it did the thing".**

## ⚠️ The `pg_eps` gate has re-opened, and this must be checked before `linf`
[[fit5230-eps-knob-inert]] closed `pg_eps` on 9 Sep: 16 vs 32 produced the same perturbation to
within 1%. **The stated reason was that at `pg_iters=40, pg_step_size=1` the optimiser never travels
far enough to reach the L2 ball.** This sweep has removed exactly that condition.

So there are two live explanations for the flat result:

| | mechanism | correct next move |
|---|---|---|
| **A · saturation** | at step ≥ 2 the optimiser now *does* reach the `pg_eps=16` ball and is clipped, so every setting spends an identical budget in a different direction | raise **`pg_eps`** (32, 64) at the best step size |
| **B · magnitude is irrelevant** | the perturbation genuinely grows with step size and `ssim_adv` still will not fall | **`attack_type='linf'`** |

`pg_eps` and `pg_step_size` are not independent, and the earlier finding was conditional on a value
of the other. **Lesson: when closing a gate, record the conditions it was closed under — a later
change to one of them re-opens it.**

**Cell 7d decides between A and B by measuring ‖protected − clean‖₂ per image directly from the
archived PNGs. Zero GPU, seconds.** If L2 is flat across step 2/4/8 → A. If it grows → B.

## Standing either way
No `R_pipe` is quotable from any of this, and none was claimed — these are all N arms, 0.00 by
construction. What has been established, at n=10 across a 2.5x range of editor stability:

**The shield produced by this implementation's L2 branch does not engage the metric it is evaluated
with, at `pg_step_size` ∈ {1, 2, 4, 8}.** That is a measured negative at four stated settings, and
it is a finding about the reference implementation, not about our wash.

---

# Addendum — perturbation-size diagnostic (cell 7d), same day, zero GPU

Measured ‖protected − clean512‖ directly from the archived PNGs, all four settings, ten images.

## 1 · The optimiser converges — it is not being clipped

| | median across images |
|---|---:|
| L2 growth, step 1 → step 8 | **+15.8%** |
| L2 growth, **step 4 → step 8** | **+0.4%** |

By step 4 the perturbation has stopped growing. **But each image converges to its own ceiling, and
those ceilings span 2.8x (2386 … 6565).** A single global `pg_eps` L2 ball would clip every image to
the *same* norm. It does not — and no plausible reading of `pg_eps = 16` (4080 levels on a [0,1]
data scale, 2040 on [−1,1]) sits at or above the observed values either.

**So hypothesis A (saturation at the eps ball) is refuted.** The optimiser is not running out of
budget; it is running out of gradient. It has converged to a per-image local optimum of PhotoGuard's
own objective, and that optimum does not disturb the editor enough to clear the seed floor.

**This is a stronger statement than "the sweep failed".** It says the L2 branch is not
under-powered — it is *finished*, and finishing is not enough.

## 2 · ⭐ Bigger steps cost fidelity and buy nothing

| | step 1 | step 8 |
|---|---:|---:|
| L∞ (worst pixel), median | 61 levels | **102 levels** (+68%) |
| L∞, worst image | 62 | **203 levels** |
| mean absolute change | 0.818 | 1.124 levels |
| images engaged | 1/10 | 1/10 |

Total energy is flat from step 4 onward while the **worst pixel nearly doubles** — 203 levels is a
blown-out pixel on a 0–255 scale. The same budget is being spent in fewer, louder places.

*Turning the step size up does not push harder. It pushes clumsier: the same shove, delivered as
one jab instead of a lean.*

**This is our own two-axis rule turned on the defence we are attacking:** the shield's cost axis
rises steadily while its effect axis is flat. The same argument we used at M1 to reject our own
purifier — *"a number that only goes up is not an improvement"* — rules out large `pg_step_size`
here, and it does so on fidelity grounds *before* the engagement question is even reached.

## 3 · Verdict and the one probe before `linf`
Evidence says **do not sweep `pg_eps`** — the budget was never binding. But *"did you try a bigger
budget?"* is the first question a reader will ask, so it is worth closing with a measurement rather
than an inference.

**Cell 7e: one run at `pg_eps = 64, pg_step_size = 4`.** Costs the same as one sweep setting.
- L2 flat at the step-4 ceiling → the budget was never binding → **`pg_eps` closed at any step
  size** → go to `linf`.
- L2 rises → the ball *was* binding, the 9 Sep result was conditional, sweep `pg_eps` instead.

**Method note worth keeping: when a sweep comes back flat, measure the thing you were sweeping
before choosing what to sweep next.** Three settings of `pg_step_size` told us the outcome did not
move. One zero-GPU read of the archived PNGs told us *why*, and changed the next experiment.
