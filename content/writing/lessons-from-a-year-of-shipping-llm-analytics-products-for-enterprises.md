---
title: "Lessons From a Year of Shipping LLM Analytics Products for Enterprises"
date: 2026-01-07T00:00:00Z
lastmod: 2026-01-07T00:00:00Z
draft: false
tags: ["ai", "llm", "analytics", "enterprise", "product", "data"]
summary: "Lessons from shipping LLM-powered analytics and decision-support systems into production for regulated enterprises: what mattered, what broke, and how we made them reliable."
description: "Six pragmatic lessons from a year of shipping LLM-backed analytics products for regulated enterprises: workflow-first design, data contracts, evaluation, layered security, inspectability, and planning for vendor drift."
---

Over the last year we've shipped a few LLM-powered analytics and decision-support products into production for regulated enterprises: finance, risk, operations, customer analytics.

2024 was around the time we went from "chat with your PDF" toys to production-ready LLM-backed solutions that sit on top of real data models, real SLAs, and real executives asking, "Can I use this in next month's review?"

A year later (and after enough releases, incidents, and "why did it say that?" moments), some patterns kept repeating. Here are six that changed how we built and operated these systems.

## Start from workflows, not from the model

Most LLM projects start the same way: pick a model, pick a vector DB, build a chat UI, and then ask, "So... what should this actually do?"

The useful ones start from a different place:

- Start with **who** this is for and **when** it shows up. Finance lead at month-end? Risk analyst in a weekly review? Ops in daily monitoring?
- Then write down the small set of questions that keep repeating. Not "everything you could ask." The questions people actually raise in reviews.

Once those are written down, design stops being abstract:

It forces decisions.

Which datasets matter (and which are distractions). What a "good" answer looks like (table vs narrative, which grain, which caveats have to be present). And what success means in a way you can defend: "If we automate these questions reliably, this is worth keeping."

We also learned to ship narrow slices first: one persona, one workflow, one coherent data slice, end-to-end. When that slice behaves like a boring internal system (no drama at month-end), then we earn the right to add the next persona or workflow.

> If you can't ignore the system for a week without anxiety, it's not ready for expansion.

## The data model is the real prompt (and it needs domain brains)

Once we'd scoped down to a narrow workflow, the next place things broke was the data.

LLMs are very good at language. They are not magic against messy data.

Every time we tried to shortcut the data work, the system paid us back with creative but wrong answers: line items moved, new hierarchies appeared, slightly different charts of accounts arrived, and the model happily pretended nothing had changed.

We started with clear separation between raw and curated data zones. Raw data lands in an immutable store; anything surfaced to analytics lives in a curated model with its own versions, owners, and release notes. On top of that, we wrote data contracts humans could actually read: metric definitions, grain, tolerances, refresh cycles. And we made prompts schema-aware: the model is given the actual schema snapshot for the current tenant. If that contract breaks, the request fails fast instead of hallucinating.

That's the structural part. The second half is domain understanding.

In early demos, we could type "Act as a [domain] expert" in a prompt, pour some definitions into a vector store, and call it done. In production, that falls over quickly. Modern LLMs already know the textbook view of a domain; what they don't know is an organisation's view, and its users' view:

How your organisation defines margin, exposure, churn, risk buckets. Which adjustments are "standard" vs "one-off". What counts as signal vs noise in your context.

We ended up needing domain experts in a few specific loops. They helped design the data model and contracts (the schema must reflect how the business thinks, not how a single data engineer saw the source system). They shaped prompts and behaviours: the prompt's job is to reliably trigger the behaviours we wanted (compare across periods, reconcile narrative with numbers, apply house definitions). This sounds obvious until you ship it.

They also validated ground truth. "Looks right" is not good enough. We needed worked examples, reconciliations back to known reports, and explicit sign-off from SMEs on what counts as "correct" or "acceptable with caveats." And finally, they pressure-tested the edge cases (partial periods, late-arriving data, restatements, backfills). This is where the system gets exposed.

> When developers own prompts and domain definitions alone, the result is usually impressive... and quietly wrong.

## Measure it like any other critical system

So we'd scoped workflows, modelled the data, and put domain experts in the loop. Now comes the part that makes it sustainable: instrumentation.

LLM systems fail differently from traditional apps, but the cure is familiar: instrumentation, evaluation, and cost visibility.

We started with a long list of metrics and cut it down to four that reliably caught regressions:

- **Answer quality:** curated question sets with expected answer characteristics (numeric tolerances, dimension coverage, mandatory caveats). Not perfect labels, but enough to catch drift when models, prompts, or schemas change. We started with around 50 curated questions and expanded to roughly 300 over three quarters as new real-world questions kept showing up.
- **Coverage:** what percentage of real user questions can be handled without hand-offs to humans or static reports?
- **Evaluation broken down by layer:** UI, ingestion, retrieval, SQL generation, post-processing, rendering, and even graphing each had their own checks. Latency was tracked per layer as well; "It's slow" isn't helpful if we don't know which part is slow.
- **Cost per question:** tokens, model calls, and a simple view of cloud cost over a representative month.

Behind those metrics, we treated every API call and contract as something to instrument: ingestion pipelines, retrieval hops, SQL generation, model responses, and visualisation steps all emitted structured logs with clear pass/fail or "flagged" statuses.

We used LLMs as judges sparingly, and only for things humans genuinely don't want to do at scale; primarily natural-language tone and surface quality. Never as the sole source of truth for correctness.

On top of the metrics, we learned to keep rich traces: prompt + response pairs, the SQL/queries that were actually executed, validation outcomes (passed, failed, flagged).

This is what we needed when:

