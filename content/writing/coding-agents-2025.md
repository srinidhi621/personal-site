---
title: "Coding Agents in 2025 and How I Actually Use Them"
date: 2025-12-12T00:00:00Z
lastmod: 2026-01-06T00:00:00Z
draft: false
tags: ["ai", "coding-agents", "developer-tools", "workflow"]
summary: "Most AI agents still feel like demos. Coding agents are the exception. This is how I use Cursor, Codex, Gemini CLI, Jules, and related tools."
description: "A practical guide to coding agents across Cursor, Claude Code, Codex, Gemini CLI, Jules, and Amp."
---

2025 was supposed to be the year of AI agents.

We were promised agents that schedule our lives, negotiate contracts, run sales calls, answer every internal query, and act like digital assistants. Most of that either turned into chatbots with extra steps or stayed in roadmaps.

The one kind of agent that did not fade was coding agents.

This piece is about how I use them on personal projects and occasional professional work.

I wrote about this in a [previous post](/writing/ai-software-engg/). The tools have changed enough since then that the workflow is worth revisiting.

Over the last couple of years, I moved from skepticism to Cursor, then to Claude Code, and now to a workflow that uses Cursor, Codex, Gemini CLI, Jules, Amp, and GitHub. A few patterns have become clear.

## What I Mean When I Say "Coding Agent"

The word "agent" has been abused to death. When I say coding agent, I mean a tool that can do this:

1. Read more than one file and work with the shape of the repository.
2. Plan a change, edit files, run commands, observe results, and adjust.
3. Work inside the places developers already use, such as the editor, terminal, CI, and GitHub.

Most of these tools follow the same loop:

1. Read context.
2. Propose a plan.
3. Use tools.
4. Observe results.
5. Iterate.

The differences are about how close they sit to the developer and what kind of work you give them.

## 1. Cursor Removed the Browser Tab

Cursor was the first tool that made me stop copying code into a browser. The model could work directly on the repository. At first, I treated it as a better autocomplete tool. It was useful, but it did not change my workflow much.

That changed when I started using Cursor's agent features for scoped work:

1. "Here's the feature I want to build, here are the relevant files. Sketch a plan."
2. "Implement steps 1 and 2 of that plan, but don't touch the infra folder."
3. "Generate tests for this endpoint and integrate them with the existing test suite."

I still read every diff. I still do not let it edit broad areas without a clear scope. The useful change was simpler. The editor knew more about the repo and could handle more of the repetitive work.

A few things worked for me:

1. The closer the agent is to where you already work, the more you will use it.
2. Repository context matters more than clever chat UI.
3. One shot demos on social media matter less than repeatable daily use.

Cursor made AI part of my editor workflow instead of a separate browser workflow.

## 2. Claude Code Made Repo Work Feel Normal

Claude Code was my first serious terminal agent.

Cursor felt close to the code I was already editing. Claude Code felt better for work where I wanted to brief the agent and let it inspect the repo:

1. "Explain the ingestion pipeline starting from main.py. Draw me a mental model and point out anything weird."
2. "We are replacing Library A with Library B. Scan the repo and propose a step by step plan with blast radius."
3. "This test fails. Trace the failure from the test to the underlying function. Suggest fixes. Apply the safer one. Run test again. Repeat."

A few things stood out:

1. It is comfortable moving through large, messy codebases.
2. It was good at getting new projects off the ground.
3. It naturally structures work into explicit steps.
4. It explains its reasoning well enough to supervise.

After using Claude Code, I stopped treating these tools as autocomplete. I started treating them as agents that can do bounded engineering tasks under review.

## 3. Codex, Gemini CLI, Jules, and Amp Split the Work

Today I do not have one favorite tool for everything. I use different tools for different kinds of work. They still get things wrong, but they help with project setup, dependency fixes, tests, and reviews.

Roughly, this is the workflow:

1. I write and review code in Cursor.
2. I think through designs in ChatGPT, Claude, or Gemini. This is usually the slowest phase.
3. I move the plan to Cursor when it needs more detail.
4. I send bounded tasks to Codex, Gemini CLI, Jules, or Amp when the plan is clear.
5. I use Codex on the web and Jules for asynchronous review or repetitive tasks.
6. I return to Cursor for review, manual testing, and cleanup.

They are not interchangeable. Each tool has a role. This is as of October 2025, and the workflow changes as the tools change.

Do the agents get it right every time? No. They fail in ways that are sometimes funny and sometimes painful. The useful part is that they speed up the boring parts of software work: dependencies, framework boilerplate, routine code, and tests.

For one project, I had a decent spec and about 40 end to end tests. I wrote code for 2 tests, then asked Claude to implement the rest. That was a bad approach. Claude worked for a couple of hours, wrote a lot of code, and then declared: "Trememdous success!! You have 100% pass rate!!!. 2/2 tests passed!" It had only run the two tests that already passed.

