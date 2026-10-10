# M3 presentation — speaking transcript (Echo, slides 1–12) · draft 10 Oct
Written for an unhurried pace (~95 words/min). Short sentences, easy to say. Numbers rounded where the slide shows the exact value.
**Timing:** slides 1–6 ≈ 3.5 min (~330 words) · slides 7–12 ≈ 6.5 min (~620 words) · total ≈ 10 min. Nissa's part follows.
Lines in [brackets] are stage notes, not spoken.

---

## Slide 1 · Title (~35 words)
Hello. We are Dark.Tyro: Echo Zhao and Nissa Corlidea. Our theme is text-to-image, on the attack side.
I will present our framework, then my own attack on another team. Nissa will present her strategy after me.

## Slide 2 · Introduction to IMPRESS (~70 words)
PhotoGuard is a defence. It adds noise to a photo that people cannot see, so AI editors produce a broken edit.
IMPRESS, from NeurIPS 2023, is an attack on that defence. It washes the noise off, so the editor works normally again.
Our goal as attackers: let an AI edit a protected photo as easily as a clean one.

## Slide 3 · Overview of milestones (~65 words)
In Milestone 1, we made IMPRESS run at all. It needed eleven repairs to work on Colab in 2026.
In Milestone 2, we changed one line: wash only the part of the photo the editor keeps.
In Milestone 3, we tested that change fairly. Every version faced the same shield, on the same ten faces.

## Slide 4 · Our method (~80 words)
This is the one line. Our wash keeps IMPRESS's result inside the mask, and the protected photo outside it.
Why the mask? The editor repaints the masked region anyway. Washing it only adds damage. Only the part the editor keeps needs cleaning.
We also ran IMPRESS for 1000 iterations, the paper's default. We call this version B. It tests whether our 100 iterations were holding IMPRESS back.

## Slide 5 · Findings (~45 words)
Three findings.
One: our version does 68 percent less damage to the photo than IMPRESS, and 58 percent less than B.
Two: longer washing damages the photo less, but recovery does not reliably improve.
Three: B's small recovery gain comes from only two of ten faces.

## Slide 6 · Conclusions and limitations (~70 words)
So, against IMPRESS, our version wins outright. Same recovery, much less damage, and no extra compute.
Against long IMPRESS, it is a trade-off. B might recover a little more. Ours does far less damage, at a tenth of the compute.
The main limit: the shield was weak at our settings, so recovery could not separate the versions. Photo damage could. A stronger shield is the next test.

---

## Slide 7 · Attack target: Cyber Ninjas (~95 words)
Now my own attack. My target is Cyber Ninjas, a Light team. Their defence is ESD-x. It erases Van Gogh's style from Stable Diffusion.
Their question was: can the style come back through indirect prompts?
I read their code and their post closely. Their test prompts used only the Latin alphabet: English and French. So my idea was to ask for Van Gogh in other writing systems.
I posted this as a prediction on Ed, before I tested it. Then I posted both results. They have not replied.

## Slide 8 · Round 1: other alphabets (~110 words)
Round one. One fixed sentence: "a painting of a village under a night sky, by" a name. Only the name changes.
Every prompt runs on two models: the original model, and the erased one. A prompt only counts as a bypass if the original model can draw the style, and the erased model still does.
My prediction was wrong. The original model does not draw Van Gogh from any of the five non-Latin names. For Chinese, Japanese and Korean, it draws an East Asian village instead. It reads the script as a place, not a painter.
With nothing to erase, there is nothing to bypass.

## Slide 9 · Round 2: titles and descriptions (~100 words)
Round two tried the open route: describing his style, or naming his paintings, without his name. I used six new seeds, and Paul Gauguin as a control.
Nothing came back. The description lost its style. Title plus description also lost it.
The painting titles did not work even on the original model.
And Gauguin kept all of his style. So the erasure is aimed at Van Gogh only. It is not damaging art in general.

## Slide 10 · Why the attack failed (~100 words)
Two reasons.
First, the original model had nothing to give back. Its text encoder was trained mostly on English. It never linked these names to the painter.
Second, ESD erases the style, not just the word. It learns how the model paints Van Gogh, and trains it to paint the opposite. It changes the layers that turn every word into painting instructions. So even without his name, a description of his style is affected.
[If you added the swirl strip:] One thing the score missed: the erased model still paints a swirling starry sky when you describe one. It removes the brushwork and the colours.

## Slide 11 · What I learned and what I would improve (~130 words)
Three lessons.
One: check the original model first. A bypass only counts if the original model could draw the style. Cyber Ninjas made this argument for misspellings. I showed it also holds for other alphabets.
Two: this erasure removes the style, not just the name. Rewording the prompt does not get around it, and other painters are safe.
Three: measure both models against one fixed reference. The erased model makes even unnamed village paintings less Van Gogh-like. Against that lowered baseline, the description looked 99 percent intact. Against a fixed reference, almost nothing was left. Without this check, I would have reported a bypass that was not real.
To improve: test a multilingual model, score the swirling sky directly, and measure the spill-over on similar scenes.

## Slide 12 · My role and thank you (~60 words)
My role: I chose the target, designed both test rounds, built and ran both notebooks, and wrote every post on Ed.
The attack did not succeed. But the method, the controls and the results are all in the shared notebooks.
Thank you. Nissa will now present her strategy.
