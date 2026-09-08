# Reading the Kaggle sweep — what these three runs actually support
*Dark.Tyro · 22 Aug 2026 · source: Echo's FigJam log of the Kaggle output (40:2, 40:10, 200:2)*

Read this before touching Ed post §4. **The numbers do not say what the current draft says
they say**, and the honest version is a better M1 anyway.

---

## 1 · The numbers, verified

Every recovery figure in your FigJam reproduces exactly from the adv/pur pairs — the
transcription is clean, including the two I had to squint at (`40:10` vifp adv = 0.2176,
`200:2` pur ssim = 0.5482).

| config | units | | adv | pur | recovery |
|---|---|---|---|---|---|
| **40:2** | 80 | psnr | 14.7405 | 16.9109 | **+2.1704** |
| | | ssim | 0.5494 | 0.5979 | **+0.0485** |
| | | vifp | 0.1989 | 0.2095 | **+0.0106** |
| **40:10** | 400 | psnr | 15.7574 | 15.8824 | +0.1250 |
| | | ssim | 0.6138 | 0.6087 | −0.0051 |
| | | vifp | 0.2176 | 0.2202 | +0.0026 |
| **200:2** | 400 | psnr | 14.6248 | 15.0376 | +0.4128 |
| | | ssim | 0.5357 | 0.5482 | +0.0125 |
| | | vifp | 0.1787 | 0.1776 | −0.0011 |

Your `R = (pur − adv)/(1 − adv)` is a **good** metric and I have kept it. Because
`pg_metric`'s SSIM is measured against the *edited clean* image, `1.0` means "the pipeline
behaved exactly as if the photo had never been protected" — so `1 − adv` is a principled
denominator that needs no third measurement. It is now in the notebook as **`R_pipe`**.

| config | units | R_pipe |
|---|---|---|
| 40:2 | 80 | **+10.8 %** |
| 40:10 | 400 | −1.3 % |
| 200:2 | 400 | +2.7 % |

> ⚠️ **Name it `R_pipe`, not `R`.** Ed post §4 defines `R` as a *CLIPScore* ratio asking "does
> the output match the prompt". Yours is an *SSIM* ratio asking "did the pipeline behave
> normally". Both are legitimate; they are different questions and you have not run the CLIP
> one yet. Publishing the SSIM number under the CLIP definition is the same claim–evidence
> mismatch we have been guarding against all week — and it is the third time this project has
> nearly had two different things called by one name.

---

## 2 · What the data supports

**With n = 2 you cannot read one metric. You can read whether three metrics agree.**

PSNR, SSIM and VIF are three different instruments pointed at the same pair of pictures. If
all three agree on the *sign* of the recovery, something real moved. If they disagree, the
recovery is inside the noise.

| config | psnr | ssim | vifp | verdict |
|---|---|---|---|---|
| **40:2** | + | + | + | **all three agree — real recovery** |
| 40:10 | + | − | + | disagree — **indistinguishable from zero** |
| 200:2 | + | + | − | disagree — **indistinguishable from zero** |

So, stated at exactly the strength the data carries:

> **At the weakest shield setting (80 grad-units) IMPRESS recovers about 11% of the damage.
> At 400 grad-units — spent either way — recovery is indistinguishable from zero.**

**The equal-compute comparison is the interesting part, and it did deliver an answer.** You
asked whether it is better to take more steps (`200:2`) or estimate each step better
(`40:10`) at a fixed 400-unit budget. The answer is **neither** — both collapse to zero. Once
the shield is past the threshold, how it spent its budget stops mattering. Two independent
parameter allocations agreeing on ≈ 0 is a replication, and it is far more convincing than
either point alone.

## 3 · What the data does NOT support

- ❌ **"The shield worked, and then we stripped it."** Ed post §4 says this. It is not true at
  400 units, and only ~11%-true at 80.
- ❌ **Any ranking between 40:10 and 200:2.** Their `adv` SSIMs (0.6138 vs 0.5357) are not even
  monotone in shield strength. At n = 2 that ordering is noise; do not build a sentence on it.
