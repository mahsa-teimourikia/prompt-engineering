# Practical lab evolution plan

## Purpose and decision

This plan is the source of truth for replacing the repository's templated
practical track with professional, notebook-first enterprise GenAI training.
The canonical destination is the 29-course tree under `curriculum/`; the 21
files under `notebooks/` are audited source material, not a second curriculum.

The rebuild will preserve useful explanations and deterministic execution, but
will replace shared pedagogy with topic-specific scenarios, implementations,
datasets, measurements, failures, debugging workflows, and production
decisions. Every practical lab must progress through:

`DESIGN → IMPLEMENT → EXPERIMENT → EVALUATE → DEBUG → COMPARE → HARDEN → PRODUCTIONIZE`

## Repository-wide audit

### Evidence collected

- All 21 legacy notebooks have exactly 20 cells: 16 Markdown and four code.
- The first three code cells are byte-for-byte identical in all 21 notebooks.
  They define the same `POLICIES → CaseBrief → retrieve() → build_case() →
  Trace` Northstar Support simulation, including hard-coded latency and cost.
- The only topic-specific executable content is normally the fourth code cell.
  Core provider integrations are commented pseudocode, not runnable adapters.
- The test suite enforces the old template (`21` notebooks, `18+` cells,
  Northstar text, Mermaid text) rather than practical quality or canonical
  course execution.
- `scripts/validate_notebooks.py` validates only `notebooks/`; none of the 29
  canonical notebooks is executed by `make notebooks`.
- The canonical tree contains the right 29 lesson folders, but depth is uneven:
  several advanced and enterprise notebooks contain only four or five cells,
  and many reusable `lab.py` files contain only two to six lines.
- The Hub has 29 valid routes, but summaries, outcomes, references, and focused
  checkpoints are generic generated text rather than course-specific training.
- Pydantic is the only practical engineering dependency beyond notebook/test
  tooling. There is no provider abstraction, dataset package, metrics/tracing
  layer, token/cost accounting, or visualization dependency.
- Reference-only material is still duplicated as executable-looking notebooks:
  technology review, technique catalog, application playbooks, resource
  library, and course coverage map.

### Retain, deepen, consolidate, repair, add

| Classification | Decision |
| --- | --- |
| Retain | Credential-free defaults, deterministic seeds, Pydantic contracts, safe failure paths, Mermaid concepts in chapters, existing topic explanations and authoritative links that remain accurate. |
| Deepen | Every canonical notebook: topic-specific datasets, measurable baseline, real instrumentation, multiple experiments, failure injection, debugging, re-evaluation, framework comparison where it changes a real decision, and production architecture. |
| Consolidate | Provider access, usage records, timing, token estimates, dataset loading, metric aggregation, bootstrap confidence intervals, tracing, and plotting into `src/prompt_course/`; keep the concept implementation visible in each notebook. |
| Repair | Notebook validation, tests, Hub metadata/checkpoints, README claims that all lessons are complete, hard-coded latency/cost, commented provider pseudocode, and canonical notebooks/labs that are placeholders. |
| Add | Synthetic datasets and slices, optional real-provider execution, measured results, diagnostic taxonomy, production upgrade tables, review questions, exercises, and advanced challenges. |

## Legacy notebook disposition

The table audits every notebook in `notebooks/`. “Replace” means its practical
role moves to the named canonical course; useful prose and references are
retained during that rewrite. Reference-only notebooks become Markdown under
`docs/reference/`, `docs/playbooks/`, or `docs/resources/` and leave the
required practical sequence.

