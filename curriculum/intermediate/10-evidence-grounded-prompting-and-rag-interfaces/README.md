# 10 — Evidence-Grounded Prompting and RAG Interfaces

## Learning objectives

Design a generation interface that labels evidence, preserves provenance,
handles conflicting or stale sources, cites claims, and abstains when approved
evidence is absent.

## Scenario and mental model

Northstar answers refund-policy questions. Model-only answers can invent policy;
retrieved text can be malicious. Retrieval is data selection, not authority.

![Mental Model Diagram](./diagram-1.svg)

## Lab, evaluation, and production

The [notebook](10_evidence_grounded_prompting_and_rag_interfaces.ipynb) demonstrates
the danger of ungrounded generation (hallucination) and contrasts it with two solutions:
classic Manual Grounding (pasting retrieved text into the prompt) and Managed Grounding
using native API tools (like Google Search Grounding) which natively provide citations.

## Technology landscape and state of the art

**Foundational:** Retrieval-Augmented Generation (RAG) is the process of retrieving relevant data from an external source and providing it to the LLM to ground its answers in factual evidence.

**Current State of the Art:**
1. **Managed RAG Endpoints:** The industry is moving away from bespoke DIY vector database pipelines (using Langchain/Chroma) towards Managed RAG services (like Vertex AI Search or native API Grounding). These managed services handle document parsing, chunking, embedding, and hybrid retrieval automatically.
2. **Native Citations:** In the past, developers had to write complex prompts to force the LLM to cite its sources. Modern APIs now return structured citation metadata alongside the generated text, ensuring every claim is backed by a verifiable source.

## Evaluation and production

Measure evidence recall, citation support, abstention correctness, source freshness, and unsupported-claim rate. Filter tenants and permissions before retrieval; validate output citations outside the model.

## References

- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [OWASP prompt injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
