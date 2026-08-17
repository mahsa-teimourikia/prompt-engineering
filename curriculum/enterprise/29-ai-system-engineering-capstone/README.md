# 29 — AI System Engineering Capstone

## Learning Objectives
- **Synthesize Curriculum Concepts:** Combine schemas, RAG, tool calling, and evaluation into a single, production-grade Compound AI System.
- **Implement the "Northstar" Pattern:** Build an enterprise-grade support routing and resolution system from scratch.
- **Enforce Safety and Governance:** Integrate strict PII redaction and outbound toxicity checks into the core workflow.
- **Deploy with Confidence:** Ensure the final system is observable, measurable, and highly resilient to failure.

## Core Concepts & Workflow

This capstone is the culmination of the entire Prompt Engineering curriculum. It moves beyond isolated techniques and requires you to architect a complete, end-to-end "Compound AI System."

You will build "Project Northstar," an enterprise support copilot. It must safely intercept untrusted user input, classify the intent, redact sensitive information, route the query to the correct specialized agent, retrieve relevant policy documents (RAG), execute authorized database queries (Tool Calling), and output a structured response that adheres to strict business logic—all while being monitored by an automated evaluation suite.

![Capstone Architecture Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Building a prototype in a Jupyter notebook that works for one specific "happy path" example.

**Current State of the Art:**
1. **Production-Grade Compound Systems:** Real-world AI engineering utilizes frameworks like **[LangGraph](https://langchain-ai.github.io/langgraph/)** to orchestrate the exact type of complex, multi-stage state machine built in this capstone.
2. **Evaluation-First Development:** In SOTA enterprise environments, you write the evaluation suite (using **Promptfoo**, **DeepEval**, or **Ragas**) *before* you write the complex prompt pipelines, ensuring every iteration is mathematically grounded.
3. **Comprehensive Observability:** The final system integrates with tracing platforms like **LangSmith** or **Phoenix by Arize** to ensure that when a complex multi-agent flow fails in production, the root cause can be isolated immediately.

## Lab and Production

### The Capstone Implementation
The `curriculum/Capstone/` directory contains the multi-milestone notebooks required to build this system. You will start with the foundational router, add RAG capabilities, integrate secure tool calling, and finally wrap the entire system in a rigid evaluation and governance harness. 

### Production Best Practices (Final Review)
- **Prompt Engineering is Software Engineering:** Treat your prompts as code. Version them, test them, and deploy them through CI/CD.
- **Trust Calibration:** Ensure your users understand the limitations of the system you built. Do not hide uncertainty behind confident UI design.
- **Defense in Depth:** Assume the LLM will be compromised. Build deterministic walls around it to protect your data, your systems, and your users.
