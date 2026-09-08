# Defend your own notebook — one page
*Dark.Tyro · Echo · for M1 (28 Aug) and reusable at the M3 presentation*

Not a script to read from. The point is that after one pass you can answer any of these in
your own words, because **you did all of this** — the notebook is a record of your decisions,
not something handed to you.

---

## The thirty-second version, if someone asks "what did you do?"

> We took an attack paper, IMPRESS, that strips protective noise off images so AI editors
> work again. The published code didn't run in 2026 — we fixed ten faults. Then we measured
> it properly against PhotoGuard and found it **recovers about 11% of the shield's damage at
> weak protection and nothing measurable once protection gets any real budget.** We also
> built two measurement instruments the baseline doesn't have, ready for M2.

That's it. Three sentences: repaired it, measured it, found where it breaks.

---

## Part 1 — the sweep *(this is your M1 result)*

| cell | one sentence | the question you'll get |
|---|---|---|
| **1–5** | Detect the GPU, clone IMPRESS, patch the 2023 code, fetch the faces. | *"Why patch in Python not sed?"* → macOS ships BSD sed, where `sed -i 's/…/…/'` fails. |
| **6** | **The only place parameters are defined.** Every path and command is an f-string off this dict. | *"Why one dict?"* → because a hard-coded parameter in a display cell showed us trial 1's images after we'd run trial 3. That was bug 9. |
| **7** | Trim to `N_IMAGES`. | *"Why at least 2?"* → `pg_metric` calls `torch.std()`, which returns `nan` on one sample. |
| **8** | The chain: protect → bridge → purify → edit → measure, plus archiving. | see the three fixes below |
| **9** | Run it. Catches out-of-memory per configuration so one dead cell doesn't cost the grid. | |
| **10** | Results table, `R_pipe`, and the sign test. | **the big one — see below** |
| **11** | The 3-panel figure. | *"Is that a fair comparison?"* → yes, and you can prove it: `pg_generate.py` re-seeds numpy and torch immediately before each of the three generations, same mask, same prompt, same steps. Every visible difference comes from the input image alone. Most teams can't say that. |

### The three fixes worth knowing cold

These are the ones that make you sound like you read the source, because you did.

- **Fix 5 — the folder contract is broken.** Protect writes `adv_<params>/`; purify reads
  `adapt_adv_<params>/`. Nobody wired them together. We added a bridge.
- **Fix 7 — the purified folder name carries no `pg_*` parameters.** So every protection
  strength writes purified output to the *same* directory, with no skip-if-exists guard.
  Run a new strength, forget to re-purify, and your "purified" panel silently belongs to a
  different experiment. **This does not raise an error.** We wipe before each config and
  archive under a stamped tag.
- **Fix 10 — `(200,10)` runs out of GPU memory.** We left it out rather than halve
  `diff_steps` for one point. *"Why not just lower it?"* → **a grid where one point used a
  different attack is not a grid.**

> If you only memorise one thing: **fixes 7 and 8 don't crash. They hand you the previous
> run's images with this run's label.** That's why they're the interesting ones.

---

## `R_pipe` — your headline number

$$R_{\text{pipe}} = \frac{\text{pur} - \text{adv}}{1 - \text{adv}}$$

**In words:** the shield knocked the pipeline down; `R_pipe` is the fraction of that damage
purification gave back.

**Why the denominator is `1 − adv`:** `pg_metric`'s SSIM is measured against the *edited clean*
image, so `1.0` means "the pipeline behaved exactly as if the photo had never been protected".
That's a free, principled ceiling — no third measurement needed.

| config | units | `R_pipe` |
|---|---|---|
| 40:2 | 80 | **+10.8 %** |
| 40:10 | 400 | −1.3 % |
| 200:2 | 400 | +2.7 % |

**Q: "You only have two images. How can you conclude anything?"**
This is the question, and you have a good answer:

> We don't read any single metric at n = 2. We read whether three independent metrics — PSNR,
> SSIM and VIF — agree on the **sign**. At 80 units all three move the same way, so something
> real happened. At 400 units they disagree, which is the signature of a quantity sitting at
> zero. We report the sign agreement, not the magnitude.

**Q: "Isn't a 10% recovery a failed attack?"**

> At M1 we're reporting where the published method stops working, which is a finding. And the
> equal-compute comparison delivered: `40:10` and `200:2` cost identically, we asked whether
> more steps or better steps wins, and the answer is *neither* — both collapse. Two
> independent parameter allocations agreeing is a replication.

**Q: "Does that confirm your saturation theory?"**
Careful — the honest answer is no:

> It's consistent with `pg_iters` saturating, but equally consistent with both shields simply
> winning. This experiment can't separate them. `pg_eps` is untested and that's M2.

---

## Part 2 — the diagnostic *(A0.5)*

**What it does:** compares the purified *input* against the protected *input* and reports a
**movement ratio** — how far purification travelled as a fraction of how far the shield had.

**Why it exists:** `pg_metric` only ever looks at the *edited* images, so it cannot tell you
whether a near-zero recovery means (a) purification barely moved the pixels — our settings
were too tight — or (b) it moved and the shield survived anyway.

> Recovery near zero is a patient who didn't get better. This checks whether they swallowed
> the medicine. Until you know that, "the drug doesn't work" isn't a conclusion you're
> entitled to.

Ratio below 0.15 → medicine stayed in the bottle. Around 1 and moving toward the original
photo → the attack ran and lost, which is a real result.

**This is the single most valuable cell in the notebook right now, and it costs 30 seconds
and no GPU. Run it before anyone asks.**

---

## Part 3 — instruments, NOT results

If you remember one sentence about this section:

> **It's built and ready, we haven't run it on these results, and we don't quote a number
> from it.**

That's a complete, defensible answer. You do not need to apologise for it.

| | what it is | if asked |
|---|---|---|
| **A1–A2 · `R_edit`** | CLIPScore of each edited image against the prompt. | *"Why a different CLIP from SD's?"* → grading SD's output with SD's own encoder is letting the chef mark the dish. |
| **A3–A4** | Fidelity vs attack success on one chart. | *"Why two axes?"* → blur an image into soup and the shield is definitely gone, and so is the photo. Success is a trade-off, not a score. |
| **B1–B2** | Radial FFT — where in frequency space the shield lives. | *"Which cutoff?"* → we report a **range**, not a number. Two reasonable onset rules disagree by 0.25 on photograph-like spectra, so quoting one would be overclaiming. |

### ⚠️ The one thing you must not mix up

| | `R_pipe` | `R_edit` |
|---|---|---|
| built from | `pg_metric` **SSIM** | **CLIPScore** |
| asks | did the *pipeline* behave normally? | does the *output* match the prompt? |
| status | **measured — your M1 number** | built, not run |

They can genuinely disagree: a shield can leave an image that is on-prompt but incoherent — a
convincing aeroplane with a broken face pasted on it. Owning that disagreement in writing is
M2 material. Confusing the two in an Ed post is the kind of thing a Light team finds.

---

## If you get stuck in a viva

Three sentences that are always available and always true:

1. *"That's measured — here's the cell."*
2. *"That's built but not yet run, so I'm not quoting a number for it."*
3. *"We can't separate those two explanations with this experiment, and here's the one that would."*

**Number 3 is not a weakness.** Knowing the limit of your own evidence is the thing being
assessed.
