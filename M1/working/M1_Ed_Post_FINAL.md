# Dark.Tyro — M1 Ed post, FINAL
*Rewritten 26 Aug 2026. Supersedes `M1_Ed_Post_DRAFT.md` (v2, 22 Aug) and the Google-doc draft.*
*Everything below the line is paste-ready Markdown. Placeholders are marked `[[…]]`.*

---
---

# [Dark.Tyro] The Tyro Wash Test — stripping PhotoGuard off the image-editing pipeline

**Theme 2 · Text-to-Image · Dark (Attack)**

| Member | Student ID | Email |
|---|---|---|
| Echo Zhao | 35507071 | ezha0053@student.monash.edu |
| Nissa Colidea | 34610960 | nnis0009@student.monash.edu |

`[[embed both member photos here]]`

---

## 1 · Baseline and reference material

| | Paper | Code |
|---|---|---|
| **The system we attack** | **Stable Diffusion v1.5 inpainting** — text-guided image editing, the same editing pathway as this theme's InstructPix2Pix sample paper ([arXiv:2211.09800](https://arxiv.org/abs/2211.09800)) | [huggingface.co/stable-diffusion-v1-5](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-inpainting) |
| **The obstacle** | **PhotoGuard** — *Raising the Cost of Malicious AI-Powered Image Editing*, ICML 2023 — [arXiv:2302.06588](https://arxiv.org/abs/2302.06588) | [github.com/MadryLab/photoguard](https://github.com/MadryLab/photoguard) |
| **Our baseline attack** | **IMPRESS** — *Evaluating the Resilience of Imperceptible Perturbations Against Unauthorized Data Usage in Diffusion-Based Generative AI*, NeurIPS 2023 — [arXiv:2310.19248](https://arxiv.org/abs/2310.19248) | [github.com/AAAAAAsuka/Impress](https://github.com/AAAAAAsuka/Impress) |
| **Our notebook** | — | `[[Colab link — set sharing to "Anyone with the link can view" and test it logged out]]` |

Read the table top-down and it is the whole project in three rows: a model that can rewrite
photographs, a countermeasure that stops it, and the attack we run to get past that
countermeasure.

### Why IMPRESS

Three filters, applied in this order.

1. **It must be an attack, because we are the Dark side.** IMPRESS is a *purification* attack:
   it takes a protected image and optimises it until it is self-consistent under the diffusion
   model's autoencoder. PhotoGuard is the defence it removes — so PhotoGuard is our **target**,
   not our baseline.
2. **It must ship runnable code and reproducible metrics.** IMPRESS ships both, including the
   `pg_metric.py` harness (SSIM / PSNR / VIF). Two otherwise-attractive papers failed this
   filter and were demoted to related work: the JPEG-bypass work
   ([arXiv:2304.02234](https://arxiv.org/abs/2304.02234)) has no official implementation, and
   the Query-Free Attack ([arXiv:2303.16378](https://arxiv.org/abs/2303.16378)) attacks the
   *prompt* rather than a protected image, so it shares no evaluation harness with ours.
3. **It must fit on one free GPU.** Confirmed — see §3.

### What is theirs and what is ours, stated plainly

**`impress.py` is 25 lines and we have not touched one of them.** That is deliberate: a
repaired reference implementation is only useful as a baseline if it is still the reference.

What is ours is everything around it — **eleven repairs** that make the 2023 code run in 2026,
a single-GPU harness, a parameter-stamped archive, the restoration rate `R_pipe`, and a
controlled three-panel figure. *The algorithm is theirs; the measurement is ours.*

**One verifiable gap, which is where M2 goes.** The IMPRESS abstract says the method "can be
used as an evaluation platform for future protection methods." The released code does not
deliver that: it ships two hardcoded scripts (`glaze_pur.py`, `pg_mask_pur_helen.py`) bound to
fixed folder contracts, with no generic entry point. You can confirm this with a `git clone`
and two `ls`. **M2's contribution in one sentence: build the generic entry point the paper's
own claim implies.**

---

## 2 · The problem, and why it is hard

**The system.** A text-to-image model conditioned on an existing photograph is not a generator,
it is an *editor*. Hand it your image, a mask and an instruction, and it rewrites reality — puts
someone somewhere they have never been, in clothes they have never worn.

**The obstacle.** Because that capability is dangerous, *immunisation* tools appeared in 2023.
PhotoGuard adds a near-invisible perturbation to a photo before it is ever posted. To your eye
nothing changed. To the model the image is unreadable, and edits come out as garbage.

> Think of PhotoGuard as an anti-counterfeit hologram stuck to a photograph. It does not stop
> you *seeing* the picture — it stops the *machine* processing it. Our attack asks whether the
> hologram peels off, and how cleanly.

**Our question:** is that lock durable, or does it only look solid?

**Why this is technically hard, not just fiddly.**

- **The two goals fight each other.** Removing an adversarial perturbation is trivial if you may
  destroy the image — blur it into soup and the shield is certainly gone, but so is the
  photograph. The attack only counts if the purified image stays faithful *and* the editor
  starts obeying prompts again. Success is a **two-axis trade-off**, and most naive purifiers
  win one axis by collapsing the other.
- **The perturbation is invisible by construction**, so you cannot look for it. It has to be
  found by changing coordinates — which is what our frequency analysis does.
- **The expensive knob is not the knob that matters.** Reading PhotoGuard's `super_l2`: every
  PGD step moves exactly L2 = 1.0 and is then projected back inside a ball of radius
  `pg_eps = 16`. From the centre you hit the wall after ~16 steps; everything after that walks
  *around* the surface, not further out. So `pg_iters` **saturates**, and the lever that
  actually raises the ceiling is `pg_eps` — which the reference experiments leave fixed.
  *(`pg_eps` is the length of the leash; `pg_iters` is how long the dog runs.)*
- **Measuring "did the attack work" is itself unsolved in the reference code** — and this turned
  out to be the most interesting thing we found. See §3.

---

## 3 · What we built, and what it measured

The 2023 code does not run as published in 2026. Our notebook is not a clone; it is a repaired
and instrumented version. **Eleven repairs, grouped by consequence.**

**Six faults that stop it running at all** — a deleted Hugging Face repo hard-coded in every
script; a missing `fp16` revision on the mirror; `sewar` imported but absent from
`requirements.txt`; a launcher that shards across four GPUs; a broken folder contract between
the protect and purify stages (`adv_*` written, `adapt_adv_*` read); and a silent `--diff_steps`
default mismatch that makes the chain read a directory that does not exist.

**Three faults that make multi-run results quietly wrong.** These are the interesting ones —
none raises an error; each hands you the *previous* run's images under *this* run's label. The
purified output folder name encodes no `pg_*` parameters, so every protection strength
overwrites the last. The bridge step selected its input with an unsorted `glob(...)[0]`. The
display cell hard-coded one configuration's parameters. All three are now driven from a single
`PARAMS` dict.

**Two limits we label rather than paper over.** `(pg_iters=200, pg_grad_reps=10)` exhausts 16 GB
on both a T4 and a P100, so that grid cell is omitted rather than run with a different
`diff_steps` — a grid where one point used a different attack is not a grid. And the Kaggle
**P100 is compute capability `sm_60`**, which current PyTorch wheels no longer ship kernels for;
the pipeline loads and then dies on the first CUDA op. Cell 1 now gates on this.

### The result

`[[insert the 3-panel figure: edited CLEAN | edited PROTECTED | edited PURIFIED]]`

This is a **controlled** comparison, which is worth stating: `pg_generate.py` re-seeds numpy and
torch immediately before each of the three generations, with the same mask, prompt, guidance and
step count. The sampling trajectory is identical across panels, so **every visible difference is
caused by the input image alone.**

`pg_metric.py` compares the *edited* protected and purified images against the *edited clean*
image, so 1.0 means "the pipeline behaved exactly as if the photo had never been protected".
That gives a restoration rate with no third measurement needed:

```
R_pipe = (SSIM_purified − SSIM_protected) / (1 − SSIM_protected)
```

| protection | `pg_iters`:`pg_grad_reps` | SSIM adv | SSIM pur | **R_pipe** | three-metric sign test |
|---|---|---|---|---|---|
| 80 units | 40 : 2 | 0.5921 | 0.6131 | **+5.2 %** | PSNR + · SSIM + · VIF + → real movement |
| 400 units | 200 : 2 | 0.5198 | 0.5143 | **−1.2 %** | signs disagree → inside the noise |

At n = 2 faces we do not trust any single metric. We trust whether three independent instruments
agree on the **sign**. They do at 80 units and they do not at 400. Stated at the strength the
data carries: **IMPRESS recovers a few percent of the pipeline at the weakest protection setting
and nothing measurable once protection reaches 400 gradient-units.**

### 🔑 The finding we did not expect: our figure and our metric disagree

At `200:2` the metric says nothing was recovered. **The figure says otherwise** — the edited
protected image is a detached face floating over an aerial view of a wing; the edited purified
image is a coherent person back in a seat. Clean → broken → restored, visibly.

Both are right, and the reason is the important part. `pg_metric`'s SSIM asks *"is the purified
edit pixel-aligned with the clean edit?"* Our purified image is a **different plausible edit**,
not a pixel-copy — so SSIM scores a genuine success as a miss.

> A ruler laid across two photographs of the same dish reports total failure. The ruler measures
> alignment. You wanted to know about the cooking.

**We are not the only team to hit this wall.** Team Megatrons (Theme 1, Dark) independently
report the mirror image of our problem: one of their preprocessing attacks *cleared* their
SSIM threshold while producing a completely different scene, so they correctly classified it a
failed attack. Theirs is a false positive, ours is a false negative, and the root cause is the
same — **SSIM measures alignment to a reference edit, not whether editing succeeded.** Two
teams reaching the same conclusion from opposite directions, on different baselines, is much
better evidence than either of us has alone. Their answer is a manual visual check; ours is the
mechanical engagement gate in §4 and a CLIPScore edit-success metric in M2. We think both are
needed and neither is sufficient alone.

**Two instruments are built and deliberately not reported here.** A CLIPScore edit-success
metric (scored with an independent CLIP model, *not* the ViT-L/14 encoder inside Stable
Diffusion — we are not grading the dish with the chef) and a radial-power-spectrum analysis of
the shield. Both work; neither has been run against the results above, so we quote no number
from either. They are listed as customisation, not as findings.

---

## 4 · The challenge: **The Tyro Wash Test**

Our attack is a **solvent, not a lock-pick.** IMPRESS never inspects the perturbation it
removes — it just optimises the image until the autoencoder agrees with itself. So it does not
care whether your shield is PhotoGuard, Glaze, Mist, or something you invented last week.

> **Win condition, in one line.** Send us ten protected images our purifier cannot restore
> (**`R_pipe` ≤ 0**) while staying within **LPIPS 0.017** of the originals. The official
> PhotoGuard baseline manages one or the other — never both. Beat that and you have beaten the
> published defence, not us.

### Track A — build a shield we can't wash off

**How to enter, in three steps.**

1. **Take the pack:** 10 clean faces at 512×512, their inpainting masks, a submission checker,
   and a working PhotoGuard protector in one cell. No protection code of your own? Change one
   parameter in that cell and you have a valid entry — we published it so you can beat us with
   our own tools.
2. **Send back 10 PNGs**, 512×512, **same filenames.** That is the entire interface. How you
   protected them is your business and you needn't tell us.
3. **We run our fixed purifier** over them, edit clean / protected / purified with identical
   settings, and publish two numbers per entry.

**Fixed pipeline parameters — identical for you and for us:**

```
prompt          = "a person in an airplane"
seed            = 0
guidance        = 7.5
inference steps = 50
resolution      = 512 x 512, with the supplied inpainting mask
purifier        = IMPRESS · pur_eps 0.1 · pur_iters 100 · pur_lr 0.005 · pur_alpha 0.01 · pur_noise 0.05
```

**The two numbers, and the bar to beat.**

| axis | meaning | you want |
|---|---|---|
| **`R_pipe`** = (SSIM_pur − SSIM_adv) / (1 − SSIM_adv) | how much of the editing pipeline our wash restored. 1.0 = stripped; 0 = your shield held | **low** |
| **LPIPS**(protected, clean) | how much of the photograph you spent to get there | **low** |

| official PhotoGuard baseline (our runs, `pg_eps` 16, n = 2) | `R_pipe` | LPIPS |
|---|---|---|
| `(iters 40, grad_reps 2)` — cheap, clean, **but leaks** | +5.2 % | **0.0169** |
| `(iters 200, grad_reps 2)` — holds, **but costs double** | **−1.2 %** | 0.0348 |

**Two dots, not one — and that is the whole challenge.** You win by landing below *and* to the
left of the line joining them: hold like `(200,2)` at the perceptual cost of `(40,2)`. Turning
`eps` up moves you *along* that line, not past it.

**Why two axes.** With robustness alone the winning move is degenerate — crank the perturbation
until the image is noise. Nothing can be washed off a ruined photo, but nothing can be *edited*
either, so that "defence" defeats its own purpose. Both axes go on one scatter plot, and a
shield that wins by wrecking the picture lands in the top-right corner where everyone can see it.

**Two rules, published in advance so you can predict them.**

- **Ranking budget: LPIPS ≤ 0.10.** Over-budget entries are still plotted and discussed, just not
  ranked. The baseline sits at 0.017, so you have roughly six times the reference defence's room.
- **Engagement gate.** If your shield does not measurably damage the edit, `R_pipe` is a ratio of
  two near-zero numbers and means nothing. We report it only when SSIM(edited-protected,
  edited-clean) ≤ 0.85; otherwise we print **"shield did not engage"** and show what we measured.

**And the number we have least reason to publish.** Our own purifier spends **LPIPS 0.15** and
about **five grey levels** of mean absolute difference; PhotoGuard spends 0.017 and about one.
**Our attack damages the photograph roughly four times more than the shield it removes.** That is
the strongest limitation of IMPRESS we have measured, and it is what a Light team should aim at:
force us to spend more still and that is a result in your favour, which we will report as one.
*(Full fidelity table — SSIM, PSNR, mean absolute difference — is in the pack README.)*

### Track B — find the fingerprint

Washing a photo leaves a trace: IMPRESS optimises for autoencoder self-consistency, and we have
measured that axis (clean **0.0071**, protected **0.0204**). So *"is purification detectable?"* is
already answered — **yes**, and we are telling you rather than letting you discover it. The open
question is harder: **does a detector that catches one purifier still catch a different one?**

You get **12 labelled** calibration images (4 clean / 4 protected / 4 purified) to fit anything
you like, then classify **30 unlabelled** ones (10 / 10 / 10) whose purified images come from
**more than one purifier setting**. Report a 3×3 confusion matrix and balanced accuracy on both
sets; the headline is the **generalisation gap** = calibration − evaluation. A small gap means you
found something real about purification. A large gap means detection does not transfer — a result
about the *defence*, not about you.

### What we commit to

- **Every outcome gets published, including ours losing.** Our purifier is deliberately blind; if
  your protection defeats it, that is a real result about IMPRESS and we report it as one.
- **Track B ground truth, our own detector, and a read of the error patterns** — released *after*
  the deadline. We are not publishing the answer key before the exam.
- **Submissions close 18 September**, with all results in our Milestone 2 post.

**Reply here or DM us for the image packs and the submission folder.**

## 5 · Scope, limitations, and ethics

- **Scale.** Two faces per configuration — enough for a real standard deviation instead of `nan`
  and enough for a controlled visual comparison, but **not** enough to rank two configurations
  against each other, and we do not attempt that ranking. M2 raises this to at least five.
- **`pg_eps` is untested.** Everything above varies `pg_iters` and `pg_grad_reps`. Both 400-unit
  points landing near zero is consistent with `pg_iters` saturating — but equally consistent with
  both shields simply winning. This experiment cannot separate those and we do not claim it does.
- **One missing grid cell**, `(200, 10)`, omitted for GPU memory rather than run with a different
  attack. It is an omission and we label it as one.
- **Why the recovery is small is open**, and we treat it as open. An autoencoder round-trip
  changes an image all by itself, so that cost must be subtracted before anything is attributed
  to the shield or the purifier. That is our first piece of M2 work and we report no number for
  it here.
- **Two different quantities in this project are called SSIM.** `pg_metric.py` compares *edited*
  images against the *edited clean* image — "did the pipeline behave normally?", not "is the
  photograph intact?" The fidelity table in §4 is the second quantity. We label which is which
  every time.
- **Ethics.** All faces come from the public Helen facial-landmark dataset, used under its
  research terms; no personal photographs of identifiable individuals were used without consent.
  Our purpose is to establish where a published protection actually breaks. Telling artists and
  ordinary users that these tools protect their photos, when cheap processing strips them, is
  worse than useless — it manufactures false confidence. Publishing the breaking point is what
  makes the next generation of defences honest.

## 6 · Where we go next

**M2** — the `pg_eps` sweep (16 → 24 → 32) on ≥ 5 faces, the CLIPScore edit-success metric run
against real results, LPIPS reported alongside SSIM throughout, and a cheap-purifier ablation
(JPEG / blur / rescale / a frequency-targeted low-pass) plotted against IMPRESS on one
fidelity-versus-success chart. Plus the generic evaluation entry point IMPRESS promises and does
not ship.

**Individual angles.** Echo — frequency-targeted surgical filtering, testing whether precision
beats brute force on the fidelity axis (the 5.24-grey-level figure above is the number it has to
beat). Nissa — model-mismatch purification, testing whether protection computed against one
autoencoder survives a different one.

**The other input.** An editing pipeline takes *two* inputs: an image and a prompt. Everything
above attacks the image. Every protection we know of — PhotoGuard, Glaze, Mist — guards pixels.
**Nobody guards the prompt.** That is the natural second flank.

Questions and attempts both welcome — we reply to every one.

**— Echo & Nissa (Dark.Tyro)**

---
---

# Pre-flight checklist

- [ ] **Verify the InstructPix2Pix vs SD-inpainting wording in §1** — the notebook runs SD
      inpainting with masks. This post says so; the old draft said InstructPix2Pix. Do not
      revert.
- [ ] Both member photos embedded
- [ ] **Colab/notebook sharing = "Anyone with the link can view"** — test from a logged-out
      browser. Single most common way to lose these marks.
- [ ] Notebook has **saved outputs visible**
- [ ] 3-panel figure inserted in §3
- [ ] Track A pack link live (`M1/tyro_wash_test_trackA/` — already built, zero GPU needed)
- [ ] **`Tyro_Analysis_Toolkit.ipynb` section B4 is NOT in the published notebook** — it is the
      answer key to our own Track B
- [ ] All `[[placeholders]]` removed — search for `[[`
- [ ] Ed post URL submitted to the **Moodle M1 page** (the Ed post alone is not the submission)
- [ ] Posted before **28 August 2026, 11:55 PM MYT**

# What changed from the Google-doc draft, and why

| # | change | why |
|---|---|---|
| 1 | **Duplicate Track A section removed**, raw LaTeX (`R_{\text{pipe}}`) replaced with plain Markdown, red highlight and `[PACK LINK]` cleared, "Questions for Ed Forum Post" header dropped | The draft had two versions of the same table and unrendered maths. Clarity of Ed Post is a marked row. |
| 2 | **§1 baseline justification restored** — three filters, "the algorithm is theirs, the measurement is ours", and the verifiable paper-vs-code gap | The draft had none of it. This is our strongest card and it was not being played. |
| 3 | **Fixed pipeline parameters listed literally** (prompt, seed, guidance, steps, purifier config) | The draft said "identical prompt, seed and mask" and named none of them. An entrant could not reproduce our conditions. Megatrons do this and it is the right call. |
| 4 | **The bar is published as two measured dots, not one number** | LPIPS was named as our ranking axis but had never been computed. Measured 26 Aug: 0.0169 at (40,2), 0.0348 at (200,2). Two dots define a frontier, which is a better challenge than a scalar bar — it cannot be won by cranking eps. |
| 5 | **Our own purifier's LPIPS (0.150–0.164) published, above our own ≤ 0.10 budget** | It is the strongest limitation of IMPRESS we have measured. Publishing the number that embarrasses us is what makes the rest credible. |
| 6 | **Megatrons cross-reference added** in §3 | They independently found the SSIM failure from the opposite direction (false positive to our false negative). Convergent evidence from another team is worth more than our anecdote, and it is free peer-engagement credit. |
| 7 | **Scope / limitations / ethics promoted to its own section** | Megatrons have one; we had limitations scattered through the body. Consolidating reads as maturity. |
| 8 | **Track B compressed to one table + one question** | It is our originality differentiator (nobody else is measuring a generalisation gap) but it was burying Track A, which is the track that actually gets entries. |
| 9 | **Three-tier "Tyro Gauntlet" dropped entirely** | Superseded by the two-track design. Tier 2 advertised a cascade whose diffusion stage recovers ≈ 0. |
| 10 | **§4 cut by ~40%: a one-line win condition up front, a 3-step "how to enter", the fidelity table moved to the pack README** | The challenge read as complicated because the *rules* arrived before the *goal*. An entrant now knows what winning looks like in one sentence (`R_pipe` ≤ 0 at LPIPS ≤ 0.017) before meeting a single formula. Everything below that line is explanation, not new requirements. |
