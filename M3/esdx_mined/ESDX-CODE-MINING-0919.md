# Mining Light.Cyber Ninjas' ESD-x baseline — 19 Sep 2026

**Source:** `M3/FIT5230_M2_ESDx__Baseline.ipynb` (their executed notebook, local copy 19 Sep).
**Mined:** every code cell + all 8 executed figures, extracted to `esdx_mined/figures/`.
**Cost:** zero GPU. Everything below comes from their own outputs.

---

## 0 · What they actually have now

| | value | where it came from |
|---|---|---|
| Base model | `CompVis/stable-diffusion-v1-4`, bfloat16, `safety_checker=None` | cell 14 |
| Hardware | single Colab **T4** | notebook metadata |
| Baseline run | **100 iterations · 40 min 16 s · final `esd_loss = 0.0029`** | cell 9 stdout |
| Multi-descriptor run | **100 iterations · 45 min 14 s · final `esd_loss = 0.0009`** | cell 11 stdout |
| Training variants | literal name + 1 English description + **1 French** translation | cell 11 |
| Evaluation | 8 prompts, **1 image each, seed 42**, judged by eye | cells 15, 18 |
| Quantitative metric | **none** | — |

So: two real checkpoints, ~85 GPU-minutes total, and **no numbers at all.**

---

## 1 · The five weaknesses, ranked by how cheaply we can exploit them

### ⭐ 1.1 The multi-descriptor arm is confounded — this is the big one
Both runs get **100 iterations**. The baseline spends all 100 on `"Van Gogh"`. The
multi-descriptor run randomly picks one of **three** phrasings per step, so the literal name gets
roughly **33**. The two checkpoints therefore differ in **two** things at once: *what* they
trained on and *how much* they trained on each thing.

> Two students study for 100 hours. One reads a single textbook; the other splits the same
> 100 hours across three. If the second scores differently, you have not learned that three books
> beat one — you have learned that 33 hours of book one differs from 100 hours of book one.

**Any difference they report is unattributable.** The missing arm is *baseline at 300 iterations*,
or *multi-descriptor at 300*, so that per-phrasing exposure is matched.

**This is exactly our own `pur_iters` finding in a different costume** — we ran IMPRESS at a tenth
of the paper's budget and it explained more than our method did. We can say that from experience,
not from the sidelines, and it reads as solidarity rather than an attack.

### ⭐ 1.2 Their specificity claim is contradicted by their own figures
Their findings say: *"Neither version messed up other artists… our erasure isn't damaging things
it shouldn't touch."* That conclusion rests on one image each for Picasso and Monet, judged by eye.

Measured off their own published panels (mean pixel contrast, interior crop):

| prompt | unmodified SD | baseline ESD-x | multi-descriptor |
|---|---:|---:|---:|
| Monet (non-target) | 0.246 | **0.158** (−36%) | **0.158** (−36%) |
| Picasso (non-target) | 0.380 | **0.312** (−18%) | **0.300** (−21%) |
| Van Gogh (target) | 0.380 | 0.155 | 0.158 |

**Both checkpoints flatten non-target artists substantially.** Whether that is stylistic drift or
genuine damage is open — but "no collateral damage" is an assertion their evidence cannot carry,
and the number that would settle it (CLIP similarity to *"a painting by Claude Monet"*, erased vs
base) costs one inference run.

⚠️ **Honest caveat, and we must publish it with the finding:** n = 1, one seed. A style change can
legitimately move contrast. This is not proof of damage — it is proof that **their test cannot
tell the difference**, which is the actual claim.

### 1.3 The obfuscated-spelling excuse — they are right, and we should say so
Their `V@n G0gh` panel: **all three models render a plain photorealistic sunflower still life.**
Unmodified SD shows **no Van Gogh style at all**. Their published defence —
*"the base model completely fails to identify the obfuscated text… a limitation of testing style
leakage through a channel that never transmitted the semantic signal"* — **is confirmed by their
own figure.**

**Concede this publicly and without hedging.** Conceding the half they are right about is what
makes the half they are wrong about land. It also costs us nothing: leetspeak was never our lane.

### 1.4 The cross-script hole is still wide open
Training variants: English description + **French**. Both Latin script.
Evaluation set (8 prompts): **zero non-Latin script.**

Their M2 conclusion already commits them to the wrong fix — *"for Milestone 3… add some
misspelled/obfuscated versions of the name into our training list"*. They are about to spend M3
patching the channel that carries no signal (1.3), while **梵高 · ゴッホ · 반 고흐 · фан гог ·
فان جوخ** stay untested and untrained.

⚠️ **Post the cross-script prediction on their thread before they train.** Once they publish an
M3 that adds obfuscation, a cross-script result becomes a reply instead of a called shot, and
half of M3's 5-mark "how did the target react" row goes unscored.

### 1.5 Two engineering traps worth flagging as a gift, not a jab
1. **Checkpoint filename collision.** Both runs save
   `esd-Van_Gogh-from-Van_Gogh-esdx.safetensors`; only the folder differs. One `--save_path`
   slip and the multi-descriptor checkpoint silently overwrites the baseline — and the filename
   gives no way to tell which is which afterwards.
2. **`load_esd_checkpoint_into_unet` verifies nothing.** It calls `set_module` per key and never
   checks that any key matched. A key-name mismatch loads **nothing** and looks exactly like
   *"the erasure didn't work"*. Two lines fix it: count the keys set, assert it is non-zero.

Flagging these is cheap engagement with a high reply rate — it is useful to them and costs us
no advantage.

---

## 2 · What this does to our M3 plan

| plan item | status after mining |
|---|---|
| ESD-x as the individual target | **confirmed** — they now have real checkpoints to attack |
| Cross-script bucket as the uncrowded lane | **confirmed and now urgent** — they are patching the wrong hole |
| Stage 1 on the authors' pre-erased UNet | **still correct** — their checkpoint is not in the fork |
| Leetspeak bucket | **keep, but as a concession** — expect base ≈ 0, publish it |
| Scoring both erased *and* base model | **confirmed essential** — 1.3 is exactly the case the control catches |
| **New:** a specificity bucket (Monet/Picasso, both models) | **add it** — 1.2 is a second finding for the same inference run |

The specificity bucket is the only addition, and it is free: same harness, two more prompts.

## 3 · Not doing
Re-training their checkpoints · a 300-iteration replication (theirs to run, ours to name) ·
any claim about collateral damage stronger than "their test cannot detect it".
