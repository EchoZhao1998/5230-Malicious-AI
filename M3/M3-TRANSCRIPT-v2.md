# M3 speaking script, simple version (18 Oct)

This follows the 18 Oct deck after slides 6 and 7 are merged, so there are 12 slides.
- It is about 960 words, which is about 10 minutes at a calm pace.
- Sentences are short, and the words are everyday words.
- Lines in [brackets] are notes for you; don't say them.

---

## Slide 1 · Title
Hello. We are Dark.Tyro. Our theme is text-to-image, on the attack side.
First, I will show our framework. Then I will show my own attack on another team.

## Slide 2 · PhotoGuard and IMPRESS
PhotoGuard is a defence. It adds tiny noise to a photo. People cannot see it, but it breaks AI photo editing.
IMPRESS is the attack. It removes the noise. How?
Stable Diffusion first shrinks a photo into a small code, then rebuilds it. A real photo comes back the same. The noise does not come back, because it is not a real part of the picture.
So IMPRESS changes the photo, step by step, until it comes back the same. Then the noise is gone.

## Slide 3 · M2 showed what, M3 explains why
In Milestone 1, we made IMPRESS run. In Milestone 2, we changed one line: we clean only the part of the photo that the editor keeps.
Our M2 feedback said: you show what happens, but not why.
So in Milestone 3, we explain why. We watched the cleaning at every step.

## Slide 4 · Watching the edit improve
This is one face. On the right is our target: the edit of the clean photo. On the left is the edit of the protected photo. It is broken.
In between, the cleaning runs longer and longer. The edit gets closer to the target.
Why do we clean only the kept part? Because the editor deletes the other part before it starts, and paints it again from nothing. So cleaning that part is wasted work. It only harms the photo.

## Slide 5 · IMPRESS's own noise
Here is something we did not expect. Longer cleaning harms the photo less, not more. Why?
We read the IMPRESS code. In the first step, IMPRESS adds random noise on purpose. This shakes the photo free from the protection. Then each training step removes some of that noise.
The change falls from 0.29 to 0.12, and stops near 0.10, IMPRESS's own limit.
So if you stop early, most of the harm is IMPRESS's own noise.

## Slide 6 · Findings (the merged slide)
Three findings.
First: our version harms the photo 68 percent less than IMPRESS, and costs no extra time.
Second: the edit quality is the same as IMPRESS. We expected this. In the part the editor keeps, our photo and IMPRESS's photo are the same.
Third: running IMPRESS ten times longer harms the photo 21 percent less. It may also give a slightly better edit, but only two of ten faces show this.
One limit: the protection was weak in our setting. So photo harm is the result we trust most.

---

## Slide 7 · Attack target: Cyber Ninjas
Now my own attack. My strategy is keen observation.
My target is Cyber Ninjas. Their defence, ESD-x, removes Van Gogh's style from Stable Diffusion. Their question: can other prompts bring the style back?
I read their code and their posts. They had added an English description and a French name to their erasure. But all their tests used the Latin alphabet.
So I asked for Van Gogh in other writing systems: Chinese, Japanese, Korean, Russian and Arabic. I posted this prediction on Ed before I tested it.

## Slide 8 · Round 1
Round one. I used one fixed sentence. Only the name changes.
Every prompt runs on two models: the original and the erased one. My rule: it is only a bypass if the original model can draw Van Gogh, and the erased model still can.
My prediction was wrong. The original model cannot draw Van Gogh from any of the five names. For Chinese, Japanese and Korean, it draws an Asian village. It reads the name as a place, not a painter.
If nothing was there, nothing can come back.

## Slide 9 · Round 2
Round two. I described his style without his name. I also tried his painting titles. I used six new seeds, and the painter Paul Gauguin as a control.
Nothing came back. The description kept almost none of the style. The titles did not work even on the original model.
Gauguin kept all his style. So the erasure removes only Van Gogh. It does not damage art in general.

## Slide 10 · Why my attack failed
Why did my attack fail? Two reasons.
First, the original model had nothing to give back. It learned mostly from English text. It never linked these names to the painter.
Second, ESD removes the style, not only the word. It looks at how the model paints Van Gogh, then trains it to paint the other way. So even without his name, his style is weakened.
What does this mean in real life? On this model, the erasure holds. The real risk is a model that understands Chinese or Japanese. An English-only erasure may not cover it.
And one thing the score missed: the swirling sky still appears.

## Slide 11 · Lessons
Three lessons.
One: check the original model first. Cyber Ninjas used this idea for misspellings. I used it for other alphabets.
Two: the erasure removes the style, and only that style.
Three: compare both models against one fixed reference. The erased model makes even plain village paintings less like Van Gogh. Against that lower baseline, the description looked 99 percent safe. Against a fixed reference, almost nothing was left. This changed how I measure.
About the interaction: I posted my prediction and both results on Ed. Cyber Ninjas did not reply, and no team chose to attack our project. So there was no counter-move to study. Next time, I would ask them one short question they can answer quickly.

## Slide 12 · My role, thank you
My role: I chose the target, designed both test rounds, built and ran both notebooks, and wrote every Ed post.
The attack did not succeed. But the method, the controls and the results are all in the shared notebooks.
Thank you.
