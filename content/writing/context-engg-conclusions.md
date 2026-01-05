---
title: "The Million-Token Question: What We Actually Found"
date: 2026-01-02T00:00:00Z
draft: false
tags: ["llm", "context", "rag"]
summary: "After 4,380 API calls, we found that context engineering matters more than context size."
description: "Results from a 10-week experiment testing naive long-context, structured context, and RAG strategies across fill percentages."
---

# The Million-Token Question: What We Actually Found

**After 4,380 API Calls and 10 Weeks of Stress-Testing the Future**

---

I'll be honest: when we started this project, I expected the results to be boring. The "long context vs RAG" debate has been done to death in blog posts and Twitter threads. Everyone has opinions. Few have data.

So we got data. A lot of it.

4,380 API calls. Four different strategies. Fill percentages from 10% to 90%. Temperature locked at 0.0 so we could actually trust the results. And after ten weeks of running experiments, debugging pipelines, and staring at log files, we found something that genuinely surprised us.

But I'm getting ahead of myself.

---

## What We Were Testing

The premise was simple. Large language models now support context windows of a million tokens (roughly 750,000 words, about ten novels crammed into a single prompt). The marketing pitch writes itself: just dump everything in and let the model figure it out.

But does that actually work?

We had two hypotheses going in. First, that even with massive windows, naively stuffing context would underperform more thoughtful approaches: structured packaging, retrieval, the stuff engineers have been doing for years. Second, that smaller models with good engineering might match or beat larger contexts used carelessly.

The real question underneath both: **When models keep getting bigger, and can theoretically read everything, does it still matter *how* you give them information?**

If you haven't read the setup, start with the prelude: **[Does More Context Actually Make LLMs Smarter?](/writing/context-engg-prelude/)**.

---

## The Four Strategies

We set up a controlled experiment with four approaches:

1. **Naive 1M**: The "just concatenate everything" approach. No structure, no organization. We literally dumped documents end-to-end and hoped for the best. This is what most people do when they first get access to a large context window.

2. **Structured 1M**: Same documents, same million-token window, but with actual engineering. A table of contents at the top. Clear document boundaries. Metadata tags. Section headers.

3. **Basic RAG (128k)**: Traditional BM25 retrieval. Top-k chunks, nothing fancy. The production workhorse.

4. **Advanced RAG**: Hybrid search combining dense embeddings with BM25, reciprocal rank fusion, query decomposition. The cutting-edge stuff from research papers.

Here's the methodological piece that mattered most: we padded all strategies to identical fill percentages. Every comparison at 30% fill meant both strategies used exactly 30% of their available context window. Without this control, you can't tell if performance differences come from better engineering or just attention dilution. We wanted clean answers, not confounded results.

---

## What Actually Happened

### The 50% Fill Percentage Cliff

Everyone's heard of "Lost in the Middle," the research showing models lose track of information buried deep in their context. We expected that effect. What we didn't expect was where it hit.

![Performance degradation showing naive collapse at 50% fill](exp1_degradation_curve_fixed.svg)

At 30% fill, naive holds at F1 0.188. Then at 50% fill, it falls off a cliff, dropping to 0.019. Not graceful degradation. Catastrophic failure. And then, weirdly, it *recovers* at 90% fill, climbing back to 0.189.

We checked the raw outputs. At 50% fill, naive was not only getting questions wrong, but it was producing garbled, incoherent responses. Our best guess: when the context gets very dense, the model leans on positional heuristics to survive. In the middle (50–70% fill), there's enough padding to diffuse attention but not enough structure to anchor it. But here, I'm not really sure, we'll need to run more experiments to figure out what's going on.

The structured metadata+TOC approach? Flat line across all fill levels. Boring. Reliable. Exactly what you want in production.

![Heatmap showing strategy and fill level interaction](exp1_strategy_fill_heatmap.svg)

That red-bordered cell in the heatmap tells the whole story. Naive at 50% fill is a danger zone.

### Engineering Actually Matters (Even at 1M Tokens)

So does structure help? Here's the headline number: **68% relative improvement**.

![Strategy comparison showing 68% improvement over naive](exp1_strategy_comparison_fixed.svg)

Structured averaged F1 0.228. Naive averaged 0.136. That's not a rounding error. That's the difference between a system that works and a system that frustrates users.

Structure helping was expected; structure helping *everywhere* was not. Even at low fill percentages, where you'd think there's plenty of room for the model to find what it needs, structure added value.

![Relative performance lift showing percentage improvements](exp1_relative_lift.svg)

The horizontal bars make it visceral. Structured: +68%. RAG: +63%. Advanced RAG: +60%. Naive: baseline. If you're using naive long-context in production, you're leaving performance on the table.

### The RAG vs Advanced RAG Surprise

Here's where our expectations got humbled. We assumed Advanced RAG (with its hybrid search, reranking, and query decomposition) would clearly beat basic BM25 retrieval. Fancier should mean better, right?

It didn't. Basic RAG averaged 0.221 F1. Advanced RAG averaged 0.217. Not only was the difference not significant, the basic approach *slightly outperformed* the fancy one.

Our theory: for technical documentation with clear keywords (model names, API parameters, error codes), BM25's lexical matching works really well. Dense embeddings add compute cost without proportional benefit. The "advanced" in Advanced RAG is domain-dependent.

This doesn't mean advanced retrieval is never worth it. But it means you should test against a BM25 baseline before piling on the complexity.

### What Happens When You Add Noise

