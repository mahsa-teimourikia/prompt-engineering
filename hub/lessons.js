export const lessons = [
  {
    "id": "behavior",
    "level": "Beginner",
    "step": 1,
    "slug": "llm-behavior-and-prompt-anatomy",
    "title": "LLM Behavior and Prompt Anatomy",
    "summary": "Test how prompt position, sampling, and missing evidence affect behavior.",
    "outcome": "Compare controlled variants and require explicit abstention when evidence is absent.",
    "material": "curriculum/beginner/01-llm-behavior-and-prompt-anatomy/README.md",
    "notebook": "curriculum/beginner/01-llm-behavior-and-prompt-anatomy/01_llm_behavior_and_prompt_anatomy.ipynb",
    "lab": "curriculum/beginner/01-llm-behavior-and-prompt-anatomy/lab01.py",
    "checkpoint": "curriculum/beginner/01-llm-behavior-and-prompt-anatomy/README.md#checkpoint",
    "refs": [
      {
        "title": "Google GenAI SDK",
        "path": "https://github.com/googleapis/python-genai"
      }
    ]
  },
  {
    "id": "contracts",
    "level": "Beginner",
    "step": 2,
    "slug": "instruction-contracts",
    "title": "Instruction Contracts",
    "summary": "Turn an ambiguous request into a testable behavior contract.",
    "outcome": "Specify inputs, authority, constraints, output, and failure states, then validate them in code.",
    "material": "curriculum/beginner/02-instruction-contracts/README.md",
    "notebook": "curriculum/beginner/02-instruction-contracts/02_instruction_contracts.ipynb",
    "lab": "curriculum/beginner/02-instruction-contracts/lab02.py",
    "checkpoint": "curriculum/beginner/02-instruction-contracts/README.md#checkpoint",
    "refs": [
      {
        "title": "Pydantic Schemas",
        "path": "https://docs.pydantic.dev/"
      }
    ]
  },
  {
    "id": "examples",
    "level": "Beginner",
    "step": 3,
    "slug": "constraints-examples-and-few-shot-learning",
    "title": "Constraints, Examples, and Few-Shot Learning",
    "summary": "Select examples that clarify real decision boundaries.",
    "outcome": "Compare zero-shot, static, random, and similarity-based examples without hiding context cost.",
    "material": "curriculum/beginner/03-constraints-examples-and-few-shot-learning/README.md",
    "notebook": "curriculum/beginner/03-constraints-examples-and-few-shot-learning/03_constraints_examples_few_shot.ipynb",
    "lab": "curriculum/beginner/03-constraints-examples-and-few-shot-learning/lab03.py",
    "checkpoint": "curriculum/beginner/03-constraints-examples-and-few-shot-learning/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "structured",
    "level": "Beginner",
    "step": 4,
    "slug": "structured-outputs-and-typed-interfaces",
    "title": "Structured Outputs and Typed Interfaces",
    "summary": "Treat model output as an untrusted proposal for a typed interface.",
    "outcome": "Separate syntax constraints from semantic and business validation, including bounded repair.",
    "material": "curriculum/beginner/04-structured-outputs-and-typed-interfaces/README.md",
    "notebook": "curriculum/beginner/04-structured-outputs-and-typed-interfaces/04_structured_outputs_and_typed_interfaces.ipynb",
    "lab": "curriculum/beginner/04-structured-outputs-and-typed-interfaces/lab04.py",
    "checkpoint": "curriculum/beginner/04-structured-outputs-and-typed-interfaces/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "patterns",
    "level": "Beginner",
    "step": 5,
    "slug": "prompt-patterns-and-technique-selection",
    "title": "Prompt Patterns and Technique Selection",
    "summary": "Choose a technique from an observed failure rather than a trend.",
    "outcome": "Compare techniques on quality and context cost, then keep the smallest useful intervention.",
    "material": "curriculum/beginner/05-prompt-patterns-and-technique-selection/README.md",
    "notebook": "curriculum/beginner/05-prompt-patterns-and-technique-selection/05_prompt_patterns_and_technique_selection.ipynb",
    "lab": "curriculum/beginner/05-prompt-patterns-and-technique-selection/lab05.py",
    "checkpoint": "curriculum/beginner/05-prompt-patterns-and-technique-selection/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "reasoning",
    "level": "Intermediate",
    "step": 6,
    "slug": "reasoning-oriented-prompting",
    "title": "Reasoning-Oriented Prompting",
    "summary": "Choose the smallest reasoning architecture that improves a verified decision.",
    "outcome": "Compare direct, sampled, and verifier-assisted approaches without exposing private chain-of-thought.",
    "material": "curriculum/intermediate/06-reasoning-oriented-prompting/README.md",
    "notebook": "curriculum/intermediate/06-reasoning-oriented-prompting/06_reasoning_oriented_prompting.ipynb",
    "lab": "curriculum/intermediate/06-reasoning-oriented-prompting/lab06.py",
    "checkpoint": "curriculum/intermediate/06-reasoning-oriented-prompting/README.md#checkpoint",
    "refs": [
      {
        "title": "OpenAI reasoning best practices",
        "path": "https://developers.openai.com/api/docs/guides/reasoning-best-practices"
      }
    ]
  },
  {
    "id": "workflow",
    "level": "Intermediate",
    "step": 7,
    "slug": "task-decomposition-and-workflow-prompting",
    "title": "Task Decomposition and Workflow Prompting",
    "summary": "Decompose complex work into observable, recoverable stages.",
    "outcome": "Use typed handoffs, stop conditions, and failure-aware workflow state.",
    "material": "curriculum/intermediate/07-task-decomposition-and-workflow-prompting/README.md",
    "notebook": "curriculum/intermediate/07-task-decomposition-and-workflow-prompting/07_task_decomposition_and_workflow_prompting.ipynb",
    "lab": "curriculum/intermediate/07-task-decomposition-and-workflow-prompting/lab07.py",
    "checkpoint": "curriculum/intermediate/07-task-decomposition-and-workflow-prompting/README.md#checkpoint",
    "refs": [
      {
        "title": "LangGraph",
        "path": "https://langchain-ai.github.io/langgraph/"
      }
    ]
  },
  {
    "id": "context",
    "level": "Intermediate",
    "step": 8,
    "slug": "context-engineering",
    "title": "Context Engineering",
    "summary": "Build a context contract with authority, scope, provenance, and budget.",
    "outcome": "Select, order, and validate context while treating retrieved content as untrusted data.",
    "material": "curriculum/intermediate/08-context-engineering/README.md",
    "notebook": "curriculum/intermediate/08-context-engineering/08_context_engineering.ipynb",
    "lab": "curriculum/intermediate/08-context-engineering/lab08.py",
    "checkpoint": "curriculum/intermediate/08-context-engineering/README.md#checkpoint",
    "refs": [
      {
        "title": "Anthropic Context Engineering",
        "path": "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents"
      }
    ]
  },
  {
    "id": "conversation",
    "level": "Intermediate",
    "step": 9,
    "slug": "conversation-and-long-context-engineering",
    "title": "Conversation and Long-Context Engineering",
    "summary": "Separate message history, application state, and durable memory.",
    "outcome": "Compare window, summary, and structured-state strategies with retention and tenant boundaries.",
    "material": "curriculum/intermediate/09-conversation-and-long-context-engineering/README.md",
    "notebook": "curriculum/intermediate/09-conversation-and-long-context-engineering/09_conversation_and_long_context_engineering.ipynb",
    "lab": "curriculum/intermediate/09-conversation-and-long-context-engineering/lab09.py",
    "checkpoint": "curriculum/intermediate/09-conversation-and-long-context-engineering/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "rag",
    "level": "Intermediate",
    "step": 10,
    "slug": "evidence-grounded-prompting-and-rag-interfaces",
    "title": "Evidence-Grounded Prompting and RAG Interfaces",
    "summary": "Design an evidence interface that can cite, abstain, and surface conflicts.",
    "outcome": "Evaluate retrieval and answer support separately while authorizing before retrieval.",
    "material": "curriculum/intermediate/10-evidence-grounded-prompting-and-rag-interfaces/README.md",
    "notebook": "curriculum/intermediate/10-evidence-grounded-prompting-and-rag-interfaces/10_evidence_grounded_prompting_and_rag_interfaces.ipynb",
    "lab": "curriculum/intermediate/10-evidence-grounded-prompting-and-rag-interfaces/lab10.py",
    "checkpoint": "curriculum/intermediate/10-evidence-grounded-prompting-and-rag-interfaces/README.md#checkpoint",
    "refs": [
      {
        "title": "LlamaIndex",
        "path": "https://www.llamaindex.ai/"
      }
    ]
  },
  {
    "id": "tools",
    "level": "Intermediate",
    "step": 11,
    "slug": "tool-calling-and-tool-interface-design",
    "title": "Tool Calling and Tool Interface Design",
    "summary": "Give models narrow typed capabilities while the application owns execution.",
    "outcome": "Validate arguments, authorize before exposure, and distinguish proposed calls from completed actions.",
    "material": "curriculum/intermediate/11-tool-calling-and-tool-interface-design/README.md",
    "notebook": "curriculum/intermediate/11-tool-calling-and-tool-interface-design/11_tool_calling_and_tool_interface_design.ipynb",
    "lab": "curriculum/intermediate/11-tool-calling-and-tool-interface-design/lab11.py",
    "checkpoint": "curriculum/intermediate/11-tool-calling-and-tool-interface-design/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "multimodal",
    "level": "Intermediate",
    "step": 12,
    "slug": "multimodal-prompt-engineering",
    "title": "Multimodal Prompt Engineering",
    "summary": "Ground document and image claims in explicit regions and evidence IDs.",
    "outcome": "Evaluate extraction, contradiction, and missing-evidence cases with a reproducible synthetic asset.",
    "material": "curriculum/intermediate/12-multimodal-prompt-engineering/README.md",
    "notebook": "curriculum/intermediate/12-multimodal-prompt-engineering/12_multimodal_prompt_engineering.ipynb",
    "lab": "curriculum/intermediate/12-multimodal-prompt-engineering/lab12.py",
    "checkpoint": "curriculum/intermediate/12-multimodal-prompt-engineering/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "security",
    "level": "Intermediate",
    "step": 13,
    "slug": "prompt-security-and-untrusted-content",
    "title": "Prompt Security and Untrusted Content",
    "summary": "Model prompt injection as a trust-boundary failure, not a wording puzzle.",
    "outcome": "Combine untrusted-data separation with least privilege, authorization, validation, and adversarial tests.",
    "material": "curriculum/intermediate/13-prompt-security-and-untrusted-content/README.md",
    "notebook": "curriculum/intermediate/13-prompt-security-and-untrusted-content/13_prompt_security_and_untrusted_content.ipynb",
    "lab": "curriculum/intermediate/13-prompt-security-and-untrusted-content/lab13.py",
    "checkpoint": "curriculum/intermediate/13-prompt-security-and-untrusted-content/README.md#checkpoint",
    "refs": [
      {
        "title": "OWASP Injection Cheat Sheet",
        "path": "https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html"
      }
    ]
  },
  {
    "id": "evaluation",
    "level": "Advanced",
    "step": 14,
    "slug": "prompt-evaluation",
    "title": "Prompt Evaluation",
    "summary": "Replace anecdotal checks with versioned cases, slices, and hard gates.",
    "outcome": "Compare baseline and candidate metrics while retaining denominators and critical failures.",
    "material": "curriculum/advanced/14-prompt-evaluation/README.md",
    "notebook": "curriculum/advanced/14-prompt-evaluation/14_prompt_evaluation.ipynb",
    "lab": "curriculum/advanced/14-prompt-evaluation/lab14.py",
    "checkpoint": "curriculum/advanced/14-prompt-evaluation/README.md#checkpoint",
    "refs": [
      {
        "title": "DeepEval",
        "path": "https://docs.confident-ai.com/"
      }
    ]
  },
  {
    "id": "judges",
    "level": "Advanced",
    "step": 15,
    "slug": "llm-as-a-judge-and-human-evaluation",
    "title": "LLM-as-a-Judge and Human Evaluation",
    "summary": "Calibrate rubric judges against human labels and known bias tests.",
    "outcome": "Measure agreement, handle ties and order effects, and route ambiguous or high-impact cases to people.",
    "material": "curriculum/advanced/15-llm-as-a-judge-and-human-evaluation/README.md",
    "notebook": "curriculum/advanced/15-llm-as-a-judge-and-human-evaluation/15_llm_as_a_judge_and_human_evaluation.ipynb",
    "lab": "curriculum/advanced/15-llm-as-a-judge-and-human-evaluation/lab15.py",
    "checkpoint": "curriculum/advanced/15-llm-as-a-judge-and-human-evaluation/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "optimization",
    "level": "Advanced",
    "step": 16,
    "slug": "evaluation-driven-prompt-optimization",
    "title": "Evaluation-Driven Prompt Optimization",
    "summary": "Improve measured behavior without leaking the final test set.",
    "outcome": "Separate development and holdout data and reject local fixes that cause global regressions.",
    "material": "curriculum/advanced/16-evaluation-driven-prompt-optimization/README.md",
    "notebook": "curriculum/advanced/16-evaluation-driven-prompt-optimization/16_evaluation_driven_prompt_optimization.ipynb",
    "lab": "curriculum/advanced/16-evaluation-driven-prompt-optimization/lab16.py",
    "checkpoint": "curriculum/advanced/16-evaluation-driven-prompt-optimization/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "dspy",
    "level": "Advanced",
    "step": 17,
    "slug": "automatic-prompt-optimization-and-dspy",
    "title": "Automatic Prompt Optimization and DSPy",
    "summary": "Search a bounded prompt-program space against an explicit metric.",
    "outcome": "Select on development data, test once on holdout, and inspect leakage and metric gaming.",
    "material": "curriculum/advanced/17-automatic-prompt-optimization-and-dspy/README.md",
    "notebook": "curriculum/advanced/17-automatic-prompt-optimization-and-dspy/17_automatic_prompt_optimization_and_dspy.ipynb",
    "lab": "curriculum/advanced/17-automatic-prompt-optimization-and-dspy/lab17.py",
    "checkpoint": "curriculum/advanced/17-automatic-prompt-optimization-and-dspy/README.md#checkpoint",
    "refs": [
      {
        "title": "DSPy Documentation",
        "path": "https://github.com/stanfordnlp/dspy"
      }
    ]
  },
  {
    "id": "agents",
    "level": "Advanced",
    "step": 18,
    "slug": "agent-and-multi-agent-prompt-contracts",
    "title": "Agent and Multi-Agent Prompt Contracts",
    "summary": "Design bounded agent tasks with typed contracts, budgets, and terminal states.",
    "outcome": "Authorize from trusted identity before capability exposure and justify multi-agent complexity against a baseline.",
    "material": "curriculum/advanced/18-agent-and-multi-agent-prompt-contracts/README.md",
    "notebook": "curriculum/advanced/18-agent-and-multi-agent-prompt-contracts/18_agent_and_multi_agent_prompt_contracts.ipynb",
    "lab": "curriculum/advanced/18-agent-and-multi-agent-prompt-contracts/lab18.py",
    "checkpoint": "curriculum/advanced/18-agent-and-multi-agent-prompt-contracts/README.md#checkpoint",
    "refs": [
      {
        "title": "CrewAI",
        "path": "https://www.crewai.com/"
      }
    ]
  },
  {
    "id": "coding",
    "level": "Advanced",
    "step": 19,
    "slug": "prompting-for-coding-agents",
    "title": "Prompting for Coding Agents",
    "summary": "Turn a software request into an enforceable change contract.",
    "outcome": "Constrain file and command scope, then require tests and diff evidence before completion.",
    "material": "curriculum/advanced/19-prompting-for-coding-agents/README.md",
    "notebook": "curriculum/advanced/19-prompting-for-coding-agents/19_prompting_for_coding_agents.ipynb",
    "lab": "curriculum/advanced/19-prompting-for-coding-agents/lab19.py",
    "checkpoint": "curriculum/advanced/19-prompting-for-coding-agents/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "models",
    "level": "Advanced",
    "step": 20,
    "slug": "model-aware-prompt-engineering",
    "title": "Model-Aware Prompt Engineering",
    "summary": "Keep durable behavior contracts separate from provider adapters.",
    "outcome": "Compare conformance, quality, latency, and cost before selecting or migrating a model.",
    "material": "curriculum/advanced/20-model-aware-prompt-engineering/README.md",
    "notebook": "curriculum/advanced/20-model-aware-prompt-engineering/20_model_aware_prompt_engineering.ipynb",
    "lab": "curriculum/advanced/20-model-aware-prompt-engineering/lab20.py",
    "checkpoint": "curriculum/advanced/20-model-aware-prompt-engineering/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "efficiency",
    "level": "Advanced",
    "step": 21,
    "slug": "cost-latency-and-token-engineering",
    "title": "Cost, Latency, and Token Engineering",
    "summary": "Optimize cost and latency without dropping required evidence.",
    "outcome": "Trace quality and resource use together and reject configurations that are merely cheaper failures.",
    "material": "curriculum/advanced/21-cost-latency-and-token-engineering/README.md",
    "notebook": "curriculum/advanced/21-cost-latency-and-token-engineering/21_cost_latency_and_token_engineering.ipynb",
    "lab": "curriculum/advanced/21-cost-latency-and-token-engineering/lab21.py",
    "checkpoint": "curriculum/advanced/21-cost-latency-and-token-engineering/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "promptops",
    "level": "Enterprise",
    "step": 22,
    "slug": "promptops",
    "title": "PromptOps",
    "summary": "Version and release the complete AI behavior artifact.",
    "outcome": "Gate prompt, schema, model configuration, dataset, and ownership changes with reproducible evidence.",
    "material": "curriculum/enterprise/22-promptops/README.md",
    "notebook": "curriculum/enterprise/22-promptops/22_promptops.ipynb",
    "lab": "curriculum/enterprise/22-promptops/lab22.py",
    "checkpoint": "curriculum/enterprise/22-promptops/README.md#checkpoint",
    "refs": [
      {
        "title": "PromptLayer",
        "path": "https://promptlayer.com/"
      }
    ]
  },
  {
    "id": "observability",
    "level": "Enterprise",
    "step": 23,
    "slug": "prompt-observability-and-failure-diagnosis",
    "title": "Prompt Observability and Failure Diagnosis",
    "summary": "Capture privacy-aware traces that identify the first failing layer.",
    "outcome": "Record correlation, versions, evidence, policy, usage, errors, and terminal state without hidden reasoning.",
    "material": "curriculum/enterprise/23-prompt-observability-and-failure-diagnosis/README.md",
    "notebook": "curriculum/enterprise/23-prompt-observability-and-failure-diagnosis/23_prompt_observability_and_failure_diagnosis.ipynb",
    "lab": "curriculum/enterprise/23-prompt-observability-and-failure-diagnosis/lab23.py",
    "checkpoint": "curriculum/enterprise/23-prompt-observability-and-failure-diagnosis/README.md#checkpoint",
    "refs": [
      {
        "title": "LangSmith",
        "path": "https://www.langchain.com/langsmith"
      }
    ]
  },
  {
    "id": "release",
    "level": "Enterprise",
    "step": 24,
    "slug": "prompt-versioning-experimentation-and-release-engineering",
    "title": "Prompt Versioning, Experimentation, and Release Engineering",
    "summary": "Run sticky canaries with declared metrics and rollback rules.",
    "outcome": "Distinguish insufficient samples from success and roll back immediately on critical failures.",
    "material": "curriculum/enterprise/24-prompt-versioning-experimentation-and-release-engineering/README.md",
    "notebook": "curriculum/enterprise/24-prompt-versioning-experimentation-and-release-engineering/24_prompt_versioning_experimentation_and_release_engineering.ipynb",
    "lab": "curriculum/enterprise/24-prompt-versioning-experimentation-and-release-engineering/lab24.py",
    "checkpoint": "curriculum/enterprise/24-prompt-versioning-experimentation-and-release-engineering/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "governance",
    "level": "Enterprise",
    "step": 25,
    "slug": "prompt-governance-and-responsible-ai",
    "title": "Prompt Governance and Responsible AI",
    "summary": "Connect AI policy to executable controls, evidence, ownership, and approval.",
    "outcome": "Use trusted, versioned approval records and fail closed when required evidence is missing.",
    "material": "curriculum/enterprise/25-prompt-governance-and-responsible-ai/README.md",
    "notebook": "curriculum/enterprise/25-prompt-governance-and-responsible-ai/25_prompt_governance_and_responsible_ai.ipynb",
    "lab": "curriculum/enterprise/25-prompt-governance-and-responsible-ai/lab25.py",
    "checkpoint": "curriculum/enterprise/25-prompt-governance-and-responsible-ai/README.md#checkpoint",
    "refs": [
      {
        "title": "Microsoft Presidio",
        "path": "https://microsoft.github.io/presidio/"
      }
    ]
  },
  {
    "id": "trust",
    "level": "Enterprise",
    "step": 26,
    "slug": "human-centred-ai-and-trust-calibration",
    "title": "Human-Centred AI and Trust Calibration",
    "summary": "Calibrate user trust with evidence, impact-aware review, and honest uncertainty.",
    "outcome": "Route by risk and support rather than treating model confidence as permission.",
    "material": "curriculum/enterprise/26-human-centred-ai-and-trust-calibration/README.md",
    "notebook": "curriculum/enterprise/26-human-centred-ai-and-trust-calibration/26_human_centred_ai_and_trust_calibration.ipynb",
    "lab": "curriculum/enterprise/26-human-centred-ai-and-trust-calibration/lab26.py",
    "checkpoint": "curriculum/enterprise/26-human-centred-ai-and-trust-calibration/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "portability",
    "level": "Enterprise",
    "step": 27,
    "slug": "prompt-portability-and-multi-model-systems",
    "title": "Prompt Portability and Multi-Model Systems",
    "summary": "Test provider adapters against one contract and shared cases.",
    "outcome": "Normalize results and allow fallback only when operation semantics make retry safe.",
    "material": "curriculum/enterprise/27-prompt-portability-and-multi-model-systems/README.md",
    "notebook": "curriculum/enterprise/27-prompt-portability-and-multi-model-systems/27_prompt_portability_and_multi_model_systems.ipynb",
    "lab": "curriculum/enterprise/27-prompt-portability-and-multi-model-systems/lab27.py",
    "checkpoint": "curriculum/enterprise/27-prompt-portability-and-multi-model-systems/README.md#checkpoint",
    "refs": [
      {
        "title": "LiteLLM",
        "path": "https://github.com/BerriAI/litellm"
      }
    ]
  },
  {
    "id": "architecture",
    "level": "Enterprise",
    "step": 28,
    "slug": "prompt-architecture-patterns-and-system-selection",
    "title": "Prompt Architecture Patterns and System Selection",
    "summary": "Select the least complex architecture that meets explicit constraints.",
    "outcome": "Expose weighted criteria, compare alternatives, and test recommendation sensitivity.",
    "material": "curriculum/enterprise/28-prompt-architecture-patterns-and-system-selection/README.md",
    "notebook": "curriculum/enterprise/28-prompt-architecture-patterns-and-system-selection/28_prompt_architecture_patterns_and_system_selection.ipynb",
    "lab": "curriculum/enterprise/28-prompt-architecture-patterns-and-system-selection/lab28.py",
    "checkpoint": "curriculum/enterprise/28-prompt-architecture-patterns-and-system-selection/README.md#checkpoint",
    "refs": []
  },
  {
    "id": "capstone",
    "level": "Enterprise",
    "step": 29,
    "slug": "ai-system-engineering-capstone",
    "title": "AI System Engineering Capstone",
    "summary": "Assemble a release portfolio for the complete Northstar system.",
    "outcome": "Pass a fail-closed gate covering contract, evaluation, threat, trace, ownership, tests, and rollback.",
    "material": "curriculum/enterprise/29-ai-system-engineering-capstone/README.md",
    "notebook": [
      {
        "title": "01 Milestone Foundation",
        "path": "curriculum/enterprise/29-ai-system-engineering-capstone/milestones/01_milestone_foundation.ipynb"
      },
      {
        "title": "02 Milestone Rag And Tools",
        "path": "curriculum/enterprise/29-ai-system-engineering-capstone/milestones/02_milestone_rag_and_tools.ipynb"
      },
      {
        "title": "03 Milestone Routing And Security",
        "path": "curriculum/enterprise/29-ai-system-engineering-capstone/milestones/03_milestone_routing_and_security.ipynb"
      },
      {
        "title": "04 Milestone Portability",
        "path": "curriculum/enterprise/29-ai-system-engineering-capstone/milestones/04_milestone_portability.ipynb"
      },
      {
        "title": "05 Milestone Production Release",
        "path": "curriculum/enterprise/29-ai-system-engineering-capstone/milestones/05_milestone_production_release.ipynb"
      }
    ],
    "lab": "curriculum/enterprise/29-ai-system-engineering-capstone/lab29.py",
    "checkpoint": "curriculum/enterprise/29-ai-system-engineering-capstone/README.md#checkpoint",
    "refs": []
  }
];

