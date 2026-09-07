# Contributing to Prompt Engineering Learning

Thank you for improving the curriculum, runnable notebooks, Hub, quiz, or
supporting guidance.

## What belongs here

- Clear explanations and experiments about prompt and AI system engineering.
- Focused corrections that help a technical reader explain, test, evaluate, or
  operate a behavior contract.
- Synthetic, deterministic examples that make trade-offs observable.
- Direct links and concise explanations of why each source belongs here.

## Submission rules

1. Search the README and curriculum before adding material.
2. Place content in the narrowest relevant course or resource section.
3. Prefer primary sources, official documentation, and maintained projects.
4. Do not include credentials, private data, realistic secrets, or ephemeral
   vendor limits.
5. Keep pull requests focused and preserve existing useful material.

## Develop from main

Create a focused branch from the latest `main`. Inspect adjacent lessons,
examples, tests, and navigation before editing. Do not commit virtual
environments, credentials, private data, or generated artifacts.

## Course expectations

A lesson README should stand on its own as a technical chapter. Contributions
should:

- state the behavior contract and evidence boundary;
- distinguish model behavior from application enforcement;
- use synthetic, deterministic data;
- explain failure modes and evaluation; and
- preserve stable headings, source links, and curriculum navigation.

## AI-assisted contributions

AI tools may assist with research, drafting, implementation, and review, but
contributors remain responsible for the artifact. Verify claims against
authoritative sources, inspect generated code, run the actual checks, validate
links, and ensure no secrets or unsafe examples were introduced.

## Validate the change

| Change | Required validation |
| --- | --- |
| Python examples or tests | `make test` |
| Internal curriculum links | `make links` |
| Changed notebooks | `make notebooks-changed` |
| Curriculum structure | `make curriculum-test` |
| Python syntax | `python -m compileall -q curriculum tests` |

Document exact checks and results in the pull request.

## Recording replays for a notebook

Notebooks should use the shared Northstar runtime and remain replayable without
credentials. Run them with `NORTHSTAR_MODE=replay` by default. When a live
response is needed, set `GEMINI_API_KEY`, use `NORTHSTAR_MODE=record`, and
write only synthetic requests and responses to the notebook's replay fixture.
Never commit credentials, private data, or realistic customer identifiers.

## Pull request review

Keep unrelated changes out of the diff. Link primary sources and explain any
judgment calls about curriculum structure, execution, or provider behavior.

By contributing, you agree that your contribution will be licensed under this
repository's MIT License.