- An auditor asks why a metric is different from last quarter's pack.
- A stakeholder says, "This answer doesn't match my spreadsheet."
- Your CFO asks, "What is this copilot costing us, exactly?"
- Your support team pings you with: "This tenant got a different answer for the same question yesterday."

> Think of it as unit tests and logging for a probabilistic system. Retrying blindly just produces a different-shaped failure. When validation failed, we needed traces (prompt, query, contracts) so we could fix the right layer.

## Security and safety: think concentric circles, not magic guardrails

Instrumentation tells you when things break. Security keeps them from breaking badly.

Most security work looks familiar: provider due diligence (data retention, training, residency), identity and access, network controls, logging, compliance. Most cloud and cyber teams already know that playbook.

Where LLM systems add nuance is in how you guard the interaction between user, model, and data. The pattern that held up for us was to think in concentric circles around the data.

### Outer ring: request filtering

Before anything hits a model, run deterministic checks:

- Length and shape of input (too long, too binary, clearly not natural language).
- Basic language / profanity screening.
- Simple pattern checks for prompt injection attempts, raw SQL, schema-dump patterns, etc.
- Rate limiting / abuse detection.

This layer is not glamorous. It's closer to a WAF for prompts. That's the point.

### Middle ring: data access and model context

This is where we make sure the model never sees what it should not see:

- RBAC enforced at the storage/query layer, not just in app code.
- Read-only identities wherever possible.
- Limits on how much data a single question can pull, in rows and in bytes.
- Context construction that only injects authorised slices of data and schema.

A model cannot leak what it never had access to.

### Inner ring: response shaping and exfiltration checks

On the way out:

- Validate that the response stays within the intended scope (no table dumps when the question was about a single entity).
- Detect obvious exfiltration attempts or schema leaks.
- In higher-risk setups, add a final, deterministic "gatekeeper" step to redact or block responses.
- When validation fails, prefer a safe failure ("I can't answer that with the data you're authorized to see") over a confident guess.

We still needed the usual security architecture around this. But treating the model as one fallible component inside layered defences is much healthier than assuming "the guardrail will handle it."

## Make it inspectable to earn trust and usage

None of this matters if people don’t use it: scoped workflows, clean data, instrumentation, layered security. People started using it once they could verify answers in under a minute

In theory, we talk about "trustworthy AI". In practice, most power users and executives want something simpler:

"Show me how you got that number."

- You can see the query or filters behind any chart.
- You can jump from a narrative answer into the underlying rows or documents.
- You can change the slice (periods, entities, metric definitions) yourself rather than treating the copilot as a mysterious oracle.
- You can report a bad answer with context attached (question + trace id + what data it actually used).

Users don't need to become data engineers. They need to tell, quickly, whether a surprising answer is:

- A genuine signal worth acting on,
- A data gap or model limitation, or
- A plain bug that needs fixing.

Most of the time, you can tell in thirty seconds—if the system shows its work.

A reasonable mental model is "very smart junior analyst": we get the best out of them when they show working, cite sources, and expect questions.

## Vendors, versions, and failure modes are part of the design

We can get all of the above right and still get blindsided by something outside our control. This is the unromantic bit.

When we build on cloud LLMs, we assume that over a 12-18 month horizon, the ground will move under us.

Sometimes it's subtle (answers get longer, refusals creep up). Sometimes it's loud (timeouts mid-demo). And sometimes it's commercial: pricing shifts, new tiers show up, and we suddenly wish we'd built in a little flexibility.

In one case, a provider changed the default behaviour behind a widely used model. Our curated question set suddenly started failing in about 10% of cases: some answers became overcautious and dropped important caveats, others became oddly verbose, and a few began refusing questions they had previously answered.

On another occasion, we walked into a high-stakes demo meeting, where multiple teams worked on the demo.  They were all hammering the same tenant: automation runs, evals, we threw the kitchen sink at this. A subtle rate-limit change at the provider level meant that, mid-demo, half the questions started timing out with "try again later" errors. From the user's point of view, the entire showcase had just fallen over.


In both these cases, nothing "broke" in the infrastructure sense, but the behaviour had drifted enough to break functionality, or bring a demo crashing down.

Those incidents forced us to treat vendors and versions as moving parts. After the demo failure, we made three changes:

- **Graceful degradation paths.** When the model is slow, down, or misbehaving, users still get something: cached answers, simpler template-based reports, or at least a clear message and a link to a canonical dashboard. "Just try again" is not a strategy during a board review.
- **Light abstraction over providers.** Not a grand orchestration platform for every model under the sun, but enough indirection that we can move a workload from Model A to Model B without rewriting the entire product.
- **Treat model/prompt upgrades like production changes.** Rollouts, regression checks, and a way to quickly revert.

One of the simplest robustness tests we now use is brutal but effective: swap the current LLM model for the equivalent "mini" version.

If we find the overall solution turns into a train wreck (wrong answers, broken SQL, incoherent charts, nonsense caveats), then we're not ready for enterprise production. The system is overfitting to one model's quirks.

If, on the other hand, users say, "The final answers could use some polish, but overall it's okay-ish" then we're on the right path. The less the product depends on a single model's personality, the more it behaves like proper enterprise software.

## Closing thought

Under the hood, these systems involve embeddings, retrieval strategies, prompt patterns, and orchestration. All of that matters to engineers.

But from a product point of view, the lessons that keep repeating are simpler.

Start with the workflow. Get the data model and definitions right. Put domain experts in the loop early, not as an end-of-demo checkbox. And then treat the thing like what it is: production software that needs tests, instrumentation, and clear failure modes.

Most of this will still apply even if base models get 10x better or 10x cheaper. The specific LLM you call will change. The hard parts won't.

> Do those well, and "we used an LLM" stops being the headline and becomes a single, unremarkable line in the architecture diagram. For serious enterprise systems, that is exactly where it belongs.


