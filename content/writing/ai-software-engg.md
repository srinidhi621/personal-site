---
title: "How AI Is Actually Changing Software Engineering"
date: 2025-06-01T00:00:00Z 
lastmod: 2025-06-01T00:00:00Z
draft: false
tags: ["ai", "software engineering"]
summary: "AI makes code cheaper to generate, which raises the value of design, review, testing, and system judgment."
description: "A practical view of how AI changes software engineering by making code generation cheaper while raising the value of design, review, testing, and system judgment."
---

*Originally written in June 2025. This is a more detailed version of a talk from around the same time.*

Everyone keeps saying "AI is changing software engineering."

Depending on who you listen to, that means either:

1. "Developers are finally 10x more productive," or
2. "Developers are finally 0x employed."

The reality is less dramatic and more useful.

A normal day for most engineers in 2025 looks something like this:

You open your IDE. You have a TypeScript backend, or a Java microservice, or a Python data pipeline. There is an issue tracker, a CI pipeline, and some dashboards that may or may not be lying to you. Someone on the team is arguing about naming and someone else is fighting with YAML.

What your day does not look like:

1. Writing assembly by hand.
2. Managing memory with a notebook.
3. Implementing your own TCP stack.
4. Rolling your own filesystem or database engine for fun.

All of that exists. You are just standing on top of it.

Under your code there is a runtime. Under that, an operating system. Under that, drivers, firmware, and hardware. Under that, manufacturing, supply chains, and physics.

Modern software sits on layers most engineers rarely touch directly.

Most of the time, that is fine. When something breaks, we remember how much of the system sits below the code we wrote.

Abstractions are the reason we can do that. They let us say "database" instead of "B trees, page caching, and disk sectors." They let us say "container" instead of "namespaces, cgroups, and whatever is going on with that overlay filesystem today."

AI in your editor fits into this story. It is the first abstraction that answers back in English.

You say, "I want a function that does X." It proposes an implementation. The stack underneath has not disappeared. You just have a new way to work with it.

That is the right mental model for me. It is another layer in the stack.

## Levels of Autonomy

"Are you using AI to code?" is the wrong question.

The better question is, "At what level are you letting it drive?"

I use this simple spectrum when talking to teams. It is not scientific, but it matches what I see in real engineering work.

### Level 0. Manual

Plain editor. Maybe syntax highlighting. Maybe a linter. You type every character. You are the compiler, the search engine, and the person talking through the problem.

### Level 1. Autocomplete With Manners

The IDE finishes your lines. Copilot style tools fit here. They save keystrokes, but they do not change how you think about the problem. You are still writing every function and steering every decision.

### Level 2. Function Sized Chunks

You ask, "Write me a function that validates this JSON and logs errors," and something reasonable appears. You choose the interfaces. You decide where it plugs in. You own the tests.

The model is your fast pair programmer for local problems.

### Level 3. Repo Level Help

Now the assistant can read multiple files, understand some shape of the project, and run a few commands.

You can say, "We need a new endpoint for this use case," and it edits several files, writes some tests, and maybe updates a client. It feels like a junior engineer who has read the codebase once and is not afraid of bash.

You still set direction. You still check the diff.

### Level 4. Feature Level Help

You hand it a ticket and some context. It plans, edits several files, runs tests, and opens a pull request. You do code review and poke holes in the reasoning.

On a good day, this feels useful. On a bad day, it feels like an intern who says "Done!" while the staging environment quietly breaks.

### Level 5. Fantasy Land

"Here is a backlog and a cloud account. Go build the product and email me when it is ready."

People demo pieces of this. Some research labs are playing in this space. Most actual companies are not.

In June 2025, most teams I see are between Level 1 and Level 4. Where they land depends on their tests and appetite for risk.

The point that matters most is:

> The limiting factor is not how "smart" the AI is.
> It is how much autonomy your engineering practices can safely absorb.

If your tests are flaky and your reviews are rushed, jumping from Level 1 to Level 4 is not bold. It is a faster way to generate incidents.

## Where This Bites You

The happy path stories get most of the attention. "We shipped a feature in two days instead of two weeks." "We reduced boilerplate by 60 percent." Those gains are real and useful.

