---
title: "The Million-Token Question: Does More Context Actually Make LLMs Smarter?"
date: 2025-12-17T00:00:00Z 
draft: false
tags: ["llm", "context"]
summary: "Why million-token windows do not remove the need for retrieval, structure, and disciplined context design."
description: "A framing piece on context engineering: what it is, why it matters, and what this experiment is trying to test."
---

# The Million-Token Question: Does More Context Actually Make LLMs Smarter?

Large context windows changed the architecture conversation around LLM systems. In this project, that question was: With new LLM models supporting million-token windows, does it mean we can stop caring about context engineering?

For a demo, "just include more" can feel good enough. For a production system, the same choice affects answer quality, wall-clock latency, token spend, and how often the model misses the one paragraph that matters.

## What I Mean by Context Engineering

I use "context engineering" to mean the design work around what the model sees and how it sees it: what you include, how documents are broken up and labeled, and how irrelevant text is kept from crowding out the answer.

That definition matters because long context is often treated as if it makes that work obsolete. I do not think it does. A larger window increases input capacity. It does not automatically improve the model's ability to reason over that input, prioritize the right details, or stay reliable under load.

This is the distinction I care about most: input capacity is not the same thing as reasoning capacity.

## The Claim Worth Testing

The claim behind this series is simple: million-token windows are useful, but they are not a substitute for context design.

I wanted to test two ideas.

First, naive long-context prompting should underperform a structured version of the same long-context approach. If both systems are given the same amount of information, the one with clearer boundaries and navigation cues should do better.

Second, a disciplined smaller-context system may match or beat careless use of a larger window. In practice, that would mean retrieval or structured packaging can outperform "just include everything" especially when the raw window size looks impressive.

If either claim is wrong, that is worth learning. If long context really does make most retrieval and packaging decisions unnecessary, a lot of current system design gets simpler. If it does not, then context engineering remains a relevant for real work systems.

## Why This Matters in Practice

Once you move past demos, this becomes a system design question.

Engineers feel this in failed answers and long response times. Product teams feel it in cloud cost and in the awkward moment when the solution hits type 1 and type 2 errors.

A system that can accept a million tokens but becomes erratic halfway through the window is not simpler in any useful sense. It just hides the complexity in a different place.

## How I Set Up the Experiment

To test the question cleanly, I compared four approaches:

1. Naive long context: concatenate documents and pass them through with minimal structure.
2. Structured long context: use the same documents, but add explicit boundaries and a table of contents.
3. Basic retrieval: retrieve relevant chunks with a simple BM25 (keyword search) pipeline.
4. Advanced retrieval: use a more complex hybrid retrieval stack with reranking and noise filtering.

The key control is fill percentage. At each test point, every strategy is padded to the same proportion of its available window. If a retrieval-based approach only needs a small amount of relevant text, the rest of the window is filled with irrelevant public-domain text so the model still has to operate under the same attention load.

That matters because many comparisons between long context and retrieval are accidentally comparing two different things: one system sees a crowded prompt, the other sees a light one. In this setup, the haystack size stays constant. What changes is how the information is organized.

For the source material, I used a corpus of 60-plus Hugging Face model cards published from September to December 2024, totaling about 700k relevant tokens, and roughly 2M tokens of Project Gutenberg text for padding and pollution. That gave me a technical corpus with clear timestamps and a noise source that was obviously irrelevant to the questions being asked.

## What This Study Can and Cannot Tell Us

This study is meant to answer a narrow question well, not a broad question poorly.

It can tell us whether different context strategies behave differently on technical documentation and lookup-style questions as the prompt gets crowded.

It cannot tell us that one strategy wins everywhere. Different model families, document types, and task shapes may behave differently. Code, legal text, scientific literature, or multi-turn agents may produce different results.

That is not a weakness. It is the boundary of the claim.

## The Question for Part 2

So the question going into Part 2 is not whether large context windows are real. They are. The question is whether they reduce the need for context engineering in any meaningful operational sense.

Part 2 covers the results. In these runs, what mattered was not the maximum window on the spec sheet. It was whether the system had structure and how much irrelevant text it had to fight through.
