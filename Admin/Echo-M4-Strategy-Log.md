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

## Week 5 (24–30 Aug) — M1 due 28 Aug

## Week 6 (31 Aug–6 Sep)

## Week 7 (7–13 Sep)

## Week 8 (14–20 Sep) — M2 due 18 Sep

## Week 9 (21–27 Sep)

## Week 10 (28 Sep–4 Oct) — individual strategy: FFT → targeted low-pass filter

## Week 11 (5–11 Oct) — sketch both M4 demos (EOT loop + switch-sides defense)

## Week 12 (12–18 Oct)
