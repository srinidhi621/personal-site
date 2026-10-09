+++
title = "Weekly Links: 28 September to 2 October 2026"
date = 2026-10-02T12:00:00+05:30
draft = false
summary = "Ten links on choosing problems, AI tools and review, incident follow-up, a clock repair, and an SNL parody."
tags = ["links"]
+++

<!-- weekly-links-local:01 -->
## How to pick and solve the next great problem

<https://engineering.stanford.edu/news/how-pick-and-solve-next-great-problem>

Choosing a research problem can take months. That sounds excessive until you consider how many years you might spend solving it. Michael Fischbach's advice is to give that choice more time, put ideas on paper, and discuss them before committing. The method can change as you learn more about the problem. This is a short introduction to that practice, so don't expect a formula that picks your next project for you.
<!-- /weekly-links-local:01 -->

<!-- weekly-links-local:02 -->
## Six things I tried with Jev

<https://isaacflath.com/writing/six-things-i-tried-with-jev>

Six fairly ordinary jobs for Jev, including checking citations, finding relevant passages in PDFs, and working out where an agent went wrong. Ordinary is useful here. These are tasks that already exist in a working day, rather than a demo in search of a reason to exist. Isaac Flath's examples give you somewhere to start experimenting, though they don't tell you how well the same approach will work on your own material.
<!-- /weekly-links-local:02 -->

<!-- weekly-links-local:03 -->
## Why Dwarkesh is Wrong about Computer Use + How OpenAI shipped its Jev competitor in 1 Week

<https://www.latent.space/p/devday-2026>

An agent that writes software should be able to use it and notice when it breaks. This conversation gets into how computer use might make that possible, with Ari Weinstein explaining the testing side and Nikunj Handa discussing the Jev-inspired Decisions API. There is also useful detail on prompt caching and keeping long agent sessions manageable. You are hearing from the people building these tools, so the confidence about where they are headed comes with the territory.
<!-- /weekly-links-local:03 -->

<!-- weekly-links-local:04 -->
## Magnitude

<https://github.com/magnitudedev/magnitude>

Running a model locally still means making choices about hardware and memory. Magnitude tries to handle more of that work by tuning execution for the machine it is running on. It also shares cached prompt prefixes across agent sessions, so several agents needn't repeat all the same computation. The performance claims come from the team's own benchmarks. The interesting test is what happens with your model, on your machine, while several sessions are running.
<!-- /weekly-links-local:04 -->

<!-- weekly-links-local:05 -->
## You Said No MCP!

<https://earendil.com/posts/you-said-no-mcp/>

Pi now supports MCP after its maintainers had said no to it. The explanation is worth reading because it gets into what changed. Tools can be loaded when needed, and an agent can use JavaScript to combine calls instead of passing every intermediate result through the conversation. That helps with the overhead. It still depends on servers returning data that another tool can actually use. A protocol can't tidy up every server on its behalf.
<!-- /weekly-links-local:05 -->

<!-- weekly-links-local:06 -->
## Interpreting Pangram

<https://lucumr.pocoo.org/2026/9/14/interpreting-pangram/>

Rewrite every sentence yourself, keep the ideas and structure, and an AI detector may still call the result AI-generated. That is what happened in Armin Ronacher's Pangram experiment. It raises an awkward question about what these detectors are identifying when a person has done the rewriting. One example cannot establish how accurate Pangram is overall. It does give a reason to be careful before treating a detector's score as proof of who wrote something.
<!-- /weekly-links-local:06 -->

<!-- weekly-links-local:07 -->
## One month without AI

<https://blog.bustikiller.com/2026/09/25/one-month-without-ai.html>

The uncomfortable moment here is a code review. A test looked convincing, but it didn't test the behaviour the code was changing. After years of using test-driven development, that was enough to make the author stop using AI coding tools for a month. Smaller changes and a better understanding of the code followed, along with enjoying programming again. This is one person's account, rather than a comparison of productivity. The question it leaves is useful even if you keep using agents. Can you still explain the change you are asking someone else to approve?
<!-- /weekly-links-local:07 -->

<!-- weekly-links-local:08 -->
## I don’t want the details

<https://michaelheap.com/i-dont-want-the-details/>

A convincing incident report can leave everyone satisfied while changing very little. The useful question is what would make the next occurrence end differently. Clear ownership or fewer pointless alerts can do more than another promise to be careful. There is a sensible limit here too. Some failures cost less than the process required to prevent them. Otherwise every incident becomes an opportunity to schedule another meeting.
<!-- /weekly-links-local:08 -->

<!-- weekly-links-local:09 -->
## Fixing the Portobello Police Station Clock

<https://pointinthecloud.com/2026-04-11-211700.html>

A nineteenth-century clock, a much newer chime controller, and no obvious instructions for either. Setting the time meant tracing the gears. Setting the chime meant figuring out a circuit board and an advance button that seemed to do nothing. There is also a moment when the clock appears to run backwards because they are looking at it from inside. A very satisfying repair account, including the checks and the uncertainty. The chime worked during testing, but they left it disconnected.
<!-- /weekly-links-local:09 -->

<!-- weekly-links-local:10 -->
## Anthropic CEO Dario Amodei on AI's Threat to Humanity - SNL

<https://www.youtube.com/watch?v=-Nvne3LzBls>

Jane Wickline plays Dario Amodei in this Weekend Update sketch about AI threatening humanity. After a week of earnest arguments about what AI will do next, there is room for an SNL parody. This one is comedy, so no attempt to extract a policy recommendation from it.
<!-- /weekly-links-local:10 -->
