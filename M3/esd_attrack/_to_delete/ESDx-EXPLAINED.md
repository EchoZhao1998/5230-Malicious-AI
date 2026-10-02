# ESD-x and my cross-script test — explained from scratch
*For me, to re-learn the logic later. Written 2 Oct 2026 after run `esdx_1002_1328`.*
*Numbers: `REPORT_esdx_1002_1328/`. Short version: `RESULT-1002-crossscript.md`.*

---

## 0. The whole story in five sentences
1. Stable Diffusion draws whatever the prompt's words point to — "Van Gogh" points to swirling skies.
2. **ESD-x** (the defence) retrains a small part of the model so the words "Van Gogh" stop pointing there.
3. Cyber Ninjas trained it on English and French versions of the name — all in the Latin alphabet.
4. I predicted that the name in **other alphabets** (梵高, ゴッホ…) would slip past the erasure.
5. **I was wrong — but for an interesting reason:** the original model never understood those names in
   the first place, so there was nothing for the erasure to miss.

---

## 1. How Stable Diffusion reads a prompt
Three steps, every time:

| step | what happens | analogy |
|---|---|---|
| **Tokenizer** | chops the prompt into pieces ("Van", "Gogh") | cutting a sentence into word cards |
| **Text encoder** (CLIP ViT-L/14) | turns each piece into a list of numbers that carries meaning | a translator who turns words into "meaning coordinates" |
| **Cross-attention** (layers named `attn2` inside the UNet) | while painting, the model ke
