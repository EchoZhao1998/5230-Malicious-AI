# D1 · `R_edit` — MEASURED 8 Sep 2026, on `M2_1st_test_result2_0907`

**No GPU was needed and no re-run was needed.** These are CLIPScores of the edited images
already sitting in the archive, scored against the prompt `"a person in an airplane"` with
`openai/clip-vit-base-patch32`.

| image | `S_clean` | `S_protected` | **P** | `S_pur` A | B | C |
|---|---|---|---|---|---|---|
| `1233476865_1` (the boy) | 24.14 | **29.19** | **−5.05** | 24.36 | 24.63 | 26.50 |
| `1525918600_1` (the man) | 29.32 | 27.49 | **+1.83** | 28.30 | 28.59 | 28.61 |

`P = S_clean − S_protected` is **protection efficacy**: how much prompt-meaning the shield
destroyed. It is supposed to be positive.

---

## The headline: on image 1, protection efficacy is NEGATIVE

**PhotoGuard made the edit match the prompt *better* than no protection at all.**
`S_protected` = 29.19 against `S_clean` = 24.14 — a five-point *improvement*.

Go and look at `m2_panel.png` and you can see it without any metric. `edited CLEAN` puts the boy
against an ambiguous pale headrest. `edited PROTECTED` puts him beside an unmistakable aircraft
window with sky and ground outside. **The protected edit is the better airplane picture.** CLIP
and your own eyes agree.

> A lock that holds the door open is not a weak lock. It is not a lock.

This is not "the shield is weak, we need more iterations." A negative `P` means the quantity
`R_pipe` divides by does not exist on this image, so **the +5.2% from M1 and every arm gap in
`m2_tradeoff.png` are ratios over a denominator with no meaning.**

## Image 2 is positive but tiny

`P` = +1.83 CLIPScore points. Two *innocent* edits of the same image at different seeds also
differ by roughly this much, so **+1.83 is probably inside the noise, not above it.** D2 measures
that floor directly (`clip_seed_gap`); until it has been run, treat image 2 as unresolved rather
than as a win.

If it does clear the floor, the wash restores 44–61% of the lost meaning — and note that
**C (61%) ≥ B (60%) > A (44%)**, the same ordering the fidelity axis gives, on the one image
where the shield arguably engaged at all.

---

## What this changes, concretely

**1 · `R_pipe` is retired as a headline.** Not deleted — reported, with this table underneath it
explaining why it cannot carry a claim at these settings. That is a stronger M2 section than a
number would have been: *Technical depth* rewards understanding your instrument.

**2 · The M2 claim becomes the fidelity claim, which is untouched by all of this.**
SSIM/LPIPS(purified, clean) compares two still photographs and never invokes the diffusion
editor — which is exactly why it reproduced to four decimals while `R_pipe` wandered.

> *"Mask-restricted purification removes IMPRESS's damage in the 70% of pixels the editor
> repaints anyway: LPIPS 0.12 → 0.05, SSIM vs clean 0.75 → 0.93, mean damage 4.7 → 1.4 grey
> levels, at identical compute. Measured on every image, reproducible to four decimals."*

**3 · `pg_eps` moves from M3 to M2, as a precondition rather than an extension.**
Limitation 1 already said `pg_eps` was the untested lever. This is the evidence that it is not
optional: until the shield engages, nothing downstream of it can be scored — not our arms, and
not a single challenge entry.

**4 · The challenge cannot be published until the reference shield engages.**
See `challenge/DRYRUN-NOTES.md`, risk R1. Our own guard rail would fire on our own reference
entry.

---

### Why this is a good result to have found, six days before the deadline

Every rubric row this touches rewards it. *Technical depth* is not "our number went up" — it is
"we built the control that could have embarrassed us, ran it, and it did." A team that reports
`R_pipe = +5.2%` without noticing the denominator is negative on half their sample has a number.
A team that catches it has a **finding about the measurement**, which is the rarer thing and the
harder one to fake.

The one honest caveat to state alongside it: **n = 2.** Two images cannot establish that
PhotoGuard fails in general — only that it failed here, at `(40, 2)`, `pg_eps = 16`, on this
editor and this prompt. Say exactly that and no more.
