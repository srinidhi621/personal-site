---
title: "The Million-Token Question: What We Actually Found"
date: 2026-01-02T00:00:00Z
draft: false
tags: ["llm", "context", "rag"]
summary: "Structured context beat naive long context, retrieval handled noise better, and simple baselines held up better than expected."
description: "Results from experiments comparing naive long context, structured context, and retrieval under controlled fill percentages."
---

# The Million-Token Question: What We Actually Found

If you only remember four points from this piece, remember these:

- Structured 1M context outperformed naive 1M context by 68 percent on answer quality in these runs.
- Retrieval mattered most when irrelevant text dominated the corpus; at 19:1 noise-to-signal, RAG variants more than doubled naive long-context performance.
- Basic BM25 retrieval matched or slightly beat the more complex hybrid setup on this dataset.
- The real decision is not "long context or RAG." It is which trade-off you want between latency, error tolerance, and system complexity.

Read the framing post first: [The Million-Token Question: Does More Context Actually Make LLMs Smarter?](/writing/context-engg-prelude/).

## What Changed My View

I expected structure to help. I did not expect it to help this consistently.

I also expected the more complex retrieval stack to beat a basic BM25 baseline. It did not, at least not on this corpus. And I did not expect naive long context to fail as sharply as it did around the middle of the window.

The project also stopped feeling theoretical once the pipeline started breaking in a few different ways. The pilot exposed a bad ground-truth entry, where our evaluation expected "256k" even though the source documents said "128k." One early 429 also forced me to make the runner resumable before the full experiments could finish cleanly.

Those surprises came out of 4,380 API calls across two experiments. That is enough volume to take the patterns seriously, but still narrow enough that the conclusions need to stay scoped to this workload.

## Finding 1: Structure Beat Naive Long Context

If you want to use long context, structure is not a cosmetic improvement. It is part of the method.

![Strategy comparison showing structured context outperforming naive long context](exp1_strategy_comparison_fixed.svg)

Across Experiment 1, structured long context averaged F1 0.228. Naive long context averaged 0.136. That is a 68 percent relative improvement. The absolute scores matter less than the gap: the same window size behaved very differently depending on how the material was packaged.

The second important result was stability across fill levels.

![Performance degradation showing naive collapse at 50% fill](exp1_degradation_curve_fixed.svg)

At 30 percent fill, naive long context held at F1 0.188. At 50 percent fill, it collapsed to 0.019. Structured long context did not show the same instability. In other words, the issue was not simply "more tokens hurt." The issue was that unstructured long context became unreliable under certain load conditions.

If a team wants to lean on long windows, explicit document boundaries, metadata headers, and a usable table of contents are part of the method, not polish added at the end.

## Finding 2: Retrieval Became Essential When Noise Increased

The second experiment tested a different question: what happens when the relevant material is buried inside a lot of plausible but irrelevant text?

![Pollution robustness showing retrieval advantage at extreme noise](exp2_pollution_robustness_fixed.svg)

At moderate pollution levels, the strategies clustered fairly closely. Nothing separated decisively. At 950k pollution tokens, the picture changed. Basic RAG reached F1 0.307. Advanced RAG reached 0.314. Naive long context reached 0.148.

The 950k-pollution run is closer to a messy internal corpus than a clean benchmark is. Tickets, PDFs, stale wiki pages, and duplicated docs compete for attention. In that setting, retrieval is not only about reducing cost. It is a way to keep irrelevant material out of the retrieval and generation steps.

The takeaway is not that full-context approaches are useless. It is that once noise crosses a certain threshold, the ability to ignore most of the corpus becomes a real advantage.

## Finding 3: Simple Baselines Held Up Better Than Expected

I assumed the advanced retrieval stack would clearly beat basic BM25 retrieval. On this dataset, it did not.

Basic RAG averaged F1 0.221. Advanced RAG averaged 0.217. That difference is small enough to treat as noise in practical terms, but it still matters directionally: the simpler baseline was at least as good as the more complicated system.

