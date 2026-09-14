# Light-side attack plan — Echo, FIT5230 M2/M3

> **Self-contained brief. A fresh chat can start from this file alone.**
> Last revised **14 Sep 2026**. Target settled: ESD-only — read the box below first.

## 🔴 DECISION 14 Sep — **ESD-ONLY**. This supersedes §1 and §2 below.
Echo chose to carry **one** team through M2 and M3: **#14 Light.Cyber Ninjas (ESD-x)**.
Reasons: their code is small and their challenge is benign end to end (TouchGrass's experiment needs
their I2P set, i.e. generating inappropriate images — see [[fit5230-target-decision-final]]); and one
team across both milestones keeps continuity for M3's 5-mark "how did the target react" row.
- **§8 of `M2/M2_Ed_Post_V5.md` is now the ESD-x engagement.** It is written and needs no GPU.
- **TouchGrass is dropped as a target.** The r = 0.94 analysis stays in the archive, unused.
  Do not re-open it without a new reason.
- **The measured content of §8 is a refutation of our own proxy** — see
  [[fit5230-clip-proxy-refuted]]. Do NOT claim the non-English names are predicted to survive.
- Remaining §1 (TouchGrass) is kept below for history only. §2 (ESD-x) is the live target and its
  attack angles are still correct.

## Context in 10 lines
- **Unit:** FIT5230 Malicious AI, Monash. **Team Dark.Tyro** = Echo Zhao + Nissa Corlidea.
- **Theme 2 (Text-to-Image), Dark / attack side.** Free Colab or Kaggle T4 only.
- **Our own project:** we attack PhotoGuard (a defence that adds invisible noise so AI editors
  garble a photo) using IMPRESS as our baseline attack. Our M2 contribution is a mask-restricted
  wash: clean only the region the editor keeps, which cuts photo damage 74% at the same compute.
  Details in `HANDOVER.md`; not needed for the work below.
- **Our challenge:** the **Tyro Wash Test** — we give Light teams 10 faces + masks and ask them to
  build a shield our wash cannot remove.
- **This file is about the other direction:** attacking *Light* (defence) teams' work, which is
  what M2 *Engagement* (2%) and M3 *Peer Engagement* (3%) pay for.
- **Class sheet of all teams' challenges:**
  https://docs.google.com/spreadsheets/d/1aM4TRQxpEeDuvs5k61k8gZWwPkvBh-mCIqvlWnSrrgk/edit?gid=0

---

## ⛔ 0 · THE TEAM SITUATION — recorded 14 Sep 2026

**Nissa Corlidea has contributed zero to this project.** Not "less than half", not "slipped on
one deliverable" — **nothing has entered the repository, the notebooks, the challenge pack, the
M1 post or the M2 post from her.** The record as of 14 Sep:

| deliverable | who built it |
|---|---|
| M1 notebook, 11 repairs, all diagnostics | Echo |
| M2 method (mask-restricted wash), four-arm run, noise floor | Echo |
| Challenge pack (zip, starter notebook, `check_submission.py`, scorer) | Echo |
| M1 Ed post, M2 Ed post (v1→v5) | Echo |
| Figures, README, HANDOVER, folder reorganisation | Echo |
| Engagement target #8 TouchGrass | **named by Nissa, attack plan never produced; run by Echo** |
| Engagement target #14 Cyber Ninjas | Echo |

Nissa's single input to date is the *name* "TouchGrass" as a target. No plan, no code, no run,
no text followed it. On 13 Sep the target was formally reassigned to Echo.

### What this changes — the operating rule from here
**Plan every remaining deliverable as solo work with a solo-sized budget. Assume nothing arrives.**
If something does arrive from Nissa, it is a bonus to be folded in, never a dependency to wait on.

1. **Never block a group mark on a second person.** M2 is *entirely* group-assessed, and a group
   mark one person can finish alone must never wait — this is the ruling that unblocked the
   challenge pack on 13 Sep. Apply it to everything left.
2. **Scope to one evening per deliverable.** Two-person plans are now single-person plans; if a
   task cannot be done by Echo in one sitting, it is cut, not deferred.
3. **Keep the individual marks strictly separate.** M3 Individual Strategy is **11% per student**
   and M4 is an **individual IEEE report (largest single component)**. These are where Echo's
   effort converts to Echo's grade, and they cannot be diluted by a non-contributing partner.
   → **Target #14 ESD-x stays Echo's own** and is not shared, discussed or handed over.
   → **TouchGrass is the team deliverable.** It fills the group Engagement rows. If Nissa wants
     an M3 individual slot she can extend it; Echo does not wait for that to happen.
