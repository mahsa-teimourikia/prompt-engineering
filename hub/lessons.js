const course = (id, level, step, slug, title, details = {}) => ({
  id,
  level,
  step,
  title,
  summary: "Canonical Course " + step + ": " + title + ".",
  outcome: "Read the chapter, run the credential-free notebook, inspect the reusable lab, then validate your understanding.",
  material: "curriculum/" + level.toLowerCase() + "/" + String(step).padStart(2, "0") + "-" + slug + "/README.md",
  notebook: "curriculum/" + level.toLowerCase() + "/" + String(step).padStart(2, "0") + "-" + slug + "/" + slug.replaceAll("-", "_") + ".ipynb",
  lab: "curriculum/" + level.toLowerCase() + "/" + String(step).padStart(2, "0") + "-" + slug + "/lab.py",
  refs: [],
  ...details,
});

export const lessons = [
  course("behavior", "Beginner", 1, "llm-behavior-and-prompt-anatomy", "LLM Behavior and Prompt Anatomy"),
  course("contracts", "Beginner", 2, "instruction-contracts", "Instruction Contracts", {
    summary: "Evolve an insurance intake request into a measurable behavioral contract across seven revisions.",
    outcome: "Measure how objective, evidence, constraints, examples, typed output, and safe failure change behavior on 20 sliced cases.",
    refs: [
      "https://developers.openai.com/api/docs/guides/text",
      "https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html",
      "https://arxiv.org/abs/2406.06608",
    ],
  }),
  course("examples", "Beginner", 3, "constraints-examples-and-few-shot-learning", "Constraints, Examples, and Few-Shot Learning"),
  course("structured", "Beginner", 4, "structured-outputs-and-typed-interfaces", "Structured Outputs and Typed Interfaces", {
    summary: "Extract typed insurance case records and prove why valid JSON is not necessarily correct.",
    outcome: "Compare five interface strategies on 20 sliced cases, diagnose parse/schema/semantic failures, and make a defensible release decision.",
    refs: [
      "https://json-schema.org/specification",
      "https://docs.pydantic.dev/latest/concepts/models/",
      "https://developers.openai.com/api/docs/guides/structured-outputs",
    ],
  }),
  course("patterns", "Beginner", 5, "prompt-patterns-and-technique-selection", "Prompt Patterns and Technique Selection"),
  course("reasoning", "Intermediate", 6, "reasoning-oriented-prompting", "Reasoning-Oriented Prompting"),
  course("workflow", "Intermediate", 7, "task-decomposition-and-workflow-prompting", "Task Decomposition and Workflow Prompting"),
  course("context", "Intermediate", 8, "context-engineering", "Context Engineering"),
  course("conversation", "Intermediate", 9, "conversation-and-long-context-engineering", "Conversation and Long-Context Engineering"),
  course("rag", "Intermediate", 10, "evidence-grounded-prompting-and-rag-interfaces", "Evidence-Grounded Prompting and RAG Interfaces"),
  course("tools", "Intermediate", 11, "tool-calling-and-tool-interface-design", "Tool Calling and Tool Interface Design"),
  course("multimodal", "Intermediate", 12, "multimodal-prompt-engineering", "Multimodal Prompt Engineering"),
  course("security", "Intermediate", 13, "prompt-security-and-untrusted-content", "Prompt Security and Untrusted Content"),
  course("evaluation", "Advanced", 14, "prompt-evaluation", "Prompt Evaluation"),
  course("judges", "Advanced", 15, "llm-as-a-judge-and-human-evaluation", "LLM-as-a-Judge and Human Evaluation"),
  course("optimization", "Advanced", 16, "evaluation-driven-prompt-optimization", "Evaluation-Driven Prompt Optimization"),
  course("dspy", "Advanced", 17, "automatic-prompt-optimization-and-dspy", "Automatic Prompt Optimization and DSPy"),
  course("agents", "Advanced", 18, "agent-and-multi-agent-prompt-contracts", "Agent and Multi-Agent Prompt Contracts"),
  course("coding", "Advanced", 19, "prompting-for-coding-agents", "Prompting for Coding Agents"),
  course("models", "Advanced", 20, "model-aware-prompt-engineering", "Model-Aware Prompt Engineering"),
  course("efficiency", "Advanced", 21, "cost-latency-and-token-engineering", "Cost, Latency, and Token Engineering"),
  course("promptops", "Enterprise", 22, "promptops", "PromptOps"),
  course("observability", "Enterprise", 23, "prompt-observability-and-failure-diagnosis", "Prompt Observability and Failure Diagnosis"),
  course("release", "Enterprise", 24, "prompt-versioning-experimentation-and-release-engineering", "Prompt Versioning, Experimentation, and Release Engineering"),
  course("governance", "Enterprise", 25, "prompt-governance-and-responsible-ai", "Prompt Governance and Responsible AI"),
  course("trust", "Enterprise", 26, "human-centred-ai-and-trust-calibration", "Human-Centred AI and Trust Calibration"),
  course("portability", "Enterprise", 27, "prompt-portability-and-multi-model-systems", "Prompt Portability and Multi-Model Systems"),
  course("architecture", "Enterprise", 28, "prompt-architecture-patterns-and-system-selection", "Prompt Architecture Patterns and System Selection"),
  course("capstone", "Enterprise", 29, "ai-system-engineering-capstone", "AI System Engineering Capstone"),
];

const check = (lesson) => ({
  question: "What does Course " + lesson.step + " require before a behavior change is accepted?",
  choices: ["A measurable, bounded decision with validation", "One appealing output", "Prompt-only authorization"],
  answer: 0,
  explanation: "Every course treats prompts as one component of a measured AI behavior system.",
});

const generatedChecks = Object.fromEntries(lessons.map((lesson) => [lesson.id, check(lesson)]));

export const checks = {
  ...generatedChecks,
  contracts: {
    question: "A claim-intake assistant has no approved evidence but produces a fluent draft. Which contract component addresses the immediate failure?",
    choices: [
      "An approved-evidence boundary with an explicit clarification path",
      "A more detailed persona",
      "Permission to approve the claim in prompt text",
    ],
    answer: 0,
    explanation: "The system must identify approved evidence and define a safe missing-evidence outcome. Authorization remains application code.",
  },
  structured: {
    question: "A provider-native structured response passes the CaseRecord schema but extracts the wrong invoice amount. Which control should reject it?",
    choices: [
      "Semantic validation against trusted labelled evidence",
      "Another JSON parse",
      "A more permissive schema",
    ],
    answer: 0,
    explanation: "Schema validity proves shape and types, not factual fidelity. Compare supported values and evidence identifiers before accepting the proposal.",
  },
};