Experiment 2 tested pollution. We started with a clean 50k-token corpus containing all the answers, then progressively buried it in plausible but irrelevant content. 50k extra tokens. Then 200k. Then 500k, 700k, and finally 950k, a 19:1 noise-to-signal ratio.

![Pollution robustness showing RAG advantage at extreme noise](exp2_pollution_robustness_fixed.svg)

At moderate pollution (50k to 700k), all strategies clustered together around F1 0.05-0.07. Structure helped a little. Retrieval helped a little. Nothing broke away from the pack.

Then came 950k pollution, and the lines diverged. RAG jumped to 0.307 F1. Advanced RAG hit 0.314. Meanwhile, naive crawled to 0.148. The green shaded region marks where retrieval became essential: the ability to *ignore* most of the context determined success.

There's a threshold, and it's not where you'd expect. Below it, everyone struggles. Above it, retrieval becomes a necessity rather than a preference.

---

## The Trade-offs You Actually Face

I wish I could tell you one strategy wins on every metric. It doesn't work that way.

![Pareto plot showing quality-latency trade-offs](pareto_quality_latency.svg)

That dotted line is the Pareto frontier, the set of strategies where you can't improve one metric without losing out on another. Structured sits at the top right: best quality (0.228 F1), but highest latency (45.8 seconds). Advanced RAG is the balanced option: slightly lower quality (0.217 F1), but faster (35.3 seconds). Naive is quick but unreliable.

![Latency vs tokens showing RAG stays constant](exp1_latency_vs_tokens.svg)

See that cluster of blue points at the left? That's RAG, processing about 92k tokens regardless of corpus size. The orange and teal scatter spreading rightward? That's naive and structured, scaling linearly with context. At 900k tokens, full-context strategies take 60+ seconds. RAG stays flat. For any system with an SLO, that predictability matters.

![Summary table with all boring metrics](summary_table.svg)

**Method notes:** All runs used Gemini 2.0 Flash Experimental at temperature 0.0, identical prompts across strategies, padded contexts to fixed fill percentages (10–90%). Latency was measured wall-clock on a single GCP VM (n2-standard-4) with serial requests and no batching. Variance across repeated runs was low enough that differences under ~0.01 F1 should be treated as noise.

---

## What This Means for Your Work

I'll resist the urge to write prescriptive rules. Your use case isn't my use case. But here are some of the takeaways.

**Production systems which are sensitive to latency**
- Prefer RAG for predictable latency and cost. Easy to build, easy to scale, easy to maintain and estimate costs & latency.
- If you need higher quality, consider structured full-context, but budget for the longer tail latencies at high fill.

**Batch or offline analysis**
- Structured 1M delivers the best quality when latency is less critical. The 68% lift over naive is effectively free performance once you add a TOC and consistent boundaries.
- Re-run evaluations when your fill percentage changes; the 50–70% naive cliff is real.

**Noisy or polluted text data**
- Route through a retriever. At 19:1 noise-to-signal, RAG variants more than doubled naive performance. Retrieval isn't just helpful in this regime; it's the only thing keeping quality above random.

**Greenfield builds**
- Start with a BM25 baseline before adding hybrid complexity. In our domain, BM25 matched or beat the fancier stack at lower operational overhead.
- Decide your fill budget early and engineer to it. Padding to controlled percentages was the most revealing part of this study.

And regardless of what you choose: **measure fill percentage**. It affected quality more than any other variable we tested.

---

##  A few important caveats, because no single study answers everything.

We tested one model: Gemini 2.0 Flash Experimental. Models from Anthropic, OpenAI, Meta and others might behave differently. We tested API documentation and financial reports; code, legal documents, and scientific papers might show different patterns. We focused on lookup and synthesis questions; summarization and multi-turn conversation might favor different strategies.

The absolute F1 numbers are low because our answers were short and the evaluation metric was strict. The value is in the *relative* differences between strategies, not the raw scores.

These limitations don't invalidate our results. They define their scope.

---

## The Bigger Picture

This project started as a hypothesis test and became an argument: **context engineering deserves serious attention as a discipline.**

"Just use a bigger window" is not engineering advice. Having a million-token window doesn't mean you should use it all, any more than having a terabyte of RAM means you should ignore memory management. Scale doesn't eliminate the need for discipline; it just changes what discipline looks like.

We found that:
- **Structure matters**, even when you have plenty of room
- **Retrieval matters**, especially when signal is buried in noise
- **Fill percentage matters**, more than raw context size
- **Simple baselines often beat fancy techniques**, at least in our domain

None of these are universal laws. All of them are testable in your context. And that's the real takeaway: **empirical evaluation beats intuition**. The only way to know what works for your use case is to measure.

---

## The Bottom Line

We started with a question: when we have models with million-token context windows, does engineering discipline still matter?

After 4,380 API calls and ten weeks, the answer is yes. Not "it depends" or "maybe." Yes.

Structured context beat naive by 68%. The gap appeared at every fill level. Retrieval filtered noise that full-context approaches couldn't ignore. Simple BM25 matched fancy hybrid retrieval. And naive long-context collapsed catastrophically at 50% fill, something no one predicted.

The "just throw more context at it" instinct is easy because it feels like progress. It's not. It's technical debt dressed up as capability.

Context engineering is a real discipline with real trade-offs. Understanding those trade-offs (quality, cost, latency, robustness) enables better decisions than following trends.

I hope this data helps you make those decisions.

---

*All data, code, and analysis available at [github.com/srinidhi621/context-engineering-experiments](https://github.com/srinidhi621/context-engineering-experiments).*

*Last updated: January 2, 2026*