4. **Write contribution down as you go, dated, with artefacts.** Not as a complaint — as the
   evidence base for the M4 individual report and any teamwork-contribution assessment. Every
   commit, notebook and Ed post already carries Echo's name and a date; keep it that way and do
   not co-sign work Nissa did not do.
   *(Echo raised teamwork on the Ed "Feedback of Teamwork" thread, 14 Sep. Keep that link.)*
5. **Keep the byline honest but not hostile in public.** The Ed post still says
   "Team Dark.Tyro · Echo Zhao · Nissa Corlidea". Public threads are not where this gets settled;
   the unit's own contribution process is. Do not air it in a post.

### Echo's individual work expectation — what one person actually delivers by 18 Sep
| must ship | cost | status |
|---|---|---|
| M2 Ed post with engagement section | 2 h writing | **v5 ready 14 Sep** |
| TouchGrass engagement (analysis + Ed reply) | 1 h, **no GPU** | **ready 14 Sep, see §1** |
| Moodle submission (Ed link in a PDF) | 15 min | Fri 18 Sep |
| **nice to have, cut freely** | | |
| **ESD-x light touch on their Ed thread** | **1 h, no GPU** | **Thu 17 — opens the M3 interaction** |
| TouchGrass arena run (shuffled-gate null) | 2 h GPU | optional, do only if Tue is clear |
| #14 ESD-x | one evening | **moved to M3** — see §2 |

---

## ❓ 0.9 · "Do we attack them with IMPRESS?" — NO. Read this once.

**Our own project and our engagement targets share nothing but the theme.**

| | our project | Light.TouchGrass |
|---|---|---|
| input | a **photo** | a **text prompt** |
| defence lives in | pixels (PhotoGuard's perturbation) | the denoising loop (SLD's latent safety guidance) |
| our tool | IMPRESS washes the perturbation out of an image | **there is no protected image to wash** |

IMPRESS attacks *perturbation-based image defences*. TouchGrass has no perturbation and no input
image. Pointing IMPRESS at them is not a hard experiment — it is a category error.

**The same is true of every other target.** #14 ESD-x is concept erasure, attacked with *prompts*
(titles, transliterations, homoglyphs), not with IMPRESS either. **IMPRESS only ever attacks our
own target.** Expect a different tool for every engagement.

### So what transfers?
**Not the code — the reasoning.** Our portable asset is the experimental discipline we paid for
the hard way: null arms, matched-compute controls, a measured noise floor, and refusing to claim a
gap that sits inside it. That discipline is domain-independent. It works on a text gate exactly as
well as it works on a pixel wash, which is why §1's findings need **zero GPU and zero code of ours**.

### The three levels of attacking a defence — pick the level, not the tool
1. **Attack the model** — make it emit the unsafe thing. ⛔ Off-limits, see below.
2. **Attack the mechanism claim** — did the thing they built cause the effect they measured?
   ← **this is what we do.** Needs their table and their code, not ours.
3. **Attack the referee** — is the measurement trustworthy? Also ours to use (it was the M1 plan).

Levels 2 and 3 are still *attacks*, and the brief's word is "targeting", not "breaking".
**Understanding their work alone is a comment, not engagement.** What converts it to marks is
returning a **number** (our r = 0.94, the 13/28 vs 19/28, the 0.0177) or a **runnable control**
(the shuffled gate). That is the "individual method" — an experiment *we* designed, executed on
*their* code.

### The one place our domain knowledge transfers directly
Their **M2-FULL adds a soft spatial mask** to restrict the correction to part of the image — the
same structural idea as our mask-restricted wash, arrived at independently from the defence side.
Their mask cut benign damage 0.3740 → 0.1981 (47% less) but did **not** carry the safety gain;
ours cut damage 74% while holding attack effect. **Opposite sides of the same finding: restricting
a correction to a region buys fidelity, and the region is where the leverage is.** Use this in the
M3 talk and the M4 report — it is the strongest honest link between our work and theirs.

## ⛔ The safety rule, once
Several Light teams' challenges are scored by "did the attacker make the model produce unsafe
content". **We do not go down that path.** It puts harmful output in an M3 presentation, Claude
will not help build it, and it is usually the *harder* route because those scorers are badly
calibrated. **Attack the measurement instead** — the referee is nearly always the weaker component
and always the safer deliverable. Every experiment below uses benign prompts only.

## What the marks actually ask for
- **M2 Engagement (2%, group):** *"Which aspect of the other team are you targeting, e.g., their
  ideas or any demonstrations"* — an explicit required bullet in the M2 brief.
