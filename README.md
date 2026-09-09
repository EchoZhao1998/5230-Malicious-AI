# Dark.Tyro — FIT5230 project folder

**Team Dark.Tyro** (Echo Zhao · Nissa Corlidea) · Theme 2 Text-to-Image · **Dark / attack**
Reorganised **8 Sep 2026**. Start here, then `M2/README.md` for current work, then
`HANDOVER.md` for the reasoning behind every past decision.

## The project in one line
IMPRESS (NeurIPS 2023) is a **purifier**: it washes PhotoGuard's invisible shield off a photo so
an AI editor works on it again. We repaired the 2023 code to run in 2026, wrapped it in our own
measurement harness, and are now building the **generic entry point the paper promised but never
shipped**.

## Where things are

| folder | what it holds | touch it? |
|---|---|---|
| `M1/submittion/` | **exactly what was submitted on 28 Aug** — the Ed post PDF and the notebook | ❄️ frozen, never edit |
| `M1/working/` | the drafts, trial logs and interpretation notes behind M1 | read-only history |
| `M2/` | **the live work. `M2/README.md` is the M2 entry point** — three notebooks, one page of status | ✍️ this is where M2 work happens |
| `lib/` | reference material — IMPRESS's four `pg_*.py` scripts, the standalone toolkit, the QF bench, test PNGs | reference only |
| `results/` | archived run outputs (`final2/`) and the headline figure | evidence, do not regenerate |
| `Admin/` | assignment brief, team plan, baseline justification, Echo's M4 strategy log, tracker | — |

## The three documents that carry the reasoning
- **`HANDOVER.md`** — every decision and why. The section *"THE BASELINE CLAIM"* is the wording to reuse everywhere.
- **`GLOSSARY.md`** — SSIM / VIF / PSNR / LPIPS / CLIPScore, every `pg_*` and `pur_*` flag, the folder-name decoder.
- **`M2/README.md`** — M2 status, results and what is left before 18 Sep.

## Three traps that have already cost us time
1. **Two different things are called SSIM.** `pg_metric`'s SSIM compares *edited* images to the *edited clean* image. Fidelity SSIM compares an *input* to the *original photo*. `R_pipe` is built on the first only.
2. **Two different things are called R.** `R_pipe` = SSIM ratio (computed, published). `R_edit` = CLIPScore ratio (built, never run).
3. **Resolution.** `clean/` originals are 2736×3582 and up; the pipeline conditions on a 512×512 BICUBIC resize. Compare against the 512 copy or you are measuring interpolation. This voided an afternoon of diagnostics on 22 Aug.

## Storage rule — archived `clean/` folders are 512x512

Every archived `clean/` holds the **512x512 tensor the pipeline conditions on**, not the
original photograph. That is deliberate twice over: the full-resolution originals were 74 MB of
the folder's 121 MB, and comparing anything against them measures interpolation rather than the
attack (repair 12). Originals are re-downloadable: `gdown 16xISe7M_DlSqM2Zf2lWI4JJXcdsDEPsl`.

## Run environment
**Kaggle, Accelerator = GPU T4 ×2.** Not the P100 — it is `sm_60` and current PyTorch wheels
ship `sm_70`+ only, so everything loads and then the first CUDA op dies.