The likely reason is domain fit. Technical documentation has strong lexical signals: model names, parameter names, endpoint names, and error strings. BM25 can do very well when the question and the source share precise terminology. In that environment, embeddings and reranking add complexity faster than they add value.

If your source material looks like API docs or model cards, start with BM25 and measure from there. Add hybrid retrieval, reranking, or query decomposition only if the simple baseline stops being good enough.

## A Decision Framework

The most useful outcome of this work is not a winner. It is a better way to choose.

- Latency-sensitive production systems: start with retrieval. In these runs, retrieval processed roughly 92k tokens regardless of corpus size, while full-context approaches scaled with window usage and could exceed 60 seconds near the high end.
- Offline or batch analysis: structured full-context is reasonable when you can tolerate higher latency and you want the best answer quality from a large window.
- Noisy corpus: retrieval is the safer default because it can filter irrelevant material before generation.
- Greenfield builds: benchmark a BM25 baseline before adding hybrid complexity. On this corpus, the simple baseline was competitive with the more elaborate stack.
- Any system using long context: measure fill percentage during evaluation. Window size alone tells you very little about how the system will behave under load.

![Latency vs tokens showing retrieval stays flatter as context grows](exp1_latency_vs_tokens.svg)

That last point matters for operational planning. Retrieval kept latency relatively predictable because the generation step stayed small. Full-context strategies grew with prompt size. If your system has SLOs, concurrency constraints, or cost targets, that difference is not abstract.

## Why Fill Percentage Mattered

Fill percentage was the most important control mechanism in the study.

A lot of long-context versus retrieval comparisons are confounded. One system sees a crowded prompt. The other sees a lighter one. If the lighter system wins, you do not know whether it won because retrieval was better or because the model had less to process.

To isolate context engineering from prompt size, every strategy was padded to the same percentage of its available window. That made fill percentage a proxy for attention strain. It is also what exposed the naive long-context failure zone around 50 to 70 percent fill.

If you are evaluating context strategies in your own stack, track fill percentage explicitly. It can change quality more than teams expect.

## Method Summary

This is the compact version of the setup:

- Four strategies: naive 1M context, structured 1M context, basic RAG, and advanced RAG.
- Fill levels ranged from 10 percent to 90 percent, in 20-point steps.
- Relevant corpus: recent Hugging Face model cards.
- Irrelevant padding and pollution: Project Gutenberg text.
- Model: Gemini 2.0 Flash Experimental at temperature 0.0.
- Environment: identical prompts across strategies; latency measured wall-clock on a single GCP VM with serial requests and no batching.

The free-tier setup mattered here. The runner had to respect rolling token caps and a 1,000-embedding daily cap, and it had to resume cleanly after 429s. I tracked answer quality, grounding behavior, latency, and cost. For the reported F1 results, differences smaller than about 0.01 should be treated as noise.

## Limits

These results are useful, but they are not universal.

The study uses one model family, one main corpus type, and question styles centered on factual lookup and synthesis. Code assistants, legal search, scientific literature, or multi-turn agents may behave differently. The absolute F1 numbers are also less important than the relative differences between strategies, because the evaluation was intentionally strict.

The safest claim is this: in this workload, context engineering changed system behavior materially. Whether the same ranking holds in your workload is something you should test, not assume.

## Bottom Line

A larger context window is capacity, not a strategy.

In these experiments, structure improved long-context behavior, retrieval protected the system when noise rose, and a simple baseline held up better than expected. The right decision was not determined by the biggest available window. It was determined by the combination of answer quality, latency tolerance, noise level, and operational complexity.

That is the reason I think context engineering deserves attention as a discipline. It is the work that turns raw model capacity into predictable system behavior.

*The full repo and analysis are available at [github.com/srinidhi621/context-engineering-experiments](https://github.com/srinidhi621/context-engineering-experiments).*

*Last updated: March 13, 2026*
