---

title: "The Scikit-Learn Moment for LLMs Has Not Happened Yet"
date: 2026-08-06T00:00:00Z
lastmod: 2026-08-21T00:00:00Z
draft: false
tags: ["ai", "llm", "machine-learning", "open-source", "enterprise"]
summary: "Enterprise teams still lack a standard workflow for adapting, evaluating, versioning, and replacing LLMs on their own terms."
description: "How do engineering teams keep control when models they use change"
---

I can get a working demo out of a hosted language model in a few days. But given how frequently the language models change, replacing that model later is still a proper pain. I think there is a gap with current AI Engineering workflows where dealing with model changes is still not as seamless as it could be. Scikit-learn enabled this kind of work for the classical ML models about fifteen years ago.

## What scikit-learn actually gave people like me

I learned machine learning through scikit-learn, and later through TensorFlow. These libraries and the lessons learnt, still shape my worldview on how to build AI systems. 

Scikit-learn gave a newbie software engineer like me a consistent way of working. You loaded your data and split it into training and test sets. After transforming the features, you trained a few candidate models through the same fit and predict interface. You compared their scores and eventually picked one, after weeping and cussing a few times. You could record that whole sequence in a pipeline so someone else could rerun it. You did not need a background in statistical computing to take part. After several sleepless nights, I learned what good practice looked like from the library's conventions. I think a whole generation of engineers and analysts learned the same way. [1](https://scikit-learn.org/stable/about.html)

