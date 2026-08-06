---
title: "The Scikit-Learn Moment for LLMs Has Not Happened Yet"
date: 2026-08-06T00:00:00Z
draft: false
tags: ["ai", "llm", "machine-learning", "open-source", "enterprise"]
summary: "Enterprise teams still lack a standard workflow for adapting, evaluating, versioning, and replacing LLMs on their own terms."
description: "Why enterprise AI needs a simple, open workflow for adapting, evaluating, versioning, and replacing LLMs."
---


An engineering team today can call a powerful language model through an API (OpenAI/Anthropic etc) and have a working prototype within days. Very few teams can take a model, teach it their own work, test it against their own standards, and decide for themselves when it changes. I have come to believe that the next big shift in enterprise AI depends on that second ability becoming simple and ordinary, the way training a classifier became ordinary fifteen years ago.

This theory is speculative. It grew out of a painful model migration in a production system my team built. The release of Inkling by Thinking Machines Lab and Satya Nadella's essay on model independence gave me two more ways to test it.

## What scikit-learn actually gave people like me

I learned machine learning through scikit-learn, and later through TensorFlow. I don’t say that as decoration. Those two libraries shaped how I still think about data science today.

Scikit-learn did not invent logistic regression, random forests, or cross-validation. What it gave a newbie software engineer like me was a consistent way of working. You loaded your data. You split it into training and test sets. You transformed the features, trained a few candidate models through the same fit and predict interface, compared their scores, wept and cussed a few times, then picked one. Pipelines let you record that whole sequence so someone else could rerun it. You did not need a background in statistical computing to take part. The library's conventions, coupled with several sleepless nights, taught me what good practice looked like, and I would think a whole generation of engineers and analysts learned the same way. [1](https://scikit-learn.org/stable/about.html)

