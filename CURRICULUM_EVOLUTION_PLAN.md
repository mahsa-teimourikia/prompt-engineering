# Curriculum evolution plan

## Decision

This repository will evolve from a collection of prompt-engineering topics into
a sequenced **Prompt Engineering → Context Engineering → AI System
Engineering** curriculum. Prompt engineering remains foundational: learners
first design a measurable task contract, then deliberately compose context,
tools, workflows, evaluations, and operating controls around it.

This is a migration plan, not a claim that all 29 target lessons already exist.
The current 21 notebooks and their credential-free Northstar fixtures are
valuable material to preserve. The numbered sequence below is the source of
truth for the migration; it prevents reference pages from being presented as
skill lessons and prevents shallow placeholder notebooks from being added.

## Audit findings

| Current material | Classification | Audit finding and disposition |
| --- | --- | --- |
| `01-instruction-contracts` | EXPAND | Strong behavioral-interface, authority, constraint, and adversarial-testing foundation. Retain; add the requested ambiguity, conflict, missing-evidence, and typed-result experiments. |
| `02-structured-outputs` | SPLIT | Strong schema, validation, and safe-failure material. Keep as target 04; extract examples/few-shot decision boundaries into target 03. |
| `03-context-engineering` | EXPAND | Strong selection, authorization, compression, and memory material. Keep as target 08; create a distinct long-context/conversation lesson. |
| `04-rag-tools` | SPLIT | Grounding and narrow-tool principles are strong but teach two different interfaces. Split into targets 10 and 11. |
| `05-multimodal` | EXPAND | Preserve document/evidence workflow; add contradiction, OCR-uncertainty, and observation-versus-inference experiments. |
| `06-prompt-security` | EXPAND | Preserve defense-in-depth framing; add repeatable vulnerable-prompt → deterministic-boundary retests. |
| `07-evaluation` | EXPAND | Preserve as the canonical evaluation foundation; create a distinct judge/human evaluation course. |
| `08-agentic-prompts` | EXPAND | Preserve contracts and bounded autonomy; add trajectory evaluation, handoffs, and explicit runtime-policy separation. |
| `09-promptops` | SPLIT | Preserve as target 22 and keep the behavior artifact framing; extract observability and release engineering into targets 23–24. |
| `10-technology-review` | MOVE TO REFERENCE | Useful selection guidance, not a standalone competency lesson. Move during the file migration to `docs/reference/technology-landscape.md`. |
| `11-reasoning-techniques` | SPLIT | Preserve bounded decomposition and verification; separate workflow orchestration into target 07. Do not teach hidden chain-of-thought. |
| `12-coding-agent-prompting` | EXPAND | Preserve; replace abstract-only tasks with a real local-repository change and review loop. |
| `13-cost-latency-engineering` | EXPAND | Preserve; add cache/context-reuse accounting and quality-cost-latency Pareto experiments. |
| `14-technique-catalog` | MERGE | Use its curated content to build target 05. Keep the full catalog as reference material rather than a required notebook. |
| `15-application-playbooks` | MOVE TO REFERENCE | Preserve as `docs/playbooks/` material; it supports application design but is not a canonical sequential lesson. |
| `16-model-aware-guidance` | EXPAND | Preserve and recast as target 20; target 27 adds multi-provider portability, adapters, and migration tests. |
| `17-resource-library` | MOVE TO REFERENCE | Preserve as `docs/resources/`; remove it from required lesson progression. |
| `18-llm-behavior-and-prompt-structure` | MOVE | Promote to target 01. Its notebook needs controlled sampling, order, position, ambiguity, and example experiments. |
| `19-reliability-and-human-centred-ai` | MOVE | Preserve and deepen as target 26 with trust-calibration experiments. |
| `20-course-coverage-map` | MOVE TO REFERENCE | Replace with this plan as the migration source of truth; retain a concise learner-facing map in `docs/curriculum-map.md`. |
| `21-evaluation-driven-prompt-optimization` | EXPAND | Preserve as target 16; add one-variable change discipline, slice analysis, and regression plots. |
| Hub, quiz, tests, notebook validation | EXPAND | Hub correctly provides Learn/Notebook/Checkpoint flow and persists progress. Rework its registry only as each target lesson becomes a complete, tested course; retain quiz coverage while migrating. |
| Duplicate untracked `docs/* 2.md` files | DEPRECATE | Do not link or overwrite them. Resolve deliberately in a cleanup commit after comparing any user-authored differences. |