The interesting stories are the ones where things go wrong.

I keep seeing the same patterns.

### 1. "The Model Understands Our Business"

It does not.

It understands patterns in text and code. That is its job. It has seen a huge amount of both.

But it has never sat in your risk committee meeting. It has never watched your head of sales promise something strange to a key customer. It has never been on a call where someone says, "We cannot change that behavior because legal will kill us."

When you ask, "Should we handle this edge case like this?" it has no secret knowledge. All it has is probability over strings.

If you treat it like a domain expert, it will produce reasonable sounding answers that are wrong in exactly the ways that hurt later.

The model is not lying. It is doing pattern completion.

You are the one who has to remember the parts of reality that never made it into the training data.

### 2. Starting From Nothing Is Different From Changing a Real System

Most AI demos start from nothing.

1. "Generate a simple REST API."
2. "Make a React app with a login page."
3. "Create a script that does these three things."

The model is good at this because it has seen many versions of that work.

Now compare that to the thing you actually work on:

1. Half is legacy and half is new.
2. Some parts are "temporary" from 2019.
3. The person who knew why a certain edge case exists left two years ago.
4. There are behaviors that nobody fully understands but everyone is scared to touch.

The hard work is not writing code. The hard work is changing something without breaking three other things you forgot about or did not know existed.

AI is useful in this world, but the jagged frontier shows up quickly. Telling an agent to modernize a monolith without a plan is an engineering risk, even if the tool looks confident.

You still need to do the boring stuff:

1. Put tests around behavior that matters.
2. Break work into smaller units.
3. Design the change.
4. Use the model inside that structure.

### 3. Invisible Technical Debt

When code becomes cheap to generate, it becomes easy to accept code you do not fully understand.

An assistant proposes a 200 line change. It looks neat. It passes tests. Everyone is tired. The deadline is close. You hit "Approve."

Do that enough times and you end up with a codebase where large chunks "just work," but nobody can explain why they work or what assumptions they carry.

That is a terrible place to be when production starts misbehaving.

Teams are already accepting AI generated code. The review standard has to change:

If nobody on the team can walk through a change in plain language and say what it does, why it exists, and what happens if it fails, you are not reviewing. You are rubber stamping.

Rubber stamping gets more dangerous when the machine can move faster than you can think.

## So What Actually Changes for Us?

If you zoom out a bit, AI mainly attacks one expensive step:

Turning intent into code.

You describe what you want. The model proposes an implementation. That step used to be limited by your memory, your search skills, and how much patience you had for boilerplate.

Now that part is dramatically cheaper.

The parts that are still expensive are the same things that were expensive before, just more exposed:

1. Deciding what is worth building in the first place.
2. Drawing the boundaries in your system.
3. Making tradeoffs between speed and safety.
4. Deciding what "correct" means in messy real world cases.
5. Keeping the whole thing understandable a year from now.

AI does not remove those choices. It increases the penalty for avoiding them, because it is so easy to flood the repo with working code that solves the wrong problem.

The job shifts a little:

Less "how do I write this loop without an off by one error."

More "should this logic live here, and what happens when we change it later."

That is a new phase in the same profession.

We have had these shifts before: from assembly to C, from C to managed runtimes, from bare metal to cloud. Every time, low level details get pushed down and design decisions become more visible.

AI is another layer in that history.

## Closing Thought

We have been adding layers under our feet for decades. Managed memory, frameworks, ORMs, containers, serverless, hosted everything. Each generation pushes the machinery further away from daily work.

In three to four years, we may stop saying "AI assisted software engineering." We may just call it software engineering. The strongest engineers will be the ones who learn to debug the gap between what the model knows and what the business needs.

That skill may not show up in simple productivity metrics. It shows up when production stays up.

AI is the first layer that feels like a colleague. It reads your code, suggests changes, writes tests, and argues with you a bit. It is easy to trust it too much or dismiss it too quickly.

The useful stance is in the middle. Treat it like the rest of the stack. Learn how it fails. Use it for boring work and heavy lifting. Keep your own judgment active.

**Do not outsource the thinking. Only outsource the doing to AI.**