| Lab | Current problem | Keep | Replace | Add | Scenario | Libraries | Evaluation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `01_instruction_contracts.ipynb` | Refund-only Northstar fixture; one contract object; no behavioral comparison. | Authority, allowed sources, forbidden actions, safe outcomes. | Canonical 02 with successive prompt-contract revisions. | 20+ clear, missing, conflicting, out-of-scope, and injected claims; optional live calls. | Insurance claims intake. | Pydantic, provider adapter, pandas, matplotlib. | Correctness, unsupported claims, clarification, schema validity by revision and slice. |
| `02_structured_outputs.ipynb` | Instantiates a known-valid model; never attempts or repairs generation failures. | Typed boundary and Pydantic validation. | Canonical 04 extraction pipeline. | Nested schema, enums, unions, dates, money, evidence IDs, malformed/semantic failures, provider-native comparison. | Enterprise claim/document extraction. | Pydantic, JSON Schema, provider adapter, pandas. | Parse success, schema validity, semantic field accuracy, repair rate. |
| `03_context_engineering.ipynb` | Selects one hard-coded policy from three strings; no ranking, budget, or context effects. | Authority/staleness distinction. | Canonical 08 context-selection lab. | 30+ mixed-authority items; everything, recency, authority, relevance, budget, summary, and JIT strategies. | Employee policy assistant. | scikit-learn, provider adapter, pandas, matplotlib. | Task success, unsupported/stale use, context precision, tokens, measured latency. |
| `04_rag_and_tools.ipynb` | Conflates retrieval and tools; a dictionary lambda cannot teach either interface. | Evidence provenance and narrow-interface principle. | Split into canonical 10 and 11. | Conflicting/stale/injected retrieval corpus; ambiguous tool catalog, schemas, errors, authorization boundary. | Compliance assistant; operations assistant. | scikit-learn retrieval, JSON Schema/Pydantic, optional framework adapter. | Groundedness/citation accuracy; tool choice/argument validity/unnecessary calls. |
| `05_multimodal_prompting.ipynb` | Uses a dictionary pretending to be an image; no visual asset or model input. | Observation-versus-inference and confidence fields. | Canonical 12 with synthetic assets. | Invoice image, table, chart, scan, OCR uncertainty, contradiction, evidence localization, optional live vision call. | Invoice discrepancy review. | Pillow, Pydantic, provider adapter, pandas, matplotlib. | Field accuracy, evidence localization, calibrated abstention, contradiction detection. |
| `06_prompt_security.ipynb` | Keyword matching on one injection; implies filtering is the defense. | Untrusted-data boundary and escalation. | Canonical 13 attack-and-defense range. | 30+ direct/retrieved/tool/exfiltration attacks; provenance, authorization, sandbox/allowlist controls. | Malicious enterprise tickets/documents. | Pydantic, provider adapter, pandas, pytest-style cases. | Attack success rate, safe-task success, control coverage by attack class. |
| `07_prompt_evaluation.ipynb` | Three cases and an asserted perfect score; no uncertainty, slices, judge, or release decision. | Identical-dataset candidate comparison and safe abstention. | Canonical 14; split judge material to canonical 15. | Development/validation/held-out/regression/adversarial partitions, deterministic and rubric graders, confidence intervals, release report. | Regulated policy assistant. | pandas, numpy, scipy/sklearn metrics, matplotlib; Promptfoo adapter/export. | Task success, per-slice metrics, CIs, latency/cost, regression gate. |
| `08_agentic_prompts.ipynb` | A two-iteration retrieval loop is labelled an agent; no real tools or trajectory evaluation. | Explicit maximum steps and bounded autonomy. | Canonical 18 workflow-versus-agent investigation. | Typed tools/state, retries, stop rules, workflow baseline, bounded agent, optional supervisor/specialist, injected tool failure. | Technical incident investigation. | Pydantic, provider adapter, optional LangGraph. | Outcome, trajectory validity, steps, retries, termination, latency and cost. |
| `09_promptops.ipynb` | Compares fabricated `Trace` numbers and a Boolean gate; no versioned artifact or release drill. | Release gate and rollback intent. | Canonical 22 and feed canonical 23–24. | Versioned behavior artifact, v1/v2 eval, manifest diff, canary, regression, rollback, generated release report. | Production GenAI release workflow. | Pydantic, YAML/JSON, Git subprocess read-only metadata, optional MLflow/Promptfoo export. | Gate outcome, regression budget, trace completeness, canary/rollback evidence. |
| `10_technology_review.ipynb` | Static score dictionary is not a meaningful executable experiment. | Selection criteria and technology comparison prose. | Move to `docs/reference/technology-landscape.md`; use comparisons inside relevant labs. | Architecture selection examples in canonical 28. | Enterprise platform selection. | None required in reference; structured ADR model in course 28. | Decision rationale/risk coverage, not notebook execution. |
| `11_reasoning_techniques.ipynb` | A fixed list of three steps does not exercise reasoning, planning, or verification. | Bounded decomposition and evidence verification. | Split into canonical 06 reasoning and 07 workflows. | Objective incident suite; direct, decomposed, planner/executor, verifier; one-prompt versus staged workflow. | Technical incident diagnosis; due-diligence research. | Provider adapter, Pydantic, pandas, optional LangGraph. | Task success, calls, tokens, latency/cost, failure localization. |
| `12_coding_agent_prompting.ipynb` | Prints a change request and plan; never inspects, edits, or tests code. | Scope, acceptance criteria, non-goals, targeted tests. | Canonical 19 using a real local repository fixture. | Retry/authorization/validation issue; inspect-plan-edit-test-debug-summary workflow. | Small Python service repository. | tempfile/pathlib/subprocess, pytest, provider adapter. | Tests passed, requirements met, files/diff size, unnecessary changes. |
| `13_cost_latency_engineering.ipynb` | Latency and cost are invented constants; no workload or quality trade-off. | Quality constraints and Pareto decision framing. | Canonical 21 measured workload. | 30–100 document cases; prune, examples, routing, caching strategies. | High-volume document processing. | `time.perf_counter`, token estimator, provider usage metadata, pandas, matplotlib. | Quality, measured latency distribution, tokens, estimated/actual cost, Pareto frontier. |
| `14_technique_catalog.ipynb` | Dictionary lookup is reference material, not a practical lab. | Failure-to-technique decision taxonomy. | Merge into canonical 05 chapter and canonical 28 ADR lab; move catalog to reference docs. | Multi-case technique selection. | Architecture review board. | Pydantic decision records, pandas. | Fit, rationale, excess-complexity and risk-control coverage. |
| `15_application_playbooks.ipynb` | Two static playbook entries; no experiment. | Reusable application-pattern descriptions. | Move to `docs/playbooks/`; use scenarios inside relevant labs. | Cross-industry design cases. | No notebook dependency. | Architecture review checklist in canonical 28, not runtime metrics. |
| `16_model_aware_guidance.ipynb` | Hard-coded model profiles and routing; no provider/model execution or measured data. | Portable behavior contract plus model-specific adaptation. | Canonical 20 and 27. | Same extraction/tool task across available adapters with fallback. | Multi-provider enterprise service. | OpenAI/Anthropic/Gemini optional SDK adapters, pandas, matplotlib. | Schema, instructions, tool choice, measured latency, usage and configured cost. |
| `17_resource_library.ipynb` | Filters two citations; no executable learning outcome. | Curated authoritative references. | Move to `docs/resources/` and topic-local references. | None—reference artifact. | None. | Link validity and source-quality review. |
| `18_llm_behavior_prompt_structure.ipynb` | Seeded random classification repeats the same output and is not model behavior. | Reproducibility warning and behavior-contract framing. | Canonical 01 controlled behavior lab. | Support triage with ambiguity, instruction order/position, sampling, and prompt variants. | Enterprise support intake. | Provider adapter, deterministic fixture, pandas, matplotlib. | Instruction adherence, output validity, variation and calibration across repeats. |
| `19_reliability_human_centred_ai.ipynb` | One forced escalation result; no trust/UX experiment or error-cost model. | Human approval for high-risk actions. | Canonical 26 and governance links to 25. | Risk-tiered administrative decisions with calibrated communication. | Healthcare administration using synthetic data. | Pydantic, pandas, sklearn metrics, matplotlib. | Selective accuracy, escalation burden, risk-weighted loss, calibration. |
| `20_course_coverage_map.ipynb` | Six hard-coded `True` flags falsely prove completeness. | Curriculum mapping intent. | Move to docs; generate coverage from repository validation. | None—maintainer report. | Path/nbformat validation. | Structural and executable quality gates generated from real files. |
| `21_evaluation_driven_prompt_optimization.ipynb` | Three hard-coded candidate scores; no data, candidate execution, slices, or overfit test. | Safety invariants and held-out winner selection. | Canonical 16; automatic optimization in canonical 17. | Policy router candidates changed one variable at a time. | Enterprise policy routing. | Provider adapter, pandas, matplotlib; optional DSPy in course 17. | Held-out and slice scores, regressions, safety invariant, optimization overfit gap. |

