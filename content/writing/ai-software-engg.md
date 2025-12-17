---
title: "How AI Is Actually Changing Software Engineering"
date: 2025-06-01T00:00:00Z 
draft: false
tags: ["ai", "software engineering"]
summary: ""
description: ""
---

*Originally written in June 2025. This is a more detailed version of a talk from around the same time.*

Everyone keeps saying “AI is changing software engineering.”

Depending on who you listen to, that means either:

- “Developers are finally 10x more productive,” or  
- “Developers are finally 0x employed.”

Reality, as usual, is less dramatic and more interesting.

When you strip away the hype videos with glowing terminals and lo-fi beats, what we are seeing in 2025 is something we have seen before. Not the end of programming. Just one more layer of abstraction piled on top of a stack that was already ridiculous.

Let me start with that stack.

---

## Living on an invisible stack

A normal day for most engineers in 2025 looks something like this:

You open your IDE. You have a TypeScript backend, or a Java microservice, or a Python data pipeline. There is an issue tracker, a CI pipeline, some dashboards that may or may not be lying to you. Someone on the team is arguing about naming and someone else is quietly fighting with YAML.

What your day does *not* look like:

- Writing assembly by hand  
- Managing memory with a notebook  
- Implementing your own TCP stack  
- Rolling your own filesystem or database engine for fun

All of that exists. You are just standing on top of it.

Under your code there is a runtime. Under that an operating system. Under that drivers, firmware, hardware. Under that, layers of manufacturing, supply chains, and physics.

Modern software is basically a city built on top of an older city built on top of a village built on top of a cave.

Most of the time we happily ignore everything below our floor, until something starts to burn and we suddenly remember there is a basement.

Abstractions are the reason we can do that. They let us say “database” instead of “B-trees and page caching and disk sectors.” They let us say “container” instead of “namespaces and cgroups and whatever is going on with that overlay filesystem today.”

AI in your editor fits exactly into this story. It is just the first abstraction that answers back in English.

You say, “I want a function that does X.” It proposes an implementation. The stack underneath has not disappeared. You just have a new way of pushing on it.

That is the right mental model, at least for me. Not magic. Not doom. Another layer.

---

## Levels of autonomy, not an on/off switch

“Are you using AI to code?” is the wrong question.

The better question is, “At what level are you letting it drive?”

Here is a simple spectrum I use when talking to teams. It is not scientific. It behaves like reality, which is good enough.

### Level 0: manual

Plain editor. Maybe syntax highlighting. Maybe a linter. You type every character. You are the compiler, the search engine, and the rubber duck.

### Level 1: autocomplete with manners

The IDE finishes your lines. Copilot-style stuff. It saves you keystrokes, but it does not change how you think about the problem. You are still steering every decision.

### Level 2: function sized chunks

You ask, “Write me a function that validates this JSON and logs errors,” and something reasonable appears. You choose the interfaces. You decide where it plugs in. You own the tests.

The model is your very fast pair-programmer for local problems.

### Level 3: repo level help

Now the assistant can read multiple files, understand some shape of the project, and run a few commands.

You can say, “We need a new endpoint for this use case,” and it edits several files, writes some tests, maybe updates a client. It feels like a junior engineer who has read the codebase once and is not afraid of bash.

You still set direction. You still check the diff.

### Level 4: feature level help

You hand it a ticket and some context. It plans, edits N files, runs tests, and opens a pull request. You do code review and poke holes in the reasoning.

On a good day, this feels like magic. On a bad day, it feels like that intern who says “Done!” with a smile while the staging environment quietly explodes.

### Level 5: fantasy land

“Here is a backlog and a cloud account. Go build the product and email me when it is ready.”

People demo pieces of this. Some research labs are playing in this space. Most actual companies are not.

In June 2025, most teams I see are living somewhere between Level 1 and Level 4, depending on the maturity of their tests, their architecture, and their appetite for risk.

The important point is this:

> The limiting factor is not how “smart” the AI is.  
> It is how much autonomy your engineering practices can safely absorb.

If your tests are flaky, your reviews are rushed, and nobody really knows what happens when production is under stress, jumping from Level 1 to Level 4 is not bold. It is just a faster way to generate incidents.

---

## Where this bites you

