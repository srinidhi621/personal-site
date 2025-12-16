# The Million-Token Question: Does More Context Actually Make LLMs Smarter?

**A prelude on context engineering, long windows, and why “just add tokens” is not a strategy**

---

It started as a small, annoying moment that felt familiar.

We had a system in production. One with users and latency budgets and those tiny niggles that only show up after we've run it for multiple data sources, multiple personas, na dhave got burnt more than a few times. 

And we kept bumping into the same constraint: context. The thing you stuff into the prompt to make an LLM API call do something.And we kept thinking: “If only we had a million-token window, this would be easy.” And we're working with a 128k context window (Looking at you, GPT-4o)

It’s a reasonable thought. Bigger context windows are genuinely useful. They save you from making hard choices. They let you carry more of the world into the prompt. They make a bunch of awkward retrieval problems feel… optional.

But does it really? Do **Bigger context windows automatically make systems better.**

That’s the claim I want to test.

Not because I’m rooting against long context. I’d love for it to work. It would simplify a lot of architecture. It would make a lot of product decisions easier. It would make half the “RAG vs long context” threads on the internet wonderfully obsolete.

I’m just not sure it’s true. We've seen glimpses of lost-in-the-middle, we've seen retrieval miss the right chunk, we've seen the model get distracted by the wrong thing. But can we prove it?

So this is the prelude: the premise, the hypotheses, and the experimental design. The results come later.

## The premise

Context windows have become the new scoreboard.

We went from 4k → 32k → 128k → 1M (and beyond) in what feels like a blink. The narrative has shifted from “be surgical with context” to “just dump everything in.”

And I get why. If you can fit an entire small book into the prompt, why bother being careful? If you can fit something closer to a bookshelf, surely the model can do the rest.

Except… models don’t read like humans read.

They allocate attention. They pattern-match. They can get distracted. They can miss the one sentence you actually cared about while confidently summarizing a dozen you didn’t.

If you’ve ever watched someone search for their keys while holding their keys, you already understand the shape of the problem.

That brings us to three questions.

## The questions

### 1) Does adding a lot of tokens actually help, or does it just add more places to get lost?

The “Lost in the Middle” line of work showed that even at relatively modest lengths, models can struggle to use information buried deep in a long context.

If you jump to a million tokens, does that problem go away?

Or does it turn into something like: “the middle is now spread out in patches” — a little bit of forgetfulness everywhere.

### 2) Can disciplined context engineering compete with brute force?

There are two ways to build a knowledge-heavy system:

One is brute force: put everything into the prompt and hope the model finds what it needs.

The other is a bit more boring, but a lot more effective: retrieve what matters, package it cleanly, add structure, and keep the model’s job simple.

The “disciplined” approach has real overhead: indexing, chunking, retrieval quality, reranking, caching, evaluation. It’s engineering work.

So the question is: **does that work still matter when the window is huge?**

### 3) What happens when the context is messy?

Most real world data isn't clean. It never is. They have duplication. They have near-duplicates. They have stale documents that still sound authoritative. They have “this is deprecated” written in a paragraph that looks like every other paragraph.

So even if long context works in a clean benchmark, does it degrade gracefully when the prompt is polluted with irrelevant material?

(“Pollution” is the term used in some papers. It sounds dramatic until you’ve debugged a prompt that’s 60% irrelevant. Then it feel painfully descriptive.)


## The hypotheses (stated plainly)

### Hypothesis 1: Long context is not a magic bullet

Even with million-token windows, naïvely stuffing context underperforms engineered packaging and retrieval.

In other words: **more tokens don’t automatically mean better results.** How you organize those tokens matters.

### Hypothesis 2: Smart can beat big (sometimes)

A smaller, disciplined approach can match or beat a naïve long-context approach on practical tasks, with better cost/latency trade-offs.

This hypothesis is not “small always wins.” It’s “small can win more often than people assume.”

If both hypotheses are wrong, that’s still useful. It would mean the architecture landscape has genuinely changed.

Either way, we get data instead of opinions.

## The experimental design (the part that makes this fair)

Here’s the trap most comparisons fall into:

If you compare a system that uses 50k tokens to a system that uses 900k tokens and then attribute the difference to “better engineering", it wouldn't be fair. Because two things are changing at once:

- retrieval/packaging quality
- the sheer **load** the model has to deal with

If one approach gives the model a small haystack and the other gives it a haystack the size of ten houses, and the small-haystack approach performs better… what did you learn?

Maybe it has better technique. Or maybe you just didn’t drown it.

So the key control in this project is **fill percentage**: how full we make the context window.

### The fill-percentage control (aka “keep the haystack size the same”)

At each condition, we target the same fill levels: **10%, 30%, 50%, 70%, 90%**.

At 70% fill, we’re aiming for roughly 700k tokens of context.

And every strategy gets a context of that size.

If a retrieval-based approach only needs ~90k tokens of relevant material, that’s fine. We still pad it to the target fill level with irrelevant content. This is intentional. It is not “extra helpful context.” It is just load.

If you want the metaphor: we keep the haystack size the same, and we fill the rest with grass.

If you want the more technical framing: we equalize attention strain so differences reflect context engineering quality, not simply “one prompt was lighter.”

And yes, the padding corpus is classic literature (Project Gutenberg), because it’s clean, free, and obviously irrelevant to the domain. Think “Charles Dickens novels" whereas the rest of our retrieval happens on HuggingFace's recent model cards. 

## The strategies

We test four strategies that represent real choices teams make:

1) **Naïve long-context**  
Sequential document concatenation. Minimal structure. The “just dump everything in” baseline.

2) **Structured long-context**  
Same underlying documents, but packaged with explicit boundaries, metadata, and a table of contents so the model can navigate instead of guessing.

3) **Basic retrieval (RAG)**  
Retrieve top-k relevant chunks and assemble a focused context.

4) **Advanced retrieval**  
Hybrid retrieval and fancier ranking tricks (the stuff you read at 1am and swear will matter under noise).

The point is not to crown a universal winner. The point is to map the behavior under different loads and different kinds of mess.

## The data (that is not memorized by our models during pre-training)

For the main corpus, we use **recent Hugging Face model cards**.

Model cards are surprisingly good for this kind of experiment:

- They’re technical but readable.
- They contain specific claims and metadata (licenses, parameter counts, training notes, usage instructions).
- They’re auditable: you can trace answers to text, not vibes.

For padding/pollution, we use Project Gutenberg text because it gives us a large, clean, obviously irrelevant pool.

The goal isn’t to trick the model with adversarial nonsense. The goal is to simulate what production looks like: plenty of plausible-looking text that is, for the current question, irrelevant.

## What we measure

“Quality” is tricky. It’s also the thing people hand-wave most.

We measure a few things that are directly useful:

- **Correctness**: did it answer accurately?
- **Grounding / citation accuracy**: are the claims supported by the provided context?
- **Latency**: how long did it take?
- **Token usage**: because at scale, tokens are cost and cost becomes product strategy

We keep the generation deterministic (temperature **0.0**) and repeat each condition multiple times to avoid over-reading a single run.

## What we’re not testing (yet)

To keep the results interpretable, this experiment avoids a few rabbit holes:

- We’re not doing a multi-provider bake-off. That turns into a model comparison, not a methodology comparison. So no OpenAI vs Anthropic vs Google vs etc.
- We’re not fully sweeping “position effects” (needle at start vs middle vs end). It matters, but it deserves its own experiment.
- We’re not claiming universal generalization across domains. The goal is a replicable harness that can be moved to other corpuses.

## Why this matters 

If you’re building LLM systems, long context is tempting because it looks like it removes the need for discipline.

But there’s a real possibility that it simply changes the failure mode:

- from “retrieval missed the right chunk”
- to “the right chunk was present, but the model didn’t use it reliably under load”

If that’s true, context engineering doesn’t go away. It becomes more important.

And if it’s false — if million-token context windows truly make naïve stuffing competitive — that’s a real shift. It would change where teams invest. It would simplify systems. It would move effort elsewhere (evaluation, monitoring, post-processing).

Either way, it’s worth measuring.

The follow-up will cover the results, the trade-offs (quality × cost × latency), and the failure cases. The kind that actually show up in production.

---

**Reference**  
Liu et al., 2023 — “Lost in the Middle: How Language Models Use Long Contexts”