export const checks = {
  "behavior": [
    {
      "question": "Why is 'The prompt used to work' not a valid diagnosis for a failure?",
      "choices": [
        "The entire request packet, context, and decoding params must be analyzed",
        "Prompts don't change behavior",
        "Models are deterministic"
      ],
      "answer": 0,
      "explanation": "A production response is conditional generation inside a whole request packet. You must isolate what changed."
    },
    {
      "question": "How does a generation request obtain conversation state?",
      "choices": [
        "The model permanently learns every prior turn",
        "The application or provider supplies the selected prior state with the request",
        "Conversation state is unnecessary"
      ],
      "answer": 1,
      "explanation": "The request receives selected state through messages, summaries, retrieval, or a provider-managed conversation abstraction; it need not replay every prior token."
    }
  ],
  "contracts": [
    {
      "question": "What is the primary flaw of asking an LLM to 'write a good summary'?",
      "choices": [
        "Summaries are too hard for LLMs",
        "It uses too many tokens",
        "'Good' is subjective, unmeasurable, and impossible to test"
      ],
      "answer": 2,
      "explanation": "A contract requires measurable, binary boundaries rather than ambiguous adjectives."
    },
    {
      "question": "Why must an instruction contract explicitly define a fallback path?",
      "choices": [
        "To prevent the model from hallucinating a guess when facts are absent",
        "To save API costs",
        "To make the prompt longer"
      ],
      "answer": 0,
      "explanation": "Without a defined fallback (like 'Output UNKNOWN'), the model's natural behavior is to guess plausibly."
    }
  ],
  "examples": [
    {
      "question": "When should few-shot examples be added to an instruction contract?",
      "choices": [
        "Whenever examples are available",
        "When a controlled evaluation shows representative boundary examples improve the target behavior enough to justify their cost",
        "Only for tone imitation"
      ],
      "answer": 1,
      "explanation": "Examples can clarify boundaries and formats, but they consume context and can bias behavior. Compare them with a zero-shot baseline."
    },
    {
      "question": "What happens if all your Few-Shot examples demonstrate 'success' paths and none demonstrate 'failure' paths?",
      "choices": [
        "The model becomes more accurate",
        "Latency decreases",
        "The model will hallucinate success when faced with a failing input"
      ],
      "answer": 2,
      "explanation": "Success-only examples leave the failure contract under-specified and may bias outputs toward success. Include representative negative and abstention cases, then test them."
    }
  ],
  "structured": [
    {
      "question": "Why prefer a provider-native schema when the selected provider and schema subset support it?",
      "choices": [
        "It relies on the model's language skills rather than native decoding enforcement",
        "It uses more tokens",
        "JSON is deprecated"
      ],
      "answer": 0,
      "explanation": "Schema-constrained generation is generally more reliable than prompt-only formatting, but the application must still handle refusals, truncation, unsupported features, and semantic errors."
    },
    {
      "question": "If a model outputs perfectly formatted JSON, does that mean the data is correct?",
      "choices": [
        "Yes",
        "No, syntax validation is separate from semantic validation"
      ],
      "answer": 1,
      "explanation": "A valid schema just means the JSON parses. Application code must still verify that the numbers or claims inside the JSON are true."
    }
  ],
  "patterns": [
    {
      "question": "What is 'Pattern Bloat'?",
      "choices": [
        "A token limit error",
        "A new type of model",
        "Blindly stacking techniques (like CoT + Few-Shot) on every prompt without measuring if they actually help"
      ],
      "answer": 2,
      "explanation": "Adding every technique increases latency and obscures failure causes. Use only the simplest pattern required."
    },
    {
      "question": "When should you use a complex multi-stage prompt instead of a simple deterministic script?",
      "choices": [
        "Only when the task requires semantic flexibility that traditional code cannot handle",
        "When writing Python is too hard",
        "Always"
      ],
      "answer": 0,
      "explanation": "If a problem can be solved with Regex or an SQL query, do not use an LLM."
    }
  ],
  "reasoning": [
    {
      "question": "What should an evaluation compare before adopting a more verbose reasoning prompt?",
      "choices": [
        "Only whether the rationale sounds convincing",
        "Task quality, evidence support, output tokens, latency, and cost against a direct baseline",
        "Only the number of reasoning steps"
      ],
      "answer": 1,
      "explanation": "More output may help some tasks and hurt others. Measure the actual outcome and operating trade-offs on the target model."
    },
    {
      "question": "Why should an operational reasoning schema request concise evidence checks instead of private chain-of-thought?",
      "choices": [
        "Evidence checks can be compared with logs or policy while field order is not proof of correctness",
        "JSON requires evidence fields",
        "It makes application validation unnecessary"
      ],
      "answer": 0,
      "explanation": "Observable claims, reason codes, and evidence can be verified. A generated rationale or its position in a schema cannot authorize an action."
    }
  ],
  "workflow": [
    {
      "question": "What happens when you give an LLM a massive 10-step instruction list?",
      "choices": [
        "It suffers from 'attention dilution' and will silently skip steps",
        "It crashes the API",
        "It executes it perfectly"
      ],
      "answer": 0,
      "explanation": "Long instructions can increase omission risk. Measure the failure first, then use the smallest useful decomposition with explicit state and terminal conditions."
    },
    {
      "question": "In a multi-stage workflow, why use programmatic 'if/else' routing between models instead of an LLM router?",
      "choices": [
        "To increase complexity",
        "Because explicit code is usually easier to test and audit for rules that are already deterministic",
        "LLMs can't route data"
      ],
      "answer": 1,
      "explanation": "Use explicit code for rules that can be expressed deterministically, while still testing implementation errors and malformed inputs."
    }
  ],
  "context": [
    {
      "question": "What is the 'Lost in the Middle' phenomenon?",
      "choices": [
        "A symptom of low temperature",
        "A network timeout error",
        "Models paying high attention to the start and end of a prompt, but ignoring data in the center"
      ],
      "answer": 2,
      "explanation": "Long-context models struggle to retrieve facts buried deep in the middle of massive context blocks."
    },
    {
      "question": "How should instruction placement be chosen for a long-context task?",
      "choices": [
        "Always at the end",
        "Always at the beginning",
        "With a controlled evaluation on the target model while keeping trusted instructions explicit and stable"
      ],
      "answer": 2,
      "explanation": "Position effects vary by task and model. Treat placement as an evaluated design choice, not a universal rule."
    }
  ],
  "conversation": [
    {
      "question": "How do LLMs actually 'remember' a conversation?",
      "choices": [
        "They learn from each turn",
        "The application or provider supplies selected prior state with each otherwise stateless generation request",
        "They use a hidden SQL database"
      ],
      "answer": 1,
      "explanation": "Conversation state is supplied by an application or provider. Production systems often select, summarize, or retrieve bounded state instead of replaying every turn."
    },
    {
      "question": "What is the safe response when a conversation exceeds its context budget?",
      "choices": [
        "Append duplicate system instructions after every user turn",
        "Apply a tested retention policy that preserves trusted instructions and required evidence while summarizing or evicting lower-priority state",
        "Silently remove the oldest messages"
      ],
      "answer": 1,
      "explanation": "Context management is an application policy. Retention must preserve authority, provenance, and task-critical state and must be regression-tested."
    }
  ],
  "rag": [
    {
      "question": "What is the fundamental purpose of RAG?",
      "choices": [
        "To ground answers strictly in retrieved evidence rather than the model's pre-trained parametric memory",
        "To search the internet",
        "To train a model on your data"
      ],
      "answer": 0,
      "explanation": "RAG supplies selected evidence at request time. Retrieval, authorization, citation, claim support, and abstention still need separate evaluation."
    },
    {
      "question": "If a RAG answer is wrong, what should be evaluated?",
      "choices": [
        "Only the generation model",
        "Only vector search",
        "Authorization, retrieval, ranking, prompt construction, citation validity, claim support, and generation"
      ],
      "answer": 2,
      "explanation": "RAG is an end-to-end system. A correct document can be filtered out, ranked poorly, omitted from the prompt, misquoted, or ignored."
    }
  ],
  "tools": [
    {
      "question": "How does an LLM execute a Python function?",
      "choices": [
        "It sends an HTTP request",
        "It runs Python natively",
        "It generates a JSON payload representing the arguments, pauses, and waits for the application to run the code and return the result"
      ],
      "answer": 2,
      "explanation": "Models are trapped in a text box. They only generate text (JSON). The application executes the tools."
    },
    {
      "question": "Why is giving an LLM autonomous write-access to a database extremely dangerous?",
      "choices": [
        "LLMs hallucinate arguments and can get stuck in loops. Destructive actions require a Human-in-the-Loop approval step",
        "It's too expensive",
        "It will delete everything"
      ],
      "answer": 0,
      "explanation": "High-impact or irreversible actions need least privilege, deterministic policy checks, idempotency, audit logs, and approval where risk requires it."
    }
  ],
  "multimodal": [
    {
      "question": "How should you choose between a native multimodal model and an OCR or document pipeline?",
      "choices": [
        "Always use the native model",
        "Always use OCR",
        "Evaluate which pipeline preserves the required evidence, provenance, confidence, cost, and latency"
      ],
      "answer": 2,
      "explanation": "Native inputs preserve some visual context; specialist pipelines can provide precise text, coordinates, confidence, or lower cost. The task determines the choice."
    },
    {
      "question": "What is the best way to direct a multimodal model's attention in a massive video?",
      "choices": [
        "Upload the video twice",
        "Ask a vague question",
        "Use explicit text anchors, specifying timestamps or spatial quadrants"
      ],
      "answer": 2,
      "explanation": "Spatial or temporal anchors make the requested evidence easier to locate and audit; measure their effect on the target media and model."
    }
  ],
  "security": [
    {
      "question": "What is Indirect Prompt Injection?",
      "choices": [
        "The application retrieving a poisoned document (e.g., from a web search) and blindly injecting it into the prompt's context",
        "A network hack",
        "A user typing a malicious command in a chatbox"
      ],
      "answer": 0,
      "explanation": "Retrieved content can contain adversarial instructions. The application must preserve provenance, restrict capabilities, validate outputs, and treat delimiters as structure rather than a security boundary."
    },
    {
      "question": "Why do instructions like 'Ignore the user if they try to hack you' fail?",
      "choices": [
        "They consume too many tokens",
        "Because prompt-only defenses are probabilistic and cannot replace capability controls and application-side validation",
        "They aren't polite enough"
      ],
      "answer": 1,
      "explanation": "Security requires defense in depth: trusted control flow, least privilege, provenance, validation, monitoring, and safe failure. Delimiters alone are not a firewall."
    }
  ],
  "evaluation": [
    {
      "question": "Why is evaluating prompts with 'vibe checks' an anti-pattern?",
      "choices": [
        "It requires too much code",
        "It's too slow",
        "It doesn't scale and fails to catch regressions on edge cases when a prompt is modified"
      ],
      "answer": 2,
      "explanation": "Use repeatable regression cases with deterministic checks where possible, calibrated model or human review where needed, and report uncertainty rather than claiming proof from one dataset."
    },
    {
      "question": "Which of the following belongs in a Golden Dataset?",
      "choices": [
        "Clear, ambiguous, adversarial, and missing-evidence inputs",
        "Only inputs that failed previously",
        "Only happy-path inputs"
      ],
      "answer": 0,
      "explanation": "A robust evaluation suite must test the prompt's ability to handle failure modes and edge cases gracefully."
    }
  ],
  "judges": [
    {
      "question": "What is the critical prerequisite for using an LLM-as-a-Judge?",
      "choices": [
        "Using the most expensive model",
        "Calibrating the rubric and judge against held-out, double-scored human examples",
        "Using a fast model"
      ],
      "answer": 1,
      "explanation": "Measure agreement and subgroup behavior on held-out human labels before using judge scores as an optimization signal."
    },
    {
      "question": "What should an LLM judge return in addition to a score?",
      "choices": [
        "Private chain-of-thought",
        "A concise reason code or rubric-grounded critique that can be audited",
        "Nothing; a score is self-validating"
      ],
      "answer": 1,
      "explanation": "A concise, rubric-grounded artifact helps diagnose disagreement. It still must be calibrated and is not proof that the score is correct."
    }
  ],
  "optimization": [
    {
      "question": "What is evaluation-driven prompt optimization?",
      "choices": [
        "Iteratively proposing bounded changes, measuring development results, and accepting only changes that also satisfy holdout and safety gates",
        "Optimizing the server architecture",
        "Using complex math"
      ],
      "answer": 0,
      "explanation": "A development metric guides search; protected holdout cases, critical slices, and release gates reduce overfitting and metric gaming."
    },
    {
      "question": "Why run the regression suite after optimizing for one reported failure?",
      "choices": [
        "It takes too long",
        "A local fix can change behavior on unrelated cases or critical slices",
        "It wastes tokens"
      ],
      "answer": 1,
      "explanation": "Prompt changes can have broad semantic effects. Compare the candidate with the baseline on development, holdout, and critical cases."
    }
  ],
  "dspy": [
    {
      "question": "What is the primary value proposition of DSPy?",
      "choices": [
        "It replaces Python",
        "It makes models run faster",
        "It automates prompt generation by compiling declarative signatures into optimized prompt strings algorithmically"
      ],
      "answer": 2,
      "explanation": "DSPy represents LM programs with typed signatures and modules, then uses an optimizer and metric to search over instructions or demonstrations."
    },
    {
      "question": "In DSPy, what replaces the manual 'Prompt String'?",
      "choices": [
        "A Signature and module, optionally compiled with an optimizer",
        "A JSON file",
        "A larger LLM"
      ],
      "answer": 0,
      "explanation": "A signature describes input/output behavior; modules and optimizers can construct or tune prompts and demonstrations against a metric."
    }
  ],
  "agents": [
    {
      "question": "What distinguishes an agent loop from a fixed workflow?",
      "choices": [
        "It uses OpenAI",
        "The model selects among bounded next actions from observed state instead of following only predetermined transitions",
        "It has a chat UI"
      ],
      "answer": 1,
      "explanation": "An agent chooses some control flow dynamically, but the application still defines tools, permissions, budgets, stop conditions, and terminal states."
    },
    {
      "question": "What additional failure surface does a multi-agent system introduce?",
      "choices": [
        "They are too fast",
        "They are too deterministic",
        "Handoff errors, duplicated work, compounding unsupported claims, and unbounded loops"
      ],
      "answer": 2,
      "explanation": "Typed handoffs, explicit ownership, bounded loops, shared evidence, and terminal-state tests are needed; the framework choice alone does not provide them."
    }
  ],
  "coding": [
    {
      "question": "Why should a coding agent run targeted tests after making a change?",
      "choices": [
        "Execution checks whether the change satisfies behavior and catches syntax or integration failures that prose review can miss",
        "To save tokens",
        "To write documentation"
      ],
      "answer": 0,
      "explanation": "Tests provide executable evidence. They should cover the changed behavior and negative cases without weakening existing assertions."
    },
    {
      "question": "What is the danger of letting an LLM write code directly to production?",
      "choices": [
        "It's not dangerous",
        "It can introduce severe security vulnerabilities, infinite loops, or wipe databases",
        "It makes the codebase too large"
      ],
      "answer": 1,
      "explanation": "Use scoped permissions, isolated execution where appropriate, tests, review, and a separate release authority proportional to the risk."
    }
  ],
  "models": [
    {
      "question": "Why must a prompt contract be re-evaluated when the model or provider changes?",
      "choices": [
        "Only API keys differ",
        "Model behavior, supported schemas, context limits, tools, latency, and pricing can differ",
        "Prompt behavior is identical across models"
      ],
      "answer": 1,
      "explanation": "Portability is an empirical property of the whole contract and adapter. Re-run conformance and quality evaluations for each profile."
    },
    {
      "question": "How should a smaller or cheaper candidate model be assessed?",
      "choices": [
        "Assume it needs a simpler prompt",
        "Run the same contract, capability, quality, cost, and latency checks before deciding whether adaptation is needed",
        "Reject it based on parameter count alone"
      ],
      "answer": 1,
      "explanation": "Model size alone does not predict task fitness. Use measured conformance and outcome evidence."
    }
  ],
  "efficiency": [
    {
      "question": "What should be verified before relying on provider prompt or context caching?",
      "choices": [
        "Only whether the prompt is long",
        "Eligibility, cache-key behavior, privacy, retention, pricing, latency, and invalidation on the exact provider",
        "Nothing; caching is portable"
      ],
      "answer": 1,
      "explanation": "Caching behavior is provider-specific and may reduce some repeated-input cost or latency; it does not make context free or universally instant."
    },
    {
      "question": "How do you minimize token costs in a RAG pipeline?",
      "choices": [
        "By ignoring the context",
        "By switching to a smaller model",
        "By aggressively pre-processing and stripping noise/HTML from the retrieved documents before injecting them"
      ],
      "answer": 2,
      "explanation": "Injecting massive, messy logs wastes money. Clean your data before sending it to the LLM."
    }
  ],
  "promptops": [
    {
      "question": "What is the core philosophy of PromptOps?",
      "choices": [
        "Prompt engineering is software engineering; prompts must pass strict CI/CD pipelines before deployment",
        "Prompts should be edited live in production",
        "Prompts are just text files"
      ],
      "answer": 0,
      "explanation": "Treating prompts as versioned, tested artifacts prevents catastrophic regressions."
    },
    {
      "question": "Why separate a prompt artifact from unrelated business logic?",
      "choices": [
        "It's too hard to read",
        "It makes versioning, review, evaluation linkage, ownership, and rollback harder",
        "Python doesn't support long strings"
      ],
      "answer": 1,
      "explanation": "Keep the prompt, schema, model profile, and evaluation manifest identifiable as one release artifact; storage and deployment can still follow the application's risk controls."
    }
  ],
  "observability": [
    {
      "question": "Why is HTTP 200 (Success) a dangerous metric for LLM APIs?",
      "choices": [
        "It means the API is down",
        "It's deprecated",
        "An LLM can return a HTTP 200 while delivering a catastrophic, confidently incorrect hallucination"
      ],
      "answer": 2,
      "explanation": "Infrastructure observability is insufficient. You need semantic observability to measure output quality."
    },
    {
      "question": "What does Distributed Tracing for LLMs accomplish?",
      "choices": [
        "It correlates sanitized inputs, outputs, decisions, timings, token use, and errors across workflow stages",
        "It speeds up the model",
        "It tracks network packets"
      ],
      "answer": 0,
      "explanation": "Correlated spans help localize retrieval, routing, validation, tool, or generation failures without requiring private reasoning or raw sensitive payloads."
    }
  ],
  "release": [
    {
      "question": "What is a Shadow Deployment for a prompt?",
      "choices": [
        "Deploying at night",
        "Routing live traffic to both the old and new prompt asynchronously, logging the new prompt's results for evaluation without showing them to the user",
        "Hiding the prompt text"
      ],
      "answer": 1,
      "explanation": "Shadow traffic reduces direct user-output risk, but copied production data still requires privacy, cost, access, retention, and side-effect controls."
    },
    {
      "question": "What can a feature flag add to a prompt release?",
      "choices": [
        "It uses fewer tokens",
        "To make the code larger",
        "Controlled exposure and a defined rollback path without requiring the prompt artifact to be hard-coded"
      ],
      "answer": 2,
      "explanation": "A flag can support staged exposure and rollback, but the release path, cache behavior, and rollback procedure must be tested."
    }
  ],
  "governance": [
    {
      "question": "What should determine whether personal data may be sent to a model provider?",
      "choices": [
        "The model's promise to keep it secret",
        "Purpose, necessity, consent or other lawful basis, provider terms, region, retention, access controls, and organizational policy",
        "Whether redaction is inconvenient"
      ],
      "answer": 1,
      "explanation": "Minimize or redact data before egress when it is not required or authorized. Compliance depends on the use and controls, not a blanket rule that every identifier is forbidden."
    },
    {
      "question": "What is an Outbound Guardrail?",
      "choices": [
        "A firewall rule",
        "A secondary system that scans the LLM's response for toxicity or restricted topics before displaying it to the user",
        "A prompt instruction"
      ],
      "answer": 1,
      "explanation": "An output check is one defense layer. It should enforce specific, tested policies and route uncertain results safely; it cannot reliably detect every hallucination."
    }
  ],
  "trust": [
    {
      "question": "What is Automation Bias?",
      "choices": [
        "A bug in the code",
        "Robots doing manual labor",
        "The psychological tendency for humans to blindly trust highly confident automated systems, even when they hallucinate"
      ],
      "answer": 2,
      "explanation": "Authoritative presentation can increase over-reliance. Show evidence, uncertainty, limitations, and review paths, then measure user decisions."
    },
    {
      "question": "What is 'Trust Calibration'?",
      "choices": [
        "Designing information and controls so user reliance better reflects measured task reliability and consequence",
        "A mathematical formula",
        "Making the user trust the AI 100%"
      ],
      "answer": 0,
      "explanation": "Use evidence, calibrated uncertainty, consequence-aware review, and outcome research to reduce both over-reliance and under-use."
    }
  ],
  "portability": [
    {
      "question": "What reduces—but does not eliminate—provider lock-in?",
      "choices": [
        "By signing a long contract",
        "By abstracting provider-specific APIs behind unified contract layers (like LiteLLM) and standardizing on JSON schemas",
        "By using only one model"
      ],
      "answer": 1,
      "explanation": "A common contract and adapter isolate API differences, but each provider still needs capability, quality, policy, and operational conformance tests."
    },
    {
      "question": "What must you do to ensure an automated fallback model is actually useful?",
      "choices": [
        "Pay for a premium tier",
        "Assume it works",
        "Run your automated evaluation suite against the fallback model continuously to ensure it meets quality thresholds"
      ],
      "answer": 2,
      "explanation": "Portability of code does not guarantee equivalent capability. Re-run the required contract, quality, safety, latency, and cost gates."
    }
  ],
  "architecture": [
    {
      "question": "What is the core principle of System Selection?",
      "choices": [
        "Prefer the lowest-complexity architecture that satisfies measured quality, safety, latency, cost, and operational requirements",
        "Never use code",
        "Always use the largest model"
      ],
      "answer": 0,
      "explanation": "Additional retrieval, routing, tools, or agents add failure surfaces and operating cost. Adopt them only when evidence shows they meet an unmet requirement."
    },
    {
      "question": "What is a 'Compound AI System'?",
      "choices": [
        "A single massive prompt",
        "An architecture that mixes deterministic code, fast classifier LLMs, and heavy reasoning LLMs in a coordinated pipeline",
        "A chemical reaction"
      ],
      "answer": 1,
      "explanation": "A compound system combines components with explicit contracts. Its value must be demonstrated against a simpler baseline."
    }
  ],
  "capstone": [
    {
      "question": "What is the ultimate goal of Project Northstar?",
      "choices": [
        "To test API keys",
        "To build a chat bot",
        "To integrate routing, retrieval, tool requests, evaluation, observability, and governance into a reviewable release candidate"
      ],
      "answer": 2,
      "explanation": "The capstone assembles a portfolio of executable evidence and verified artifacts; it does not grant production authority by itself."
    },
    {
      "question": "Why is 'Prompt Engineering is Software Engineering' the central thesis?",
      "choices": [
        "Because prompts and their schemas, model settings, evidence policy, and evaluations form versioned release artifacts",
        "Because prompts require compilation",
        "Because it sounds good"
      ],
      "answer": 0,
      "explanation": "Software practices make changes attributable, testable, reviewable, observable, and reversible while governance supplies the required authority."
    }
  ]
};
