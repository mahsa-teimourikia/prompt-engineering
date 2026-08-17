# 24 — Prompt Versioning, Experimentation, and Release Engineering

## Learning Objectives
- **Execute Shadow Deployments:** Test new prompts against live production traffic without showing the results to the user.
- **Run A/B Tests:** Statistically compare two prompt versions in production to measure actual business impact.
- **Manage Phased Rollouts:** Gradually shift traffic to a new prompt version to monitor for edge-case regressions.
- **Implement Hot-Swapping:** Change the active prompt version in production with zero downtime or code redeploys.

## Core Concepts & Workflow

Passing an offline regression suite is a requirement for deployment, but it is not a guarantee of production success. Users will interact with your system in ways your Golden Dataset never anticipated. 

Enterprise release engineering minimizes this risk through phased deployments. Before a major prompt change goes live to 100% of users, it should be **Shadow Deployed** (the application executes both the old and new prompt, returns the old result to the user, but logs both for comparison) or **A/B Tested** (routing 10% of users to the new prompt and comparing business metrics like task completion rate). 

![Release Engineering Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Merging a PR and immediately pushing the new prompt to 100% of production traffic, hoping nothing breaks.

**Current State of the Art:**
1. **Feature Flagging for Prompts:** Enterprises use tools like **[LaunchDarkly](https://launchdarkly.com/)**, **Statsig**, or native features in LLM gateways (like **Braintrust** or **PromptLayer**) to decouple prompt deployment from code deployment. A new prompt can be turned on for 5% of users via a toggle.
2. **Shadow Traffic Routing:** SOTA API gateways (e.g., **Cloudflare AI Gateway** or Envoy proxies) can duplicate inbound requests at the network layer, sending the copy to a new model or prompt version asynchronously to test scale and accuracy under real-world load.
3. **Automated Canary Analysis:** Systems automatically monitor the error rates and token costs of the new prompt during a phased rollout. If anomalies are detected, the system automatically triggers a rollback to the stable version.

## Lab and Production

### The Lab
The [notebook](24_prompt_versioning_experimentation_and_release_engineering.ipynb) simulates a shadow deployment pipeline. It takes a stream of live requests, routes them to both a stable `v1` prompt and an experimental `v2` prompt, and logs the variance in outputs and token costs without exposing the `v2` results to the end-user.

### Production Best Practices
- **Decouple Deployments:** Never require a full Kubernetes or microservice restart just to change a prompt string or tweak a temperature setting. Fetch these configurations dynamically.
- **Measure Business Metrics, Not Just LLM Metrics:** An A/B test shouldn't just measure if the LLM output was "better written." It must measure if the new prompt increased the actual business KPI (e.g., did more users successfully complete their purchase?).
- **Beware State Conflicts:** If your new prompt outputs a completely different JSON schema than the old prompt, your downstream application code must be version-aware to handle both formats during an A/B test.