At the time, the common pattern was to plan, write tests, and ask agents to make the tests pass. The pattern can work, but I had not written the spec in enough detail. The agent did not understand the full context.

Now I write the spec in more detail, split work into tasks, and include acceptance criteria before handing work to an agent. The agents are more reliable when the work is shaped that way. Even this process will keep changing.

## The Patterns That Work for Me

Once you use these tools for a while, benchmarks and launch announcements matter less. A few practical patterns remain.

### 1. Most of My Agent Work Falls Into Three Layers

**Everyday environment:** Editors, inline completions, quick refactors, planning, and reviews. Cursor is my main tool here.

**Generate code:** Tools that can execute a plan and write code. Claude Code, Codex, Gemini CLI, and Amp fit here.

**Task factory:** Tools for bounded work such as test writing, cleanup, and small features. Codex Review and Jules fit here. They do not work well all the time, but they are useful when the task is narrow and failure is cheap.

The mistake is to expect one tool to be good at every layer.

Some teams are starting to use several agents for different parts of the work. I am not there yet.

### 2. Your Process Is the Bottleneck

If your process is:

1. fuzzy requirement
2. fuzzy prompt
3. generated code
4. shallow review
5. merge

agents will amplify the weak process. You can end up with a repo full of generated code that does not work, then blame the model instead of the workflow.

If your process is:

1. clear responsibility
2. constrained scope
3. clear plan
4. agent work
5. real review
6. tests
7. success metrics

agents become useful.

A simple rule of thumb I follow is:

1. Do we know what we are trying to build?
2. Do we know how we judge the result?
3. Do we have a tight enough feedback loop when the agent gets it wrong?

### 3. Code Is Cheaper, So Starting Over Is Easier

Developers get attached to their work. We treat designs and code as precious, so we hesitate to start over. That made more sense when code was slower to write.

Now, if a design is wrong after a couple of days, starting over can be the cheaper option. You can keep what you learned, rewrite the plan, and ask the agent to rebuild from a cleaner spec.

## Quick, Opinionated Verdicts on the Tools Themselves

Very briefly, because people always ask which one they should use.

**Cursor:** This is where I am happiest when I am writing code. It is good for flow, incremental changes, code review, and reading docs. For 20 USD a month, it gives access to several models, including some launch previews.

**Claude Code, Codex, and Gemini CLI:** All three major providers have strong models, but their agent harnesses vary a lot.

Claude Code is still too eager to please, and it adds too many defensive checks in code. It also burns through tokens quickly. Gemini CLI can be excellent or frustrating depending on the task.

Codex is the standout for me right now. It gets most things right most of the time, and its harness feels the most mature.

Recently, I removed Claude Code from my regular workflow because the usage limits were too restrictive. Gemini CLI has taken its place as the workhorse, mostly because it is free on my mobile plan. The downside is that Gemini's harness is the weakest of the lot and can be frustrating.

**Jules and Codex on the web:** These are useful for boring but necessary engineering work such as test coverage, dependency bumps, cleanup, and PR review. Do not expect them to design your core domain. They still fail often enough that the tasks need to be low risk.

Together, they form a useful first generation agent workflow. As the tools change, our roles and workflows change with them.

Side note: Amp has a strong harness and a usable free tier supported by ads. It is model agnostic, but the user has little control over which model is used. The experience is one of the best right now. It is the tool I am watching most closely in 2026. I also expect Claude Code to improve again.

## What I Expect Over the Next Year or Two

I do not pretend to know exactly how this shapes up, but a few trends feel likely.

1. **Skills.** Claude Code started the pattern, and other tools are adopting it.
2. **Agents move into CI.** They will become part of staged development, testing, review, and deploy workflows. I would still be careful about letting them touch production code without strong review.
3. **Surfaces converge.** The separation between editor, terminal, and cloud agents will blur. The task will matter more than the product surface.
4. **Prompt governance becomes a feature.** Teams will want to know which agent touched which files, under which instructions, with whose review, and with what version history.
5. **Benchmarks matter less than workflows.** A small benchmark lead matters less than integration, predictability, and team fit.
6. **The best developers look different.** Lines of code were never a good productivity metric. The better measure is how reliably a team ships correct changes with fewer regressions.

## Closing Thought

Most of the grand AI agent story so far has been marketing and wishful thinking. Coding agents are the exception because they live in a brutally honest environment: repos, builds, tests, and production.

There is nowhere to hide. Either they help us ship better systems faster, or they make a mess and we stop using them. That pressure is healthy.

Our job is to design work and processes where they can do what they are good at, without lowering the bar for what we call good engineering.

Model names, launch events, agent harnesses, and confusing product tiers will keep changing. The engineering standard should not.
