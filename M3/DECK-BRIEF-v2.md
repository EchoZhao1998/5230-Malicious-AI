# M3 deck v2 — slide design guide (18 Oct 2026)

Replaces `DECK-BRIEF.md` for the slide layout. Echo's part is still 12 slides and about 10 minutes, at about 95 words a minute. Nissa's slides come after.

**Why v2 exists.** M2 got 6.3/8. The three deductions were:
- choices explained by *what* we did, not *why* (−0.4);
- "a sensitivity study, not an attack investigation" (−0.9);
- no evidence that other teams changed our method (−0.4).

The same three gaps sit in M3's biggest rows: Framework 5, Design 4, Critical 5 and Peer 3. v2 adds a **why** to every result.

**Where the new material comes from.** Nothing below needs a new GPU run.
- Every number is from runs you already have: Part 1/2 on 4 Oct, ESD-x T1 on 2 Oct and T2 on 8 Oct.
- One new figure, `figures/slides/fig5_wash_cleans_its_own_noise.png`. Claude drew it on 18 Oct from your own `REPORT_part2/training_log.csv`; it is not a new measurement.
- Two facts were checked in IMPRESS's source code on 18 Oct (`impress.py`, `utils.py`). They are marked ✔code below.

---

## Design rules, for every slide

1. **The title is the claim**, as one plain sentence. A marker who reads only titles should get the whole story.
2. **One picture per slide, at most two numbers.** Anything else goes to a backup slide after "Thank you".
3. **Text at least 24 pt in Canva.** If it doesn't fit at 24 pt, the slide has too much on it.
4. **Delete the template leftovers:** "Shodwe Co_", "cybersec_", "WASH PHOTOGUARD", and the "eps step iter" headers. They look like content but mean nothing.
5. **Keep colours consistent:** our method (C) is always blue, as in the figures. Keep the green theme for titles only.
6. **Fix the typos:** imperceptable → imperceptible · traning → training · diffirent → different · "what can I do diffirent" → "what I would do differently".
7. **No internal names on slides** (R_pipe, pg_eps, arms). Say "recovery" and "photo damage".

---

## Section A — our framework (slides 1–6, about 4 min) · Framework 5%

### Slide 1 · Title — keep as is
**Say (35 words):** Hello. We are Dark.Tyro: Echo and Nissa . Our theme is text-to-image, on the attack side.
I will present our framework, then my own attack on another team. Nissa will present her strategy after me.

### Slide 2 · "PhotoGuard hides noise in a photo; IMPRESS washes it off by testing what survives a VAE round trip"
**Show:** keep the IMPRESS paper's clean / protected / purified picture. Replace the flowchart with three boxes: `photo → PhotoGuard adds noise → IMPRESS washes → editor`. Put one line under the "washes" box: *keeps changing the photo until the model's own compress-and-rebuild step returns it unchanged.*

**Say (75 words):** PhotoGuard is a defence. It adds noise that people can't see but that breaks the editor. IMPRESS is the attack. Stable Diffusion first compresses a photo and then rebuilds it. A normal photo survives that round trip. PhotoGuard's noise doesn't, because it isn't real image content. So IMPRESS keeps adjusting the photo until the round trip gives back the same photo. Whatever does not survive gets washed out.

> My understanding script: PhotoGuard is a defense mechanism. It adds noise that is imperceptible to the human eye but can disrupt the editor. IMPRESS, on the other hand, is the attacker. Stable Diffusion first compresses the photo and then reconstructs it. Ordinary photos can withstand this round-trip processing, but PhotoGuard’s noise cannot, because it is not genuine image content. Therefore, IMPRESS continuously adjusts the photo until, after this round-trip processing, it is ultimately restored to its original state. Any content that cannot withstand this process is eliminated.

**Understand it:** this is a photocopier test. Copy a real document and it looks the same. A forged watermark smudges. IMPRESS keeps retouching the page until a photocopy of it looks identical, and the forgery is gone by then. ✔code: the loss is `MSE(rebuilt photo, photo) + 0.01 × max(LPIPS(photo, protected) − 0.10, 0)`. The second term stops the wash from drifting too far from the protected photo.

