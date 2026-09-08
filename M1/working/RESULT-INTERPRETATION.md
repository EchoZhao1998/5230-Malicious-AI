# Reading our M1 result — a walkthrough for Echo and Nissa
*Dark.Tyro · 22 Aug 2026 · written against the executed run `tyro-m1-final`, Kaggle T4*

**Nissa: you can read this cold.** It assumes you know what PhotoGuard and IMPRESS are and
nothing else. Echo: this is also the thing to re-read before the M3 presentation.

---

## 1 · What we actually ran

Two configurations, two faces each, on a Kaggle T4.

| config | what it means | wall clock |
|---|---|---|
| `40:2` | PhotoGuard takes **40 PGD steps**, averaging **2** noisy gradient samples per step | 12.5 min |
| `200:2` | **200 steps**, still 2 samples each — a **5× stronger** protection budget | 38.5 min |

For each one the pipeline does: take a clean photo → let PhotoGuard shield it → let IMPRESS
purify it → run the same AI edit on all three versions → measure.

> **The one thing that makes this an experiment rather than a demo.** `pg_generate.py`
> re-seeds numpy and torch immediately before each of the three generations, with the same
> mask, prompt, guidance and step count. So the random noise the generator starts from is
> byte-identical across clean, protected and purified. **Every visible difference between
> the three panels is caused by the input image alone.** Most teams cannot say that about
> their figure. Say it in the presentation.

---

## 2 · The picture, and what to say about it

`sweep_grid.png`, bottom row (`iters=200`):

| panel | what you see |
|---|---|
| **edited CLEAN** | a boy in a plane seat. Coherent body, hoodie, window behind him. The editor behaving normally. |
| **edited PROTECTED** | **a detached oval face floating over an aerial view of a wing.** No neck, no body. The generator could not read the face, so it painted a scene that has nothing to do with the person. **The shield worked.** |
| **edited PURIFIED** | a boy back in a seat, coherent, with a neck and a grey hood. **The shield was stripped.** |

That is clean → broken → restored, in three pictures, under identical randomness. **It is the
strongest single asset we have** and it is the figure that goes in the Ed post.

The top row (`iters=40`) shows something different and equally worth understanding: the
protected panel is *already fine* — the boy is coherent, wearing headphones. **At 80
gradient-units the shield is too weak to break the edit at all.** There is nothing to strip,
so "purification" has nothing to do.

---

## 3 · The numbers, and the trap inside them

```
config  units  metric      adv       pur    recovery
 40:2      80    psnr   14.5712   17.1335    +2.5623
 40:2      80    ssim    0.5921    0.6131    +0.0210
 40:2      80    vifp    0.2209    0.2268    +0.0059
200:2     400    psnr   13.7992   14.0264    +0.2272
200:2     400    ssim    0.5198    0.5143    -0.0055
200:2     400    vifp    0.1545    0.1666    +0.0120
```

**Vocabulary, because this is where people get lost:**

- **`adv`** — the *edited protected* image compared against the *edited clean* image.
  **Lower means the shield worked better.**
- **`pur`** — the *edited purified* image compared against the same reference.
  **Higher means our attack worked better.**
- **`recovery` = `pur − adv`** — how much of the editing pipeline our attack gave back.

And the single number we derived:

$$R_{\text{pipe}} = \frac{\text{pur} - \text{adv}}{1 - \text{adv}}$$

The denominator is the distance still to go: SSIM `1.0` means "the pipeline behaved exactly
as if the photo had never been protected". So `R_pipe` is *the fraction of the shield's
damage that purification undid*.

| config | `R_pipe` |
|---|---|
| 40:2 | **+5.2 %** |
| 200:2 | **−1.2 %** |

### How to read two images honestly

**Never trust a single metric at n = 2.** What you *can* trust is whether three independent
instruments agree on the **direction**:

| config | psnr | ssim | vifp | |
|---|---|---|---|---|
| 40:2 | + | + | + | **all agree → something real moved** |
| 200:2 | + | − | + | **they disagree → the recovery is inside the noise** |

That is the whole statistical claim, and it is a defensible one. When three different
measurements of the same pair of pictures cannot agree on the sign, the honest answer is
"we measured nothing", **and saying so is a result** — not a failure to get one.

### ⚠️ The trap: the metrics and your eyes disagree, and your eyes are not wrong

Look again. The **figure** says the story is in row 2 (`200:2`) — broken face, then restored.
The **numbers** say `200:2` recovered nothing and `40:2` is the only real movement.

Both are correct, because **they are answering different questions.**