- ❌ **The `pg_iters` saturation prediction, confirmed or refuted.** 40:10 and 200:2 both give
  ≈ 0, which is *consistent* with saturation but also consistent with "both shields simply
  won". This experiment cannot separate those. `pg_eps` is still untested.
- ⚠️ **The three-panel visual story.** In your FigJam the edited-protected images look far
  less broken than TRIAL-LOG's "crazed-skin floating head" description. Worth a second look —
  if the visual gap is smaller than we remembered, the figure needs a caption that matches
  what a marker will actually see.

---

## 4 · The question this all turns on

Recovery near zero has **two completely different explanations**, and everything downstream
depends on which one it is:

| | what it means | what M2 looks like |
|---|---|---|
| **(a) purification barely moved the pixels** | our attack did not really run. `pur_eps=0.1` and `pur_iters=100` were too tight a leash | tune the purifier — this is a configuration finding, not a result about IMPRESS |
| **(b) purification moved, and the shield survived** | the attack ran and lost | a real finding about PhotoGuard's *diffusion* attack, and the most interesting thing in the project |

> Recovery near zero is a patient who did not get better. Before concluding the drug does not
> work, check they swallowed it.

**`pg_metric.py` cannot answer this**, because it only ever looks at the *edited* images. The
answer is in the *input* images, which you already have.

### The decisive test — no GPU, ~30 seconds

**Cell A0.5, now in `Dark_Tyro_M1.ipynb`.** It compares the purified input against the
protected input and reports a **movement ratio**: how far purification pushed the image, as a
fraction of how far the shield had pushed it.

- **ratio < 0.15** → the medicine stayed in the bottle. Explanation (a). The cell says so and
  tells you to raise `pur_eps` to 0.3 and `pur_iters` to 300 on **one** configuration before
  concluding anything.
- **ratio ≈ 1, and moving toward the original photo** → explanation (b). The attack ran and
  lost, and that is a publishable result.
- **ratio ≈ 1, moving away from the original** → the purifier is damaging the photo without
  undoing the shield. Check `pur_alpha`, and check the fix-7 guard actually wiped.

Run it first. It costs nothing and it decides how §4 should be written.

### Second test, if you have ten GPU-minutes

VAE round-trip inconsistency for clean / protected / purified inputs. IMPRESS's entire premise
is that protected images are *less self-consistent* under a VAE round-trip — you measured
0.0071 clean vs 0.0204 protected earlier, but that was against PhotoGuard's **encoder**
attack. These runs used the **diffusion** attack, which optimises through the whole denoising
process rather than the VAE alone. **If the gap has collapsed, IMPRESS's premise does not hold
for this attack** — and that is a genuinely strong M2/M4 finding, not a setback.

---

## 5 · What to write in the Ed post

M1's rubric has rows for baseline justification, problem statement, challenge design and
setup. **There is no row for "your attack works."** A rigorous negative result with a
diagnosis scores better than a confident positive one that a marker can poke.

The line to write:

> We reproduced the baseline end-to-end and measured it. Against PhotoGuard's diffusion
> attack at the reference purification settings, IMPRESS recovers about 11% of the shield's
> damage at the weakest protection setting and nothing measurable once protection reaches 400
> gradient-units — with two independent parameter allocations agreeing at that budget.
> Whether that is a limit of the purifier's configuration or of its premise is the question
> M2 answers, and we have the experiment that separates them.

That is honest, it is specific, and it makes the reader want the next instalment — which is
the actual job of an M1 post.

**Consequence for Tier 2.** The challenge currently advertises a cascade whose diffusion-
purification stage recovers ≈ 0. Do not publish a bar we cannot clear. Either scope Tier 2 to
the cheap purifiers we can evidence (JPEG, blur, rescale, the low-pass filter), or state the
open question and invite Light teams to help close it. Do not quote a purifier number until
A0.5 tells you which world we are in.