**If asked "why does the round trip remove it?":** the noise is tuned to push the encoder somewhere specific. The decoder can only draw natural-looking images, so it cannot redraw that noise.

### Slide 3 · "M2 showed *what* happens; M3 explains *why*"
**Show:** two columns. Left, "M2 feedback": *design decisions not justified theoretically* · *a sensitivity study more than an attack investigation*. Right, "What M3 adds": *trained the wash and logged every iteration* · *explained each result from how the model works* · *all four versions faced one identical shield*.

**Say (60 words):** In Milestone 1 we made IMPRESS run in 2026. In Milestone 2 we changed one line: wash only the part of the photo the editor keeps. The feedback said we showed what happens, not why. So Milestone 3 does both. We trained the wash, watched it at every step, and explain each result from how the model works.

**Understand it:** showing the marker that you read the feedback and acted on it is itself evidence of progress. That is what the Framework row asks for.

### Slide 4 · "We trained the wash and watched the edit converge on the clean target"
**Show:** `M3_training/REPORT_part2/fig4_training_progress_one_face.png`, **large**, filling most of the slide. Put the formula as one small line underneath: `ours = mask · washed + (1 − mask) · protected`. Move the parameter box, the 10-face grid and the code snippet to backup.

**Say (80 words):** This is one face. Left is the edit of the clean photo, which is our target. Then the edit of the protected photo. Then the edits after 50, 100, 250, 500 and 1000 iterations of washing. The edit moves towards the target as training goes on. Our version washes only the region the editor keeps. The reason: the editor blanks the region it repaints before it reads the photo. Washing those pixels changes nothing in the edit. It only damages the photo.

**Understand it:** ✔code. IMPRESS edits with Stable Diffusion's inpainting pipeline, and the inpainting code sets the repaint region to zero before encoding (`masked_image = image * (mask < 0.5)`). Analogy: you don't clean the part of a wall that is about to be repainted.

⛳️ **If asked "how do you know which region is repainted?":** an inpainting attacker chooses the mask, so they always know it. The limitation is that this doesn't carry over to edits of the whole image.

### Slide 5 · NEW · "Most of IMPRESS's photo damage is its own start-up noise, which training removes"
**Show:** `figures/slides/fig5_wash_cleans_its_own_noise.png`. Two numbers on the slide: **0.29 → 0.12**.

**Say (85 words):** Why does longer washing damage the photo less? This surprised us. The answer is in IMPRESS's first step. It adds random noise to the photo on purpose, to knock it out of PhotoGuard's trap. Then training removes that noise. The distance from the protected photo falls from 0.29 to 0.12. It stops near 0.10, the limit where IMPRESS's penalty switches on. So at 100 iterations, most of the damage is IMPRESS's own noise that hasn't been removed yet.

**Understand it:** ✔code. `X_p = X_adv + randn × pur_noise` (0.05 here), and a cosine learning-rate schedule spread over the total number of iterations. Analogy: a painter who splashes primer on the wall first, then sands it back. Stop early and you see primer everywhere.
- Be careful here: "it stops near 0.10 because of the penalty" is the explanation that fits the numbers. You haven't tested it directly, so say "near the limit", not "because of the limit".
- The y-axis is IMPRESS's own LPIPS (VGG net) **against the protected photo**. Your "photo damage" number elsewhere uses the AlexNet LPIPS **against the clean photo** (0.181 → 0.143). They are different scales; don't mix them on one slide.

**If asked "then why not skip the start-up noise?":** that's my M4 idea, a gentler wash. Without the noise kick the wash may stay stuck in the shield's trap, so it has to be tested, not assumed.

### Slide 6 · "Our wash: same recovery as IMPRESS, 68% less photo damage, no extra compute"
**Show:** `M3_training/REPORT_part2/fig2_iteration_curve.png`. Merge the old slides 5 and 6. Add a small box at the bottom right: **Limitation:** *the shield changed the edit less than the editor's own randomness on 10 of 10 faces, so recovery can't separate the versions; photo damage can.* Move the shield-sweep figure to backup.