## Canonical lab depth priorities

| Priority | Courses | Reason |
| --- | --- | --- |
| P0 foundation | 01–04 | Courses 01–03 contain useful depth; 04 is still shallow. These establish shared contracts and practical conventions. |
| P0 core engineering | 06–14 | Most are 5–9-cell demonstrations and cover the central reasoning/context/tool/security/evaluation skill chain. |
| P0 advanced/production | 15–27 | Most are 4–5-cell placeholders with 2–4-line labs; they cannot support the advertised professional outcomes. |
| P1 selection/capstone | 05, 28–29 | Must integrate the completed primitives instead of becoming checklists or catalogs. |

## Shared infrastructure design

Create a small installable package without hiding the lesson's core mechanism:

```text
src/prompt_course/
├── providers/          # protocol, deterministic adapter, optional OpenAI/Anthropic/Gemini adapters
├── datasets.py         # typed fixtures, slices, deterministic splits
├── evaluation.py       # metric records, slice aggregation, confidence intervals
├── tracing.py          # visible structured events; never private chain-of-thought
├── token_usage.py      # measured/estimated usage with explicit provenance
├── pricing.py          # user-supplied/versioned prices; never invented billing
└── visualization.py    # reusable, accessible plotting helpers
data/
├── claims/
├── tickets/
├── policy/
├── evaluation/
├── security/
└── multimodal/
```