`pg_metric`'s SSIM asks *"is the purified edit pixel-for-pixel similar to the clean edit?"*
The purified image in row 2 shows a boy in a plane seat — coherent, plausible, clearly
restored — but wearing a grey hood rather than a hoodie, framed slightly differently. **A
different plausible edit, not a pixel-copy.** SSIM scores that as a near-total miss.

> **Metaphor.** You ask two chefs to cook the same dish from the same recipe. One produces a
> beautiful plate that is not a millimetre-perfect match to the reference photograph. A ruler
> laid over both photographs reports total failure. The ruler is measuring alignment, and you
> wanted to know about the cooking.

**This is not a flaw we discovered late — it is exactly why we built a second metric.** The
Ed post's §4 item 11, the CLIPScore edit-success rate, asks *"does the output match the
prompt?"* instead of *"is it pixel-aligned?"* Our own figure is now the evidence that the
second question needed asking.

**Say this out loud in M3.** "Our fidelity metric and our own eyes disagreed, we worked out
why, and it justified the metric we added" is a much stronger story than a clean number.

---

## 4 · Is the attack working?

Honestly: **barely, at these settings, and we can say exactly what "barely" means.**

- At the weakest shield (80 units) purification recovers about 5% of the damage — small, but
  all three metrics agree it is real.
- At 400 units it recovers nothing measurable.
- Visually, at 400 units, something clearly *is* restored — which the pixel metric cannot see.

**And we replicated it.** An earlier run on a different GPU gave `R_pipe` = +10.8% for `40:2`
and +2.7% for `200:2`. Different magnitudes, **identical structure**: the weak config shows
three-metric agreement, the strong one does not. That the magnitude moved by 2× across runs
is itself informative — it is the noise level at n = 2, and it is why we do not rank
configurations against each other.

**Where "why" is answered:** `M2_diagnostics.ipynb`, deliberately outside the M1 notebook. The
one measurement that survived scrutiny there: a bare autoencoder round-trip changes an image
by ~4.3 levels, and everything purification did amounts to ~4.75. Purification's whole effect
is about the size of just passing the image through the VAE. **That is the M2 thread.** No
number from it is quoted in M1.

---

## 5 · Questions you will be asked, and the answers

**"Your attack barely works. Isn't that a failure?"**
> M1 is assessed on baseline justification, problem statement, challenge design and getting a
> 2023 codebase running in 2026. We did all four. Where the published method stops working is
> a finding, and we have the measurement plus a diagnosis plan.

**"Only two images?"**
> Two is the minimum for `pg_metric` to report a real standard deviation instead of `nan`. We
> therefore make no distributional claim and do not rank the two configurations. M2 goes to
> five or more.

**"Doesn't the weaker shield recovering more contradict your theory?"**
> No, and it is the expected shape. At 80 units the shield barely blocks the edit, so a small
> absolute recovery is a large fraction of a small quantity. At 400 units the shield holds.
> The interesting question — whether that is `pg_iters` saturating or simply a stronger
> shield winning — this experiment **cannot** separate, and we do not claim it does.

**"Why didn't you run the fourth grid cell?"**
> `(200, 10)` exhausts 16 GB. We omitted it rather than halve `diff_steps` for one point,
> because a grid where one point used a different attack is not a grid.

**"Which SSIM is that?"**
> There are two in this project and we always say which. `pg_metric`'s compares *edited*
> against *edited clean* — "did the pipeline behave normally". The other compares a purified
> *input* against the *original photograph* — "is the photo intact". `R_pipe` uses the first.

**The three sentences that are always available:**
1. *"That's measured — here's the cell."*
2. *"That's built but not run, so I'm not quoting a number for it."*
3. *"We can't separate those two explanations with this experiment, and here's the one that would."*

Number 3 is not a weakness. Knowing the limit of your own evidence is most of what is being
assessed.

---

## 6 · The five ideas worth carrying into M2, M3 and M4

1. **Three metrics agreeing on a sign beats one metric with a big number.** Cheap, robust,
   and it works at any sample size.
2. **When a metric and your eyes disagree, find out why before choosing a side.** That
   disagreement is usually a finding about the metric.
3. **A control that agrees with your hypothesis returns a confident wrong answer.** We hit
   this twice — the randomly-initialised mock autoencoder, and an FFT test run against a
   flat reference spectrum that hid a real bug.
4. **Audit shape and scale before comparing two images.** A silent resample turned an entire
   afternoon of diagnostics into a measurement of interpolation error.
5. **Check the rubric before starting an investigation.** Curiosity about a result is not the
   same thing as work the deadline requires.
