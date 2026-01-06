---
title: "Coding Agents in 2025: How I Actually Use Them (and What I'd Bet On Next)"
date: 2025-12-12T00:00:00Z
lastmod: 2026-01-06T00:00:00Z
draft: false
tags: ["ai", "coding-agents", "developer-tools", "workflow"]
summary: "2025 was supposed to be the year of AI agents. Most faded into slideware. Coding agents are the exception. Here's how I actually use them."
description: "A practitioner's guide to coding agents: from skeptic to daily user, across Cursor, Claude Code, Codex, Gemini CLI, and Jules."
---

2025 was supposed to be the year of AI agents.

We were promised agents that schedule our lives, negotiate contracts, run sales calls, answer every internal query, and act like digital super-helpers. Most of that either quietly turned into chatbots with extra steps, or disappeared into roadmaps and slideware and are currently gathering digital dust. 

One kind of agent did not fade: coding agents.

This piece is about why that happened, and my personal journey of using them in the real world, for mostly limited, personal projects, and the odd professional assist.

I had written about this in a [previous post](/writing/ai-software-engg/), but there's so much that has happened in this space since then, it's worth revisiting.

Over the last couple of years I've gone from a skeptic, to Cursor-only, to adding Claude Code, and now to a workflow that routinely hops between Cursor, Claude Code, Codex, Gemini CLI, Jules and GitHub. Along the way a few patterns have become obvious, both about the tools and about teams that use them well.

## What I Mean When I Say "Coding Agent"

The word "agent" has been abused to death. When I say coding agent, I mean something with these characteristics:

- It understands a repository, not just a single file and can act as a pair-programmer, executing design choices, reviewing artifacts, writing and running tests.
- It keeps a plan in its head: break work into steps, execute, adjust, stop when done or stuck.
- It lives in the places developers already work: IDE, terminal, CI/CD, GitHub.

They're all doing variations of the same underlying loop:

read context → propose plan → act using tools → observe results → iterate

The differences are about how close they sit to the developer and what kind of work you give them.

## Act 1: Cursor – Closing the "LLM in the Browser" Tab

Cursor was the first tool that made me stop alt-tabbing to a browser to talk to an LLM.

At the start I treated it as a somewhat better smart-complete IDE. Useful, but not mind-bending.

The shift happened when I started using Cursor's agentic features more seriously:

- "Here's the feature, here are the relevant files. Sketch a plan."
- "Implement steps 1 and 2 of that plan, but don't touch the infra folder."
- "Generate tests for this endpoint and integrate them with the existing test suite."


I still read every diff. I still do not let it run wild on release-critical code. But it stopped feeling like I was "using AI." It just felt like the editor knew more about the repo and could do more of the grunt work.

Few things clicked for me here:

- The closer the agent is to where you already work, the more you'll actually use it.
- Repo-level context matters more than clever chat UX.
- One-shot wonders that you see often on social media are not nearly as important as people think

Cursor turned me from "LLM as sidecar in the browser" into "AI as part of the editor." That was the first inflection point.

## Act 2: Claude Code – Letting an Agent Think Across the Repo

Claude Code was my first serious "sit in the terminal, operate on the repo" agent.

Where Cursor felt like an extension of my hands, Claude Code felt like a junior engineer I could brief:

- "Explain the ingestion pipeline starting from main.py. Draw me a mental model and point out anything weird."
- "We're migrating from Library A to Library B. Scan the repo and propose a step-by-step plan with blast radius."
- "This test fails. Trace the failure from the test to the underlying function. Suggest fixes. Apply the safer one. Run test again. Repeat"

A few things stood out:

- It is comfortable wandering through large, messy codebases. Its also very good at getting 0-1 projects off the ground. Sorting out tool dependencies was particularly easy.
- It naturally structures work into explicit steps.
- It is pretty good at explaining its reasoning, which makes it easier to supervise.

This was the second inflection point for me: I stopped thinking of these tools as autocomplete and started thinking of them as colleagues working under constraints.