**Say (90 words):** Three results. One: our version does 68 percent less photo damage than IMPRESS at the same compute. Two: its recovery is the same. We predicted that: in the region the editor keeps, our photo *is* IMPRESS's photo, so the edit should match. Three: running IMPRESS ten times longer cuts damage by 21 percent. Recovery may rise about 4 points, but two faces carry that. The main limit: at our affordable shield strength, PhotoGuard barely changed the edit. So photo damage is the result to trust.

**Understand it:** "same recovery" is a **confirmed prediction**, not a disappointment. Our version and IMPRESS differ only in the region the editor throws away, so their edits *should* match. The data agrees: the difference is +0.7 points, inside the ±3 noise band.

**The question most likely to come up — "isn't 68% less damage true by construction?":** "Yes, and that's the finding. About two-thirds of IMPRESS's damage lands on pixels the editor discards anyway. We removed that waste at zero cost."

**If asked "why is recovery so noisy?":** recovery divides by how much the shield hurt the edit. Where the shield barely hurt it, we divide by a small number and small differences blow up. The two faces with the weakest shield effect gave the biggest swings, −17 and −16 points.

---

## Section B + C — my attack on Cyber Ninjas (slides 7–12, about 6 min) · Peer 3 · Design 4 · Critical 5 · Role 2

### Slide 7 · "My strategy, keen observation: their test set used only the Latin alphabet"
**Show:** their research question as one line, and their challenge screenshot, small. Then a big line: **Strategy: keen observation, finding a gap in what they tested.** Keep "Van Gogh 梵高 ゴッホ 반 고흐" as the visual.

**Say (80 words):** Now my individual strategy, keen observation. My target is Cyber Ninjas, a Light team. Their defence, ESD-x, erases Van Gogh's style from Stable Diffusion. Their question: can indirect prompts bring the style back? Before I touched a GPU, I read their code and their posts. They had widened the erasure to an English description and a French translation, but every test was in the Latin alphabet. So my attack asks for Van Gogh in other writing systems.

**Understand it:** the Design row asks you to *name* a distinct strategy. Before this, the words "keen observation" were not on any slide or in the script.

### Slide 8 · "I set the rules before running: a bypass only counts if the original model could draw the style"
**Show:** a four-row verdict rule, typed on the slide:
- original model can't draw it → **NO SIGNAL**
- both models can't → **ERASED**
- erased model keeps less than half → **PARTIAL**
- erased model keeps half or more → **BYPASS**

Next to it, the round-1 result table you already have, cropped to 4 rows. Add one line: *threshold = 2 × the no-artist prompt's spread across seeds · prediction posted on Ed before running · stopping rule: one session, prompt list frozen.*

**Say (105 words):** I wrote the rules before running anything. Every prompt runs on the original model and the erased one. It's only a bypass if the original model can draw Van Gogh *and* the erased model still does. I took this rule from Cyber Ninjas' own argument about misspellings, and applied it to other alphabets. I posted my prediction on Ed first, so the result could prove me wrong. It did. The original model doesn't draw Van Gogh from any of the five non-Latin names. For Chinese, Japanese and Korean, it draws an East Asian village. It reads the script as a place, not a painter.

**Understand it:** the rule is the design depth. It stops you counting an image as a "bypass" when the original model never knew the style. Analogy: you can't call a lock picked if the door was never locked.

### Slide 9 · "No route brought Van Gogh back; a neighbouring painter was untouched"
**Show:** the round-2 image strip with the description and title+description columns highlighted, as on your current slide. Keep 3 rows of the table: description −4% · title + description 27% · Gauguin 105%.

**Say (75 words):** Round two tried the open route: describe his style without his name, or name his paintings. I used six new seeds and Paul Gauguin as a control. The description kept minus 4 percent of the style. Title plus description kept 27 percent. Both count as erased. Painting titles failed even on the original model. Gauguin kept all of his style, so the erasure is aimed at Van Gogh only.