The happy path stories get all the airtime. “We shipped a feature in two days instead of two weeks.” “We reduced boilerplate by 60 percent.” All true, and genuinely useful.

The interesting stories are the ones where things go sideways.

I keep seeing the same patterns.

### 1. “The model understands our business”

It does not.

It understands patterns in text and code. That is its job. It has seen a ridiculous amount of both.

But it has never sat in your risk committee meeting. It has never watched your head of sales promise something strange to a key customer. It has never been on a call where someone says, “We cannot change that behavior because legal will kill us.”

When you ask, “Should we handle this edge case like this?” it has no secret knowledge. All it has is probability over strings.

If you treat it like a domain expert, it will happily hallucinate extremely reasonable sounding answers that are wrong in exactly the ways that hurt you later.

The model is not lying. It is doing pattern completion.

You are the one who has to remember the parts of reality that never made it into the training data.

### 2. 0→1 is not the same as 1→2

Most AI demos start from nothing.

“Generate a simple REST API.”  
“Make a React app with a login page.”  
“Create a script that does these three things.”

The model is very good at this, because it has seen a million variations of exactly that.

Now compare that to the thing you actually work on:

- Half is legacy, half is new.  
- Some parts are “temporary” from 2019.  
- The person who knew why a certain edge case exists left two years ago.  
- There are behaviors that nobody fully understands but everyone is scared to touch.

The hard work here is not “write code.” The hard work is “change something without breaking three other things we forgot about.”

AI is not useless in this world, but the jagged frontier shows up very quickly. Telling an agent, “Modernize this monolith,” and watching it go to town is the engineering equivalent of taking your hands off the steering wheel because the brochure says “lane assist.”

You still need to do the boring stuff:

- Put tests around behavior that matters.  
- Break work into smaller units.  
- Design the change.  
- Use the model *inside* that structure, not instead of it.

### 3. Invisible technical debt

When code becomes very cheap to generate, it becomes easy to accept code you do not fully understand.

An assistant proposes a 200 line change. It looks neat. It passes tests. Everyone is tired. The deadline is close. You hit “Approve.”

Do that enough times and you end up with a codebase where large chunks “just work,” but nobody can explain *why* they work or what assumptions they carry.

That is a terrible place to be when production starts misbehaving.

The point is not “never accept AI generated code.” That ship has sailed. The point is:

If nobody on the team can walk through a change in plain language and say what it does, why it exists, and what happens if it fails, you are not reviewing. You are rubber-stamping.

And rubber-stamping gets more dangerous when the machine can move faster than you can think.

---

## So what actually changes for us?

If you zoom out a bit, AI mainly attacks one expensive step:

Turning intent into code.

You describe what you want. The model proposes an implementation. That step used to be limited by your memory, your search skills, and how much patience you had for boilerplate.

Now that part is dramatically cheaper.

The parts that are still expensive are the same things that were expensive before, just more exposed:

- Deciding what is worth building in the first place  
- Drawing the boundaries in your system  
- Making trade offs between speed and safety  
- Deciding what “correct” means in messy real world cases  
- Keeping the whole thing understandable a year from now

AI does not remove those choices. It increases the penalty for not making them consciously, because it is so easy to flood the repo with “working” code that solves the wrong problem.

The job shifts a little:

Less “how do I write this for loop without an off by one error.”  
More “should this logic even live here, and what happens when we change it later.”

That looks less like an ending and more like a new phase in the same profession.

We have had these shifts before: from assembly to C, from C to managed runtimes, from bare metal to cloud. Every time, the low level details get pushed down and the design decisions become more visible.

AI is just another turn of that crank.

---

## Closing thought

We have been adding layers under our feet for decades. Managed memory, frameworks, ORMs, containers, serverless, hosted everything. Each generation pushes the machinery further away from the day-to-day work.

AI is the first layer that feels like a colleague. It reads your code, suggests changes, writes tests, argues with you a bit. It is easy to either fall in love with it or dismiss it entirely.

Both are lazy responses.

The useful stance is somewhere in the middle. Treat it like the rest of the stack. Learn how it fails. Use it for the heavy lifting. Keep your own model running.

**Do not outsource the thinking. Only outsource the doing to AIs.**
