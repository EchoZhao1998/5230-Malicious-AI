I’m simplifying the draft for a broader audience while preserving the technical meaning and the challenge framing.

Read 

Replacing 154 lines with 144 lines in 

## Simpler version of the post

Below is a cleaner, more accessible version you can use for a broader audience.

---

# M2 — Dark.Tyro: a cheaper wash and a challenge for defenders

Team Dark.Tyro  
Theme 2 (Text-to-Image), Dark / attack side  
Milestone 2, 18 September 2026

In short, we found a simple way to make the wash step in the IMPRESS attack cheaper without losing much of its effect. We also found that the usual evaluation metric in this setting can miss the protection signal, so we created a public challenge: the Tyro Wash Test.

## 1. The main idea

The editor does not treat every pixel in an image the same way. Some pixels are kept, while others are repainted.

In this project, the inpainting mask tells us which region is preserved and which region is regenerated. The white area is mostly kept by the editor. The black area is largely redrawn.

The original wash process cleaned the whole image, even the areas the editor would repaint anyway. That wastes effort and damages the photo more than necessary.

So we changed the wash to act only in the region the editor keeps:

```python
purified_v2 = mask * purified_impress + (1 - mask) * protected
```

This means:
- keep the cleaned result inside the mask
- keep the protected image outside the mask
- blur the edge of the mask so it does not create a visible seam

In plain terms, we wash only the part that matters instead of scrubbing the entire photo.

> Think of it like sanding only the wall that stays visible, instead of sanding the whole room.

## 2. What we measured

We compared several variants under the same attack setting and the same input faces:

- no wash
- the original IMPRESS wash
- a stronger IMPRESS wash
- our mask-restricted wash

We looked at two quantities:

- R_pipe: how much the wash recovered the editing pipeline
- LPIPS: how much the photo itself was damaged

A strong attack should do two things:
- recover the image generation pipeline
- keep the original photo visually close to the clean one

The trade-off is the key point: if a method undoes the attack but destroys the image, it is not really useful.

## 3. The result

We found that our mask-restricted wash performs almost as well as the baseline IMPRESS wash, but costs much less.

| Variant | Wash type | Recovery (R_pipe) | Photo damage (LPIPS) |
|---|---|---:|---:|
| N | no wash | 0.00 | 0.018 |
| A | original IMPRESS wash | 4.75 | 0.150 |
| B | stronger IMPRESS wash | 9.41 | 0.109 |
| C | our method: mask-restricted wash | 7.05 | 0.039 |

The main point is this:

- C is not the strongest wash
- but it reaches a similar recovery level at a much lower perceptual cost

So the method is cheaper, and that matters. It lets us achieve a large part of the benefit without paying the full visual cost of washing the whole image.

## 4. Why this matters

This project is not just about making an attack stronger. It is about finding a better balance between:

- making the attack work
- preserving the photograph

A method that destroys the image is not a practical attack, because it removes the content the editor would otherwise have used.

Our result suggests that the wash should be targeted to the part of the image that matters, not applied blindly everywhere.

## 5. Why the usual metric can be misleading

We also found that the standard metric used in the original setup does not always detect the protection well enough. In other words, the metric can miss the effect of the shield even when the attack is genuinely there.

This is important because it means we cannot trust a single number without checking the full trade-off. We therefore report both:
- how much the wash restored the edit
- how much visual quality was lost

This makes the result more honest and more useful for future work.

## 6. The Tyro Wash Test

To make the problem concrete, we created the Tyro Wash Test.

The challenge is simple:

- you are given 10 clean face images and their masks
- you must create a protected version of each image
- the protected image should resist our wash
- but it must still look close to the original

You only need to change one function, `protect()`. The rest of the notebook is just scaffolding.

We do not inspect your perturbation. The purifier is blind to how the defense was made. It only sees the output images.

The challenge is to create a defense that survives the wash without turning the photo into noise.

### Scoring

We score each submission on two axes:

- R_pipe: how much the wash restores the edit
- LPIPS: how much the photo was damaged

A good defense is low on both. A broken defense may survive the wash only by destroying the image completely, but that is not a useful defense because the photo is no longer usable.

This is why we publish both numbers together.

## 7. Why this challenge is useful

The goal is not only to attack a model, but to understand where the attack breaks down, what it can and cannot do, and what a better defense must survive.

This challenge gives other people a clear target:
- build a defense that resists the wash
- keep the image believable and natural
- do not sacrifice the whole photo to win

That makes the competition meaningful and honest.