## Act 3: Codex, Gemini CLI and Jules – From One Agent to a Small Team

Today my day-to-day looks less like "I have a favourite tool" and more like "I have a small team of agents that sometime get things fantastically wrong, but help me a lot in getting projects started, fixing dependencies, building small-ish tools for day to day use."

Roughly:

- I live-code in Cursor. Its still the go-to way to review code.
- I ideate and find problems/solutions in ChatGPT/Claude/Gemini apps. This phase is the most time-consuming. The plans move to Cursor for detailing and planning. 
- I spread the plans to Codex or Gemini CLI for the task of converting the design and plans into code.
- PRs handled between Codex on the web, or Jules. Both are asynchronous cloud agents that I can ship off PRs for review, or repetitive but well planned tasks. Again, sometimes they don't work at all, but since these are non-critical tasks that I can ship to Cursor in case of failures, I keep this step in place.
- Back to Cursor for review and manual testing.

They are not interchangeable. They each have a role. And this is as of October 2025. As the tools change, my workflow changes accordingly.

Do the agents work in lock-step and get it right always? Hell no. They have failed in sometimes funny, sometimes tragic and sometimes in a tear your hair out, yell at the screen kind of way. But for me, the important thing was that they accelerated the most boring parts of building software: Getting dependencies sorted, boilerplate for frameworks, and finally the code and the tests. 

True story: For one of my projects, I had a decent spec, and a test suite of about 40 odd end to end tests. I wrote out code for handling 2 of them, and then told Claude to go about implement the rest so that all of the remaining would pass. In hindsight, bad approach, but it was fun to watch it work. Claude spun furiously for a couple of hours, wrote a bunch of code and then proudly declared: "Trememdous success!! You have 100% pass rate!!!. 2/2 tests passed!". I was this close to destroying my computer. 

Back then the prevailing pattern was to plan, write tests, and have agents go about writing all code so the tests would pass. This was a bad approach, but it was fun to watch it work. I'm glad I did it. 

Now, I plan extensively, write out the spec in detail, with tasks and sub-tasks decomposed, with clear acceptance criteria, then hand off to agents. This is a much better approach, and the agents are much more reliable and predictable. But then, even this will evolve. 

## The Patterns That Actually Matter

Once you live with these tools for a while, the benchmarks, the buzz and hype of new models falls away and a few patterns remain.

### 1: Three layers, not one magical tool

Almost everything I do with coding agents falls into one of three layers:

**Everyday environment:** Where developers live minute-to-minute. Editors, inline completions, quick refactors, planning, reviews. Cursor lives here for me.

**Generate code:** The workhorses that can execute a plan, and spit out code. Claude Code, Codex and Gemini CLI live here.

**Task factory:** Where you offload well-bounded work. Test writing, test runs, housekeeping, small features. Codex Review and Jules live here. They may not work well all the time, but nothing beats the joy of handing off a large PR or a 2 hour test run and moving on to other things, while the agents on the cloud do your bidding.

The mistake is to expect one tool to be great at all three. That's like expecting the same person to be your principal architect, your best debugger, and your bulk test runner.

Once you stop looking for "the one tool" and accept this multi-layer view, decisions get much easier. People now have multiple sub agents, or swarms of agents, to handle different parts of the work. I'm not there yet, but who knows what the future holds. 

### 2: The bottleneck is not the model, it is your process

If your process is:

fuzzy Jira story → fuzzy prompt → auto-generated code → shallow review → merge,

agents will happily amplify your sloppiness. You'll get a whole repo full of AI slop that wont work, and you'll blame it on the model, the harness, the clouds, your dumb luck and everything in between.

On the other hand, if your process is:

clear responsibility → constrained scope → clear plan → agent work → real review → tests and success metrics,

agents become boringly useful.

A simple rule of thumb I follow is;

- "Do we know what work we are handing to them?"
- "Do we know how we judge the result?"
- "Do we have a tight enough feedback loop when they screw up?"

