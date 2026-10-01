# Echo — Private M4 Strategy Log (Weeks 2–12)

> **This is my individual, private log. NOT the shared Tyro tracker.**
> M4 rubric wants a *strategy diary*, not a task list: "strategies used to maximize
> marks & advantage over other teams **including my own teammate**." Each entry should
> answer *why I did it and what edge it bought me*, not just *what I did*.
> Worth 3% on its own; reconstructing it in November is misery. Two honest lines a week is enough.

**How I fill this (tell Claude these four things each week):**
1. **Did** — what I personally worked on (mine alone, not Nissa's).
2. **Why** — the strategic reason. What advantage was I chasing?
3. **Learned / adapted** — what changed my mind or plan.
4. **Interaction** — anything with other teams or with Nissa (who did what).

---

## Week 2 (3–9 Aug)
- **Did:** Set up the team's shared Google Drive with a subfolder structure as our collaboration space and seeded it with primers so we both build the fundamental concepts. Locked the team name and the Dark side, and sent the tutor registration email. Read the PhotoGuard paper end-to-end to pin down exactly what we're attacking, and wrote myself a working definition of *defense* vs *attack* for this theme (defense = add invisible noise so an AI editor garbles the image; attack = strip that noise so editing works again). Ran the Colab feasibility smoke test and polished the full four-milestone plan.
- **Why:** Two edges. Strategically, registering early secures our Theme-2 Dark slot before the 10-team cap fills, and owning the plan + shared space cements my role as research/strategy lead — where 26 of 50 individual marks live. Pedagogically, I won't write code I don't understand: grasping the *logic* of the attack first is what lets me later judge whether the code is doing the right thing and chasing the right goal.
- **Learned / method:** Picked PhotoGuard as our baseline via a quick literature review, then stress-tested the whole plan by cross-checking it against the AI tools we each prefer — a sanity check that a two-person team of newcomers can actually deliver it. Confirmed compute is not the bottleneck (10 min GPU for a 50-image run vs a 15–30 hr budget); coordination is.
- **Interaction:** Briefed Nissa and gave her the smoke-test notebook to read as a warm-up. Nissa proactively recommended arXiv:2304.02234 (JPEG compression breaks protective perturbations) as support for our JPEG attack — an on-target contribution that becomes a citation for M1.

## Week 3 (10–16 Aug)
- **Did:** Locked the baseline paper — not by reading abstracts, but by *running the code*. Stood up both candidates on Colab (IMPRESS, NeurIPS 2023, and QF / Query-Free, arXiv:2303.16378) and pushed IMPRESS's PhotoGuard pipeline end-to-end on a single T4. Also emailed the lecturer (Jessie) to get the milestone requirements pinned down in writing rather than inferred from the PDF.
- **Why:** The lecturer's bar is that a baseline must ship **runnable code + replicable metrics** — a paper that only *sounds* right is a trap you discover in week 8. Testing first buys me the one thing that can't be recovered later: certainty that our comparison numbers will actually exist. Emailing Jessie is cheap insurance on the same axis — a written requirement beats my interpretation of a brief, and it puts my name on the record as the team's point of contact.
- **Learned / adapted:** Two corrections. (1) **QF is the wrong axis.** It perturbs the *text prompt* through the CLIP encoder, so it's a cousin of PhotoGuard — another *disruptor* — not something that attacks a protected image. Demoted it to Related Work. Same fate for the JPEG-bypass paper (arXiv:2304.02234): no official code → not a valid baseline, but the JPEG trick is one line to re-implement, so it survives as our simplest ablation. (2) **Path A confirmed:** baseline = IMPRESS, target = PhotoGuard, our contribution = a purification stack (JPEG → blur → down/upscale → DiffPure) plugged into IMPRESS's metric harness. Practically, IMPRESS's 2023 code is rotted — the `runwayml` SD repo was deleted from HuggingFace and `sewar` is missing from requirements; both patched, and the repo's quick-start script assumes 4 GPUs, so everything runs with `--parallel_index=-1 --device="cuda:0"`. Debugging someone else's code *is* the advantage: every other team hits these same three walls in week 6.
- **Interaction:** QF was Nissa's suggestion, so I tested it properly before ruling it out and wrote up the reasoning rather than just saying no — keeps her contributing, and the write-up itself is Related Work content we need anyway. I own the working Colab recipe end to end.

### 16 Aug addendum — measurement, challenge design, and cutting the iteration cost

- **Did:** Built the two things the pipeline was missing. (1) A **quantitative attack-success metric**: IMPRESS reports image-fidelity numbers but judges whether the *edit* succeeded by eye, so I added an independent-CLIP score of each edited image against the edit prompt, reduced to one headline number — restoration rate `R = (S_pur − S_prot) / (S_clean − S_prot)`, where 1.0 = editor fully restored, 0 = shield held. (2) An **FFT band analysis** of clean vs protected images that locates the frequency band PhotoGuard injects into, plus a Butterworth low-pass built to that spec and a private detector built from the same statistic. Then I found that PhotoGuard's **encoder attack** costs ~30 s/image against the diffusion attack's ~77 min, and rebuilt the whole toolkit to run standalone on a blank T4 — protect, purify four ways, edit, measure, ~15 min end to end — including a 15-line reimplementation of IMPRESS's actual objective so the comparison isn't against a straw man. Also read the M1 rubric properly and designed our interactive challenge, and drafted the Ed post.
- **Why:** Three separate edges. **The metric is the real one.** Without a success axis you cannot compare purifiers at all — you are reduced to arguing about screenshots, and my "surgical beats brute force" claim stays an assertion instead of something falsifiable. It is also the piece Nissa's model-mismatch angle needs before it can produce a number, which makes me the dependency rather than the dependent — that is exactly what M3's *Integration & Role* asks you to demonstrate. **The 77-minute problem was iteration latency, not compute.** At one experiment per evening I could not develop ideas; at 30 seconds I can test a dozen before dinner. The fix was to find a cheaper version of the expensive stage rather than to cut scope. **The challenge is engagement insurance.** M1's challenge-design mark is 0.5%, but M2 *Engagement* (2%) and M3 *Peer Engagement* (3%) both depend on other teams actually attempting it — so I built three tiers with a deliberately five-minute Tier 1 on-ramp, because a clever challenge nobody tries costs 5%, not 0.5%.
- **Learned / adapted:** Three corrections. (1) **I was too quick to reject QF.** It stays wrong as an M1–M3 baseline, but it maps directly onto two M4 rows — *Unconstrained Enhancement* (4%) and *Role Reversal* (5%) — because "PhotoGuard guards the pixels, nobody guards the prompt" is a two-flank attack with a working demo behind it. The general lesson: check the individual rubric before discarding a paper, since M4 rewards breadth that M1–M3 penalise. (2) **Over-filtering is as detectable as under-filtering.** A purified image that is unnaturally *smooth* leaves as clear a fingerprint as one with residual noise — so the surgical filter has a floor as well as a ceiling, and I tune toward matching clean rather than toward maximum stripping. (3) A methodological one worth keeping: my verification harness reported a false failure because the stand-in autoencoder's fixed point happened to coincide with the attack's target. **A control that accidentally agrees with the hypothesis returns a confident wrong answer** — I now check what my baseline is actually baselining.
- **Interaction:** QF was Nissa's find, and rather than veto it I relocated it to where it earns marks and gave her the reasoning in writing — she keeps a contribution, and I get Related Work plus an M4 section out of it. I also handed her the analysis toolkit, since her model-mismatch attack now has a metric to plug into and a standalone harness that doesn't require her to fight the IMPRESS install. Critical path still runs through me: I own the metric, the frequency analysis, the challenge design and the Ed post, so nothing stalls if she goes quiet.

## Week 4 (17–23 Aug)
*(Weeks 4–7 written up 13 Sep from my working notes — I let the diary slip while the pipeline was
moving fastest, which is exactly when the strategic reasoning is worth capturing. Logged the lesson
rather than pretending the entries were contemporaneous.)*

- **Did:** Stopped treating IMPRESS as a black box and read it properly. `impress.py` turns out to
  be **25 lines** — the entire published attack is a short optimisation loop asking the model's own
  autoencoder to agree with the image again. Then I settled, in writing, exactly what is ours and
  what is theirs, and designed the M1 challenge (the **Tyro Wash Test**) rather than leaving it as
  a slogan.
- **Why:** Two edges. First, **the provenance sentence is a defensive weapon.** Some Light team
  will eventually say "you just ran their code", and the only reply that survives is *the algorithm
  is theirs and unmodified; the eleven repairs, the harness, the metric and the archive are ours* —
  which is both true and stronger than claiming I modified an algorithm I did not. Deliberately
  leaving `impress.py` untouched is the point: a repaired reference implementation is only useful
  as a baseline if it is still the reference. Second, I found a **verifiable gap** I can stand on:
  the IMPRESS abstract offers the code as *"an evaluation platform for future protection methods"*,
  and the released code ships two hardcoded folder contracts and no generic entry point. Provable
  with a `git clone` and two `ls`. That gives me a contribution I can state in one line — *build the
  generic entry point the paper's own claim implies* — which is a far better position than
  "we invented something".
- **Learned / adapted:** The challenge design rule I keep reusing: **a challenge with a single axis
  has a degenerate winner.** Score robustness alone and the winning move is to perturb until the
  photo is noise. So Track A scores robustness *and* perceptual cost on one scatter, with the
  ranking budget set at LPIPS ≤ 0.10 — precisely the allowance my own purifier gets. Symmetric,
  principled, and from no paper. Generalisable: whenever designing a benchmark, ask what the
  laziest winning move is, then measure its cost. I also settled that challengers are **not**
  restricted to PhotoGuard, because `impress()` never asks how the perturbation got there — so the
  challenge is defined by an *interface*, not a method. Restricting it would have made it
  unattemptable by nine of ten Light teams and killed the participation the marks depend on.
  And I noticed the framing trap: "we built an evaluation platform" is a *Light-sounding* sentence,
  so I lead attacker-first — a purifier that works without knowing which protection it removes is
  more dangerous than a tailored one.
- **Interaction:** Handed Nissa the code walkthrough rather than the conclusions, so she could
  audit the 25 lines herself. She delivered her two M1 sections on time on 22 Aug. Recorded the
  division honestly: I own the baseline claim, the challenge design and the harness.

## Week 5 (24–30 Aug) — M1 due 28 Aug

- **Did:** Shipped M1. The pipeline ran end to end on a **Kaggle T4** (not Colab) and scored
  `R_pipe = +5.2%` on one image and **−1.2%** on the other. I published both. I also measured what
  the wash *cost*: LPIPS 0.15 against a shield that cost ~0.018 to apply.
- **Why:** The negative number was the decision. It would have been easy to report the positive
  image and call the run a success, and it would have been the expensive kind of easy — every
  later milestone would have been built on a result I could not reproduce. Publishing a
  contradiction at M1 is cheap; discovering it at M3 in front of the class is not. The strategic
  read: **an early honest negative buys you the right to be believed later**, and M2's entire
  finding is only credible because M1's post already admitted the instrument was shaky.
- **Learned / adapted:** Two things, one of which reshaped the whole project. (1) **My attack was
  breaking my own published budget.** I had told other teams their shields must stay under LPIPS
  0.10, while my purifier was spending 0.15 — nine times what the protection it removes cost. *The
  bar is two dots, not one:* a solvent that damages the photograph more than the dye did has not
  won anything. That single realisation is what made the mask idea inevitable. (2) Infrastructure
  lessons that cost real hours and are now written down: Colab's P100 is sm_60 and effectively dead
  for this stack, outputs vanish on disconnect, `requirements.txt` is unpinned upstream, and
  `notebook_login()` / `HfFolder` no longer behave as the 2023 code assumes.
- **Interaction:** Nissa's sections went in as written. I did the integration, the run and the
  post, which is the pattern I should expect to continue — so from here I plan every deliverable to
  be shippable by me alone, and treat anything she adds as upside rather than as a dependency.

## Week 6 (31 Aug–6 Sep)

- **Did:** Turned M1's cost problem into M2's method. Measured how much each region of the image
  actually moves between a clean photo and its edit — **4–7 grey levels inside the white inpainting
  mask, 86–96 outside** — and used that to restrict the wash to the region the editor *preserves*.
  Four lines of arithmetic. Then rebuilt the experiment as **four arms including a null**, and
  reorganised the whole repo so the archive, not the prose, is the source of truth.
- **Why:** I wanted a contribution that is **small enough to be obviously mine and obviously
  correct**. Four lines plus a measurement beats a clever architecture I cannot defend in a
  15-minute presentation, and the diff *is* the contribution — which is exactly what the M2
  "changes you've made to the reference Colab" row asks for. The null arm is the part I am most
  pleased with strategically: it skips purification entirely, so `R_pipe = 0` by construction and
  anything worse than it did more harm than not attacking at all. It costs one extra run and it
  makes the table impossible to argue with. Building the defender's starter notebook in the same
  week was deliberate too — the challenge is the only lever I have on other teams' behaviour, and a
  challenge shipped late is a challenge nobody enters.
- **Learned / adapted:** The smoke run caught that **my mask polarity was backwards.** I had
  assumed white meant repainted. Had I not checked, the method would have been exactly inverted and
  the numbers would still have looked plausible. **Verify polarity by measurement, never by
  intuition** — and more generally, run the cheap smoke version first: it fails in four minutes
  instead of forty. I also fixed a resolution bug (always resample toward the *smaller* image) that
  had been quietly voiding earlier diagnostics, and found the `pur_iters` gap — I had been running
  at 100 iterations where the reference script uses 1000, which I promoted from an embarrassment
  into arm B, a legitimate control.
- **Interaction:** Kept the shared Drive mirrored and the README as the map, so the project stays
  legible to Nissa without a handover conversation. No new input from her this week.

## Week 7 (7–13 Sep)

- **Did:** Ran the four arms, then spent most of the week attacking **my own instrument** rather
  than improving my score. Three controls: a seed floor (edit the clean image twice with different
  seeds), an L2-matched random-noise null, and a genuine re-run at double shield strength. Then
  recomputed every published number directly from the archived PNGs, built the challenge zip,
  chose the engagement targets, and rewrote the M2 post for an outside reader.
- **Why:** The controls were the highest-value thing available to me, and they are not a detour —
  they are the milestone. **PhotoGuard at its own settings moves the image less than one grey
  level, and the editor's own seed-to-seed variation disturbs the edit *more* than the shield
  does.** So IMPRESS's own published evaluation metric cannot detect the defence it was built to
  evaluate. That is a finding about the baseline paper, not about me, and it is worth far more than
  another percentage point of `R_pipe` — a team that reports a number is competing on the same axis
  as everyone else; a team that shows the axis is broken is not. The rewrite for outside readers is
  the same logic applied to marks: the Engagement and Peer Engagement rows (2% + 3%) only pay if
  other teams can actually follow the workflow and enter the challenge.
- **Learned / adapted:** Three corrections, all of which I would have published wrong. (1) **A
  headline number in my own README was a transcription error** — LPIPS 0.12 → 0.05 was a pair
  matching no run I ever did. Recomputing from the PNGs gave 0.150 → 0.039, which is 26%, and makes
  *"a quarter of the perceptual cost"* literally true where the wrong pair would have made it
  overstated. **The archive is the source of truth; the prose is a cache.** (2) **The documented
  strength knob is inert.** `pg_eps` 16 vs 32 produces the same shield to within 1%, because at
  `pg_iters=40, pg_step_size=1` the optimiser never travels far enough to reach the L2 ball. I had
  planned a whole M3 sweep on that lever; closing the gate early saved the week. (3) **My published
  engagement gate was wrong.** I had promised to report `R_pipe` only when SSIM ≤ 0.85; measuring
  the actual seed floor across ten images gave **0.285–0.707**, so 0.85 would have passed
  everything — including my own shield. Replaced with a measured per-image floor, and I will
  publish the correction rather than quietly change it. The through-line: **a control that
  accidentally agrees with your hypothesis returns a confident wrong answer.**
- **Interaction:** Chose **#14 Cyber Ninjas (ESD-x Van Gogh)** as my own engagement target and read
  their Colab closely enough to find that it trains nothing — so I also found the route round it
  (the authors publish pre-erased UNets). Nissa named **#8 TouchGrass** as her target but has
  produced no attack plan, so I assessed it myself: their arena is the best-engineered artefact in
  the class, but their own sanity-check probe failed and their scorer has never registered a
  breach. **I am taking both targets.** Two distinct targets is also the correct hedge for M3,
  where 11% is assessed individually on *one distinct strategy each* — keeping ESD-x as mine
  protects that regardless of what she delivers.

## Week 8 (14–20 Sep) — M2 due 18 Sep
*(planned in advance on 13 Sep, deliberately — see the jam note below)*

- **Plan:** Sun — publish the challenge pack (the two blockers are a Colab share link and a host
  for a 3.6 MB zip; neither needs a second person). Mon — TouchGrass: replicate their own failed
  undefended-control probe across all five public seeds. Tue — post it to their thread. Wed —
  ESD-x: swap in the pre-erased UNet and sweep the routes their description-erasure cannot reach
  (painting titles, neighbouring artist, non-English name, homoglyphs). Thu — finalise the M2 post
  and re-capture one stale metric dump. Fri — submit.
- **Why plan it a week out:** last milestone I discovered the real work in the last 48 hours. Three
  deliverables converge on Thursday, so Sunday and Monday are the buffer, and I have pre-decided
  the cut: **if the challenge pack is not public by Monday morning, ESD-x moves to M3.** It is a
  5-mark side-quest; the challenge is a group deliverable I publicly promised at M1 and it feeds
  four separate rubric rows. Deciding that now, while it is cheap, is worth more than deciding it
  on Thursday under pressure.
- **Strategic note on the target choice:** TouchGrass's literal win condition asks an attacker to
  generate content a detector flags as sexual or violent. I am not going there — it is the wrong
  thing to put in an M3 presentation, and it is also the *harder* path, because the gate is
  unpassable as published. **Attack the measurement instead.** It is the weaker component and
  always the safer deliverable, and it generalises: when a challenge's win condition requires
  producing harmful content, the referee is the real target.

### Week 8 — what actually happened *(written 19 Sep, one day still to run)*

- **Did:** Submitted M2 **three days early** (post PDF archived 15 Sep against a Fri 18 deadline)
  on the back of a fresh Colab cold run, and then spent the rest of the week on M3's foundations
  rather than on M2 polish. Recomputed the canonical four-arm table — **N 0.00 / A 9.51 / B 13.54 /
  C 14.48 `R_pipe`**, LPIPS 0.017 / 0.150 / 0.108 / **0.038** — rebuilt the challenge starter
  notebook (12 cells → 9, four number bugs in the published version corrected), read the M3 rubric
  off the brief line by line and wrote `M3/M3-PLAN.md`, decided to run the rest of the unit solo,
  drafted the cross-script prediction post, and on the 19th rebuilt the experiment notebook for
  **n = 10 with the engagement gate wired in** and mined Cyber Ninjas' newly released ESD-x
  baseline for their weaknesses.
- **Why:** Two reallocations, both made by reading rather than by building. **First, the rubric.**
  Of M3's 25 marks only **5** are "did the attack get better" — **11** are an individual strategy
  aimed at another team, 5 are Colab hygiene. My instinct all week was to improve the notebook;
  the marks say the notebook is the cheap half. Budgeting effort by row weight rather than by what
  is technically interesting is the single highest-leverage decision of the week, and it is only
  available to someone who reads the brief instead of inferring it. **Second, submitting early.**
  A milestone due date is a deadline, not a post date — other teams posted M2 up to a week ahead,
  and a thread that goes up early collects the replies the Engagement rows are actually worded
  around. Finishing on the 15th also bought me four clear days to think about M3 while everyone
  else was still writing M2.
- **Learned / adapted:** Three, and the first one changes what M3 *is*. **(1) My own engagement
  gate, applied in hindsight to my own published M2 images, fails them.** Per-image `ssim_adv` was
  0.5055 and 0.6404 against measured seed floors of 0.4721 and 0.4149 — **neither image engaged.**
  The shield never pushed the edit below what a seed change does by itself, so a large part of what
  `R_pipe` measured was ordinary generator variation. The M2 table is not wrong; it is a correctly
  measured quantity on a test that could not discriminate. So M3's first job is **the input, not
  the method** — sweep `pg_step_size`, fall back to `linf`, then re-run the same four arms
  unchanged. *We built a better stain remover and measured it on a shirt that was barely stained.*
  The generalisable form: **build the gate that can fail your own result, then actually run it on
  your own result.** I had published the gate as a rule for challengers and never turned it on
  myself. **(2) Two images was never a sample.** The ten measured seed floors span 0.28–0.71, a
  2.5× spread, so the two I happened to run could have been the easiest or the hardest pair in the
  set and nothing in the table would have said so. n = 10 is now pinned to exactly those ten
  images, and the finding will be reported as *how many of ten engaged*, never as a mean over
  images of unequal difficulty. **(3) The CLIP proxy is dead** — text-embedding distance cannot
  rank which prompts an erasure misses (ρ = +0.03; pooling flips the order). I had been carrying it
  as a cheap shortcut for the ESD-x work. Killing it early is the same move as closing the `pg_eps`
  gate in Week 7: **a knob you can prove is inert is worth more than a knob you keep hoping about.**
- **Interaction:** Read Cyber Ninjas' M2 closely enough to find three things their own write-up
  does not: both their checkpoints train for **100 iterations**, but the multi-descriptor arm splits
  those 100 across three phrasings, so the literal name gets ~33 — the two checkpoints differ in
  *what* and *how much* at once and any difference between them is unattributable (**this is my own
  `pur_iters` mistake from Week 6 in a different costume**, which is why I can raise it as
  experience rather than as a hit); their "no collateral damage to other artists" claim rests on one
  eyeballed image each, while their published Monet panel shows a **36% contrast drop** against
  unmodified SD; and their leetspeak excuse is **correct** — their own figure shows base SD
  rendering no Van Gogh style at all for `V@n G0gh`, so there was nothing to erase. I will concede
  that publicly, because conceding the half they are right about is what makes the half they are
  wrong about land. Their stated M3 is to add obfuscated spellings to training — they are about to
  patch the channel that carries no signal, while **梵高 / ゴッホ / фан гог** stay untrained and
  untested. That is my lane and it is still uncrowded. On the team: **Nissa has contributed nothing
  since M1.** Groups cannot be changed after formation, so I emailed the tutor, recorded it, and
  replanned every remaining deliverable as solo work — the brief permits individual projects
  outright, and M3's presentation instructions carry the matching wording, so the Integration row
  is answerable as *coordinated, did not land, adapted* rather than as *worked alone*.

- **Plan vs actual — the pre-decided cut fired.** I wrote on 13 Sep that *"if the challenge pack is
  not public by Monday morning, ESD-x moves to M3."* It did move, though for a second reason I had
  not anticipated: TouchGrass's win condition asks for harmful content, so I reduced it to a
  zero-GPU measurement critique and made ESD-x the October build. **Worth keeping: the cut I
  pre-decided while it was cheap was still the right cut when the reason for taking it turned out
  to be different from the one I predicted.** Pre-deciding bought the decision, not the forecast.

## Week 9 (21–27 Sep) — `pg_step_size` sweep (+ `linf` fallback) · pre-erased UNet + base SD v1-4 running

### Week 9 — what actually happened *(written 1 Oct; includes the 1 Oct close-out review)*

- **Plan vs actual.** The plan above was already overtaken on 19 Sep: the step sweep finished in
  Week 8, `linf` was dropped, and the stopping rule fired. So Week 9 became **moving the result onto
  the platform the brief actually accepts** — Colab — and closing IMPRESS. The ESD-x run did not
  start; it moved to Week 10 (notebook written 1 Oct).
- **Did:** (1) **25 Sep, `run_0925_0152`** — all four wash arms at n = 10 on **one shared protect
  stage** on Colab. This removed the one soft spot in the table: until then arm B came from a
  different session with its own shield. (2) The first 25 Sep attempt carried the four arms *and*
  the shield sweep in one session (~5.5 h) and died. I **split by question**: a separate sweep
  notebook that carries only the sweep. (3) **27 Sep, `sweep_0927_0210`** — the shield sweep at
  (16,1) / (64,4) / (256,4). Row (16,1) was **reused** from `run_0925_0152` instead of spending 39 min
  re-measuring a number I already owned, with a `measured_here = False` flag so the provenance
  travels with the data. (4) **1 Oct close-out review**: recomputed every number from the
  notebooks' own output tables, joined engagement with cost (**noticed AND within budget: 1 / 1 / 0
  of 10**), checked our shield against the reference code, and traced the visible noise.
