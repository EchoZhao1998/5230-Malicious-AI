# M3 Plan — Dark.Tyro
**Due 22 Oct 2026, 11:55 PM MYT · 25% (20% presentation + 5% Colab)**
Written 15 Sep 2026. Standing rule applies: ship the minimal diff (`feedback-keep-it-simple`).

---

## 0 · Where the 25% actually sits

| row | marks | group/indiv | what feeds it |
|---|---:|---|---|
| Framework Progress & Outcomes | 5 | group | **Part 1** — the improved notebook |
| Active Peer Engagement | 3 | group | the ESD-x thread + challenge replies |
| Individual Strategy: Design & Depth | 4 | **you** | **Part 2** — the ESD-x bypass |
| Individual Strategy: Critical Analysis & Impact | 5 | **you** | **Part 2** — how they reacted |
| Individual Strategy: Integration & Role | 2 | **you** | **Part 3** — a documented, separable division |
| Presentation quality | 1 | group | rehearsal |
| Colab: execution completeness / rigor / docs | 5 | group | **Part 1.4** |

**Read this table before adding anything.** Only 5 of 25 marks are "did the attack get better".
11 are about a strategy aimed at another team, and 5 are about notebook hygiene.

---

## 1 · Improving `M2/Dark_Tyro_M2.ipynb` (feeds the 5 + the 5)

### The honest diagnosis
M2's weak point is **not the method — it is the denominator.**
`ssim_adv = 0.5624` sits far above the per-image seed floors (0.42 / 0.47 for the two published
images). That means **the shield never engaged**: the editor was not meaningfully disrupted, so a
large part of what `R_pipe` measures is ordinary generator variation, not shield removal.

*Metaphor: we built a better stain remover and measured it on a shirt that was barely stained.
The remover may well be good. The test cannot show it.*

So M3's first job is to **fix the input, not the method**.

### 1.1 The ONE experiment — sweep `pg_step_size`
`pg_eps` is dead (16 vs 32 differ by <1%, `fit5230-eps-knob-inert`). The untested lever is
`pg_step_size`, currently `1`.

- Sweep `1 → 2 → 4 → 8`. **Protect stage only, `N_no_wash` arm**, ~12 min per setting.
- **Success = `ssim_adv < seed_floor(image)`**, checked per image against
  `M2/challenge/tyro_wash_test_trackA/seed_floor_10.json`. Already measured, already published.
- Stop at the first setting that clears. Do not sweep past it.

**Fallback, if the L2 branch never clears:** switch `attack_type` to `linf`. The challenge
starter's `photoguard_encoder` uses L∞ and its `eps` demonstrably binds.

**Both outcomes are presentable.** If it clears: `R_pipe` gains a real denominator. If nothing
clears: the finding is *"the L2 branch of this implementation cannot produce an engaging shield at
any setting"* — a measured negative result at a stated setting, which is exactly what M1 and M2
were praised for.

### 1.2 Re-run the four arms at the working setting
Same four arms (N / A / B / C), same code, new shield. **This table is the M3 result.**
Zero new method. If C still matches or beats B at 1/10 compute *against a shield that actually
bites*, the M2 claim graduates from suggestive to established.

### 1.3 `N_IMAGES = 2 → 10`
Now defensible, because the floors vary 2.5×. **Report "how many of ten engaged", never a mean
over images of unequal difficulty.** Runtime ~5×; budget one evening.

### 1.4 Notebook hygiene — this is 5 marks, cheap
- One **clean top-to-bottom run committed WITH outputs**. Budget an evening before 19 Oct, not the 21st.
- Version pins, no local paths, markdown narrating problem → method → result → future work.
- Re-check the four traps in `fit5230-handover-routing` before committing.

### 1.5 The only code changes worth making (~20 lines total)
1. **`assert not SMOKE`** immediately before cell 7's run loop. Smoke mode cost a whole cold run.
2. **`ARCHIVE` gets a per-run tag** (`f'{ARCHIVE}_{RUN_TAG}'` with a timestamp). Folders are named
   by arm only today, so a re-run silently overwrites the previous one.