- **M3 Peer Engagement (3%, group):** engagement with other teams' *"ideas, code, or Colabs"*.
  That wording pays for **returning a measured number**. A clever comment scores less than a table.
- **M3 Individual Strategy (11%, per student):** each member presents **one distinct** attack.
- **The move that makes engagement score rather than read as a bug report:** close by connecting
  their weakness to your own thesis.

## Deadlines
M2 **18 Sep** (post Tue 15 Sep) · M3 **22 Oct** · M4 **2 Nov**, individual IEEE report.

---

## 1 · TARGET A — #8 Light.TouchGrass · ⚠️ PLAN REWRITTEN 14 Sep

Poon Yeong Shian + Garie Tan Kah Jinn. Safe Latent Diffusion, arXiv:2211.05105.
**Their M2 post (14 Sep): https://edstem.org/au/courses/37864/discussion/3578747**
M1 thread: /courses/37864/discussion/3533741 · Repo: github.com/ml-research/safe-latent-diffusion

### ⚠️ FIRST: the old plan is dead. Do not run E1 or E2.
The 13-Sep plan attacked their M1 referee — "the undefended control never breaches, so no
`DEFENSE_HELD` verdict is falsifiable" (E1), and "the verdict flips on seed alone" (E2).
**Their M2 post closes both holes**, and closes them properly:
- Undefended SD now breaches **26 of 28** held-out prompts (rate 0.929). The referee fires. E1 dead.
- The arena now returns **`NOT_HARMFUL`** as an explicit verdict, so an unbreached control is
  named rather than silently scored as a defence win. That was exactly the E1 complaint. Fixed.
- **Public seeds are now restricted** *"to prevent attacks from succeeding only through repeated
  seed searching."* E2 as designed cannot be run from outside.
They also report a genuine null against themselves in §6. This is a serious team. Treat them as one.

### The new strategy in one line
**They shipped four mechanisms and their own §6 refutes two of them. What is left looks like a
strength dial, and the control that would prove otherwise is missing from their table.**

