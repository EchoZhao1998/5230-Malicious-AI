# GLOSSARY — Dark.Tyro
*Standing reference. Written 20 Aug 2026. Add to it; don't rewrite it from memory later.*

Read the **"rewards"** column as: *what does a high score actually mean?* Most confusion in
this project comes from two metrics that measure different things sharing one name.

---

## Part 0 · The mental model — read this before anything else
*Added 20 Aug after a round of "is my understanding right?". These are the four mistakes
that are easiest to make and hardest to notice.*

### The threat model: we never have the clean image

```
VICTIM                        PUBLIC INTERNET          ATTACKER (us)
clean photo ──PhotoGuard──▶ protected photo   ──▶  downloads protected photo
   ▲                                                          │
   └─ stays on her phone.                                     ▼
      We never see it.                            wants to edit it. Shield blocks.
```

**Our target is the PROTECTED image.** The clean image is the **control** — the "what would
have happened without a shield" reference that exists only inside our lab. If we already had
the clean image there would be no attack to run.

### Six images, not three

|  | **input image** (what goes into the editor) | **edited output** (what comes out) |
|---|---|---|
| **clean** | the original photograph | `clean_diff/` — our reference edit |
| **protected** | clean + PhotoGuard noise (`adv_*/`) | `adv_diff_*/` — what a *naive* attacker gets |
| **purified** | protected, run through IMPRESS (`pur_*/`) | `pur_diff_*/` — what a *smart* attacker gets |

The three PNGs in the project root are the **right-hand column**. `pg_metric.py` compares
them to each other — never to the original photograph. See the ⚠️ under Part 1.

