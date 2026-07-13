---
title: How chain-of-thought reasoning works in LLMs
date: 2026-07-13
series: AI
description: A visual explanation of how reasoning tokens help an LLM work through a problem and why they do not reveal everything happening inside the model.
---

When an AI product says a model is *thinking*, I instinctively imagine an inner voice working through the problem and then reporting the answer.

That picture is helpful, but not quite right.

I wanted to understand what actually happens between a prompt and an answer. We will begin with ordinary token generation, watch a chain of thought form, and then look at why the written reasoning is not the same as seeing inside the model.

## One token at a time

Suppose we ask:

> A box holds 24 pencils. How many pencils are in 17 boxes?

The model first breaks this text into **tokens**: words, word fragments, punctuation, and numbers. Those tokens pass through a transformer, the neural network behind most modern LLMs.

Inside the transformer, layers of numerical computation connect relevant parts of the prompt. The temporary numbers produced during this work are called **activations**. They are part of the internal computation, not a hidden English paragraph.

The model then produces probabilities for the next token:

```text
"408"   18%
"We"    15%
"The"   11%
...
```

One token is selected and appended to the context. The model processes the enlarged context and predicts again. This repeats until the answer is complete.

That loop is called **autoregressive generation**: previous output becomes input for the next prediction.

## Give the model a scratchpad

For an easy question, the model might jump directly to `408`. A difficult question benefits from intermediate work:

```text
10 boxes contain 240 pencils.
7 boxes contain 168 pencils.
240 + 168 = 408.
```

This generated intermediate text is called a **chain of thought**.

The scratchpad analogy is the cleanest explanation I found. When the model writes `240`, that value becomes part of its context. Later tokens can attend to it. The model no longer has to keep every partial result only inside temporary activations.

Use **Next** to follow one run, or **Watch** to play the complete loop.

[INTERACTIVE: chain-of-thought-loop]

The extra tokens help in a few connected ways:

- They give the model more sequential computation before the final answer.
- They preserve intermediate results in the context.
- Each useful step moves later predictions towards a useful region.
- A reasoning-trained model can reconsider an earlier step and try another path.

But extra tokens are not automatically good reasoning. A wrong intermediate step also becomes context and can pull everything after it in the wrong direction.

## How reasoning models learn this

A normal LLM and a reasoning model both predict tokens. A reasoning model does not have a special `reason()` function.

Instead, post-training rewards sequences that lead to correct or useful outcomes. Across many examples, the model learns patterns such as breaking a task apart, checking a calculation, comparing alternatives, or backing up after finding a contradiction.

At inference time, it can spend more tokens exploring before producing the final response. More reasoning tokens mean more computation, which is why difficult questions can take longer and cost more.

The important idea is simple:

> Each generated reasoning token becomes new working context for the tokens that follow.

## The scratchpad is not the mind

This is where the phrase *chain of thought* becomes dangerous. It makes three different things sound like one:

- **Internal computation:** activations inside the transformer.
- **Chain of thought:** generated intermediate tokens used while solving the task.
- **Final explanation:** the polished response shown to us.

The chain participates in the computation, but it does not have to record every influence on the answer.

Researchers test this by slipping a subtle hint into a question. The hint may change the model's answer, while its reasoning produces a clean justification that never admits using the hint. This is known as the **faithfulness problem**.

A readable chain can therefore be useful, incomplete, mistaken, or reconstructed after the fact. Fluency does not prove that we are seeing the true cause of the result.

That was the part I was missing. The scratchpad is real work, but it is not a debugger attached to the model's mind.

## What should we trust?

Chain of thought can improve answers and expose obvious mistakes. It can also help another model monitor an agent's behaviour. We should treat it as a clue, not proof.

For important work, stronger evidence comes from outside the narration:

- Execute the calculation independently.
- Check whether cited sources support the claims.
- Run the generated code and its tests.
- Verify important intermediate results.
- See whether irrelevant hints change the answer.

So when a product says a model is *thinking*, I now read it as a convenient interface label. What we may be watching is generated intermediate work: tokens that give the model a scratchpad and more computation before answering.

Sometimes that scratchpad carries the solution. Sometimes it carries a convincing story. Verification is how we tell the difference.

## References

- [1] Wei et al., [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)
- [2] Turpin et al., [Language Models Don't Always Say What They Think](https://arxiv.org/abs/2305.04388)
- [3] Anthropic, [Measuring Faithfulness in Chain-of-Thought Reasoning](https://www.anthropic.com/research/measuring-faithfulness-in-chain-of-thought-reasoning)
- [4] Anthropic, [Reasoning Models Don't Always Say What They Think](https://www.anthropic.com/research/reasoning-models-dont-say-think)
- [5] OpenAI, [Evaluating Chain-of-Thought Monitorability](https://openai.com/index/evaluating-chain-of-thought-monitorability/)
- [6] Quanta Magazine, [How Chain-of-Thought Reasoning Helps Neural Networks Compute](https://www.quantamagazine.org/how-chain-of-thought-reasoning-helps-neural-networks-compute-20240321/)
