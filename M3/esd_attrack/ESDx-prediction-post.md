# Ed comment — the cross-script prediction (post BEFORE measuring)
*Drafted 16 Sep 2026. Reply on Light.Cyber Ninjas' M2 thread (discussion/3581230, post #57).*

**Why this is posted before the experiment:** M3's 5-mark row is scored on *how the target team
reacted*. A prediction invites a reply; a finished result does not. Post it, then build.

---

On test case 5 — your reasoning is right, and I want to say so clearly before I disagree with part
of it. "V4n G0gh" tokenises into fragments CLIP has no Van Gogh association for, so the base model
never carried the signal in the first place. An erasure cannot remove what was never there. That is
a limitation of the probe, not of your defence.

But obfuscated spelling and a different writing system are not the same channel. Your multi-descriptor training saw English plus one French translation — both Latin script — and CLIP's text encoder has seen the artist's name written in scripts that are not.

So, as a prediction before I measure it: **your erasure holds on obfuscated spelling and leaks on
non-Latin names.**

Your own argument gives me the test. I will score every prompt on two models — base SD v1-4 and an
esd-x checkpoint. A variant counts as a bypass only if the base model renders the style *and* the
erased model still does. Where the base model shows nothing, your case-5 explanation stands and I
will report it that way.

Your limitations mention wanting a CLIP-based style metric. I will bring those numbers for both
models, so they are directly comparable to your side-by-side results.

Your M2 Colab is still access-restricted, so I am starting from the ESD authors' pre-erased Van Gogh
UNet — same method, same concept, same base model. If you can share the multi-descriptor
checkpoint, I can also test whether variant training closes this gap, which is the more interesting
question and the one I cannot answer without your weights.

---

## Notes for the next session (do not post these)
- **Do not name other Dark teams in the comment.** No reason to point their attention elsewhere.
- **State the hypothesis and the control, not the implementation.** The thread is public; the
  prompt set and harness stay ours until the results post.
- The concession in paragraph 1 is doing real work: it proves the post was read carefully, and it
  is what makes the disagreement in paragraph 2 credible rather than contrarian.
- The last paragraph is the open loop — it asks for something only they can give, so it is the line
  most likely to produce a reply.