A few years later, TensorFlow [3](https://www.tensorflow.org/) and PyTorch [2](https://pytorch.org/) did similar work for deep learning. You could define and train a network on a GPU, or wait overnight on a laptop. When something went wrong, you could inspect it without building the underlying matrices and optimizers. Tools like Weights & Biases helped with tracking those runs. Most importantly, Google stood behind TensorFlow. Facebook stood behind PyTorch. That kind of backing is part of why these libraries became industry standards.

## Today, a model migration isn't just about bumping a version number, yet.

A while back, we built an application for questions over financial data. For each question we generate SQL and check the results. Depending on the question, we build a graph or reason over documents, then present the answer in a form finance users can trust.

Getting it to work took much more than picking a capable model (gpt-4o in this case). We built the data pipelines and formalised the financial definitions. We then built query generation. We constrained it, then validated and reconciled the outputs with finance SMEs. We captured the expected behaviour in an evaluation suite. Over many months we learned how the model read our schemas and where it made mistakes. We found which instructions it followed reliably. We had to catch the remaining failures elsewhere in the system. In effect, we had tuned every part of the application around the habits of one specific model.

Then we had to move off that model because OpenAI decided to retire it in June 2026. I'm still sour about this. We could not just change a config. We had to rebuild the API integration figure out how to get structured outputs and tool calling with the new model and API. Not to mention review prompts, eval suites all over again. The replacement model, gpt-5.2, was much more capable, but we didnt need all that capabiity.  

For me, the LLM was a small but important part of the whole system. Keeping every application current all the time today is near impossible. For context, we're now at gpt-5.6, barely 3 months since we started out. How any self-respecting engineering team building solutions for a regulated enterprise can keep upgrading base models and maintain quality is frankly beyond me.

But, looking back a decade or so, we had much more control over releases in classical machine learning, and some of you who lived through that can tell the difference. We trained a model and saved its version. We also recorded the data and parameters that produced it. After deployment, we monitored it until we chose to test a replacement. The decision to replace it was ours. We tried our best to detect data drift and model drift, but nobody retired our checkpoint for us. We still do not have that kind of release control in the LLM systems.

## But, what about Fine-tuning?

Fine-tuning was supposed to restore that control by teaching a general model from a team's own examples. Teams later dropped it from most enterprise architectures for sound reasons. Hosted fine-tuning cost a lot, and teams had little visibility into how it was done. The tuned model also remained tied to one provider. Prompting and retrieval often delivered faster gains. I've made this suggestion to many clients when the question comes up. Above all, frontier labs released better models so quickly that by the time you finished tuning one and getting it to behave, the next release might beat it out of the box. The Bitter Lesson of AI effectively calls this out. [13](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)

That last objection is the strong one, and perhaps holds for fine-tuned small models as well. If frontier progress continues, why would the cycle not simply repeat?

I can see four reasons why I'm bullish on open models, other than the obvious fact that they are getting really good. 

First, bounded enterprise tasks have a ceiling. If you generate SQL against a known schema, or classify a fixed set of financial exceptions, more general intelligence stops helping once you clear the reliability bar the business needs. The model does not need current knowledge about unrelated fields. Over years of operation, you care about reliability and stability more than raw capability. Cost and response time still have to stay practical.

Second, at large enough scale, a smaller model is almost always cheaper to run. A universal model brings a lot of capability to every request, most of it irrelevant to the task. If a smaller model meets the quality bar, the savings at production scale can pay for the adaptation work many times over.

Third, if a team holds the open-weight files itself, that team controls releases. It can keep running a proven version while it tests a newer one. A stronger base model is just another candidate. The team migrates only after its own evaluation shows that the gain justifies the engineering work. A checkpoint is a saved copy of the model at a point in time. Owning those files is what makes this possible.

Fourth, and this is the reason I find most persuasive, the process the team owns is what lasts. Worked examples and corrections record how the task should be done. You add recorded failures to the evaluation set. You decide when a model can ship against a written acceptance bar. If a team keeps that material in good order, it can apply the same process to a better base model later. The base model is replaceable. The examples and checks are what lower the cost and risk of the next adaptation.

My own experience with LLM solutions in production supports the fourth point more than anything. Organisational knowledge, custom workflows, skills and evaluations are what makes a solution work in an enterprise, not the latest shiny model. 

## A new direction - Inkling 

Thinking Machines Lab released Inkling in July, and it was a bit different to the typical bench-maxxing we're used to seeing. [4](https://thinkingmachines.ai/news/introducing-inkling/) It is a large open-weight model, and by the company's own admission it is not the strongest model available. Even Inkling-Small is small only next to its sibling. [5](https://thinkingmachines.ai/news/inkling-small/) Neither are small langiage models that an ordinary team could run on modest hardware.

But Thinking Machines presents Inkling as a model that teams are expected to adapt. The weights are downloadable. But, fine-tuning through their Tinker platform [6](https://thinkingmachines.ai/tinker/) is part of the main product workflow. In the launch demonstration, Inkling creates training data and uses Tinker to run a post-training job, evaluates the result, then loads the improved weights into its harness. I'd recommend the launch video because it shows the whole process.

I honestly don't know whether that bet pays off for them. I do think it shows a new direction that is different from the norm, and I think that is really interesting in the next few months. 

## Nadella said the strategic part better than I could

A few weeks later, Satya Nadella published an essay on Microsoft's MAI models. He argues for what he calls "product-specific evals and model independence". [12](https://x.com/satyanadella/status/2082601792538640465) In simple words, a company should measure each model against its own product outcomes, and it should be able to replace that model. He describes keeping the agent runtime outside the model. The runtime holds product context, stores memory, and connects tools, so the product can keep improving after a model is removed.

Microsoft operates at a scale that has nothing to do with the teams I am writing about, and Nadella is also talking his own book. Even so, this matches what the migration taught me. General intelligence is a weak guide to production fit. I need a model that works with the product's context and tools to produce the required outcome at an acceptable cost, and that result has to hold across releases.

## The tools exist now. But getting to a clean workflow takes a lot.

The individual stages of this control place exist -  but each project defines a narrow boundary. You can use Tinker [6](https://thinkingmachines.ai/tinker/) for post-training. Axolotl [7](https://github.com/axolotl-ai-cloud/axolotl) and torchtune [9](https://github.com/meta-pytorch/torchtune) expose adaptation through open frameworks. Unsloth [8](https://github.com/unslothai/unsloth) focuses on lowering local training costs. After that, you still have to serve the model. vLLM [10](https://docs.vllm.ai/) is aimed at private deployments at high throughput. llama.cpp [11](https://github.com/ggml-org/llama.cpp) runs compressed models on ordinary hardware. Each project solves its stage. The team still has to define the release process across them.

I still cannot find a widely adopted way to treat the whole model system as one versioned product. A single catalog that should keep:

- the base model (weights + tokenizer)
- the data used for training and evaluation
- prompts and tool definitions
- the inference settings that affect behaviour
- evaluation results and the rollback version

Skills, hooks, extensions, MCP connections would all exist in the application layer. 

A team should be able to reproduce a release from that record and compare it against a potential replacement. The team should own the release decision, and promote a replacement candidate only after it passes the quality and risk checks within its cost limit. The good old MLOps lifecycle. 

If that workflow layer arrives, my guess is that it will be an open source project with a large company as its long-term maintainer. A standard has to survive model changes and compatibility problems for years before enterprise teams will trust it. Google made that commitment to TensorFlow, and Facebook did the same for PyTorch. Both companies used the frameworks themselves and kept engineers on them. That connection between internal use and sustained maintenance is why teams could build on the conventions. I do not know which company will take on that role for LLMs. I expect the winning version to be open because the earlier workflow standards were open.

## Ok, but what about RAG ?

None of this means you should post-train your enterprise knowledge into model weights every time.

Facts that change should stay in databases and sharepoint locations and reach the model through retrieval and tools. Any real-time data, prices, indices are the obvious examples, because the values may be different on the next request. The same applies to customer records and current policies. From these systems you get fresh data, you can enforce access control, and you can delete a record, which you cannot do with open weights. But fine-tuning is for stable behaviour instead. You can train a specialised model to read your schemas and follow your approved process, e.g. when to call a tool and how to structure the output. Use retrieval for current facts. Use fine-tuning to change how the system does the job.

## What this new workflow could look like

Picture a model supporting a bank's financial close and reconciliation process. It needs the bank's chart of accounts and reconciliation rules, not broad expertise across every domain. Current balances still come from governed systems through tools. You could train its behaviour on years of resolved exceptions, analyst corrections, and accepted or rejected queries. After each production cycle, the team would add governed examples to the next training and evaluation set. Over time the bank would own a compact model for this one workflow, plus the examples, failures, evaluations, and version history that surround it.

A frontier API model would still be smarter in the general sense. For this workflow, that may not matter. The specialist could cost less and respond faster, and the bank could keep it inside its own boundary. The bank would still pay for the universal API model when a job is unbounded, or needs external tool calls. The workflow would still take real engineering the first time through. But the repeatable, boring, time consuming parts should be owned by the org. This is what should make the KPIs look good, not what the latest rented model brings as capability. 

## So, how do we know when this comes together

The scikit-learn/tensorflow moment will have arrived when a mid-sized product team, with no dedicated model infrastructure group, can take one bounded use case from examples to a production specialist model in weeks. The team should compare candidate base models against its own evaluations and adapt the best one. After deployment inside its required boundary, monitoring and later releases should follow an ordinary engineering process. When a better base model appears, the same data and evaluations should decide whether it makes sense to migrate. 

If specialist teams at large companies (think OpenAI, Anthropic etc) are still the only ones able to do this a few years from now, then I was wrong or at least early. If it has become routine, the most valuable model in many enterprises will be a small one that has learned exactly how that one organisation works.

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
