+++
title = "Weekly Links: 20 November 2026"
date = 2026-11-20T12:00:00+05:30
draft = false
summary = "Independent checks for coding agents, replayable failures, retrieval evaluation, and new models to compare on real workloads."
tags = ["links"]
+++

## At a glance

This week’s links ask how to make agent work easier to check: protect review rules, count failed attempts, inspect retrieval at each stage, and replay simulated failures. The model releases bring more choices, but the useful comparison is still what works on your tasks, at what cost. There are also practical ideas for keeping plans, data contracts and application rules readable.

## Top Stories

### Claude Code: keep review rules outside the change

In [How the Claude Code team thinks about verification](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/), Addy Osmani describes end-to-end, property and differential tests, review rules read from the base or default branch, and a commit gate that logs what it would block before enforcement begins. A PR can add tests, but it should not be able to rewrite the rules used to judge that same change. These checks provide evidence about observed behaviour; they do not prove correctness for every input.

### FrontierHarness v1.1: benchmark the model and harness together

Shilin Zhu’s [Runta evaluation](https://runta.com/blog/introducing-frontierharness-eval-v1-1/) compares 22 harness configurations across 62 terminal tasks. Codex CLI ranked first by average cost per task with GLM‑5.3 and 16th with Kimi‑K3. Among scored runs, 64.5% of estimated list-price inference cost went to failures or timeouts.

Cost per task and cost per verified pass answer different questions. Runta calculates cost per pass by dividing average cost per task by the pass rate. For your own evaluation, count failed attempts in the bill: total spend divided by verified passes. These results cover one inference provider and one task suite, so they are not a general production ranking. Via Hacker News.

### GPT‑6.2 Astra and Sol: measure the cost of a correct answer

[GPT‑6.2 Astra and Sol](https://openai.com/index/introducing-gpt-6-2-astra-sol/) are available in Codex and the OpenAI API. Microsoft Foundry also lists [Astra](https://ai.azure.com/catalog/models/gpt-6.2-astra?publisher=openai) and [Sol](https://ai.azure.com/catalog/models/gpt-6.2-sol?publisher=openai). Astra’s standard OpenAI API input and output token prices are 20% below GPT‑6 Astra’s; Sol keeps GPT‑6.1 Sol’s prices. Via Simon Willison.

One implementation detail: in the Responses API, GPT‑6.2 places top-level `instructions` after `input` and bills those instruction tokens at the uncached rate, even when repeated. Put reusable instructions in the first `developer` message in `input` to make them [eligible for caching](https://developers.openai.com/api/docs/guides/prompt-caching).

[Qwen4-Max is also available through Alibaba Cloud Model Studio](https://www.alibabacloud.com/help/en/model-studio/newly-released-models), via AINews. Compare models on the same workload and count correct results, rather than choosing by token price alone.

### Microsoft Decision 1.1: probabilities for fixed choices

[Microsoft Decision 1.1](https://ai.azure.com/catalog/models/Microsoft-Decision-1.1?publisher=microsoft) is [generally available in Foundry](https://commandline.microsoft.com/microsoft-decision-model-ga/). Give it text or images and a fixed set of answer options; it returns probabilities rather than prose. It accepts up to eight images per call. That is an input limit, not a promise of eight separate classifications.

This is Microsoft’s decision model. The [Azure OpenAI Decisions API](https://learn.microsoft.com/azure/foundry/openai/how-to/decisions) is a separate offering using GPT‑6 Luna. For routing or document triage, test how well the probabilities match actual outcomes on your own examples before setting an escalation threshold.

### Deterministic simulation: make failures replayable

In [Deterministic Simulation Testing](https://martinfowler.com/articles/deterministic-simulation-testing.html), Unmesh Joshi explains how simulated clocks, networks and storage make distributed-system failures reproducible. His quorum key-value store example uses seeded fault injection to replay failures and check correctness.

The trade-off is architectural: the application’s core must keep time, randomness and I/O under the simulator’s control. Replaying an observed simulated failure makes it easier to investigate and test a fix; it does not establish correctness across every possible execution.

## Miscellaneous Links

- [DeepSeek’s application APIs](https://api-docs.deepseek.com/updates/) · Web search, file input, URL reading and content-safety checks are available alongside model inference, with separate speech APIs too. The [chatbot guide](https://api-docs.deepseek.com/guides/build_a_chatbot/) explains which work the service handles and how clients should preserve returned blocks between turns.

- [Cursor’s security incident update](https://cursor.com/blog/security-incident-update) · Cursor reports that stored coding-agent traces included credentials that had escaped redaction. The operational lesson is to review how long agent logs are retained, who can access shared copies, and whether secret redaction works.

- [Joy & Curiosity #106](https://registerspill.thorstenball.com/p/joy-and-curiosity-106) · Thorsten Ball describes Amp’s Monday meeting: discuss priorities, take a few minutes to write down planned work in silence, then review those plans together. Writing makes each person’s proposed contribution concrete before the group goes through it.

- [Gemini 4 Neon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/) · Google positions Neon between Carbon’s longer projects and Hydrogen’s fast execution, with a focus on coding, analysis and enterprise workflows. The launch includes the Gemini API and access through several Google products; the performance comparisons are Google’s.

- [Data Contracts](https://martinfowler.com/articles/data-contracts.html) · Simon Harrer and Arif Wider explain how to describe a dataset’s schema, quality guarantees, ownership and terms of use. Keeping those expectations explicit and versioned gives both people and agents something firmer to work from than guessed column meanings.

- [Qwen3.8-27B adapted to Pi](https://huggingface.co/harness-hub/Qwen3.8-27B-pi-adapted) · Harness Hub reports a corrected improvement from 39.2% to 64.7% on SWE-bench Pro’s hard-51 subset, with thinking disabled and one attempt per task under the same Pi settings. This is a small, budget-limited comparison, and checkpoint selection used SWE-bench Pro scores plus part of Terminal-Bench, so it is not a fully independent held-out evaluation.

- [How to Evaluate Agent Retrieval](https://content.delphi.co/hamel/how-to-evaluate-agent-retrieval-810066338bb2) · Glean’s search quality team separates evaluation of search results, selected snippets and final answers, then checks changes in live experiments. Engineers include analysis of 5–10 affected queries in a launch document; that is a review sample, not the full evaluation suite.

- [The Sweet Side of the Bitter Lesson](https://www.youtube.com/watch?v=xRJMiaUoD_8&t=774s) · Around 12:54, Thariq Shihipar discusses separating engine code from readable specifications and editable rules. The idea is to keep behaviour understandable and adjustable even when an agent writes much of the implementation.

- [Claude and black-hole physics](https://www.anthropic.com/research/claude-black-hole-physics) · Anthropic reports two theoretical-physics results, concerning the Hawking–Page transition and the modular bootstrap, and links the preprints. The Lean verification described in the article applies to the modular-bootstrap result, not both results.

- [Intra-Turn Interaction](https://demos.liubruce.me/intra-turn/) · [Bruce Liu](https://www.liubruce.me/) explores AI interaction beyond taking turns. The author’s site lists the demo; it has not been tested for this roundup.

- [Critical thinking when agents do the work](https://threadnavigator.com/thread/2117512471930167377/) · Addy Osmani’s November 3 essay on forming your own hypothesis and understanding what a passing check leaves untested. This link is a non-X mirror.

- [OpenCode Browse](https://opencode.ai/product/browse) · An MCP server and Chromium extension that let coding agents use your browser, record tabs and capture network traffic. It supports multiple MCP clients and lets you restrict agent tabs to named sites. Via Hacker News.

- [We rebuilt LangSmith around the agent](https://www.langchain.com/blog/we-rebuilt-langsmith-around-the-agent) · Sam Crowder describes a shared agent record with a stable ID and named owner, connecting environments, traces and evaluations. Registration with an identity provider remains on the roadmap. Via AINews.

- [Evals for AI Engineers](https://ai-evals.com/) · Shreya Shankar and Hamel Husain’s book covers finding errors, building automated evaluators and monitoring AI in production. Via Hamel’s newsletter.