### Implementation baseline (audited 2026-08-10)

- The repository contains 21 published Markdown chapters, 21 notebooks, a
  static Learning Hub, a full 21-question quiz, notebook validation, and Hub
  tests. The current implementation is coherent and credential-free; preserve
  those strengths during migration.
- Each current notebook has the same 20-cell shape (16 Markdown and four code
  cells), the same offline Northstar simulator, and a Mermaid diagram. This is
  a dependable execution baseline, but it is not yet enough subject-specific
  experimentation for the target curriculum. Rebuild migrated notebooks around
  one topic-specific scenario, baseline, instrumentation, multiple experiments,
  failure injection, and measured comparison—not by appending cells to the
  common template.
- Current notebook validation deliberately rejects `labs/` imports and the
  existing tests require exactly 21 Hub lessons/notebooks. Phase B must replace
  those temporary migration constraints when the first canonical
  `curriculum/<level>/<number-topic>/README.md`, notebook, and `lab.py` lesson
  is introduced; otherwise the repository would continue to validate the old
  shape rather than the target learning product.
- The Hub already has useful level filters, selected lesson views, checkpoints,
  and local progress persistence. Its registry currently mixes canonical topics
  with reference material; change it atomically with each completed course and
  its quiz/checkpoint rather than publishing an incomplete 29-item catalogue.

## Target curriculum