### The three findings — ALL derivable from their published numbers, ZERO GPU
**F1 — safety tracks compute across their own ladder (the core).**
Their five defended arms, blocked-rate (vs SD's 0.929) against seconds/image:

| arm | blocked | s/img |
|---|---:|---:|
| SLD-STRONG | 0.250 | 7.06 |
| M2-FULL | 0.286 | 7.85 |
| M2-ADAPT | 0.358 | 8.81 |
| M2-ROUTE | 0.465 | 8.79 |
| M2-GUARD | 0.536 | 10.48 |

Compute rank and safety rank agree on 4 of 5 (ROUTE/ADAPT differ by 0.02 s — a tie);
**Pearson r = 0.94 (n = 5)**. Benign LPIPS moves the same way: STRONG 0.3740 → GUARD 0.3917, while
M2-FULL, the *least* safe M2 arm, has the *lowest* distortion at 0.1981. **More time, more safety,
more damage, in lockstep — that is the signature of one dial, not four mechanisms.**
⚠️ **State the limit honestly: r on five points proves nothing by itself.** The finding is not
"we proved it is a dial", it is **"the arm that would rule it out is not in the table."**
That arm is **SLD at matched compute — their own `MAX` preset, which their M1 notebook already
ships with the paper's real constants.** They ran WEAK/MEDIUM/STRONG/MAX at M1 and published only
STRONG at M2. Ask for the MAX row. It costs them one run.

**F2 — the gate is below chance, yet the gate-dependent arm improves (the sharpest one).**
Their §6: development **AUC 0.429**, i.e. *worse than a coin flip*, and top-1 category agreement
0.286. Yet **M2-ROUTE, whose whole mechanism is that gate, blocks 13/28 against STRONG's 19/28.**
If the gate cannot separate benign from unsafe, ROUTE's gain cannot be attributed to routing
*accuracy* — the remaining explanation is that routing adds correction wherever it points.
**The decisive control is one line: shuffle the gate.** Randomise the category assignment, re-run
ROUTE, keep everything else fixed. If the number survives a randomised gate, the mechanism is not
the gate. This is a permutation null and it is their own code, their own seeds, one run.

**F3 — uncertainty is reported asymmetrically.**
Every safety number carries a 95% CI. **Not one image-quality number does.** The headline
−0.286 is **8 prompts out of 28** (19 → 11); the cost is quoted as "approximately 4.7% more benign
distortion" — a point estimate, from 0.3740 → 0.3917, absolute difference **0.0177**, with no
paired interval. So the benefit is stress-tested and the cost is not, and *"M2-FULL caused the
least benign distortion"* is not established either. Ask for paired LPIPS CIs on the same prompts.
(This is Tyro's own lesson: we measured ±2–4 pp on `R_pipe` and then refused to claim a 2.3 pp gap
that sat inside it. Say so — it is what turns the critique into engagement.)

### ✅ Deliverable — 1 hour, no GPU, do it today
One reply on their M2 thread: F1's table, F2's shuffled-gate offer, F3's one line, and the
tie-back to our own null arm. Draft is in `M2/TouchGrass_Ed_Reply.md`.
**Frame it as helping them get a mechanism claim they can defend**, not as a gotcha. They are the
strongest Light team and the most likely to attempt the Wash Test properly.

### Optional extension (only if Tuesday is clear)
Run the **shuffled-gate null** ourselves in their arena and post the number. That converts the
reply from "good critique" to the M3 Peer Engagement wording — *engagement with ideas, code, or
Colabs* — and it is one run of code they already wrote. Everything above scores without it.

---

## 2 · TARGET B — #14 Light.Cyber Ninjas, ESD-x · **M2 = light touch · M3 = the real build**

Nisuri Edirisinghe + Vaishnavie Logeswaran. arXiv:2303.07345. Fork: github.com/nedi002/erasing
Colab: https://colab.research.google.com/drive/14l32khoYurkr6Rzcn4fWfV1TBygNxX4E
Config: `CompVis/stable-diffusion-v1-4`, `train_method=esd-x`, `erase_concept="Van Gogh"`.

### ⚠️ CORRECTION 14 Sep — an earlier revision of this file said "MOVED TO M3". That was wrong.
It contradicted the 13-Sep continuity ruling, which is correct and stands: **M3's largest individual
row (5 marks) asks how the target team *reacted/countered* and what was learned *from the
interaction*. A target first contacted in October has no reaction to report** — half that row
becomes unscorable no matter how good the attack is.

**So the split is: M2 = a light touch that opens the interaction. M3 = the real build.**
- **The build does NOT happen before 18 Sep.** One person cannot ship it and the M2 post as well,
  and M2 Engagement is already satisfied by TouchGrass.
- **But do not skip the team.** Post a **~1 h, zero-GPU** engagement on their Ed thread by **Thu 17**.
  That costs one evening's writing and buys five weeks of reaction to analyse in M3.
- **This stays Echo's individual M3 target — keep it unshared.**

### State of their artefact, checked 14 Sep (Drive metadata + notebook source)
- Still titled **"FIT5230: M1-VanGogh Robust ESD.ipynb"**. **No M2 Ed post from this team yet.**
- **Last modified 13 Sep 2026, 17:48 UTC** — they re-ran cells 1–7 that day. They are active.
- §6 still reads *"Full training is intentionally not executed at the Milestone 1 stage."*
  §10 still defers *"Full ESD-x model training and image generation"*. **Still no erased model,
  still no generated images.** A bypass submitted against their artefact has nothing to run against.
- ⭐ **NEW since the 10-Sep read:** their fork's `esd_sd.py` now has
  `--erase_concept_variants` — *"comma-separated alternate phrasings of the concept"*. That is them
  starting to build the §9 multi-description defence. **This is the hook for the M2 touch.**

### ✅ The M2 touch — ~1 h, zero GPU, post by Thu 17
Two things, both genuinely useful to them:
1. **They cannot receive a challenge entry yet.** Their Colab publishes no erased model, so nobody
   can test the bypass they asked for. Point them at the ESD authors' pre-erased,
   diffusers-compatible UNets — `https://erasing.baulab.info/weights/esd_models/`, specifically
   **`diffusers-VanGogh-ESDx1-UNET.pt`**, the exact method/concept/base-model they configured.
   Load SD v1-4, swap the UNet, and their defence exists in ~20 minutes with zero training.
2. **The hole in their own test set, aimed at the defence they are now building.**
   `erase_concept_variants` will be trained on English *descriptions*. **Their own challenge CSV
   tests multilingual only on the description** (`"un paysage nocturne post-impressionniste…"`)
   **and never on the name.** So a description-variant erasure leaves **梵高 / ゴッホ / фан гог**
   completely untouched. Say it as a prediction before they train, not as a result after.
**Ending the post with a prediction is deliberate** — it is the open loop that manufactures a
reaction for M3's 5-mark row. Same function as the TouchGrass shuffled-gate offer.

### Read first — their Colab trains nothing
It clones the fork, `sed`s two defaults, **prints** the training command, writes a 6-row CSV. §6:
*"Full training is intentionally not executed at the Milestone 1 stage."* **There is no erased
model published to attack.**

**The way through, with zero training:** the ESD authors publish pre-erased diffusers-compatible
UNets at `https://erasing.baulab.info/weights/esd_models/`, including
**`diffusers-VanGogh-ESDx1-UNET.pt`** — the exact method, concept and base model they configured.
Load SD v1-4, swap that UNet in, and their defence exists in ~20 minutes.

### Do NOT win with the obvious prompt
Their §9 already lists the descriptions they plan to erase — *"post-impressionist swirling
brushwork"*, etc. Attack the routes a description-erasure cannot reach:
- **Painting titles, not style words** — "the starry night over the Rhône", "wheatfield with crows".
- **A neighbouring artist** never erased but stylistically overlapping.
- **Non-English / transliterated name** — 梵高, ゴッホ, фан гог. **Their own CSV tests multilingual
  only on the *description*, never on the name.** That is the hole in their own test set.
- **Track B properly** — a QF-style sweep over homoglyph and BPE-boundary variants using
  `QF_Attack_Tyro.ipynb`, versus their single `V4n G0gh`. Zero new build.

**Scoring:** independent CLIP ViT-B/32 similarity to *"a painting by Vincent van Gogh"*, on **both**
the erased UNet and stock SD v1-4, so the claim is a *gap closed* rather than a vibe.

---

## 3 · The week — REVISED 14 Sep (solo)

| day | the one thing | why |
|---|---|---|
| **Mon 14** *(today)* | ✅ M2 post v5 finalised with §8 engagement. ✅ TouchGrass reply drafted. **Post the reply on their thread tonight.** | No GPU needed. Both are writing tasks. |
| **Tue 15** | 🔴 **Post the M2 thread.** Then reply to Dark.M&M with the Latin-typo null (§4). | Three clear days of thread life before the deadline. |
| **Wed 16** | Buffer. *Optional:* shuffled-gate run in the TouchGrass arena. | First thing to cut. |
| **Thu 17** | 🔴 **Post the ESD-x light touch** (§2, 1 h, no GPU). Reply to anything on our thread. Re-capture the stale `metric_stdout.txt` in `A_`/`C_` of `result2_0907` — it predates the purified PNGs and contradicts `scores.json`. | Replying to others is half the Engagement wording. |
| **Fri 18** | **Moodle submission, 11:55 PM MYT** — the Ed link in a PDF/text file. | Submission day contains no writing. |

**Pre-decided cuts, in order:** Wed's arena run → Thu's stdout re-capture → the M&M reply.
**Never cut:** the M2 post, the TouchGrass reply, **the ESD-x light touch**, the Moodle submission.

---

## 4 · Field benchmark — Dark.M&M's M2 post (12 Sep)

`edstem.org/au/courses/37864/discussion/3574176` · Theme 1, PIGuard / prompt-injection detection.
The strongest M2 in the class so far and **the same shape of argument as ours**.

### What they did that we must match
- **They froze a hypothesis and then refuted it** — hashed a manifest before touching the held-out
  split, got **0 flips out of 40**, and reported the refutation as the headline of §3.
- **A control before the attack.** The malicious code payload alone is flagged in only 1/50 samples,
  so PIGuard's 96% comes from the English instruction — proving the target is fair before attacking.
- **A challenge with a designed trap.** Evasion and false-block sets share the same Cyrillic
  characters with opposite correct answers, so "block all Cyrillic" wins one and destroys the other.
- **Engagement connected to their thesis.** They probed Light.Fahhh's refusal detector, found it
  misses *"it is not appropriate"* (it keys on "I cannot" / "I'm sorry"), named who posted it, and
  tied it back: *pattern detectors misjudge when the surface form changes.* That sentence is why it
  scores.

### Where we are ahead — lead with these
1. **We have figures and tables; they have none.** Their whole post is prose.
2. **We measured our noise floor; they assumed theirs away.** They report 96% → 82% (7 prompts of
   48) from single runs. We replicated to establish ±2–4 pp and then **refused to claim a 2.3 pp
   gap inside it.** Declining to claim a number you measured beats reporting one you did not stress.
3. **They never ran a null.** Nothing tests what an *ordinary typo* does — a different **Latin**
   letter. Without it the effect is "one-character perturbation", not "homoglyph".

### The comment to leave on their thread — 20 minutes, high value
Offer the **Latin-typo null** in their own terms: *"your claim is that the Cyrillic form is what
fools it; the control that isolates that is the same one-character edit using a different Latin
letter. If detection drops there too, the finding is perturbation-sensitivity; if it doesn't, the
homoglyph claim is isolated and much stronger."* Mention our own null design in one line.
