# 22 — PromptOps

## Learning Objectives
- **Treat Prompts as Code:** Integrate prompt engineering fully into traditional software engineering lifecycles.
- **Implement CI/CD for Prompts:** Build automated pipelines that block prompt deployments if regression tests fail.
- **Separate Prompts from Logic:** Decouple prompt definitions from application code to enable non-developer iteration.
- **Maintain Audit Trails:** Track exactly who changed a prompt, when, and what evaluation score justified the release.

## Core PromptOps Workflow

In the enterprise, prompt engineering is indistinguishable from software engineering. An individual developer cannot simply change a prompt in a production codebase and push it live based on a "vibe check."

PromptOps is the application of DevOps principles to AI. Prompts must be treated as versioned artifacts. When a prompt is updated, it must pass through a strict Continuous Integration (CI) pipeline. This pipeline automatically runs the new prompt against a frozen "Golden Dataset." If the accuracy drops, or if latency/cost limits are exceeded, the deployment is blocked. This ensures that a prompt optimized to fix one edge case doesn't silently break 100 others in production.

![PromptOps Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Hardcoding prompt strings directly into Python files and relying on manual PR reviews to catch errors.

**Current State of the Art:**
1. **Prompt Registries:** Organizations use external registries (e.g., **[PromptLayer](https://promptlayer.com/)**, **[Braintrust](https://www.braintrustdata.com/)**) to store, version, and serve prompts dynamically. Application code fetches the active prompt by an ID or tag (e.g., `get_prompt("support_router", version="production")`).
2. **Evaluation-Driven CI/CD:** SOTA pipelines use GitHub Actions/GitLab CI integrated with tools like **[DeepEval](https://docs.confident-ai.com/)** or **Promptfoo**. A PR containing a prompt change automatically triggers a regression suite, and the PR cannot be merged unless the test passes.
3. **Role-Based Access Control (RBAC):** Product Managers and Domain Experts can tweak and test prompts in a UI, but deploying those prompts requires passing the automated engineering gates.

## Lab and Production

### The Lab
The [notebook](22_promptops.ipynb) simulates a PromptOps CI/CD pipeline. It demonstrates extracting a hardcoded prompt into a standalone, versionable configuration payload. It then shows a simulated GitHub Action step that blocks a deployment when a proposed prompt candidate fails to beat the baseline score on a regression test.

### Production Best Practices
- **Never Hardcode Prompts:** Prompts belong in configuration files (JSON/YAML) or external CMS/Registries, never hardcoded as strings in core business logic.
- **Automated Rollbacks:** If a prompt causes a spike in production errors (measured via observability tools), the system must be able to automatically roll back to the previous known-good version without requiring a full code redeploy.
- **Audit Logging:** Every prompt execution in production must be tagged with the exact `prompt_version_id` so failures can be traced back to the specific commit that introduced them.