### Slide 10 · "ESD erases how the model paints a style, not the word, and that is why rewording fails"
**Show:** left, a one-line explanation of how ESD trains: *the model is shown how it paints "Van Gogh", then retrained to move the opposite way.* Right, the swirl strip from your current Reflection slide. At the bottom, a **Real-world impact** box (new):
- *For artists:* on this model, rewording and other alphabets don't bring the style back. But the swirling sky survives when described, so the erasure is partial.
- *The real risk:* a model whose text encoder understands Chinese or Japanese might know 梵高. An erasure trained only in English may not cover it.

**Say (110 words):** Why did it fail? Two reasons. First, the original model had nothing to give back. Its text encoder was trained mostly on English and never linked 梵高 to the painter. Second, ESD doesn't delete a word. It shows the model how it paints Van Gogh, then retrains the layers that turn words into painting instructions, so they push the other way. Any prompt that asks for that style gets pushed away, named or not. What it means in practice: on this model, the erasure holds. The real risk is a multilingual model that already knows these names. And one thing the score missed: the swirling sky still survives.

**Understand it:** ESD's training rule is `new prediction = unconditioned prediction − η × (Van Gogh prediction − unconditioned prediction)`. In words: work out the direction "Van Gogh" pulls the image, then train the model to go the opposite way. ESD-x changes only the cross-attention layers, which turn every prompt word into painting instructions. That's why a description without the name is also weakened.
- Analogy: the model isn't taught to forget a name. It's taught to steer away from a destination, whatever directions you give it.

**If asked "why does the swirl survive?":** the score measures overall "Van Gogh-ness" with CLIP. A starry swirl is also a generic night-sky motif, so ESD may remove the brushwork and colours but keep the shapes. That rests on one seed, so say "by eye, one seed".

### Slide 11 · "What the interaction changed in my method"
**Show:** a timeline across the top, then three lessons below.
- **Timeline:**
  - Sep: they widen the erasure to an English description and French — still all Latin script
  - ~18 Sep: I post my prediction
  - 2 Oct: round 1 refutes it, result posted
  - 8 Oct: round 2, result posted ✏ *check the T2 reply is actually up*
  - No reply from them yet
- **Lessons:**
  1. *From their own argument:* check the original model first.
  2. *From what I saw in their model:* it lowers even no-artist paintings, so compare both models against **one fixed reference**. Against its own lowered baseline the description looked 99% intact; against a fixed one, −4%.
  3. ESD erases the style, not the word, and only that style.

**Say (100 words):** This interaction changed my method twice. Their own misspelling argument became my first rule: check the original model before claiming a bypass. Then I saw that the erased model makes every village painting less Van Gogh-like, even with no artist named. Against its own lowered baseline, the description looked 99 percent intact. Against one fixed reference, it kept nothing. Without that fix I would have reported a bypass that wasn't real. Cyber Ninjas haven't replied. Their next move could be adding other alphabets to their erasure list. My result suggests that's unnecessary on this model.

**Understand it:** this answers M2's −0.4 directly, because it shows peer interaction *changed your method*. "They didn't reply" is fine to say. The Critical row asks how the target reacted, and their earlier widening of the erasure counts as a reaction you can point to.

### Slide 12 · "My role" + thank you
**Show:** keep your current text. ⚠ The sentence about Nissa's slides is true only if her slides are actually appended. Otherwise delete it, and delete the "Nissa's work" page.

**Say (45 words):** My role: I chose the target, designed both test rounds, built and ran both notebooks, and wrote every Ed post. The attack did not succeed, but every step is in the shared notebooks, and it changed how I measure. Thank you.

---

## Backup slides, after "Thank you", only if asked
- B1 · shield sweep, "why only these settings": `figures/slides/fig2_shield_sweep_two_panels.png`
- B2 · parameter box (pg_eps, pg_iters, pur_iters), moved from old slide 4
- B3 · the 10-face grid, `REPORT_part2/fig3_all_faces.png`

## Before 22 Oct
- [ ] Rebuild slides in Canva from this guide
- [ ] Update `M3-TRANSCRIPT.md` to these "Say" lines (≈ 920 words)
- [ ] One timed read-aloud
- [ ] Confirm the T2 reply is posted on Ed
- [ ] Nissa's slides: appended, or her sentence removed
- [ ] Moodle PDF with the four Colab links