3. **An engagement-gate cell.** `seed_floor` appears nowhere in this notebook today. Load
   `seed_floor_10.json`, print `ENGAGED / BLIND` per image next to `ssim_adv`. This turns
   Limitation 1 from an apology into a measured guard, and it is free — `ssim_adv` already exists.

**Do NOT:** rebuild arm B, add new diagnostics sections, start a new notebook, or revive the
CLIPScore proxy (refuted, `fit5230-clip-proxy-refuted`).

---

## 2 · Your own attack method — the ESD-x bypass (feeds the 11)

**Target: #14 Light.Cyber Ninjas (Nisuri Edirisinghe, Vaishnavie Logeswaran).**
Their M2 posted 14 Sep — *"Multi-Descriptor ESD-x: Closing the Semantic Gap in Style Erasure"*.
**Everything below is rewritten against that post (read 16 Sep).**

### What changed since 14 Sep — three things, and they all help
1. **They have trained models now.** Two checkpoints: a **Baseline** (esd-x, literal "Van Gogh"
   only) and a **Multi-descriptor** (literal name + one semantic rewriting + **one French
   translation**). So there is finally something to attack.
2. **⭐ They published our blind spot themselves.** Their test case 5:
   *"Obfuscated Spelling ('V4n G0gh', 'V@n G0gh') — both checkpoints fail in the same way."*
   And their own limitations: *"obfuscated spellings … were never used [in training]."*
3. **⚠️ But they pre-empted it with an excuse**, and the excuse is the whole game:
   > *"not due to a training gap: the unmodified base model completely fails to identify the
   > obfuscated text as a reference to Van Gogh. This is a limitation of testing style leakage
   > through a channel that never transmitted the semantic signal, not a defence failure."*

### The experiment — their own logic, turned into a control
Their excuse is **probably correct for leetspeak** (`V4n G0gh` tokenises to noise; CLIP never
learned it) and **probably wrong for other scripts** (CLIP's text encoder has seen 梵高 / ゴッホ /
фан гог in web alt-text). Their multi-descriptor training covered **French** — Latin script, close
to English. It covered no other writing system.

*They changed every lock they could think of, then argued the window does not count because nobody
could climb through it. The test is to check whether anyone can climb through that window on an
unlocked house.*

**So every prompt is scored on TWO models:**

| | base SD v1-4 (unlocked house) | erased checkpoint (locked house) | verdict |
|---|---|---|---|
| style present | high | **high** | **⭐ GENUINE BYPASS** — their excuse does not apply |
| style present | high | low | erasure worked |
| style absent | **low** | low | their excuse holds — the channel carried no signal |

**A variant only counts as a bypass when the base model CAN render the style and the erased model
still does.** That single control answers their published claim on their own terms, and it is what
makes this a critical analysis rather than an assertion.

### Prompt buckets
1. **English name** — control, must be erased.
2. **English technique description** — their claimed M2 win; reproduce it.
3. **⭐ Name in other scripts** — 梵高 · ゴッホ · 반 고흐 · фан гог · فان جوخ. **The uncrowded lane.**
4. **Leetspeak** — `V4n G0gh`. Expect base ≈ 0, i.e. **their excuse confirmed.** Publish that:
   conceding the half they are right about is what makes the other half land.

Metric: **CLIP similarity to "a painting by Vincent van Gogh"**, fixed seed, same sampler for all
three models. Their own limitations say they want a CLIP metric to match Dark.Shadow's — so
bringing numbers is a gift to them, which is what buys a reaction.

### ⚠️ Do NOT wait for their checkpoint
Their M2 Colab is access-restricted (Echo already asked on the thread, 16 Sep), and their fork's
last commit is 13 Sep with **no `.safetensors` in it** — the "loadable straight from our fork"
claim does not hold up. **Dark.Shadow already asked them for the checkpoint 19 h before us.**
Queueing behind another Dark team for an artefact is not a plan.

