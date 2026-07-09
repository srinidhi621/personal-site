---
title: "The Million Token Question: What We Actually Found"
date: 2026-01-02T00:00:00Z
draft: false
tags: ["llm", "context", "rag"]
summary: "Structured context beat naive long context. Retrieval handled noise better. Simple baselines held up better than expected."
description: "Results from experiments comparing naive long context, structured context, and retrieval under controlled fill percentages."
---

# The Million Token Question: What We Actually Found

These results came after a pilot fix and 4,380 API calls across two experiments. I chose to keep the fill percentage control even when retrieval needed fewer relevant tokens, because the comparison would otherwise reward smaller prompts rather than better context strategy. The pilot expected "256k" for one answer, but the source documents said "128k," so I fixed the label before running the full set. Then the first full run hit a 429, so I made the runner resumable. After those fixes, the main results were:

- Structured 1M context outperformed naive 1M context by 68 percent on answer quality in these runs.
- Retrieval helped most when irrelevant text dominated the corpus. At 19 to 1 noise to signal, RAG variants more than doubled naive long context performance.
- Basic BM25 retrieval matched or slightly beat the more complex hybrid setup on this dataset.
- Choosing a strategy means choosing tradeoffs in latency and error tolerance. It also changes how much system complexity you are willing to own.

Read the framing post first. [The Million Token Question: Does More Context Actually Make LLMs Smarter?](/writing/context-engg-prelude/).

## What Changed My View

I expected structure to help. I did not expect it to help this consistently.

I also expected the more complex retrieval stack to beat a basic BM25 baseline. It did not on this corpus. Naive long context also failed more sharply than I expected around the middle of the window.

The project stopped feeling theoretical when the pipeline broke in specific ways. The pilot found a bad ground truth entry. The evaluation expected "256k" even though the source documents said "128k." An early 429 forced me to make the runner resumable before I could finish the full experiments.

Those surprises came out of 4,380 API calls across two experiments. That is enough volume to take the patterns seriously. It is still narrow enough that the conclusions need to stay scoped to this workload.

## Finding 1. Structure Beat Naive Long Context

If you use long context, structure is part of the method.

![Strategy comparison showing structured context outperforming naive long context](exp1_strategy_comparison_fixed.svg)

Across Experiment 1, structured long context averaged F1 0.228. Naive long context averaged 0.136. That is a 68 percent relative improvement. The absolute scores matter less than the gap. The same window size produced different behavior when I changed how the material was packaged.

The second important result was stability across fill levels.

![Performance degradation showing naive collapse at 50% fill](exp1_degradation_curve_fixed.svg)

At 30 percent fill, naive long context held at F1 0.188. At 50 percent fill, it fell to 0.019. Structured long context did not show the same instability. More tokens were not the whole problem. Unstructured long context became unreliable under some load conditions.

If a team wants to use long windows, it should add explicit document boundaries and metadata headers from the start. For large sets of documents, it should also add a usable table of contents.

## Finding 2. Retrieval Became Essential When Noise Increased

The second experiment tested what happens when relevant material appears inside a lot of plausible but irrelevant text.

![Pollution robustness showing retrieval advantage at extreme noise](exp2_pollution_robustness_fixed.svg)

At moderate pollution levels, the strategies clustered fairly closely. No strategy separated decisively. At 950k pollution tokens, the picture changed. Basic RAG reached F1 0.307. Advanced RAG reached F1 0.314. Naive long context reached F1 0.148.

The 950k pollution run looked closer to a messy internal corpus than to a clean benchmark. A stale wiki page or duplicated doc can look plausible enough to distract the model. In that setting, retrieval is useful because it keeps most irrelevant material out before generation.

Full context approaches can still be useful. Once noise crosses a certain level, a system that can ignore most of the corpus has a clear advantage.

## Finding 3. Simple Baselines Held Up Better Than Expected

I assumed the advanced retrieval stack would clearly beat basic BM25 retrieval. On this dataset, it did not.

