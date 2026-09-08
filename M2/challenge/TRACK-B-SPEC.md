# Tier 3 starter pack — build spec
*Dark.Tyro · written 22 Aug 2026 · owner: Echo*

What has to exist in the shared folder before the Ed post goes live, and the order to build
it in. Nothing here is research — it is assembly — but the ordering matters, because step 0
can change the design.

---

## The design in one paragraph

Two sets. A **calibration set** with labels, so entrants can fit something. An **evaluation
set** without labels, whose purified images come from **two different purifier
configurations** — announced as plural, never specified. Score is a 3×3 confusion matrix and
balanced accuracy on both sets; the headline number is the **generalisation gap** between
them. We publish ground truth, our own detector, and a read of the error patterns after the
deadline — not before.

**Why the gap is the metric.** A detector that scores 95% on calibration and 55% on
evaluation has learned our settings, not purification. That is the finding, and it is a
finding whoever produces it. The old design ("here are 30 images, our accuracy is the bar to
beat") had exactly one good outcome and two bad ones.

---

## Step 0 — run the answer key first *(do this before anything else)*

Run **section B4 of `Tyro_Analysis_Toolkit.ipynb`** — the private detection key — over the
purified output of both configurations you intend to ship.

You are looking for one number:

> Can a single threshold on one statistic separate purified from clean at high accuracy?

- **If yes at >90%** — the two configurations are too similar and the evaluation set has one
  fingerprint, not two. Change the second configuration until they separate (different
  `pur_iters`, or a different purifier entirely — the Butterworth low-pass rather than
  IMPRESS). The point of the tier collapses otherwise.
- **If no** — ship it.

**B4 never leaves your machine.** It is the solution to our own riddle. It is not in
`Dark_Tyro_M1.ipynb` and must not be in the published notebook — there is a checklist item
for this.

> Knowing the answer to your own challenge before you publish it is not cheating; it is the
> difference between *choosing* the difficulty and *discovering* it. The M3 rubric calls that
> keen observation.

---

## Step 1 — what to generate

| set | count | composition | source |
|---|---|---|---|
| **calibration** | 12 | 4 clean · 4 protected · 4 purified-A | held-out faces, **not** reused in evaluation |
| **evaluation** | 30 | 10 clean · 10 protected · 10 purified (**mixed A/B**) | disjoint faces |

- **Purifier A** = IMPRESS at the shipped settings (`pur_eps=0.1, pur_iters=100, pur_lr=0.005`).
- **Purifier B** = deliberately different. Cheapest honest option: the frequency-targeted
  Butterworth low-pass from Part B. Second option: IMPRESS at a much lower `pur_iters`.
- Split the 10 purified evaluation images **7 / 3 or 6 / 4**, not 5 / 5 — an even split is
  guessable and makes "half of them" a working strategy.
- Same protection configuration throughout, so purifier is the only thing varying.
- **Strip EXIF and re-encode everything identically as PNG.** File size, timestamps, and
  encoder metadata are all side channels that would let someone win the tier without looking
  at a pixel.
- **Randomise filenames** (`img_001.png` … `img_030.png`) and shuffle before assigning
  numbers — do not let class order survive into the ordering.

## Step 2 — folder layout

```
tyro_tier3/
├── README.md                  # the task, the scoring rule, the submission format
├── calibration/
│   ├── labels.csv             # filename,label   (clean|protected|purified)
│   └── images/                # 12 png
├── evaluation/
│   └── images/                # 30 png, no labels
└── score_tier3.py             # entrants run this on their own predictions
```

## Step 3 — `score_tier3.py`

Takes a `predictions.csv` (`filename,label`) and prints the 3×3 confusion matrix and
balanced accuracy. Fifteen lines with `sklearn`. Ship it so every submission is comparable —
if teams each compute accuracy their own way the results cannot be pooled, and pooling them
is what makes the M3 write-up interesting.

`README.md` states: chance = 33.3%, report *both* sets, and the generalisation gap is
`balanced_acc(calibration) − balanced_acc(evaluation)`.

## Step 4 — our own submission

Run our detector against both sets and record the numbers **now**, sealed. Publish after the
deadline alongside everyone else's. Recording it in advance is what stops us quietly
retuning once we see how the teams did.

---

## If time runs out before 28 Aug

Ship **calibration + evaluation with purifier A only**, and say in the Ed post that a second
configuration will be added to the evaluation set in week 8 with the labels released at the
same time. That is a smaller challenge, not a broken promise.

**Do not ship a link that does not work.** Fall back to "reply in this thread and we will
send you the set" — a delayed pack costs less than a dead link.