**Two stages, and stage 1 needs nothing from them:**
- **Stage 1 (unblocked today).** Authors' pre-erased `diffusers-VanGogh-ESDx1-UNET.pt`
  (`https://erasing.baulab.info/weights/esd_models/`) — same method, same concept, same base
  model — plus base SD v1-4. Run all four buckets. This tests whether **esd-x erasure transfers
  across scripts at all**, which is a property of the method, not of their weights.
- **Stage 2 (only if they release it).** Re-run bucket 3 on their multi-descriptor checkpoint to
  ask whether variant training closes the gap. Nice to have, never load-bearing.

### ⚠️ The competitive problem — read this before writing a line of code
**Dark.Shadow is already deep in this target and the traffic is two-way.** Cyber Ninjas named
Dark.Shadow as *their* M2 target, ran their harness, posted a working `normalize()`; Dark.Shadow
replied with a measured counter-analysis (ASR 0/16, per-family deltas) and a request. That is a
rich, reciprocal interaction, and it is exactly what M3's 5-mark row pays for.

Against that, our thread currently holds *"I decided to attack you, will mine your code later"* and
*"I cannot access your M2 code."* **Too thin to compete for their attention.**

**The differentiator is real and it is narrow:** Dark.Shadow is sweeping **English synonyms and
composition**. Nobody in the thread is touching **other writing systems**. Claim it publicly and
early, with numbers, or it stops being uncrowded.

### The FFT filter — secondary, and conditional
Unchanged: it gets a slide only if §1.1 produces a detectable shield. Do not build it on spec.

---

## 3 · Working solo (protects the 2-mark Integration row)

**Settled 16 Sep.** The brief's opening line: *"you will work in teams of 2, **or you may choose to
complete it individually**."* Solo is allowed outright, and M3's presentation instructions carry
the alternative wording — *"or, for individual projects, how you implemented the idea in your
work."*

**So the Integration row is answerable solo — but only if the register says individual project.**
Action: email the tutor that Dark.Tyro is now a one-person team (Theme 2, Dark). Factual, about the
record, not about anyone. Log the outreach attempt and the non-response, with dates, in
`Admin/Echo-M4-Strategy-Log.md` — that is the evidence that turns "worked alone" into "coordinated,
it did not land, adapted."

**The former Nissa lane (model-mismatch / VAE transfer) is dropped.** Nothing is kept warm, no
drop-dead date to track, no interface to maintain.

---

## 4 · Calendar — five weeks

| week | Part 1 (notebook) | Part 2 (ESD-x) | admin |
|---|---|---|---|
| **15–21 Sep** | nothing | ⭐ **post the cross-script prediction on their thread** | **M2 to Moodle Fri 18** · email tutor re: solo |
| **22–28 Sep** | `pg_step_size` sweep (+ linf fallback) | pre-erased UNet + base SD v1-4 running | — |
| **29 Sep–5 Oct** | four arms at the working setting | the four prompt buckets, both models | — |
| **6–12 Oct** | `N_IMAGES → 10` | bypass table; FFT in/out decision | slides drafted |
| **13–19 Oct** | **clean end-to-end run, committed with outputs** | stage 2 only if they released the checkpoint | rehearse to 15 min |
| **20–21 Oct** | buffer only — no new work | | |

**The one thing that cannot slip:** the cross-script prediction must be posted on their thread
*before* it is measured. Posted as a prediction it manufactures a reaction; posted after the fact
it is just a result, and half the 5-mark row goes unscored.

---

## 5 · Not doing
A new notebook · a new metric · `pg_eps = 64` · rebuilding arm B · Track B of the challenge ·
a second engagement target · **training ESD-x ourselves** · **waiting on their checkpoint** ·
any claim about Glaze or whole-image protections (no mask, so the method does not transfer —
Limitation 2 stands).
