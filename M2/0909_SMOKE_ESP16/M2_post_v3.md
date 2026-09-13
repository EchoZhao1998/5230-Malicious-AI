# M2 — Dark.Tyro: washing less of the photo, and getting the same result

**Team Dark.Tyro** · Echo Zhao · Nissa Corlidea
**Theme 2 (Text-to-Image) · Dark / attack side** · Milestone 2

**In short.** Four lines of arithmetic let our attack damage the photo **74% less**, with no
measurable change in how well it works. Our challenge, the **Tyro Wash Test**, is open — it takes
one function to enter, and everything you need is in §5.

---

## 1 · How the pipeline works

If you have not worked with image protection before, this is the whole process.

```
  clean photo
      │
      │  ① PROTECT  ─ the defence (PhotoGuard)
      ▼               add noise you cannot see, so an AI editor produces a mess
  protected photo
      │
      │  ② PURIFY  ─ the attack (IMPRESS). We call this the "wash".
      ▼              remove that noise and get a usable photo back
  purified photo
      │
      │  ③ EDIT  ─ Stable Diffusion inpainting, using a mask and a text prompt
      ▼
  edited photo
      │
      │  ④ MEASURE  ─ did the edit work? how much was the photo damaged?
      ▼
   two numbers
```

**PhotoGuard** (arXiv:2302.06588) is the defence. It adds a small, invisible pattern to a photo so
that anyone who runs it through an AI editor gets a garbled result.

**IMPRESS** (arXiv:2310.19248, `github.com/AAAAAAsuka/Impress`) is the attack we start from. It
adjusts a protected photo until the model's own autoencoder accepts it again, which removes most of
the protection. We are on the Dark side, so improving IMPRESS is our job.

**The difficulty.** The protection is small and the wash is not. A wash strong enough to remove the
noise also strips real detail out of the photograph. Damage the photo more than the protection did
and you have won nothing — there is nothing worth editing left.

---

## 2 · What we changed

Inpainting does not redraw the whole picture. The mask splits it into a **kept region**, where the
editor leaves the original pixels almost untouched, and a **repainted region**, which is generated
from scratch. We confirmed this by measurement: across our images the kept region moves by a few
grey levels during an edit, the repainted region by nearly a hundred.

IMPRESS washes both. But the repainted region is thrown away and redrawn a moment later, so
cleaning it achieves nothing — while still costing us real damage to the photo.

So we wash only the region that survives:

```python
purified_v2 = mask * purified_impress + (1 - mask) * protected
```

In words: **keep IMPRESS's cleaned pixels inside the mask, and put the protected photo's own pixels
back outside it.** We blur the mask edge by 3 pixels, because a hard line between washed and
unwashed pixels is a visible artefact and an easy thing for a detector to spot.

---

## 3 · The two numbers we report

| number | what it means | better |
|---|---|---|
| **`R_pipe`** | how much of the editing pipeline the wash restored, as a % of the gap between "fully shielded" and "no shield at all" | higher |
| **`LPIPS`** | how different the photo looks from the clean original, judged by a perceptual network instead of pixel arithmetic. 0 means identical | lower |

We never report one without the other. Report only the first and you reward an attack that wins by
destroying the photograph. Report only the second and you reward an attack that does nothing.

---

## 4 · Result

Four versions, one shield setting, same faces, same seed, **n = 2 images**. Version N skips the
wash entirely, so it marks the starting point.

| version | wash | `R_pipe` % ↑ | LPIPS vs clean ↓ |
|---|---|---|---|
| **N** | none — the starting point | 0.00 | **0.018** |
| **A** | IMPRESS, 100 iterations — our M1 baseline | 4.75 | 0.150 |
| **B** | IMPRESS, 1000 iterations — the paper's own budget | 9.41 | 0.109 |
| **C** | **ours** — IMPRESS 100 iterations, mask only | 7.05 | **0.039** |

*(attached: `m2_tradeoff.png`, the four versions on one plot; `m2_panel.png`, clean / protected /
purified / edited for both images.)*

C uses exactly the same compute as A, and damages the photo 74% less.

**What we do not claim.** C's `R_pipe` is 2.3 points above A. Re-running the same experiment
unchanged moves `R_pipe` by ±2–4 points on its own, so 2.3 is smaller than our own noise and we
claim nothing from it. Read the order of these rows, not the size of the gaps.

---

## 5 · One thing worth knowing before you enter

We checked whether `R_pipe` means what we wanted it to mean, and the answer was partly no.

Edit the same **clean** photo twice, changing only the random seed. Nothing is protected, so any
difference is just the generator being random. Measured with SSIM against the first edit — lower
means the edit was disturbed more:

| image | changing the seed | the actual shield |
|---|---|---|
| 1233476865_1 | **0.472** | 0.584 |
| 1525918600_1 | **0.415** | 0.610 |

**Changing the random seed disturbs the edit more than PhotoGuard does.** At these settings the
shield is quieter than the pipeline's own randomness, so `R_pipe` is partly measuring noise. We
also doubled the shield strength setting and nothing changed — that setting has no effect on this
code path.

This is why the challenge scorer tells you whether your shield actually registered before it gives
you a number, and it is the honest reason our damage figure is solid while our strength figure is
not. The full check is in `Tyro_M2_diagnostics.ipynb` if you want it.

---

## 6 · The challenge is open — the Tyro Wash Test

**Build a shield we can't wash off.** One function. You do not need to understand our attack.

**What you get**

- 📦 `tyro_wash_test_trackA.zip` (3.6 MB) — 10 clean 512×512 faces, their masks, and
  `check_submission.py` so you can score yourself before sending
- 📓 Starter notebook: **[COLAB LINK]** — runs on a free Colab T4

**What you do.** Open the starter and edit one function, `protect()`. Everything else is set up.
We ship a working PhotoGuard protector, so if you have no code of your own you can enter by
changing a single number in one cell. If you do have your own method, delete ours and use it.

**What you send back.** 10 PNGs at 512×512, keeping our filenames. **You never have to tell us how
you made them** — our purifier only sees the images. Any defence is allowed.

**How we score you.** Two numbers, both published, on one plot:

- **`R_pipe`** — how much of the edit our wash restores. Lower is better for you.
- **`LPIPS`** — how much your shield damaged the photo. Lower is better for you.

Both, always. With only the first, the winning entry is one that adds so much noise the photo is
ruined — nothing can be washed off it, but nothing can be edited either.

**One rule: keep LPIPS under 0.10.** Ours sits at 0.0665, so there is room. Go over and we still
plot you, we just do not rank you.

`check_submission.py` gives you both numbers, plus a "shield did not engage" flag when a photo's
protection was too quiet to register — same check we run, so there are no surprises. *(This
replaces the fixed SSIM ≤ 0.85 rule from our M1 post; we measured it and it was too loose.)*

**Submissions close 18 September.** Every result gets published in a follow-up here, **including
any that beat us.** If anything in the pack does not run, reply and we will fix it the same day.

---

## Code

Kaggle, T4 ×2, Internet ON, run top to bottom. Each notebook has a smoke mode, so a broken setup
fails in four minutes instead of forty.

- `Dark_Tyro_M2.ipynb` — the attack. M1 plus four lines.
- `challenge/Tyro_Wash_Test_STARTER.ipynb` — the defence code, for you to run.
- `Tyro_M2_diagnostics.ipynb` — the check in §5.

The IMPRESS algorithm itself is unchanged — `impress.py` is 25 lines and we did not touch it. Ours
is everything around it: the repairs needed to make the 2023 code run, the single-GPU harness, the
`R_pipe` metric, and the four-line mask restriction.