Provider adapters return a common structured response containing text, model,
provider, measured elapsed time, optional usage metadata, and whether the result
is deterministic. Core business policies, schemas, and evaluators remain
provider-neutral. Optional SDKs load lazily; no API key is stored or printed.

## Notebook contract

Every canonical practical notebook will be checked for the following semantic
sequence, adapted rather than copied mechanically:

1. Scenario, enterprise impact, experimental question, success criteria,
   constraints, non-goals, and safety boundaries.
2. Environment manifest: Python/dependencies, seed, offline/provider mode,
   expected runtime, and synthetic-data statement.
3. Architecture image or useful data visualization and a manual walkthrough.
4. Measured naive baseline on a multi-case dataset.
5. Failure inspection using the taxonomy `PROMPT / CONTEXT / EXAMPLE / MODEL /
   SCHEMA / RETRIEVAL / TOOL / WORKFLOW / EVALUATOR / SECURITY / RUNTIME`.
6. Incremental implementation of the topic primitive, with visible structured
   state and design explanations before code.
7. Multiple experiments changing meaningful variables; framework comparison
   only when it informs a real choice on the same task and dataset.
8. Quantitative re-evaluation, slice analysis, and interpretation of outputs.
9. Deliberate failure injection, diagnosis, mitigation, and regression test.
10. Production architecture, security/governance, reliability, observability,
    measured cost/latency/scalability, and explicit “when not to use it.”
11. Three to five review questions, two practical exercises, one advanced
    challenge, and a concise engineering decision.

## Validation redesign

- Discover canonical notebooks from `curriculum/*/*/*.ipynb`; legacy notebook
  count and Northstar text are not quality gates.
- Validate JSON, kernels, relative paths, imports, dataset/assets existence,
  deterministic seeds, credential-free mode, and clean top-to-bottom execution.
- Add unit tests for provider fallbacks, dataset splits/slices, metrics,
  confidence intervals, trace records, token/cost provenance, and plotting.
- Add semantic notebook checks for scenario, experimental question, baseline,
  measured evaluation, failure injection, diagnosis, production upgrade,
  exercises, and advanced challenge. These checks complement execution; they do
  not reward empty headings.
- Update Hub tests to require course-specific summaries, outcomes, references,
  checkpoints, and valid chapter/notebook/lab routes.
- Keep the full quiz and focused checkpoints synchronized with the same 29
  course IDs. Every checkpoint must test its course's actual engineering
  decision rather than the same generic release question.

## Phased execution and reporting

| Phase | Deliverable | Exit gate |
| --- | --- | --- |
| 1 — Audit | This plan, including all 21 dispositions and canonical depth findings. | Audit covers notebooks, docs, tests, validation, requirements, Hub, quiz, and canonical courses. |
| 2 — Infrastructure | Provider adapters, datasets, evaluation, tracing, usage/cost, visualization, tests. | Unit tests pass; deterministic fallback works without credentials. |
| 3 — Core beginner | Canonical 01–04 rebuilt; 05 integrates their selection trade-offs. | Notebooks execute; datasets, charts, failures, and checkpoints are topic-specific. |
| 4 — Reasoning/context | Canonical 06–13 rebuilt. | Workflow, context, RAG, tools, multimodal, and security experiments pass. |
| 5 — Advanced | Canonical 14–21 rebuilt. | Real eval partitions, judges, optimization, agents/coding fixture, model and Pareto comparisons work. |
| 6 — Production | Canonical 22–29 rebuilt; reference-only legacy notebooks retired. | Release, observability, governance, trust, portability, architecture, capstone gates work. |
| 7 — Validation | Execute all canonical notebooks; run tests/link/Hub/quiz checks; remove obsolete template track. | Clean credential-free run, no broken routes, and deployed Hub/quiz HTTP 200 after merge. |