TensorFlow [3](https://www.tensorflow.org/) and PyTorch [2](https://pytorch.org/), a few years later, did something similar for deep learning. They made neural networks programmable. An engineer could define a network, train it, use a GPU (or your laptop if you could wait overnight), inspect what went wrong without building any of the underlying machinery or matrices, optimizers etc. Tools like Weights & Biases helped massively with tracking all those runs. Google built and stood behind TensorFlow. Facebook built and stood behind PyTorch. That backing mattered more than we sometimes remember, and I will come back to it near the end.

The LLM era has given us something narrower so far. Any team can access a very capable model through an API. But the provider controls the weights, the serving infrastructure, the pricing, the model's behaviour, and its retirement date. A team can build prompts, retrieval, and tools around the model. The intelligence underneath is still *rented*. You pay for a service, but you don’t always own the thing.

## What a model migration taught us

This came true for me while my team was running a project in production. The application answers questions over financial data. It generates SQL, checks the results, builds graphs, reasons over documents, and presents them in a form finance users can trust.

Getting it to work took far more than picking a capable model (gpt-4o in this case). We built the data pipelines, formalised the financial definitions, constrained how queries were generated, validated and reconciled the outputs with finance SMEs, and wrote an evaluation suite. Over many months we learned how the model read our schemas, where it made mistakes, which instructions it followed reliably, and which failures we had to catch elsewhere in the system. In effect, we had tuned every part of the application around the habits of one specific model.

Then we had to move off that model because OpenAI decided to retire it in June 2026. It was not a configuration change. We rebuilt the API integration and re-examined how the replacement model used our tools. Then we retested the prompts, reran the evaluations, investigated regressions, and put the application through a full release cycle. The replacement model, gpt-5.2, was *way* more capable. That did not reduce the work.

The experience taught me something I had not fully appreciated. For a production system, capability is not a benchmark score. It is whether the system performs a defined task at the required accuracy, latency, and cost, release after release. The LLM is one, small but important part of the whole system. And when the provider ships an upgrade, the development team and consumer inherit this load, on the provider's schedule rather than our own. And these updates keep coming at a rate its impossible for dev teams to keep everything upto date all the time, not to mention, they always cost more.

Classical machine learning never worked this way, and I lived through the difference. We trained a model, versioned it, recorded the data and parameters, deployed it, and watched it. We replaced it when we decided the replacement was worth the work. We tried our best to detect data drift, model drift, but nobody retired our checkpoint for us. That kind of control is still mostly missing from enterprise LLM systems, and I keep asking myself why.

## Fine-tuning LLMs faded, but the maths may be changing

The obvious answer to that question was supposed to be fine-tuning. Take a general model, train it further on your own examples, and make it yours. Instead, fine-tuning drifted out of most enterprise architectures, and the reasons were sound. Hosted fine-tuning was expensive, opaque, and tied to one provider. Prompting and retrieval often delivered faster gains. I’ve made this suggestion to many clients when the question comes up. Above all, frontier models improved so quickly that by the time you finished tuning one and getting it to behave, the next release might beat it out of the box. The Bitter Lesson of AI effectively calls this out. [13](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)

That last objection is the strong one, and perhaps holds for fine-tuned small models as well. If frontier progress continues, why would the cycle not simply repeat?

I can see four reasons why I’m bullish on open models;

First, bounded enterprise tasks have practical ceilings. A model that generates SQL against a known schema, or classifies a fixed set of financial exceptions, does not benefit forever from more general intelligence. Once it crosses the reliability bar the business needs, extra capability adds little. It does not need a training cut-off, doesn’t need to know biology, history and all else. Cost, speed, reliability and stability, year on year matter way more than raw capability.

Second, at large scale, the economics of inference favour the smaller model. A universal model brings enormous capability to every request, most of it irrelevant to the task. If a smaller model meets the quality bar, the savings at production scale can pay for the adaptation work many times over.

Third, open weights change who controls releases. When a team holds the model files itself, it can keep running a proven version while it tests a newer one. A stronger base model becomes an option to *evaluate* rather than a *migration* to plan, re-engineer and absorb. The word "checkpoint" simply means a saved copy of the model at a point in time, and owning your model checkpoints is what makes this possible.

Fourth, and this is the reason I find most persuasive, the tuned model is not the main asset. The old ML models never were either. The main asset is everything around it. The quality of the data, the worked examples, the corrections, the recorded failures, the evaluation sets, the acceptance criteria. If a team keeps that material in good order with rigor, it can apply the same process to a better base model later. The base model becomes replaceable. The accumulated learning then becomes the asset, not the liability that has to justify more spend.

My own experiences with LLM solutions in production supports the fourth point more than anything. Almost everything durable we built was around the model, not inside it. What we lacked was a way to carry that work across models cheaply.

## Inkling made me look again

Inkling, released by Thinking Machines Lab in July, is the development that made me revisit all of this. [4](https://thinkingmachines.ai/news/introducing-inkling/)

This is a large open-weight model, and by the company's own admission it is not the strongest model available. [4](https://thinkingmachines.ai/news/introducing-inkling/) Even Inkling-Small is small only next to its sibling. [5](https://thinkingmachines.ai/news/inkling-small/) Neither is the compact model I am imagining, the kind an ordinary team could run on modest hardware.

What caught my attention is the positioning. Thinking Machines presents Inkling as a *base for adaptation* rather than a finished product. The weights are downloadable. Fine-tuning through their Tinker platform [6](https://thinkingmachines.ai/tinker/) is treated as the main way to use the model, not an afterthought. In the launch demonstration, the model builds its own training data, runs a post-training job on itself, and loads the improved weights back into its own harness. The demonstration is simple, but the product idea behind it is the interesting part. This is a lab betting that models people can shape will beat models people can only query. The launch video showed a fascinating example of this, which I’d highly recommend checking out.

I honestly don’t know whether that bet pays off for them. I do think it hints that adaptation is moving toward the centre of how models are sold, and that is the direction of my argument here.

## Nadella said the strategic part better than I could

A few weeks later, Satya Nadella published an essay on Microsoft's MAI models that gave the same idea a strategic frame. He argues for what he calls "product-specific evals and model independence". [12](https://x.com/satyanadella/status/2082601792538640465) In simple words, a company should measure models against its own product's outcomes, and it should build so that any single model can be swapped out. He describes keeping the harness, context, memory, and tools outside the model, so that the product keeps improving even when a particular model is removed.

Microsoft operates at a scale that has nothing to do with the teams I am writing about, and Nadella is also talking his own book. Even so, this idea matches what my personal experience taught me the hard way. It’s never about which model is smartest in general. What’s more useful is which combination of model, context, tools, and learned behaviour produces the required outcome at an acceptable cost, reliably, consistently. With this foundation, the model is one versioned component inside a larger system, and this is what scikit-learn, TensorFlow, and MLOps made true for classical models.

## The tools exist now. But getting to a clean workflow takes a lot.

We are not starting from zero, and there is some work already done in this space. Tinker [6](https://thinkingmachines.ai/tinker/) offers managed post-training. Axolotl [7](https://github.com/axolotl-ai-cloud/axolotl) and torchtune [9](https://github.com/meta-pytorch/torchtune) are open frameworks for adapting models. Unsloth [8](https://github.com/unslothai/unsloth) makes local training cheaper. vLLM [10](https://docs.vllm.ai/) serves models privately at high performance, and llama.cpp [11](https://github.com/ggml-org/llama.cpp) runs compressed models on ordinary hardware. Each of these solves a piece of the problem, which is why saying the moment "has not happened" needs some nuance.

What I cannot find anywhere is the coherence that scikit-learn brought. There is no widely adopted way to treat the whole model system as one versioned product, where a single manifest binds together the base model, the tokenizer, the training and evaluation data, the adapted weights, the prompts and tools, the inference configuration, the evaluation results, and the rollback version. A team should be able to reproduce a release from that manifest, compare it against a potential candidate replacement, and promote the candidate only when it passes defined quality, risk, and cost gates. Scikit-learn's success was never the algorithms. It was the conventions that made everything around the algorithms one comprehensible workflow.

If that layer arrives, my guess is that it comes as an open source project with a large company standing behind it. TensorFlow spread because Google used it internally, staffed it, and kept it maintained for years. PyTorch spread because Facebook did the same. A workflow standard needs sustained maintenance and enterprise trust before anyone builds on it, and history suggests that takes a backer with deep pockets and its own reasons for wanting the standard to exist. OpenAI, Anthropic, Microsoft, Meta, and Thinking Machines all have plausible motives here. I do not know which of them, if any, will do it. I am fairly confident the winning version will be open, because every previous layer of this stack that became a standard was open.

## What belongs in the model, and what does not. AKA, why not just use RAG for everything

None of this means post-training your enterprise knowledge into model weights.

Facts that change, such as balances, prices, customer records, and current policies, should stay in governed databases and reach the model through retrieval and tools. Those systems give you freshness, access control, and the ability to delete, and open weights give you none of that. Fine-tuning is suited to stable behaviour instead. A specialised model can learn how to read your schemas, follow your approved process, call the right tool, produce output in your required structure, and recognise when a case must go to a human. Retrieval supplies the current facts. Fine-tuning changes how the system does its job.

## What this new workflow could look like

Picture a model supporting a bank's financial close and reconciliation process. It does not need broad expertise across every domain. It needs the bank's chart of accounts, reconciliation rules, materiality thresholds, approved query patterns, exception categories, and escalation policies. Current balances still come from governed systems through tools.

Its behaviour, though, could be trained on years of resolved exceptions, analyst corrections, accepted and rejected queries, and final decisions. Each production cycle would add governed examples to the next training and evaluation set. Over time the bank would own a compact model shaped to this one workflow, a curated corpus of examples and failures, an evaluation suite that measures the actual job, and a recorded history of versions and acceptance decisions.

A frontier API model would still be smarter in the general sense. For this workflow, that may not matter. The specialist would be cheaper, faster, deployable inside the bank's own boundary, stable across releases, and easier to audit. Most importantly, the bank would improve it using its own operational history, on its own schedule. That combination of model and learning process would be an asset the bank owns. The universal API model, however capable, stays a service the bank pays for. It *owns* some parts, it *rents* the rest.

## So, how do we know when this comes together

The scikit-learn/tensorflow moment will have arrived when a mid-sized product team, with no dedicated model infrastructure group, can take one bounded use case from examples to a production specialist model in weeks. The team should be able to compare candidate base models against its own evaluations, adapt the best one, deploy it inside its required boundary, monitor it, and ship improved versions through an ordinary engineering process. When a better base model appears, the same data and evaluations should decide whether it earns a replacement, and the production model should not change until that decision is made.

If, a few years from now, that is still the preserve of specialist teams at large companies, then I was wrong, or at least early. If it has become routine, then the pattern that played out with scikit-learn, TensorFlow, and PyTorch will have repeated, and the most valuable model in many enterprises will be a small one that has learned exactly how that one organisation works.

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