###  3: Code is cheap, and fast. Don't be afraid to start over.

Developers always get too attached to their work. We tend to treat our designs, our code, our work as precious, and generally are very hesitant to let go and start over. In the past, this was understandable. In the current world, it's a lot easier to start from scratch, figure out what works, what doesn't and give it another throw of the dice.

Lets say you made a plan on ChatGPT/Cursor for a certain architecture: stack up your layers a certain way, design the data model a certain way and the UX to behave how you wanted. Then, a couple of days into coding, you realise some functionality was missing or needed a different design, or a different tech stack. It's a lot easier now to just start over, and redo the process than to get stuck in the intractable rabbit holes.

## Quick, Opinionated Verdicts on the Tools Themselves

Very briefly, because people always ask "which one should I use."

**Cursor:** Where I'm happiest when I'm actually writing code. Great for flow, great for incremental changes. It shines as "the place I live." My go-to place to review code, read docs and do the things that aren't possible in a CLI. For the price of 20 USD a month, you get a a wide variety of models to choose from, some newer that are provided free during launch as a preview.

**Claude Code/Codex/Gemini CLI:** All three major providers have great models, but their agent harnesses vary wildly.

Claude Code is still like an over-enthusuatic intern who desperately wants to please you. It also adds way too many defensive checks in code. Gemini CLI is like an erratic genius - spectacularly good, or horribly bad, given the day.

Codex is the standout as of now, gets most things right, most of the time, and feels the most mature of all the agent harnesses.

Recently, I've removed Claude Code altogether, because the usage limits were too restrictive, with Gemini CLI taking its place as the workhorse. Mostly because its free on my mobile plan, which helps . But the harness on Gemini is by far, the worst of the lot, and can sometimes be very frustrating.

**Jules/Codex on web:** The async contractor. Worth piloting on boring but necessary engineering work: test coverage, dependency bumps, cleanup, PRs. Don't expect it to design your core domain. Half the time doesn't do anything at all.

None of these is "the answer." Together, they form a pretty decent first-generation agent team. And as they evolve, our roles and workflows change with them.

Side note: Amp, the latest entrant to this space has a rock solid harness, a very usable free tier that is ad-supported. They are model agnostic, to the point where the user has no agency in choosing certain models. But the experience is by far the best of the lot. For me, this is the one to watch out for in 2026. And I expect the OG Claude code to come back strong soon. 

## What I Expect Over the Next Year or Two

I don't pretend to know exactly where this lands, but a few trends feel likely.

- **Skills.** Claude code started it, but now is seeing adoption from others.
- **Agents move into CI/CD** as part of a staged develop-test-review-deploy process. Given where we are now, I would strongly advise against using AI in production code, but maybe this will change in the future.
- **Surfaces converge:** The separation between "agent" in the editor, terminal, cloud starts to blur. You'll care less which one you're using and more about the kind of work you're asking for.
- **Governance becomes a feature,** not a compliance afterthought. Teams will want to know which agent touched which parts of the codebase, under what instructions, with whose review and version history. Tools that make that traceability easy will stand out. 
- **Benchmarks matter less than workflows.** Whether model A or B is slightly better on some coding benchmark will be less important than: how well the agent integrates with your stack, how predictable its behaviour is, how easily your team can work with it.
- **The highest-leverage developers look different.** Lines of code as a productivity metric was never correct, and now is simply meaningless. The premium shifts towards how many successful PRs can be shipped for each team, and how this helps in closing sprints faster, delivering more with better quality.

## Closing Thought

Most of the grand "AI agent" story so far has been marketing and wishful thinking. Coding agents are the exception because they live in a brutally honest environment: repos, builds, tests, production.

There is nowhere to hide. Either they help us ship better systems faster, or they make a mess and we stop using them. That pressure is healthy I feel.

Our job is to design work and processes where they can do what they're good at, without lowering the bar for what we call good engineering.

That part is on us.

Everything else (model names, launch events, agent harnesses, confusing product tiers) will come and go.