## Phase 3 report — core beginner complete

- **Courses rebuilt:** canonical 01–05 now meet the
  `professional-lab-v1` notebook gate.
- **Measured scenarios:** request-packet behavior, instruction contracts,
  few-shot selection, typed interfaces, and system-technique selection.
- **Datasets:** 20 behavior cases, 20 contract cases, 24 training plus 24
  held-out few-shot tickets, 20 structured-output cases, and 24 architecture
  decisions.
- **Experiments:** controlled packet variants, seven contract revisions,
  seven example-selection policies, five output-interface strategies, and
  three technique selectors.
- **Failure coverage:** missing evidence, injection and authority boundaries,
  poisoned labels, parse/schema/semantic separation, and avoidable complexity.
- **Hub and quiz:** Courses 01–05 have topic-specific summaries, outcomes,
  references, and decision checkpoints; the remaining course registry and
  generic checkpoints stay intact during phased migration.
- **Credential policy:** every lab runs offline by default. Optional integration
  cells require each learner's own `OPENAI_API_KEY`, explicit provider opt-in,
  and never treat one live call as evaluation evidence.
- **Validation:** 32 tests pass; all 50 notebooks are structurally validated;
  five professional notebooks execute top-to-bottom without credentials.
- **Remaining work:** rebuild canonical 06–29, retire or convert legacy
  executable-looking reference notebooks according to their dispositions, and
  complete deployment/link validation after merge.

## Phase 2 report — infrastructure baseline

- **Notebooks changed:** none; shared foundations were completed before course
  rewrites as required by the phased plan.
- **Shared utilities created:** installable `prompt_course` package with typed
  provider requests/responses, deterministic and OpenAI Responses API adapters,
  stable dataset splits/JSONL loading, transparent evaluation and bootstrap
  intervals, structured tracing, token-component estimates, source-dated cost
  estimates, and accessible comparison plots.
- **Credential policy:** live OpenAI execution requires each learner's own
  `OPENAI_API_KEY` and explicit `PROMPT_COURSE_PROVIDER=openai`; tests and CI
  never use a key or make network calls. Keys and local environment files are
  ignored, and the README documents secure setup without printing the secret.
- **Frameworks used:** OpenAI Python SDK for optional live Responses API calls;
  Pydantic remains available for topic contracts; pandas, matplotlib, and
  scikit-learn are installed for the upcoming measured labs.
- **Measurement controls:** elapsed time uses `time.perf_counter`; provider
  token metadata is marked `provider`; offline counts are marked `estimated`;
  pricing requires an explicit HTTPS source and effective date.
- **Tests added:** provider fallback/selection, missing-key behavior, stable
  dataset splits, slice aggregation, evaluation, deterministic bootstrap,
  usage/cost provenance, component token estimates, and structured traces.
- **Validation at Phase 2 exit:** 12 tests passed, Python sources compiled, and
  legacy notebook JSON validation passed. See the Phase 3 report for current
  totals.
- **Weaknesses recorded at Phase 2 exit:** course rewrites, canonical notebook
  execution, course-specific Hub/checkpoints, and retirement of legacy
  templates remained; the first three are complete for Courses 01–05.

## Phase 1 report

- **Notebooks audited:** 21 legacy and 29 canonical notebooks.
- **Scenarios planned:** claims, ticket routing, document extraction, incident
  investigation, due diligence, policy assistance, conversations, compliance,
  operations, invoices, malicious content, regulated evaluation, coding,
  high-volume processing, healthcare administration, releases, and governance.
- **Shared utilities identified:** providers, datasets, evaluation, tracing,
  usage/tokens, pricing, and visualization.
- **Framework policy:** teach primitives first; compare at most two relevant
  abstractions on the same task; all provider/framework integrations optional.
- **Evaluation gap:** current practical notebooks use three cases or hard-coded
  values; no confidence intervals, real latency, usage provenance, or slices.
- **Visualization gap:** current notebooks contain conceptual Mermaid text but
  no experiment-result charts.
- **Failure gap:** most topic cells assert a happy path; security contains one
  keyword injection and no defense-in-depth comparison.
- **Execution finding:** legacy notebook JSON is validated, but canonical
  notebooks are not covered by `make notebooks`.
- **Tests passed before changes:** repository baseline was already green at the
  merge commit; Phase 2 will replace obsolete template assertions.
- **Remaining weakness:** all implementation phases remain; this audit does not
  declare any shallow canonical notebook complete.
