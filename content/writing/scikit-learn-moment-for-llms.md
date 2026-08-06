---
title: "The Scikit-Learn Moment for LLMs Has Not Happened Yet"
date: 2026-08-06T00:00:00Z
draft: false
tags: ["ai", "llm", "machine-learning", "open-source", "enterprise"]
summary: "Enterprise teams still lack a standard workflow for adapting, evaluating, versioning, and replacing LLMs on their own terms."
description: "Why enterprise AI needs a simple, open workflow for adapting, evaluating, versioning, and replacing LLMs."
---


An engineering team today can call a powerful language model through an API (OpenAI/Anthropic etc) and have a working prototype within days. Very few teams can take a model and teach it their own work. Even fewer can test it against their own standards and decide when a new version ships. I have come to believe that the next big shift in enterprise AI depends on that ability becoming simple and ordinary, the way training a classifier became ordinary fifteen years ago.

This theory is speculative. It grew out of a painful model migration in a production system my team built. The release of Inkling by Thinking Machines Lab and Satya Nadella's essay on model independence gave me two more ways to test it.

## What scikit-learn actually gave people like me

I learned machine learning through scikit-learn, and later through TensorFlow. I don’t say that as decoration. Those two libraries shaped how I still think about data science today.

Scikit-learn did not invent the algorithms or cross-validation. What it gave a newbie software engineer like me was a consistent way of working. You loaded your data and split it into training and test sets. After transforming the features, you trained a few candidate models through the same fit and predict interface. You compared their scores and eventually picked one, after weeping and cussing a few times. Pipelines let you record that whole sequence so someone else could rerun it. You did not need a background in statistical computing to take part. With several sleepless nights, the library's conventions taught me what good practice looked like. I would think a whole generation of engineers and analysts learned the same way. [1](https://scikit-learn.org/stable/about.html)