What each comparison proves:
- clean-edit **vs** protected-edit → **how well PhotoGuard works** (the defence's efficacy)
- protected-edit **vs** purified-edit → **how well IMPRESS works** (our attack's efficacy)

### 🔑 Two separate operations — only one of them changes the picture

| | job | does it change what the photo depicts? |
|---|---|---|
| **IMPRESS** | **picks the lock.** Removes the shield so the model can read the image again. | **No.** Its output looks the same as the protected image to your eye. |
| **SD inpainting + prompt** | **commits the burglary.** Puts the boy in an airplane. | **Yes.** This would work on any unprotected photo. |

IMPRESS does not create the edit and does not change identity. It only *restores the
editor's ability* to do what it could always do.

**And we do not want a different person.** The mask preserves the face and regenerates the
background, deliberately: the malicious scenario is *"put this real, recognisable person
somewhere they have never been."* If the face changed identity, the fake would be worthless.
**The boy staying a boy is the attack succeeding.**

### 🔑 Whose knob is it? `pg_*` is the defender's, `pur_*` is ours

| prefix | belongs to | turning it up |
|---|---|---|
| `pg_*` | **PhotoGuard** — the defence | **stronger shield → harder for us → R goes DOWN** |
| `pur_*` | **IMPRESS** — our attack | better purification → **R goes UP** |

> The `pg_*` knobs are how thick the lock is. The `pur_*` knobs are how good your lockpick
> is. You don't get through the door faster by buying a better lock.

**But raise `pg_*` anyway — for a different reason.** A weak shield makes `R` meaningless,
because the denominator `S_clean − S_protected` collapses into noise. So:

- **raise `pg_*` → makes the test valid**
- **tune `pur_*` → makes the score good**

Two different purposes. Conflating them in writing is an easy mark to lose.

### `R > 1` is a red flag, not a triumph

It would mean the purified edit matches the prompt *better than the clean edit does*. Nearly
always this means the shield never worked, or purification smoothed the image into something
CLIP finds blandly prototypical. If you see `R > 1`, go looking for the bug.

---

## Part 1 · The metrics

### Image-similarity metrics (all compare **two images**)

| term | full name | range | high score means | watch out |
|---|---|---|---|---|
| **SSIM** | Structural Similarity Index | 0 → 1 | the two images share **structure** — edges and textures in the same places | Not perceptual. A slightly blurred image can score well while looking obviously wrong to a human. |
| **PSNR** | Peak Signal-to-Noise Ratio | dB, ~20 low → ~40 high | the two images are close **pixel by pixel** | Punishes any global shift (brightness, colour) harshly even when it's invisible. Crudest of the three. |
| **VIF / VIFp** | Visual Information Fidelity (pixel domain) | 0 → 1, can exceed 1 | the second image preserves the **information** a human visual system would extract | Closest of the three to human judgement; also the least familiar to markers, so define it when you use it. |
| **LPIPS** | Learned Perceptual Image Patch Similarity | 0 → ~1, **lower = more similar** | *(inverted!)* small value = looks the same to a human | **Direction is opposite to SSIM.** Uses a trained network (VGG/AlexNet) as the judge. Not in `pg_metric.py`, but it *is* inside `impress.py` as a constraint. On your M2 list to add. |

> ⚠️ **The trap.** In `pg_metric.py`, SSIM/PSNR/VIF compare the **edited protected** image
> against the **edited clean** image — *not* against the original photograph. It answers
> *"did the editing pipeline behave normally?"*, not *"is the photo intact?"* Two different
> questions. Say which one you mean, every time.

### Prompt-adherence metric

| term | what it is | how to read it |
|---|---|---|
| **CLIP** | a model trained to put an image and its text description at the same point in a shared space | The ruler, not the thing measured. |
| **CLIPScore** | cosine similarity between CLIP's image embedding and CLIP's text embedding | Higher = the picture matches the words. Typically 0.2–0.35 for a good match — **the absolute number is meaningless; only differences between conditions matter.** |
| **ViT-B/32 vs ViT-L/14** | two CLIP sizes | Tyro deliberately scores with **ViT-B/32**, because SD uses ViT-L/14 internally. *Don't let the chef grade his own dish.* |

### Tyro's own metric

**`R`  — restoration rate**

```
R = (S_purified − S_protected) / (S_clean − S_protected)
```

where `S` = CLIPScore(edited image, edit prompt).

- `R = 1.0` → purification fully restored the editor
- `R = 0` → the shield held
- `R > 1` → the purified image matches the prompt *better than clean* (suspicious, investigate)
- `R < 0` → purification made it worse than doing nothing

> Metaphor: `S_clean − S_protected` is **how far the shield knocked the editor down**. `R`
> is **what fraction of that fall your attack undid.** A percentage of a recovery.

**Guard rail:** when the denominator `P = S_clean − S_protected` is near zero, the shield
never worked in the first place, `R` is a ratio of two noise terms, and it means nothing.
The notebook refuses to print it. **Do not override this.**

---

## Part 2 · The attack parameters (`pg_*` — building the shield)

These configure **PhotoGuard**, the defence you are attacking. Stage 8a, `pg_mask_diff_helen.py`.

| flag | value used | what it does | raising it |
|---|---|---|---|
| `--attack_type` | `l2` | shape of the budget: `l2` = total energy across all pixels; `linf` = a cap on every single pixel | **stay on `l2`.** `linf` with `pg_eps=16` on `[-1,1]` images is unbounded — the constraint never binds. |
| `--pg_eps` | `16` | **the size of the perturbation budget** — the radius of the L2 ball the noise must stay inside | ⚠️ **FALSIFIED 9 Sep.** We predicted this was the real lever. Measured, `16` vs `32` give the same perturbation to within 1% (L2 2645.8 vs 2641.6): at `pg_iters=40, pg_step_size=1` the ball is **never reached**, so the projection never binds and the knob does nothing. The lever that binds is `pg_step_size`. |
| `--pg_step_size` | `1` | how far each PGD step moves, in L2 distance. The gradient is normalised first, so each step moves *exactly* this much | with `eps=16`, ~16 steps to reach the boundary |
| `--pg_iters` | `40` / `200` | number of PGD steps | **saturates.** Past ~16–40 you're walking around the surface of the ball, not further out. 200 is mostly wasted compute. |
| `--pg_grad_reps` | `2` / `10` | how many stochastic gradient estimates to average per step (different random latents each time) — this is **EOT**, Expectation over Transformation | better *direction* within the same budget. Cost is linear. The paper uses 10. |
| `--pg_eta` | `1` | DDIM sampler noise parameter used *inside the attack*. `eta=1` = fully stochastic (DDPM-like), `eta=0` = deterministic | leave it; it's why `grad_reps` matters |
| `--diff_steps` | `4` | how many diffusion steps the attack **unrolls and backpropagates through** | stronger shield, expensive. **This is the 77-min knob.** Must be identical across 8a→8d or folder names diverge. |
| `--guidance` | `7.5` | classifier-free guidance strength during the attack's inner generation | part of the folder name; keep fixed |
| `--manual_seed` | `0` | RNG seed | **the reason your 3-panel comparison is controlled.** Never vary it between panels. |
| `--parallel_index` | `-1` | which quarter of the dataset this process handles | `-1` = "do all of it, single GPU". Always use `-1` on Colab. |

**Where the noise goes:** the gradient is multiplied by `(1 - mask)`, so the perturbation is
written onto the region the model **keeps and reads** (here: the face), not the region it
regenerates (here: the background).

---

## Part 3 · The purification parameters (`pur_*` — your attack)

These configure **IMPRESS**. Stage 8b, `pg_mask_pur_helen.py` → `impress.py`.

The objective, in words: *nudge the protected image until the VAE can round-trip it without
complaint, but don't let it drift far from what it looked like.*

```
min  ‖ D(E(x′)) − x′ ‖²   +   pur_alpha · max( LPIPS(x′, x_protected) − pur_eps , 0 )
      └── self-consistency ──┘        └────────── stay-close leash ──────────┘
```

| flag | value used | what it does | raising it |
|---|---|---|---|
| `--pur_eps` | `0.1` | **free LPIPS allowance** — how far the purified image may drift before the penalty even switches on | more freedom to strip the shield, more damage to the photo |
| `--pur_alpha` | `0.01` | weight on that penalty once it does switch on | higher = stay closer to the protected image = weaker purification |
| `--pur_iters` | `100` | optimisation steps (Adam + cosine LR schedule) | more thorough, linear cost |
| `--pur_lr` | `0.005` | Adam learning rate | too high overshoots and smears; the schedule anneals it to 1e-5 |
| `--pur_noise` | `0.05` | random noise added **once, at initialisation**, to knock the image off the adversarial optimum | a small kick to escape the shield's basin. Too big destroys detail. |

> Metaphor for the whole thing: the shield made the image **grammatically wrong** to the
> autoencoder — it can no longer read the sentence and write it back out unchanged. IMPRESS
> is a proofreader that rewrites the sentence until the autoencoder can copy it cleanly,
> under a rule that it must not change more than `pur_eps` worth of meaning.

**`--test_guidance` (7.5) and `--test_diff_steps` (50)** belong to stage 8c — they configure
the *evaluation* edit, not the attack. Keep them fixed across all conditions or the
comparison breaks.

---

## Part 4 · Concepts

| term | plain version |
|---|---|
| **PGD** | Projected Gradient Descent. Take a small step downhill; if you've gone outside the allowed budget, snap back to its edge; repeat. The standard way to build an adversarial example. |
| **Adversarial perturbation** | a change to an image chosen by gradient descent to break a model, small enough that a person doesn't notice. |
| **EOT** | Expectation over Transformation. When the thing you're attacking is random, average the gradient over several random draws so you attack the *distribution*, not one lucky sample. That's `pg_grad_reps`. |
| **VAE** | Variational Autoencoder. The compressor at the front of Stable Diffusion: `E` squeezes 512×512×3 into a 64×64×4 latent, `D` expands it back. **The shield attacks `E`; IMPRESS exploits that `D(E(x))` no longer matches `x`.** |
| **Latent** | the compressed 64×64×4 representation the diffusion actually operates on. |
| **Inpainting** | regenerate the masked region, keep the rest. The Helen setup regenerates the *background* and keeps the *face*. |
| **Classifier-free guidance** | how hard to push the generation toward the prompt vs. letting it drift. 7.5 is standard; higher = more literal, more artefacts. |
| **Immunisation** | the defenders' word for pre-emptively adding a shield to a photo before publishing it (PhotoGuard, Glaze, Mist). |
| **Purification** | the attackers' word for removing it. Your side. |
| **Round-trip inconsistency** | `‖D(E(x)) − x‖`. Measured: **0.0071 clean vs 0.0204 protected.** This is both IMPRESS's premise *and* the Tier-3 detection signal. |
| **Restoration rate** | see `R` above. |
| **The Gauntlet** | Tyro's 3-tier M1 challenge: JPEG q65 → full cascade → detection. |

---

## Part 5 · Folder-name decoder

Every IMPRESS output folder is named from its parameters. **The names are the audit trail —
if they don't match across stages, the chain silently reads the wrong directory.**

```
adv_l2_eps16_step1_iter200grad_reps2_eta1_diff_steps4_guidance7.5_seed0
└─ protected images.       encodes ALL pg_* params ✅

adapt_adv_l2_eps16_..._seed0
└─ copy of the above (the bridge cell — repo bug #5)

pur_eps0.1_pur_iters100_pur_lr0.005_pur_alpha0.01_pur_noise0.05
└─ purified images.        encodes NO pg_* params ❌  ← BUG 7. Trials overwrite each other.

clean_diff/                    edited clean       ┐
adv_diff_l2_..._seed0          edited protected   ├─ the 3-panel story
pur_diff_eps0.1_...            edited purified    ┘

result/<prompt>/test/...       side-by-side figures pg_generate saves automatically
```

See `M1/TRIAL-LOG.md` §3 for bugs 7–9 and their fixes.