Basic RAG averaged F1 0.221. Advanced RAG averaged F1 0.217. That difference is small enough to treat as noise in practical terms. It still matters directionally because the simpler baseline was at least as good as the more complicated system.

The likely reason is domain fit. Technical documentation often repeats exact names from the source. A question may include the same model name or parameter name that appears in the answer. BM25 can work well when the question and the source share precise terms. In that environment, embeddings and reranking add complexity faster than they add value.

If your source material looks like API docs or model cards, start with BM25 and measure from there. Add hybrid retrieval only after the simple baseline stops being good enough. Reranking and query decomposition should earn their complexity in your own evals.

## A Decision Framework

The most useful outcome of this work is a better way to choose.

- For latency sensitive production systems, start with retrieval. In these runs, retrieval processed roughly 92k tokens regardless of corpus size. Full context approaches grew with window usage and could exceed 60 seconds near the high end.
- For offline or batch analysis, structured full context can be reasonable when you can tolerate higher latency and want the best answer quality from a large window.
- For noisy corpora, retrieval is the safer default because it can filter irrelevant material before generation.
- For new builds, benchmark a BM25 baseline before adding hybrid complexity. On this corpus, the simple baseline was competitive with the more elaborate stack.
- For any system using long context, measure fill percentage during evaluation. Window size alone tells you very little about how the system will behave under load.

![Latency vs tokens showing retrieval stays flatter as context grows](exp1_latency_vs_tokens.svg)

That last point matters for operational planning. Retrieval kept latency relatively predictable because the generation prompt stayed small. Full context strategies grew with prompt size. If your team has strict latency or cost targets, that difference changes capacity planning.

## Why Fill Percentage Mattered

Fill percentage was the most important control in the study.

A lot of long context versus retrieval comparisons are confounded. One system sees a crowded prompt. The other sees a lighter one. If the lighter system wins, you do not know whether it won because retrieval was better or because the model had less to process.

To isolate context engineering from prompt size, I padded every strategy to the same percentage of its available window. That made fill percentage a rough measure of attention strain. It also exposed the naive long context failure zone around 50 to 70 percent fill.

If you are evaluating context strategies in your own stack, track fill percentage explicitly. It can change quality more than teams expect.

## Method Summary

This is the compact version of the setup.

- The comparison used four strategies. Two used the full 1M context window, one with structure and one without it. The other two used retrieval, with basic RAG and advanced RAG.
- I tested 10 percent to 90 percent fill in 20 point steps.
- The relevant corpus was recent Hugging Face model cards.
- The irrelevant padding and pollution came from Project Gutenberg text.
- The model was Gemini 2.0 Flash Experimental at temperature 0.0.
- The environment used identical prompts across strategies. I measured elapsed time on a single GCP VM with serial requests and no batching.

The free tier setup shaped the runner. I had to throttle requests for rolling token caps and stop before the 1,000 embedding daily cap. After an early 429, I changed the runner so it could resume from the last completed item. I tracked answer quality and grounding behavior. I also tracked latency and cost. For the reported F1 results, differences smaller than about 0.01 should be treated as noise.

## Limits

These results are useful, but they are bounded.

The study uses Gemini 2.0 Flash against Hugging Face model cards. The questions are mostly factual lookup and synthesis questions. Do not assume the same ranking will hold for code assistants or legal search. The absolute F1 numbers are also less important than the relative differences between strategies, because the evaluation was intentionally strict.

The safest claim is narrow. In this workload, context engineering changed system behavior materially. You should test whether the same ranking holds in your workload.

## Bottom Line

A larger context window gives capacity. A team still has to decide how to use that capacity.

In these experiments, structure made long context more reliable. Retrieval helped once the corpus had a lot of irrelevant text. Basic BM25 was better than I expected. The right choice depends first on latency and noise. Operational complexity comes next.

That is why I think context engineering deserves attention as a discipline. Teams need that work if they want raw model capacity to produce predictable system behavior.

*The full repo and analysis are available at [github.com/srinidhi621/context-engineering-experiments](https://github.com/srinidhi621/context-engineering-experiments).*

*Last updated: March 13, 2026*
