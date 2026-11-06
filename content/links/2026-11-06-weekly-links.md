+++
title = "Weekly Links: 6 November 2026"
date = 2026-11-06T12:00:00+05:30
draft = false
summary = "What agent checks actually establish, reading and editing model weights, training models to use notes, and the Ripple and Sarvam Prism releases."
tags = ["links"]
+++

## At a glance

This week, researchers examine what can go wrong even when an agent completes its task or a human approves its work. Ripple and Sarvam Prism offer new open weights for different kinds of work. Engram explores training models to use changing notes, while experiments with neural network weights test how much models can understand and alter directly.

## Highlight

### A successful result still needs the right check

[Foresight-SWE](https://arxiv.org/abs/2611.01181), by Shaswat Patel and colleagues, tests whether coding agents can complete a task while avoiding a defect that was discovered later in the repository's history. Across 212 selected tasks from 35 repositories and eleven models, average success on the stated task was 60.7%. Requiring the agent to also avoid the later defect reduced it to 14.8%.

These tasks were deliberately selected from changes with later-discovered defects. The result is not a production failure rate, and there is no human baseline. Models also ran with different supporting software. A test can establish that the requested feature works while overlooking a consequence of the change. The authors provide code and a dataset alongside the paper so others can investigate this gap.

[OpenAI's Linux vulnerability work](https://openai.com/index/a-thousand-fewer-paths-to-root/) provides a different example. Some agents obtained root access through a vulnerability other than the one they had been assigned. Getting root was insufficient evidence that the assigned flaw had been exploited. Researchers needed to check how the agent reached that outcome.

OpenAI reports producing 948 distinct patches. These are the company's research results, and the count includes patches still subject to maintainer review. It does not mean all 948 fixes are already merged upstream.

For teams evaluating agents, both studies favour checks tied to the intended change. A feature test should be accompanied by checks for consequences elsewhere in the code. An exploit test needs to establish which vulnerability the agent used.

## Top Stories

### 1. Human signoff can inherit the agent's judgment

In [Anthropic's study of experts' judgment calls](https://www.anthropic.com/research/agents-judgment-calls), Amaç Herdağdelen, Hailey Joren and Alex Tamkin asked analysts to assess a farming advisory programme. Fifty causal-inference practitioners worked with agents whose preferences on reasonable analytical choices were secretly randomised. Eleven other participants chose to work without AI.

The experts' analytical choices agreed with their agents' preferences 86% of the time. Using their planned statistical analysis, the researchers did not find a statistically significant direct effect on the final recommendation.

The researchers tested one model on a single analysis task and deliberately strengthened its preferences. The eleven participants who worked without AI chose that themselves, so they were not a comparable control group. These limits prevent treating the result as a measure of influence across everyday expert work.

Human approval needs to include scrutiny of the analytical choices, e.g., why productivity was measured per hectare instead of per unit of cost. A reviewer who considers only the finished analysis may accept assumptions introduced by the agent without examining the alternatives.

### 2. Ripple and Prism offer different kinds of open model

[Ricursive Intelligence's Ripple-65B Preview](https://www.ricursive.com/ripple) is a dense 65-billion-parameter model pretrained from scratch. Both base and instruction checkpoints are available under Apache 2.0, including the [released instruction weights](https://huggingface.co/ricursiveAI/Ripple-65B-Preview). The weight files in BF16, a 16-bit number format, total roughly 130 GB before allowing for additional memory needed to run the model.

Ricursive's headline coding comparison is restricted to US open-weight models. It is a vendor evaluation using its own testing setup, so it does not establish global leadership. A dense model applies the same network to each token. A mixture-of-experts model selects a subset of its expert networks, so comparing total parameter counts alone says little about serving costs. Ripple's available weights and documented training recipe make it possible to test the company's claims independently.

[Sarvam Prism](https://www.sarvam.ai/blogs/sarvam-prism) addresses a narrower task. It reads the supplied context and a question, then assigns a probability to each of the allowed answers in one pass. That could help software decide whether to route a request or ask for human review, without generating a long answer first.

Prism has open weights, but it is built on Sarvam 105B and requires at least 120 GB of GPU memory when using its 8-bit FP8 format. Sarvam's speed and accuracy comparisons are its own measurements. Before using those probabilities to automate a decision, a team would need to test how reliably they reflect errors on its own work.

### 3. Training a model to use notes

[Engram's Learning in a World of Notes](https://engram.com/blog/learning-in-a-world-of-notes) explores training models to consult notes and check the underlying sources. The aim is to learn how to find and verify information even when that information changes after training.

A separate agent prepares the notes. The model being trained reads them, with rewards for accurate answers and penalties for unnecessary cost. During training, the workspace and notes stay fixed. The researchers then examine whether the learned behaviour transfers when the available information changes.

Engram reports gains across three workspaces, but comparisons with frontier models are mixed. On its warehouse analysis tasks, the trained model still falls short of the strongest frontier results. The cost estimates depend on assumed usage and pricing. These remain the company's experimental results, without independent replication reported here.

This gives teams adapting smaller models a specific behaviour to test. They can check whether a model notices incomplete or outdated notes and consults the underlying records. Engram's approach is worth comparing with giving the same notes to a model without this additional training.

### 4. Reading weights and editing them are different experiments

[Rikiya Takehi and colleagues' weight-space programming experiments](https://rikiyat.github.io/blog/weight-space-programming/) include identifying what small neural networks do from their raw weights, without tools. Other experiments use Python to inspect or change weights. In the Qwen experiment, the editing fixed repetitive reasoning loops and improved measured performance. A comparison using Gemma, which did not have the looping problem, did not demonstrate a mathematical improvement.

[Matthew Honnibal's critique](https://honnibal.dev/blog/astra-read-write-misleading) focuses on presenting these different methods together. His objection is that readers can mistake the tool-assisted language-model work for the same capability as interpreting small networks from raw numbers. Each experiment needs to be judged by the tools and feedback available to the model.

[Simon Willison tried the interpretation task on his laptop](https://simonwillison.net/2026/Nov/3/qwen-can-interpret-model-weights/) with Qwen 3.8 27B. It identified Pac-Man and Pong, and also recognised Breakout, taking roughly 46 to 65 minutes on the successful runs. It missed Freeway. This is a small, self-reported test of interpreting weights. It does not replicate the weight-editing experiments or establish a general ability to improve another model.

## Miscellaneous Links

- [Do Research Agents Have Taste?](https://arxiv.org/abs/2610.40488). Art Kanke's rTaste study asks agents to propose and rank experiments based on seven NLP papers. Their rankings did not measurably improve on taking the proposal written first. Model-generated judgments and the absence of a human baseline limit the conclusion. The findings apply to this experiment-selection setup, and do not establish how well agents judge research more broadly.
- [Progress on provable inference](https://www.anthropic.com/research/provable-inference). Anthropic and collaborators introduce FlashProve, a research prototype for proving that an answer was generated using a previously specified set of model weights, without revealing those weights. The proof concerns the computation performed. It cannot establish whether the answer is true. The prototype selects the highest-scoring next token at each step and uses an integer version of the model. In the reported tests, generating proofs took roughly 70 to 95 times the GPU time of ordinary inference.
- [Martin Fowler's Software Architecture Guide](https://martinfowler.com/architecture/). This guide, dated August 1, 2019, is an evergreen reference. Fowler connects architecture to a team's shared understanding of a system and the decisions that make future changes easier or harder. It provides an entry point to the site's architecture writing, organised around the effect of design decisions on later development.
