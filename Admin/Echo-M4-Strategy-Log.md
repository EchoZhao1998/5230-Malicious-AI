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

## Week 9 (21–27 Sep)

## Week 10 (28 Sep–4 Oct) — individual strategy: FFT → targeted low-pass filter

## Week 11 (5–11 Oct) — sketch both M4 demos (EOT loop + switch-sides defense)

## Week 12 (12–18 Oct)