TensorFlow [3](https://www.tensorflow.org/) and PyTorch [2](https://pytorch.org/), a few years later, did something similar for deep learning. They made neural networks programmable. An engineer could define and train a network on a GPU, or wait overnight on a laptop. When something went wrong, the engineer could inspect it without building the underlying matrices and optimizers. Tools like Weights & Biases helped massively with tracking all those runs. Google built and stood behind TensorFlow. Facebook built and stood behind PyTorch. That backing mattered more than we sometimes remember, and I will come back to it near the end.

The LLM era has given us something narrower so far. Any team can access a very capable model through an API. The provider owns the weights and runs the service. It also sets the price and shapes the model's behaviour. The provider decides when to retire it. Prompts can guide the model. Retrieval and tools can connect it to company data and software. The intelligence underneath is still *rented*. You pay for a service, but you don’t always own the thing.

## What a model migration taught us

This came true for me while my team was running a project in production. The application answers questions over financial data. It generates SQL and checks the results. Depending on the question, it builds a graph or reasons over documents. It then presents the answer in a form finance users can trust.

Getting it to work took far more than picking a capable model (gpt-4o in this case). We built the data pipelines and formalised the financial definitions. Query generation came next. We constrained it, then validated and reconciled the outputs with finance SMEs. The evaluation suite captured the expected behaviour. Over many months we learned how the model read our schemas and where it made mistakes. We found which instructions it followed reliably. The remaining failures had to be caught elsewhere in the system. In effect, we had tuned every part of the application around the habits of one specific model.

Then we had to move off that model because OpenAI decided to retire it in June 2026. It was not a configuration change. We rebuilt the API integration and re-examined how the replacement model used our tools. Then we retested the prompts and reran the evaluations. We investigated the regressions before putting the application through a full release cycle. The replacement model, gpt-5.2, was *way* more capable. That did not reduce the work.

The experience taught me something I had not fully appreciated. In production, we measured capability against a defined task. Correct answers came first. The response also had to meet our latency limit without pushing the run over budget, and we had to prove that again on every release. The LLM was a small but important part of the whole system. OpenAI's retirement decision set our deadline. Our development team had to do the migration, and our users had to accept the risk of another release. The updates also arrived faster than development teams could absorb them. Keeping every application current all the time was impossible. In our experience, each move cost more.

I had much more control over releases in classical machine learning, and I lived through the difference. We trained a model and saved its version. We also recorded the data and parameters that produced it. After deployment, we monitored it until we chose to test a replacement. The decision to replace it was ours. We tried our best to detect data drift and model drift, but nobody retired our checkpoint for us. That kind of control is still mostly missing from enterprise LLM systems, and I keep asking myself why.

## Fine-tuning LLMs faded, but the maths may be changing

Fine-tuning was supposed to answer that question by teaching a general model from a team's own examples. It later drifted out of most enterprise architectures for sound reasons. Hosted fine-tuning cost a lot, and teams had little visibility into how it was done. The tuned model also remained tied to one provider. Prompting and retrieval often delivered faster gains. I’ve made this suggestion to many clients when the question comes up. Above all, frontier models improved so quickly that by the time you finished tuning one and getting it to behave, the next release might beat it out of the box. The Bitter Lesson of AI effectively calls this out. [13](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)

That last objection is the strong one, and perhaps holds for fine-tuned small models as well. If frontier progress continues, why would the cycle not simply repeat?

I can see four reasons why I’m bullish on open models;

First, bounded enterprise tasks have practical ceilings. A model that generates SQL against a known schema, or classifies a fixed set of financial exceptions, does not benefit forever from more general intelligence. Once it crosses the reliability bar the business needs, extra capability adds little. It does not need current knowledge about unrelated fields. Over years of operation, reliability and stability matter way more than raw capability. Cost and response time decide whether the system is practical.

Second, at large scale, the economics of inference favour the smaller model. A universal model brings enormous capability to every request, most of it irrelevant to the task. If a smaller model meets the quality bar, the savings at production scale can pay for the adaptation work many times over.

Third, open weights change who controls releases. When a team holds the model files itself, it can keep running a proven version while it tests a newer one. A stronger base model becomes another candidate. The team migrates only after its own evaluation shows that the gain justifies the engineering work. The word "checkpoint" simply means a saved copy of the model at a point in time, and owning your model checkpoints is what makes this possible.

Fourth, and this is the reason I find most persuasive, the durable asset is the process the team owns. Worked examples and corrections capture how the task should be done. Recorded failures feed the evaluation set, and the acceptance criteria define when a model can ship. If a team keeps that material in good order, it can apply the same process to a better base model later. The base model becomes replaceable. The accumulated learning lowers the cost and risk of the next adaptation.

My own experience with LLM solutions in production supports the fourth point more than anything. Most of what lasted sat in the examples and evaluations we kept. The application controls carried the rest. We needed a cheap way to apply that work to another model.

## Inkling made me look again

Inkling, released by Thinking Machines Lab in July, is the development that made me revisit all of this. [4](https://thinkingmachines.ai/news/introducing-inkling/)

This is a large open-weight model, and by the company's own admission it is not the strongest model available. [4](https://thinkingmachines.ai/news/introducing-inkling/) Even Inkling-Small is small only next to its sibling. [5](https://thinkingmachines.ai/news/inkling-small/) Neither is the compact model I am imagining, the kind an ordinary team could run on modest hardware.

What caught my attention is the positioning. Thinking Machines presents Inkling as a model that teams are expected to adapt. The weights are downloadable. Fine-tuning through their Tinker platform [6](https://thinkingmachines.ai/tinker/) is part of the main product workflow. In the launch demonstration, Inkling creates training data and uses Tinker to run a post-training job. It evaluates the result, then loads the improved weights into its harness. The simple loop makes the product idea clear. Thinking Machines expects customers to customise the model as part of normal use. I’d recommend the launch video because it shows the whole process.

I honestly don’t know whether that bet pays off for them. I do think it hints that adaptation is moving toward the centre of how models are sold, and that is the direction of my argument here.

## Nadella said the strategic part better than I could

A few weeks later, Satya Nadella published an essay on Microsoft's MAI models that gave the same idea a strategic frame. He argues for what he calls "product-specific evals and model independence". [12](https://x.com/satyanadella/status/2082601792538640465) In simple words, a company should measure each model against its own product outcomes. The company should also be able to replace that model. He describes keeping the agent runtime outside the model. That software supplies product context and stores memory. It also connects tools, so the product can keep improving after a model is removed.

Microsoft operates at a scale that has nothing to do with the teams I am writing about, and Nadella is also talking his own book. Even so, this idea matches what my personal experience taught me the hard way. General intelligence is a weak guide to production fit. I need a model that works with the product's context and tools to produce the required outcome at an acceptable cost. The result also has to hold across releases. With that foundation, the model becomes one versioned component inside a larger system. Classical machine learning already had this release discipline.

## The tools exist now. But getting to a clean workflow takes a lot.

The individual stages already have tools, but each project defines a narrow boundary. Tinker [6](https://thinkingmachines.ai/tinker/) manages post-training. Axolotl [7](https://github.com/axolotl-ai-cloud/axolotl) and torchtune [9](https://github.com/meta-pytorch/torchtune) expose adaptation through open frameworks, while Unsloth [8](https://github.com/unslothai/unsloth) focuses on lowering local training costs. The serving projects begin after that work ends. vLLM [10](https://docs.vllm.ai/) targets private deployments at high throughput, and llama.cpp [11](https://github.com/ggml-org/llama.cpp) runs compressed models on ordinary hardware. This division explains the gap. Each project solves its stage, while the team still has to define the release process across them. That is why saying the moment "has not happened" needs some nuance.

What I cannot find anywhere is the coherence that scikit-learn brought. There is no widely adopted way to treat the whole model system as one versioned product. A single manifest should identify the base model and tokenizer, then point to the adapted weights. The same record would capture the data used for training and evaluation. Prompts and tool definitions belong there as well. The inference settings that affect behaviour should sit beside them. Evaluation results and the rollback version would complete the release record. A team should be able to reproduce a release from that manifest and compare it against a potential replacement. The team should own the release decision, promoting a candidate only after it passes the quality and risk checks within its cost limit. Scikit-learn's success was never the algorithms. It was the conventions that made everything around the algorithms one comprehensible workflow.

If that workflow layer arrives, my guess is that it will be an open source project with a large company as its long-term maintainer. A standard has to survive model changes and compatibility problems for years before enterprise teams will trust it. Google made that commitment to TensorFlow, and Facebook did the same for PyTorch. Both companies used the frameworks themselves and kept engineers on them. That connection between internal use and sustained maintenance is why teams could build on the conventions. I do not know which company will take on that role for LLMs. I expect the winning version to be open because the earlier workflow standards were open.

## What belongs in the model, and what does not. AKA, why not just use RAG for everything

None of this means post-training your enterprise knowledge into model weights.

Facts that change should stay in governed databases and reach the model through retrieval and tools. Balances and prices are the clearest examples because the values may be different on the next request. The same applies to customer records and current policies. Governed systems give you fresh data and enforce access control. They also let you delete a record, which open weights cannot do. Fine-tuning is suited to stable behaviour instead. A specialised model can learn how to read your schemas and follow your approved process. It can learn when to call a tool and how to structure the output. It can also recognise when a case must go to a human. Retrieval supplies the current facts. Fine-tuning changes how the system does its job.

## What this new workflow could look like

Picture a model supporting a bank's financial close and reconciliation process. It does not need broad expertise across every domain. It needs the bank's chart of accounts and reconciliation rules. Materiality thresholds tell it which differences matter. Approved query patterns constrain what it can ask. Exception categories and escalation policies govern what happens next. Current balances still come from governed systems through tools.

Its behaviour, though, could be trained on years of resolved exceptions and analyst corrections. Accepted and rejected queries would show which steps were allowed. Final decisions would show the outcome. Each production cycle would add governed examples to the next training and evaluation set. Over time the bank would own a compact model shaped to this one workflow. It would also own the curated examples and failures used to improve it. Its evaluation suite would measure the actual job, and its version history would record every acceptance decision.

A frontier API model would still be smarter in the general sense. For this workflow, that may not matter. The specialist could cost less and respond faster. The bank could deploy it inside its own boundary and hold it stable across releases. That would make audits easier. The bank would improve it using its own operational history, on its own schedule. The bank would own that workflow and learning process. It would continue to pay for access to the universal API model.

## So, how do we know when this comes together

The scikit-learn/tensorflow moment will have arrived when a mid-sized product team, with no dedicated model infrastructure group, can take one bounded use case from examples to a production specialist model in weeks. The team should compare candidate base models against its own evaluations and adapt the best one. After deployment inside its required boundary, monitoring and later releases should follow an ordinary engineering process. When a better base model appears, the same data and evaluations should decide whether it earns a replacement. The production model should not change until that decision is made.

If specialist teams at large companies are still the only ones able to do this a few years from now, then I was wrong or at least early. If it has become routine, then the pattern that began with scikit-learn and continued in deep learning will have repeated. The most valuable model in many enterprises will be a small one that has learned exactly how that one organisation works.

I lived through the first version of this democratisation as a beneficiary of it. That is probably why I find the second version so easy to believe in, and why I can’t wait for it to happen.

## References

1. [https://scikit-learn.org/stable/about.html](https://scikit-learn.org/stable/about.html)

2. [https://pytorch.org/](https://pytorch.org/)

3. [https://www.tensorflow.org/](https://www.tensorflow.org/)

4. [https://thinkingmachines.ai/news/introducing-inkling/](https://thinkingmachines.ai/news/introducing-inkling/)

5. [https://thinkingmachines.ai/news/inkling-small/](https://thinkingmachines.ai/news/inkling-small/)

6. [https://thinkingmachines.ai/tinker/](https://thinkingmachines.ai/tinker/)

7. [https://github.com/axolotl-ai-cloud/axolotl](https://github.com/axolotl-ai-cloud/axolotl)

8. [https://github.com/unslothai/unsloth](https://github.com/unslothai/unsloth)

9. [https://github.com/meta-pytorch/torchtune](https://github.com/meta-pytorch/torchtune)

10. [https://docs.vllm.ai/](https://docs.vllm.ai/)

11. [https://github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

12. [https://x.com/satyanadella/status/2082601792538640465](https://x.com/satyanadella/status/2082601792538640465)

13. [http://www.incompleteideas.net/IncIdeas/BitterLesson.html](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)
