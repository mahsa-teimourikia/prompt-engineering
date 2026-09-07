# Prompt Engineering Learning Roadmap

The repository revision is organized into three phases. Each phase makes the
next layer of learning evidence easier to run and review.

## Phase 1 — Structure and hygiene — complete

- Consolidate the Northstar capstone milestones under course 29.
- Repair internal links and add curriculum navigation.
- Add contributor scaffolding, repository policy, and issue/PR templates.
- Validate curriculum structure, Hub paths, quiz sources, and notebook artifacts.
- Add changed-notebook CI without rewriting provider-dependent notebook content.

## Phase 2 — Shared offline runtime — complete

- Add a deterministic fixture and replay runtime for credential-free execution.
- Keep live Gemini access optional and explicit when `GEMINI_API_KEY` is set.
- Add shared schema, evidence, trust-boundary, and metric invariants.

## Phase 3 — Per-level content — complete

- Beginner courses 01–05 use the shared replay runtime, course-local fixtures,
  deterministic notebook assertions, and focused tests.
- Intermediate courses 06–13 now use fixture-backed labs, replayed responses,
  executable notebooks, and integrated legacy documentation.
- Advanced and enterprise content follow in the next content milestones.
