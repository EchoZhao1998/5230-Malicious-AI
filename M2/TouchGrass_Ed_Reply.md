# Ed reply — post on Light.TouchGrass M2 thread
Thread: https://edstem.org/au/courses/37864/discussion/3578747
From: Echo Zhao (Dark.Tyro) · drafted 14 Sep 2026
**Paste everything below the line. No GPU needed. ~700 words.**

---

Really strong post — the pre-declared primary comparison, the held-out split and §6 are more care than most M2s are showing, and reporting the gate failure against yourselves is the part we respect most.

We are Dark.Tyro (Theme 2, attacking PhotoGuard). We did not attempt a breach. We looked at a different question, because it is the question we got wrong in our own project first: **do your numbers show that the new mechanisms produced the gain, or that more correction was applied?**

Three things from your own published results.

**1. Safety tracks compute across all five defended configurations.** Plain SD sits at 0.929; the column is how much of that each config removes.

| config | inappropriate prompts blocked vs SD | s/image |
|---|---:|---:|
| SLD-STRONG | 0.250 | 7.06 |
| M2-FULL | 0.286 | 7.85 |
| M2-ADAPT | 0.358 | 8.81 |
| M2-ROUTE | 0.465 | 8.79 |
| M2-GUARD | 0.536 | 10.48 |

Compute order and safety order agree on four of five positions, and the pair that swaps differs by 0.02 s. Pearson r = 0.94 over the five. Benign LPIPS moves with it too: 0.3740 → 0.3917 from STRONG to GUARD, while M2-FULL — the least safe of your new configs — has the lowest distortion of the three you report, 0.1981.

Five points prove nothing on their own and we are not claiming they do. The point is which row is missing: **plain SLD at matched compute.** Your M1 notebook already ships WEAK/MEDIUM/STRONG/MAX with the paper's constants, and M2-GUARD is running 1.48× SLD-STRONG's time. An SLD-MAX row would separate "the new mechanisms did this" from "more correction did this", and it costs you one run. Right now that row is the whole difference between a strength result and a mechanism result, and we think you have earned the mechanism result if it is there.

**2. Your gate scores below chance, but the configuration built on it improves.**

§6 gives development AUC 0.429 and top-1 category agreement 0.286. M2-ROUTE depends entirely on that gate and still blocks 13/28 against SLD-STRONG's 19/28. If the gate cannot separate benign from unsafe prompts, that gain is unlikely to be coming from routing to the *correct* category — the simplest remaining explanation is that routing adds correction wherever it points.

**One run settles it: shuffle the gate.** Randomise the category assignment, hold prompts, seeds and everything else fixed, re-run M2-ROUTE. If the number survives a randomised gate, the gate is not the mechanism, and you would know that before building the trained probe you have planned for M3. If it collapses, you have a much stronger claim than the AUC currently lets you make.

**We are happy to run this ourselves and post the result** if you expose the category assignment as an argument in the arena, or point us at the line to patch. Your code is the most extension-friendly in the class and we would rather return a number than an opinion.

**3. Uncertainty is reported on one side only.**

Every safety number has a 95% CI. No image-quality number does. The headline −0.286 is 8 prompts out of 28, and its cost is a single point estimate, 0.3740 → 0.3917, a difference of 0.0177. Paired LPIPS intervals on the same prompts would tell you whether the 4.7% cost — and the claim that M2-FULL distorts benign images least — survives the same test your safety numbers already passed. Given QUICK-preset counts, we would guess at least one of those intervals crosses zero, and it is better for you to find that than for a marker to.

**Why we went looking here.** We made the same mistake and caught it late. Our masked wash scores 2.3 `R_pipe` points above the full-image baseline; we then replicated and found `R_pipe` moves ±2–4 points on its own, so we do not claim that gap. It is why our results table carries a no-wash null and a same-method-ten-times-the-compute arm — anything that costs more has to be separated from more of the same treatment before it can be called a new mechanism. Those are exactly the two controls we are handing back: a matched-compute baseline, and a randomised null.

Our own M2 and the Tyro Wash Test go up tomorrow — your team is the one we would most like to see attempt it, and the same critique applies to us, so please be as blunt with our table as we have been with yours.

— Echo, Dark.Tyro
