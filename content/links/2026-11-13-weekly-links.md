+++
title = "Weekly Links: 13 November 2026"
date = 2026-11-13T12:00:00+05:30
draft = false
summary = "Independent checks for AI agents, model substitution, durable execution, and a YouTube guide for builders."
tags = ["links"]
+++

## At a glance

This week's links are about making agent work easier to trust: protect the specification, check against a source the agent doesn't control, and choose models based on the job they actually have to do.

## Top Stories

### AlphaProof Code: keep the specification independent

In [Introducing AlphaProof Code](https://deepmind.google/blog/introducing-alphaproof-code/), Pushmeet Kohli and Swarat Chaudhuri describe DeepMind's work verifying selected properties of Signal's cryptographic implementation. Humans reviewed the specifications, agents generated proofs, and Lean checked them. A separate check compared the theorem statements and their underlying definitions against an approved copy. Without that check, an agent could make a proof easier by changing what it had to prove. See the [technical paper](https://deepmind.google/documents/36/Formal_Verification_of_Signal_4.pdf).

The study covers specified properties of libsignal's one-to-one protocol in an AArch64 test harness. Group messaging is outside scope, and the proofs rely on stated assumptions about cryptographic primitives. The pattern is useful beyond formal verification: keep the requirements under independent control, then let the agent work out how to satisfy them.

### Agent-written code needs checks it cannot quietly rewrite

Matteo Vaccari's [Tests as data](https://martinfowler.com/articles/tests-as-data.html) proposes keeping acceptance examples in human-readable data. That gives domain experts something they can review directly. If the same agent can change the implementation, expected answers and test runner, a passing test tells you less than you might think.

Swaminathan Sivasubramanian's [AWS Emulator write-up](https://www.allthingsdistributed.com/2026/11/aws-emulator-and-the-engineers-job-when-agents-write-the-code.html) shows a version of that approach at scale. AWS describes agents building the emulator against fidelity tests checked on real AWS, with those checks gating merges. The [code is public](https://github.com/aws/aws-emulator), and AWS documents gaps in behaviour. These are useful engineering examples, not controlled comparisons.

### Smaller models work best when the job is well defined

In [Amazon's Strands Decider deployment](https://strandsagents.com/blog/amazon-saves-millions-replacing-sonnet-with-strands-decider/), Carr Onstott, Mehul Jaiswal and the Strands team describe replacing Sonnet for a fixed-category ticket-labelling task. The part worth copying is the rollout: run both models on the same work before switching, tune thresholds, and keep a way back. The savings depend on pricing and utilisation, and the accuracy dataset isn't public. Via Mario Zechner.

Google's [Gemini Decisions API](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/), introduced by Min Choi and Felix Yu, offers another option for bounded decisions like routing and tool selection, including multimodal inputs. [Gemini 4 Hydrogen and Orchestrator](https://antigravity.google/blog/gemini-4-hydrogen-in-google-antigravity/) tackles a different problem: a stronger model plans and reviews while Hydrogen executes, with difficult work handed back mid-task. Both approaches are candidates for testing on your own workload; the published performance comparisons are the vendors'.

### A financial agent can validate the wrong answer consistently

Handshake's [ATLAS-Finance](https://joinhandshake.com/research/benchmarks/articles/atlas-finance-evaluating-ai-agents-inside-a-bank/) shows an agent embedding an incorrect tax assumption in its calculation, then using that same calculation to validate the result. A clean workbook can still be wrong. The useful check is whether its financial method agrees with a governing source. This older benchmark is the provider's own evaluation; the [Latent Space interview](https://latent.space/p/handshake/) revisits it.

Kiran Prakash's [Long-horizon agents and durable execution](https://martinfowler.com/articles/durable-execution-agents.html) makes a related point about resuming work. An approval can expire while the agent waits, or an external action can succeed even if its response never comes back. Saving workflow state helps recovery; the application still has to decide whether to continue or check again.

## Miscellaneous Links

- [Coding Agents Copy Your Secrets to a Hidden File](https://apiiro.com/blog/coding-agents-leaking-secrets-github-dont-ask-again), Shmulik Cohen and Matan Giladi. Approval records can contain credentials. Treat them as sensitive and keep them out of version control. Apiiro did not validate every suspected exposure.
- [Introducing Inkling 2 Small](https://thinkingmachines.ai/news/inkling-2-small/), Thinking Machines Lab. The 12 November update links to [downloadable weights](https://huggingface.co/thinkingmachines/Inkling-2-Small). With 594B total and 17B active parameters, “Small” doesn't mean cheap to self-host.
- [The components of agent memory](https://www.anthropic.com/research/components-of-agent-memory), Lance Martin. Linked memory helped some cross-document questions without clearly improving simple retrieval in the reported experiments. Via Mario Zechner.
- [Claude Fable 5.2 and Mythos 5.2](https://www.anthropic.com/claude-fable-and-mythos-5-2), Anthropic. Fable is available through the API; Mythos access is gated. [Ethan Mollick's Fable experiments](https://www.oneusefulthing.org/p/fable-52-and-jagged-agi) are a useful companion: accumulated rules and poorly chosen targets can send capable agents off course.
- [Muse Ember](https://research.meta.ai/blog/muse-ember), Meta. A lower-cost API model aimed at repeated work such as tool calls and extraction. The efficiency comparisons are Meta's.
- [Gemini 4 Carbon is now available](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/), Koray Kavukcuoglu. API access has widened to paying developers and enterprises; Swarm remains in preview.
- [Subagents considered harmful?](https://nikvdp.com/notes/subagents-considered-harmful/), Nik van der Ploeg, via TLDR. Summaries can lose intent and corrections; full conversation forks can bury them in noise. The author experiments with choosing which original passages to pass along.
- [Generated Glossary](https://martinfowler.com/bliki/GeneratedGlossary.html), Martin Fowler. Let agents propose definitions, have domain experts review them, and keep terms separate where different teams use the same word differently.
- [Thomas Ankcorn on agent handovers](https://x.com/thomas_ankcorn/status/2119743906271432810). Two formats to borrow: BLUF puts the conclusion first; SBAR separates the situation, background, assessment and recommendation.
- [My YouTube tier list, six years later](https://thume.ca/2026/11/01/youtube-tier-list-2026/), Tristan Hume. Try Applied Science for experiments and replication, Clickspring for precision craftsmanship, or Animagraffs for visual explanations of machinery.