- **Why:** The brief requires a **Colab link**; a Kaggle result, however good, is not the
  submittable artefact. And free Colab has no booking and drops idle sessions, so **the unit of
  work has to fit one session**. Splitting by question (wash vs shield) rather than by convenience
  means each notebook answers one thing and survives a disconnect on its own.
- **Learned / adapted:** Three. **(1) Check the reference parameters before writing the claim.**
  Same `eps` and `step` as PhotoGuard and IMPRESS — but **40 × 2 iterations against their
  200 × 10, 1/25 of the effort**, a cut I made for cost in August and had stopped seeing. It goes on
  the slide as a limitation, said by me before a marker asks. **(2) When a number and your eye
  disagree, make a picture of the difference.** LPIPS 0.027 said the eps 16 shield was invisible; my
  own eye said it was clearly visible. The ×5 difference image said both were partly right: the
  visible part is mostly a smooth glow and seam from **IMPRESS's save step** (identical at eps 16 and
  256), while PhotoGuard's own noise is a fine speckle inside the face that doubles from 16 to 256.
  Without that picture I would have presented an artifact of the baseline's code as "the shield".
  **(3) The finding is about the baseline's test, not about my wash.** On recovery, every arm is
  inside noise — mine included — because the shield barely changes the edit. On photo damage, the
  clean axis, my masked wash does **68% less damage than IMPRESS at the same compute**, and
  IMPRESS's own 10× budget buys nothing measurable. Claiming less than I measured, on purpose, is
  the stronger position.
- **Interaction:** None with other teams this week — this was group-row work on our own
  notebook. *(If the cross-script prediction went up on Cyber Ninjas' thread this week, add the
  date here.)* Nissa: nothing; plan remains solo.

## Week 10 (28 Sep–4 Oct) — four arms at the working setting · the four prompt buckets on both models
*(heading corrected 19 Sep: the individual strategy is the **ESD-x cross-script bypass**, not the FFT
filter. FFT is now conditional and secondary — it earns a slide only if the `pg_step_size` sweep
produces a shield that engages. Do not build it on spec.)*

## Week 11 (5–11 Oct) — the n=10 run · bypass table · FFT in/out decision · slides drafted
*(M4 demo sketches — EOT loop + switch-sides defence — move to after the M3 presentation.)*

## Week 12 (12–18 Oct) — clean end-to-end run committed **with outputs** · rehearse to 15 min
*(20–21 Oct is buffer only. No new work. M3 due 22 Oct.)*