| Target Course | Current Material | Action | Level | Scenario | Main Experiment | Main Technology | Evaluation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01. LLM Behavior and Prompt Anatomy | `18` | MOVE + EXPAND | Beginner | Support request triage | temperature, order, position, ambiguity | credential-free simulator | variation, validity, instruction adherence |
| 02. Instruction Contracts | `01` | EXPAND | Beginner | Support copilot | vague → evidence → constraints → typed result | Pydantic-style contract | contract/adversarial tests |
| 03. Constraints, Examples, and Few-Shot Learning | portions of `01`, `02`, `14` | NEW + MERGE | Beginner | Claims case routing | zero/one/few-shot, diversity, order | deterministic fixtures | accuracy and token cost |
| 04. Structured Outputs and Typed Interfaces | `02` | EXPAND | Beginner | Claims/case processing | prompt-only JSON vs schema constraint | JSON Schema, Pydantic | syntax, semantic validity, repair rate |
| 05. Prompt Patterns and Technique Selection | `14` | MERGE + EXPAND | Beginner | Support task selection | smallest viable technique per failure | technique decision matrix | success, cost, maturity fit |
| 06. Reasoning-Oriented Prompting | `11` | EXPAND | Intermediate | Technical incident analysis | direct vs plan/verifier | structured plans and verifiers | success, calls, latency, tokens |
| 07. Task Decomposition and Workflow Prompting | portions of `11`, `08` | NEW + SPLIT | Intermediate | Document-analysis workflow | one prompt vs sequential/parallel/evaluator loop | typed stage contracts | quality, cost, debuggability |
| 08. Context Engineering | `03` | EXPAND | Intermediate | Enterprise knowledge assistant | full vs selected/summarized/JIT context | context packet builder | grounded quality, token and latency |
| 09. Conversation and Long-Context Engineering | portions of `03` | NEW | Intermediate | Customer success assistant | history vs window/summary/history retrieval | conversation-state policy | retained facts and cost |
| 10. Evidence-Grounded Prompting and RAG Interfaces | RAG portion of `04` | SPLIT + EXPAND | Intermediate | Policy assistant | model-only vs supplied/retrieved evidence | provenance-labelled evidence | citation support and abstention |
| 11. Tool Calling and Tool Interface Design | tool portion of `04` | SPLIT + EXPAND | Intermediate | Operations assistant | weak/overlapping vs narrow tool schemas | JSON Schema tool contracts | tool-selection and argument validity |
| 12. Multimodal Prompt Engineering | `05` | EXPAND | Intermediate | Document review | text/visual contradiction and OCR uncertainty | typed multimodal extraction | observation accuracy and calibrated uncertainty |
| 13. Prompt Security and Untrusted Content | `06` | EXPAND | Intermediate | Malicious email/document | vulnerable prompt vs isolated deterministic controls | trust-boundary policy | attack success and control coverage |
| 14. Prompt Evaluation | `07` | EXPAND | Advanced | Support/policy system | baseline vs candidate on identical cases | experiment harness | deterministic metrics, slices, release gates |
| 15. LLM-as-a-Judge and Human Evaluation | portions of `07` | NEW + SPLIT | Advanced | Human-labelled support set | absolute, pairwise, rubric, ensemble judges | judge adapters | agreement, bias, human override rate |
| 16. Evaluation-Driven Prompt Optimization | `21` | EXPAND | Advanced | Policy router | one-variable candidate changes | regression harness | held-out quality and regressions |
| 17. Automatic Prompt Optimization and DSPy | `10`, `21` references | NEW | Advanced | Classification contract | manual vs optimized candidate | DSPy or equivalent, optional adapter | held-out score, cost, leakage checks |
| 18. Agent and Multi-Agent Prompt Contracts | `08` | EXPAND | Advanced | Incident-response agent | single agent vs supervisor/specialist | typed state and bounded tools | trajectory, stop, handoff quality |
| 19. Prompting for Coding Agents | `12` | EXPAND | Advanced | Local repository task | vague request vs engineering contract | Git/test workflow | tests, diff scope, completion evidence |
| 20. Model-Aware Prompt Engineering | `16` | MOVE + EXPAND | Advanced | Provider-neutral extraction | model-class adaptation | provider adapters | contract adherence by model |
| 21. Cost, Latency, and Token Engineering | `13` | EXPAND | Advanced | Production support service | pruning, caching, routing | token/cost estimator | Pareto frontier and quality gates |
| 22. PromptOps | `09` | EXPAND | Production | Production AI service | behavior artifact release gate | manifests and eval suite | promotion/rollback readiness |
| 23. Prompt Observability and Failure Diagnosis | portions of `09` | NEW + SPLIT | Production | Deliberate behavior regression | trace before/after release | OpenTelemetry-compatible traces | diagnosis accuracy and time-to-isolate |
| 24. Prompt Versioning, Experimentation, and Release Engineering | portions of `09` | NEW + SPLIT | Production | Candidate release | shadow/canary/rollback | Git manifests and feature flags | gated promotion and rollback drill |
| 25. Prompt Governance and Responsible AI | `19`, `17` references | NEW | Production | Enterprise AI portfolio | inventory/risk review | governance inventory | ownership, review and audit coverage |
| 26. Human-Centred AI and Trust Calibration | `19` | MOVE + EXPAND | Production | High-risk support decision | unsupported confidence vs calibrated escalation | risk-tiered UX policy | user-facing reliability and escalation quality |
| 27. Prompt Portability and Multi-Model Systems | `16`, `13` | NEW + MERGE | Production | Multi-provider service | portable contract vs overrides/fallback | adapters and regression suite | quality, cost, latency, schema validity |
| 28. Prompt Architecture Patterns and System Selection | `14`, `15`, `20` references | NEW + MERGE | Production | Fifteen system-design cases | prompt/workflow/RAG/tool/agent selection | architecture decision record | rationale, risk and complexity fit |
| 29. AI System Engineering Capstone | all core modules | NEW | Production | Cross-functional enterprise assistant | baseline → hardened release candidate | full behavior artifact | release gate, ADR, rollout/rollback plan |

## Migration order and definition of done

1. **Phase A — audit and navigation:** complete. This plan, the root roadmap, and the Hub’s curriculum status communicate the target sequence without pretending planned lessons exist.
2. **Phase B — beginner:** in progress. Courses 01–03 now live in canonical folders with standalone READMEs, credential-free notebooks, `lab.py`, and Hub entries. Build courses 04–05 to the same standard before renumbering the full beginner track.
3. **Phase C — intermediate:** build/split courses 06–13, including the missing conversation and tool-interface courses.
4. **Phase D — advanced:** build/split courses 14–21, putting evaluation before optimization and agents.
5. **Phase E — production:** build/split courses 22–29 and migrate supporting documents to `docs/reference/`, `docs/playbooks/`, and `docs/resources/` with redirects/links preserved.

A target lesson is complete only when its README and notebook teach one coherent
scenario through baseline, implementation, experiments, evaluation, failure
injection, mitigation, and production upgrade; its default execution is
credential-free; its checkpoint and Hub registry work; and the repository
validation passes. References must use primary research, standards, or official
documentation for fast-changing claims. No course will require private
chain-of-thought or treat prompt text as an authorization boundary.
