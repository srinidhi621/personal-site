+++
title = "Weekly Links: 27 November 2026"
date = 2026-11-27T12:00:00+05:30
draft = false
summary = "Nate Silver on forecasting with AI, what consultants own after handover, and a 15-second lesson in software architecture."
tags = ["links"]
+++

## At a glance

Nate Silver’s team is shipping forecasting models faster, Mani Doraisamy found a 15-second delay hiding in a few lines of logging, and two researchers ask what clients still need consultants for when analysis gets cheaper. In each case, doing the work faster still leaves someone with a judgment call.

## Top Stories

### AI is moving way too fast
[Nate Silver · Silver Bulletin](https://www.natesilver.net/p/ai-is-moving-way-too-fast)

Silver’s four-person team launched or substantially upgraded four forecasting models between March and September. Only the World Cup model, PELE, was built from scratch. AI sped up coding and data preparation, so the team could try more model designs, but Silver still had to push back when the tools tried too hard to improve the backtest. A model can get better at predicting matches that have already happened without getting any better at predicting the next one. Silver likes the current division of labour. What unsettles him is how long it will last.

### Management consulting is not a thin wrapper on intelligence
[Rod Moshtagi and Sayash Kapoor · AI as Normal Technology](https://www.normaltech.ai/p/management-consulting-is-not-a-thin)

A well-written long-form piece on what clients pay for beyond analysis: judgment, coordination, credibility and accountability. The authors make a good case that cheaper analysis creates more work putting recommendations into practice. They’re also clear that incumbent firms aren’t guaranteed to win that work.

I’d draw a sharper line between the consultant whose reputation is on the line and the team that owns the outcome after handover. A recommendation can fit on a single slide. Agreeing what a finance metric means, reconciling it against the books, and keeping it correct after the chart of accounts changes can take months. In the [enterprise analytics write-up](https://ascendion.com/ideas-and-insights/lessons-from-a-year-of-shipping-llm-analytics-products-for-enterprises/), changes to account hierarchies produced plausible but wrong answers. The write-up makes the case for versioned data definitions, reconciliation and sign-off from people who know the business. That’s the work I’d look for when someone sells accountability.

### We promoted developers into architects without informing them
[Mani Doraisamy · Developer forever](https://manidoraisamy.com/developer-to-architect.html)

A few lines of AI-written logging put Google identity lookups on the critical path of an add-on’s first run. Doraisamy says the welcome screen took 15 seconds. His simpler proposal: log only the install timestamp and tell marketing it can’t get an email address from the install alone. That’s a better example of architecture than most architecture diagrams: ask what the business actually needs before deciding what the user has to wait for. One slow screen doesn’t prove coding is going away; it does show how easily a locally sensible change can make the whole product worse.

## Miscellaneous Links

- [The job is gone: leave and let die](https://www.reddit.com/r/SoftwareEngineerJobs/comments/1y0gu0i/the_job_is_gone_leave_and_let_die/) · The Reddit thread behind Joe Masilotti’s post. An engineer misses solving problems and mentoring juniors after their job shifted toward prompting and reviewing generated code. An anecdotal counterpoint to Doraisamy’s “promotion.”
- [Agent platform of 2027](https://x.com/john_ssuh/status/2124336124172935336) · John Suh’s illustrated proposal separates the agent runtime, compute and persistent workspace, with an inbox for approvals and event-triggered workflows. The [original workflow diagram](https://pbs.twimg.com/media/HXsjuw-acAAJhec.jpg) shows how the pieces are meant to fit together.
- [SVS on building a career that travels](https://x.com/_svs_/status/2124800762819858847) · A prompt to build skills, relationships and a body of work that carry across employers. The career advice can stand on its own without taking anonymous layoff reports as evidence of how widespread the cuts were.
