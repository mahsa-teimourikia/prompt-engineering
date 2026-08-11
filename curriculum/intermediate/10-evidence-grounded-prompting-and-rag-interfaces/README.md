# 10 — Evidence-Grounded Prompting and RAG Interfaces

## Learning objectives

Design a generation interface that labels evidence, preserves provenance,
handles conflicting or stale sources, cites claims, and abstains when approved
evidence is absent.

## Scenario and mental model

Northstar answers refund-policy questions. Model-only answers can invent policy;
retrieved text can be malicious. Retrieval is data selection, not authority.

    authorize sources → retrieve/rank → label provenance → generate with claim rule
                      → validate citations → answer or abstain

## Lab, evaluation, and production

The [notebook](evidence_grounded_prompting_and_rag_interfaces.ipynb) compares a
model-only answer, all retrieved text, and selected authorized evidence.
[lab.py](lab.py) shows why a poisoned retrieved instruction cannot become an
approval. Measure evidence recall, citation support, abstention correctness,
source freshness, and unsupported-claim rate. Filter tenants and permissions
before retrieval; validate output citations outside the model.

## References

- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [OWASP prompt injection guidance](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html)
