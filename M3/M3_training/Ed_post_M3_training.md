# Dark.Tyro M3 · Training the IMPRESS wash: what do more iterations buy?

**Notebooks (run on a Kaggle T4, uploaded to Colab with outputs):**
- **Part 1** — protects 10 photos once, runs versions N, A and C: [PART 1 COLAB LINK]
- **Part 2** — runs version B (1000 iterations) on the **same protected photos**, then scores and plots all four versions together: [PART 2 COLAB LINK]

Part 2 ran straight after Part 1 on the same machine and reused Part 1's protected photos and results, so all four versions face an identical shield. The clean edits from the two parts are pixel-identical. Start with Part 2 if you only open one.

## What we tested
PhotoGuard adds noise to a photo so an AI editor (Stable Diffusion inpainting) breaks its edit. IMPRESS removes that noise with an optimisation loop that changes the photo step by step. In M3 we logged that loop's loss at every iteration, saved the photo at 50, 100, 250, 500 and 1000 iterations, and sent each saved photo through the editor.

| version | what it is | iterations |
|---|---|---:|
| N | no wash | 0 |
| A | IMPRESS | 100 |
| C | ours: A's output, washed only in the region the editor keeps | 100 |
| B | IMPRESS at the paper's budget | 1000 |

## Results (10 faces)
- **More iterations damage the photo less:** LPIPS 0.181 at 50 → 0.143 at 1000 (21% less), flat after 500.
- **More iterations bring the edit slightly closer to the clean edit:** recovery +0.4 → about +5 pp, flat after 250. This clears our ±3 pp noise band but rests mostly on 2 of 10 faces, so we treat it as suggestive.
- **Our version C damages the photo 68% less than A and 58% less than B**, at a tenth of B's compute. It does not recover more: B recovers 3.9 pp more than C.
- **The shield was weak in this run:** on all 10 faces it changed the edit less than changing the random seed does. Photo damage is the score to trust here.

**Takeaway:** longer training makes the wash gentler and may recover a little more; washing only the kept region makes it much gentler with no extra training.

## A question for defence teams
At this shield strength the editor's own randomness is larger than the shield's effect. If your team has a PhotoGuard setting that clearly beats seed noise while keeping LPIPS under 0.10, we would like to run our four versions against it.
