# Application playbooks: reusable prompt-system designs

## Classification and routing

**Contract:** define closed labels, a confidence/escalation rule, and output schema. Add contrast examples for labels commonly confused in production. Measure class-level precision/recall and unknown-rate, not only aggregate accuracy.

**Northstar example:** route `refund`, `shipping`, `account`, or `unknown`; use `unknown` when no intent is supported rather than forcing a label.

## Information extraction

**Contract:** name fields, source constraints, normalization rule, and unknown value. Use page/region citations for documents. Validate dates, currencies, IDs, and ranges deterministically.

**Example:** extract invoice ID and visible total; do not infer payment status from an invoice.

## Summarization and executive briefing

**Contract:** audience, purpose, required sections, word budget, evidence threshold, and omissions. Ask for decisions, risks, and open questions separately from summary. Evaluate faithfulness and coverage against source material.

## Grounded Q&A and RAG

**Contract:** answer only from approved evidence; attach source IDs; identify conflict; abstain when context is insufficient. Evaluate retrieval, evidence support, citation correctness, and abstention separately.

## Synthetic data and evaluation generation

Use a schema and explicit distribution targets (intent, difficulty, language, attack type). Label synthetic data as synthetic and inspect samples. Never let generated test cases replace real failure cases; use them to expand coverage.

## Image generation and editing

Specify subject, composition, style, constraints, text requirements, and prohibited content. For edits, name the invariant elements and only the requested delta. Evaluate images against an acceptance rubric; do not infer visual licensing or factual claims.

## Coding and review

Use specification-first prompts: repository inspection, smallest plan, implementation constraints, tests, execution feedback, and residual-risk report. Human approval remains required for migrations, credentials, dependency changes, and production deploys.

## References

- [Google prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [OpenAI structured outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [OpenAI evals](https://platform.openai.com/docs/guides/evals)
