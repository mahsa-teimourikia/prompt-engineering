# 03 — Constraints, Examples, and Few-Shot Learning

**Level:** Beginner · **Estimated time:** 60–90 min · **Prerequisites:** Courses 01–02 and Python collections

## Scenario

Northstar must route support messages to a small closed set of categories.
Direct instructions can leave boundary cases underspecified, so this lab
compares zero-shot, static, random, and similarity-selected examples. The
evaluation set has five labelled cases and the replay records intentionally
produce 3/5, 4/5, 3/5, and 5/5. Similarity is offline lexical-hash retrieval:
it is deterministic and useful for teaching the measurement loop, but it is
not semantic embedding behavior.

## Lab walkthrough

- Zero-shot renders no examples and asserts a recorded accuracy of 3/5.
- Static selection uses two fixed examples and asserts 4/5.
- Random selection uses `random.Random(case_id)` and asserts reproducible 3/5.
- Similarity selection calls `client.embed()`, prints `HASH_EMBEDDING_NOTICE`,
  and asserts 5/5 while labelling token counts as estimated.
- The leakage guard ensures `select_examples(k=2)` never returns the query
  itself when it is present in the bank.

## Exercises

1. Modify `EXAMPLE_BANK` with a new boundary example and watch the static
   `static_accuracy` numerator over the denominator of five.
2. Change the random case ID and watch `random_accuracy`; explain why the
   seed must remain deterministic.
3. Replace one similarity example and watch both `similarity_accuracy` and
   the estimated token metric.

## Checkpoint

1. Why prefer boundary examples to a large example collection? **They teach
   the decision boundary with less context cost and noise.**
2. What does the offline similarity notice mean? **Hash embeddings are
   lexical and deterministic, not semantic provider embeddings.**
3. What must example retrieval do before rendering a prompt? **Filter for
   relevance, permissions, tenant scope, freshness, and query leakage.**

## Learning Objectives
- **Shape Behavior with Examples:** Use Few-Shot learning to demonstrate desired outputs rather than relying solely on complex instructions.
- **Define Decision Boundaries:** Curate examples that explicitly map the edge cases and boundary lines of a task.
- **Include Negative Examples:** Provide examples of what *not* to do, or how to handle missing data safely.
- **Measure Example Impact:** Calculate the token cost vs. quality tradeoff of adding examples to a prompt.

## Core Concepts & Workflow

Even the most perfectly written Instruction Contract will sometimes fail on complex edge cases. When a direct instruction fails, the solution is not to write a longer, more complicated instruction. The solution is to *show*, not just tell.

This is "Few-Shot Learning." By providing a few examples of the exact Input and the desired Output within the prompt, you anchor the model's behavior. The goal is not volume; it is variance. You should select examples that define the *boundaries* of your logic—for instance, an example that barely qualifies for Category A, and an example that barely falls into Category B. 

![Mental Model Diagram](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Believing that writing a longer, more detailed instruction is the only way to fix an LLM mistake.

**Current State of the Art:**
1. **Dynamic Few-Shot Routing:** Instead of hard-coding the same 5 examples into every prompt, advanced systems use a vector database to dynamically retrieve the 5 examples that are most semantically similar to the user's current query.
2. **Automated Example Selection:** Frameworks like **[DSPy](https://github.com/stanfordnlp/dspy)** (specifically its BootstrapFewShot optimizers) automate the process of finding the best possible combination of examples from a training set to maximize evaluation scores.
3. **Agentic Workflows:** Multi-stage reasoning flows often use different few-shot examples for different stages (e.g., planning examples vs. execution examples).

*Note: While massive context windows (like Gemini 1.5 Pro) make blanket large few-shot blocks less strictly necessary, targeted negative and boundary examples remain critical for shaping specific behavioral nuances.*

## Lab and Production

### The Lab
The [notebook](03_constraints_examples_few_shot.ipynb) demonstrates fixing a boundary failure. It first establishes a baseline where instructions alone fail to categorize an edge case correctly. It then injects a single, targeted Few-Shot example mapping that edge case, proving how examples override instruction ambiguity.

### Production Best Practices
- **Curate, Don't Hoard:** 3 highly specific boundary examples are vastly superior to 20 random examples.
- **Include the 'Unknown':** Always include at least one example where the correct behavior is to decline the request or output a fallback state.
- **Tenant Filtering:** If selecting examples dynamically, production systems *must* apply tenant/permission filtering before retrieval to ensure data from Customer A is never used as a few-shot example in a prompt for Customer B.

## Further reading

Read an entry in a technique catalog by asking what failure it addresses, what
it changes, what it costs, and what evidence would justify keeping it. Direct
instructions, role framing, one-shot and few-shot examples, delimiters,
templates, schemas, constrained decoding, and output validation solve
different problems. Examples are valuable for labels, format, tone, missing
data, and contrasts; they are not a substitute for validation. Similarity
selection can reduce irrelevant context, but a production retriever needs
permission and tenant filters before examples enter a prompt. A static bank is
easy to audit; random selection tests robustness but should never use
process-randomized hashes; dynamic retrieval needs freshness and provenance.
Measure quality and estimated context cost together. If a direct contract
already passes, adding examples may increase noise without improving the
metric.

References: [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165),
[DSPy](https://github.com/stanfordnlp/dspy), and
[JSON Schema](https://json-schema.org/specification).
