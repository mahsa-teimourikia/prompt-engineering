export const lessons = [
  {
    "id": "behavior",
    "level": "Beginner",
    "step": 1,
    "slug": "llm-behavior-and-prompt-anatomy",
    "title": "LLM Behavior and Prompt Anatomy",
    "summary": "Understand the fundamental structure of a prompt payload.",
    "outcome": "Deconstruct prompts into System Instructions, Context, and User Input, and diagnose stateless failures.",
    "material": "curriculum/beginner/01-llm-behavior-and-prompt-anatomy/README.md",
    "notebook": "curriculum/beginner/01-llm-behavior-and-prompt-anatomy/llm_behavior_and_prompt_anatomy.ipynb",
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
    "summary": "Move from polite requests to rigid engineering contracts.",
    "outcome": "Define exact inputs, constraints, and fallback paths to eliminate ambiguity.",
    "material": "curriculum/beginner/02-instruction-contracts/README.md",
    "notebook": "curriculum/beginner/02-instruction-contracts/instruction_contracts.ipynb",
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
    "summary": "Guide models using demonstration rather than just description.",
    "outcome": "Implement strict Few-Shot examples to anchor tone, schema, and boundary behavior.",
    "material": "curriculum/beginner/03-constraints-examples-and-few-shot-learning/README.md",
    "notebook": "curriculum/beginner/03-constraints-examples-and-few-shot-learning/constraints_examples_and_few_shot_learning.ipynb",
    "refs": []
  },
  {
    "id": "structured",
    "level": "Beginner",
    "step": 4,
    "slug": "structured-outputs-and-typed-interfaces",
    "title": "Structured Outputs and Typed Interfaces",
    "summary": "Force LLMs to return parseable data structures.",
    "outcome": "Use native JSON mode and strict schemas to guarantee application-readable output.",
    "material": "curriculum/beginner/04-structured-outputs-and-typed-interfaces/README.md",
    "notebook": "curriculum/beginner/04-structured-outputs-and-typed-interfaces/structured_outputs_and_typed_interfaces.ipynb",
    "refs": []
  },
  {
    "id": "patterns",
    "level": "Beginner",
    "step": 5,
    "slug": "prompt-patterns-and-technique-selection",
    "title": "Prompt Patterns and Technique Selection",
    "summary": "Map specific failures to specific prompt techniques.",
    "outcome": "Avoid pattern bloat by selecting only the techniques required to fix a measured failure.",
    "material": "curriculum/beginner/05-prompt-patterns-and-technique-selection/README.md",
    "notebook": "curriculum/beginner/05-prompt-patterns-and-technique-selection/prompt_patterns_and_technique_selection.ipynb",
    "refs": []
  },
  {
    "id": "reasoning",
    "level": "Intermediate",
    "step": 6,
    "slug": "reasoning-oriented-prompting",
    "title": "Reasoning-Oriented Prompting",
    "summary": "Trade latency for accuracy using Chain-of-Thought.",
    "outcome": "Force the model to emit intermediate reasoning tokens before generating a final answer.",
    "material": "curriculum/intermediate/06-reasoning-oriented-prompting/README.md",
    "notebook": "curriculum/intermediate/06-reasoning-oriented-prompting/reasoning_oriented_prompting.ipynb",
    "refs": [
      {
        "title": "O1 Native Reasoning",
        "path": "https://openai.com/index/learning-to-reason-with-llms/"
      }
    ]
  },
  {
    "id": "workflow",
    "level": "Intermediate",
    "step": 7,
    "slug": "task-decomposition-and-workflow-prompting",
    "title": "Task Decomposition and Workflow Prompting",
    "summary": "Break massive prompts into narrow, specialized pipelines.",
    "outcome": "Orchestrate state machines to prevent compounding errors in complex tasks.",
    "material": "curriculum/intermediate/07-task-decomposition-and-workflow-prompting/README.md",
    "notebook": "curriculum/intermediate/07-task-decomposition-and-workflow-prompting/task_decomposition_and_workflow_prompting.ipynb",
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
    "summary": "Safely inject background data into the prompt context.",
    "outcome": "Use XML delimiters and pruning strategies to manage massive context windows.",
    "material": "curriculum/intermediate/08-context-engineering/README.md",
    "notebook": "curriculum/intermediate/08-context-engineering/context_engineering.ipynb",
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
    "summary": "Manage state across multi-turn chat sessions.",
    "outcome": "Implement sliding windows and background summarization to prevent context collapse.",
    "material": "curriculum/intermediate/09-conversation-and-long-context-engineering/README.md",
    "notebook": "curriculum/intermediate/09-conversation-and-long-context-engineering/conversation_and_long_context_engineering.ipynb",
    "refs": []
  },
  {
    "id": "rag",
    "level": "Intermediate",
    "step": 10,
    "slug": "evidence-grounded-prompting-and-rag-interfaces",
    "title": "Evidence-Grounded Prompting and RAG Interfaces",
    "summary": "Ground answers in private database retrieval.",
    "outcome": "Design strict citation contracts that force the model to hallucinate less and say 'I don't know' more.",
    "material": "curriculum/intermediate/10-evidence-grounded-prompting-and-rag-interfaces/README.md",
    "notebook": "curriculum/intermediate/10-evidence-grounded-prompting-and-rag-interfaces/evidence_grounded_prompting_and_rag_interfaces.ipynb",
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
    "summary": "Give models the ability to execute external code.",
    "outcome": "Design clear function schemas and secure application-side execution loops.",
    "material": "curriculum/intermediate/11-tool-calling-and-tool-interface-design/README.md",
    "notebook": "curriculum/intermediate/11-tool-calling-and-tool-interface-design/tool_calling_and_tool_interface_design.ipynb",
    "refs": []
  },
  {
    "id": "multimodal",
    "level": "Intermediate",
    "step": 12,
    "slug": "multimodal-prompt-engineering",
    "title": "Multimodal Prompt Engineering",
    "summary": "Interleave images, video, and audio directly into the prompt.",
    "outcome": "Use text anchors to ground the model's spatial and temporal reasoning over media.",
    "material": "curriculum/intermediate/12-multimodal-prompt-engineering/README.md",
    "notebook": "curriculum/intermediate/12-multimodal-prompt-engineering/multimodal_prompt_engineering.ipynb",
    "refs": []
  },
  {
    "id": "security",
    "level": "Intermediate",
    "step": 13,
    "slug": "prompt-security-and-untrusted-content",
    "title": "Prompt Security and Untrusted Content",
    "summary": "Defend against prompt injection and context poisoning.",
    "outcome": "Isolate untrusted data using strict delimiters and outbound schema enforcement.",
    "material": "curriculum/intermediate/13-prompt-security-and-untrusted-content/README.md",
    "notebook": "curriculum/intermediate/13-prompt-security-and-untrusted-content/prompt_security_and_untrusted_content.ipynb",
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
    "summary": "Replace vibe checks with automated, deterministic regression testing.",
    "outcome": "Build massive Golden Datasets to mathematically prove prompt efficacy.",
    "material": "curriculum/advanced/14-prompt-evaluation/README.md",
    "notebook": "curriculum/advanced/14-prompt-evaluation/prompt_evaluation.ipynb",
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
    "summary": "Use models to grade other models.",
    "outcome": "Design strict rubrics and calibrate LLM judges against human-expert baselines.",
    "material": "curriculum/advanced/15-llm-as-a-judge-and-human-evaluation/README.md",
    "notebook": "curriculum/advanced/15-llm-as-a-judge-and-human-evaluation/llm_as_a_judge_and_human_evaluation.ipynb",
    "refs": []
  },
  {
    "id": "optimization",
    "level": "Advanced",
    "step": 16,
    "slug": "evaluation-driven-prompt-optimization",
    "title": "Evaluation-Driven Prompt Optimization",
    "summary": "Treat prompt engineering as a gradient descent problem.",
    "outcome": "Iteratively tune prompts based solely on automated evaluation metrics.",
    "material": "curriculum/advanced/16-evaluation-driven-prompt-optimization/README.md",
    "notebook": "curriculum/advanced/16-evaluation-driven-prompt-optimization/evaluation_driven_prompt_optimization.ipynb",
    "refs": []
  },
  {
    "id": "dspy",
    "level": "Advanced",
    "step": 17,
    "slug": "automatic-prompt-optimization-and-dspy",
    "title": "Automatic Prompt Optimization and DSPy",
    "summary": "Automate prompt generation entirely.",
    "outcome": "Use frameworks like DSPy to compile and optimize prompt strings algorithmically.",
    "material": "curriculum/advanced/17-automatic-prompt-optimization-and-dspy/README.md",
    "notebook": "curriculum/advanced/17-automatic-prompt-optimization-and-dspy/automatic_prompt_optimization_and_dspy.ipynb",
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
    "summary": "Design autonomous loops that plan, reflect, and act.",
    "outcome": "Define explicit personas and constraints to govern multi-agent collaboration.",
    "material": "curriculum/advanced/18-agent-and-multi-agent-prompt-contracts/README.md",
    "notebook": "curriculum/advanced/18-agent-and-multi-agent-prompt-contracts/agent_and_multi_agent_prompt_contracts.ipynb",
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
    "summary": "Optimize prompts for code generation and software architecture.",
    "outcome": "Use strict test-driven development constraints to prevent syntactic hallucinations.",
    "material": "curriculum/advanced/19-prompting-for-coding-agents/README.md",
    "notebook": "curriculum/advanced/19-prompting-for-coding-agents/prompting_for_coding_agents.ipynb",
    "refs": []
  },
  {
    "id": "models",
    "level": "Advanced",
    "step": 20,
    "slug": "model-aware-prompt-engineering",
    "title": "Model-Aware Prompt Engineering",
    "summary": "Understand the differing inductive biases of foundational models.",
    "outcome": "Tailor prompts specifically for the quirks of Claude, GPT, or Gemini.",
    "material": "curriculum/advanced/20-model-aware-prompt-engineering/README.md",
    "notebook": "curriculum/advanced/20-model-aware-prompt-engineering/model_aware_prompt_engineering.ipynb",
    "refs": []
  },
  {
    "id": "efficiency",
    "level": "Advanced",
    "step": 21,
    "slug": "cost-latency-and-token-engineering",
    "title": "Cost, Latency, and Token Engineering",
    "summary": "Optimize the financial and temporal costs of prompts.",
    "outcome": "Implement Context Caching and token pruning strategies at scale.",
    "material": "curriculum/advanced/21-cost-latency-and-token-engineering/README.md",
    "notebook": "curriculum/advanced/21-cost-latency-and-token-engineering/cost_latency_and_token_engineering.ipynb",
    "refs": []
  },
  {
    "id": "promptops",
    "level": "Enterprise",
    "step": 22,
    "slug": "promptops",
    "title": "PromptOps",
    "summary": "Integrate prompt engineering into traditional CI/CD pipelines.",
    "outcome": "Block prompt deployments automatically if regression tests fail.",
    "material": "curriculum/enterprise/22-promptops/README.md",
    "notebook": "curriculum/enterprise/22-promptops/promptops.ipynb",
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
    "summary": "Implement distributed tracing for multi-step LLM workflows.",
    "outcome": "Capture inputs, outputs, and token costs at every node to diagnose silent failures.",
    "material": "curriculum/enterprise/23-prompt-observability-and-failure-diagnosis/README.md",
    "notebook": "curriculum/enterprise/23-prompt-observability-and-failure-diagnosis/prompt_observability_and_failure_diagnosis.ipynb",
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
    "summary": "Execute shadow deployments and A/B tests in production.",
    "outcome": "Gradually shift traffic to new prompt versions without risking catastrophic failure.",
    "material": "curriculum/enterprise/24-prompt-versioning-experimentation-and-release-engineering/README.md",
    "notebook": "curriculum/enterprise/24-prompt-versioning-experimentation-and-release-engineering/prompt_versioning_experimentation_and_release_engineering.ipynb",
    "refs": []
  },
  {
    "id": "governance",
    "level": "Enterprise",
    "step": 25,
    "slug": "prompt-governance-and-responsible-ai",
    "title": "Prompt Governance and Responsible AI",
    "summary": "Automatically redact PII and enforce toxic content guardrails.",
    "outcome": "Align prompt engineering with strict corporate and legal compliance policies.",
    "material": "curriculum/enterprise/25-prompt-governance-and-responsible-ai/README.md",
    "notebook": "curriculum/enterprise/25-prompt-governance-and-responsible-ai/prompt_governance_and_responsible_ai.ipynb",
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
    "summary": "Design UI friction for high-stakes AI decisions.",
    "outcome": "Counteract automation bias by explicitly signaling model uncertainty to the user.",
    "material": "curriculum/enterprise/26-human-centred-ai-and-trust-calibration/README.md",
    "notebook": "curriculum/enterprise/26-human-centred-ai-and-trust-calibration/human_centred_ai_and_trust_calibration.ipynb",
    "refs": []
  },
  {
    "id": "portability",
    "level": "Enterprise",
    "step": 27,
    "slug": "prompt-portability-and-multi-model-systems",
    "title": "Prompt Portability and Multi-Model Systems",
    "summary": "Abstract model-specific APIs behind unified contract layers.",
    "outcome": "Build resilient systems that automatically failover to backup providers.",
    "material": "curriculum/enterprise/27-prompt-portability-and-multi-model-systems/README.md",
    "notebook": "curriculum/enterprise/27-prompt-portability-and-multi-model-systems/prompt_portability_and_multi_model_systems.ipynb",
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
    "summary": "Map strict business constraints to the appropriate AI architecture.",
    "outcome": "Minimize complexity: choose simple prompts over sprawling agents whenever possible.",
    "material": "curriculum/enterprise/28-prompt-architecture-patterns-and-system-selection/README.md",
    "notebook": "curriculum/enterprise/28-prompt-architecture-patterns-and-system-selection/prompt_architecture_patterns_and_system_selection.ipynb",
    "refs": []
  },
  {
    "id": "capstone",
    "level": "Enterprise",
    "step": 29,
    "slug": "ai-system-engineering-capstone",
    "title": "AI System Engineering Capstone",
    "summary": "Build Project Northstar, an end-to-end Enterprise AI system.",
    "outcome": "Synthesize routing, RAG, tools, evaluations, and governance into a single pipeline.",
    "material": "curriculum/enterprise/29-ai-system-engineering-capstone/README.md",
    "notebook": [
      {
        "title": "Milestone 1: Router",
        "path": "curriculum/enterprise/29-ai-system-engineering-capstone/01_routing_and_intent_classification.ipynb"
      },
      {
        "title": "Milestone 2: RAG",
        "path": "curriculum/enterprise/29-ai-system-engineering-capstone/02_retrieval_augmented_generation.ipynb"
      },
      {
        "title": "Milestone 3: Tools",
        "path": "curriculum/enterprise/29-ai-system-engineering-capstone/03_tool_calling_and_execution.ipynb"
      },
      {
        "title": "Milestone 4: Eval",
        "path": "curriculum/enterprise/29-ai-system-engineering-capstone/04_evaluation_and_optimization.ipynb"
      },
      {
        "title": "Milestone 5: Deploy",
        "path": "curriculum/enterprise/29-ai-system-engineering-capstone/05_deployment_and_governance.ipynb"
      }
    ],
    "refs": []
  }
];

export const checks = {
  "behavior": [
    {
      "question": "Why is 'The prompt used to work' not a valid diagnosis for a failure?",
      "choices": [
        "Models are deterministic",
        "The entire request packet, context, and decoding params must be analyzed",
        "Prompts don't change behavior"
      ],
      "answer": 1,
      "explanation": "A production response is conditional generation inside a whole request packet. You must isolate what changed."
    },
    {
      "question": "Why do LLMs require the entire conversation history injected into every request?",
      "choices": [
        "To save tokens",
        "Because they are stateless text prediction engines",
        "To train the model on your data"
      ],
      "answer": 1,
      "explanation": "LLMs do not 'remember' you between requests. Every API call must contain the entire state of the world."
    }
  ],
  "contracts": [
    {
      "question": "What is the primary flaw of asking an LLM to 'write a good summary'?",
      "choices": [
        "It uses too many tokens",
        "'Good' is subjective, unmeasurable, and impossible to test",
        "Summaries are too hard for LLMs"
      ],
      "answer": 1,
      "explanation": "A contract requires measurable, binary boundaries rather than ambiguous adjectives."
    },
    {
      "question": "Why must an instruction contract explicitly define a fallback path?",
      "choices": [
        "To make the prompt longer",
        "To prevent the model from hallucinating a guess when facts are absent",
        "To save API costs"
      ],
      "answer": 1,
      "explanation": "Without a defined fallback (like 'Output UNKNOWN'), the model's natural behavior is to guess plausibly."
    }
  ],
  "examples": [
    {
      "question": "Why are Few-Shot examples superior to lengthy Zero-Shot instructions?",
      "choices": [
        "They consume fewer tokens",
        "They ground the model's output schema and tone far more effectively than abstract rules",
        "They require less engineering effort"
      ],
      "answer": 1,
      "explanation": "Models are pattern-matchers. Demonstrating the pattern is mathematically more effective than describing it."
    },
    {
      "question": "What happens if all your Few-Shot examples demonstrate 'success' paths and none demonstrate 'failure' paths?",
      "choices": [
        "The model will hallucinate success when faced with a failing input",
        "The model becomes more accurate",
        "Latency decreases"
      ],
      "answer": 0,
      "explanation": "The model learns the distribution of the examples. If it only sees positive responses, it becomes biased toward returning positive responses even for negative inputs."
    }
  ],
  "structured": [
    {
      "question": "Why is 'Return JSON' inside the prompt text considered an anti-pattern?",
      "choices": [
        "JSON is deprecated",
        "It relies on the model's language skills rather than native decoding enforcement",
        "It uses more tokens"
      ],
      "answer": 1,
      "explanation": "Modern APIs natively enforce JSON schemas directly in the decoding phase, which is vastly more reliable than asking politely in text."
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
        "A new type of model",
        "Blindly stacking techniques (like CoT + Few-Shot) on every prompt without measuring if they actually help",
        "A token limit error"
      ],
      "answer": 1,
      "explanation": "Adding every technique increases latency and obscures failure causes. Use only the simplest pattern required."
    },
    {
      "question": "When should you use a complex multi-stage prompt instead of a simple deterministic script?",
      "choices": [
        "Always",
        "Only when the task requires semantic flexibility that traditional code cannot handle",
        "When writing Python is too hard"
      ],
      "answer": 1,
      "explanation": "If a problem can be solved with Regex or an SQL query, do not use an LLM."
    }
  ],
  "reasoning": [
    {
      "question": "What is the primary trade-off of using Chain-of-Thought reasoning?",
      "choices": [
        "It lowers accuracy",
        "It significantly increases latency and cost",
        "It requires complex coding"
      ],
      "answer": 1,
      "explanation": "Every reasoning token generated is 'compute time' spent, which costs money and forces the user to wait longer."
    },
    {
      "question": "In a JSON schema enforcing reasoning, why must the 'reasoning' field come BEFORE the 'answer' field?",
      "choices": [
        "JSON formatting rules",
        "Because LLMs generate sequentially; if the answer comes first, the reasoning is just post-hoc justification",
        "It saves tokens"
      ],
      "answer": 1,
      "explanation": "The model must generate the intermediate logic tokens *before* it predicts the final answer token to benefit from CoT."
    }
  ],
  "workflow": [
    {
      "question": "What happens when you give an LLM a massive 10-step instruction list?",
      "choices": [
        "It executes it perfectly",
        "It suffers from 'attention dilution' and will silently skip steps",
        "It crashes the API"
      ],
      "answer": 1,
      "explanation": "Models struggle to adhere to long, complex instruction sets. Decomposition is required for reliability."
    },
    {
      "question": "In a multi-stage workflow, why use programmatic 'if/else' routing between models instead of an LLM router?",
      "choices": [
        "To increase complexity",
        "Because deterministic code is faster, cheaper, and 100% reliable",
        "LLMs can't route data"
      ],
      "answer": 1,
      "explanation": "Never use a probabilistic LLM to route data if a simple Python script can reliably evaluate the state."
    }
  ],
  "context": [
    {
      "question": "What is the 'Lost in the Middle' phenomenon?",
      "choices": [
        "A network timeout error",
        "Models paying high attention to the start and end of a prompt, but ignoring data in the center",
        "A symptom of low temperature"
      ],
      "answer": 1,
      "explanation": "Long-context models struggle to retrieve facts buried deep in the middle of massive context blocks."
    },
    {
      "question": "Where should the final instructions be placed relative to a massive injected document?",
      "choices": [
        "At the very beginning",
        "In the middle",
        "At the very end, closest to generation"
      ],
      "answer": 2,
      "explanation": "Placing instructions immediately before the model's generation turn maximizes adherence."
    }
  ],
  "conversation": [
    {
      "question": "How do LLMs actually 'remember' a conversation?",
      "choices": [
        "They learn from each turn",
        "The application developer appends the new message to a massive array and resends the entire history",
        "They use a hidden SQL database"
      ],
      "answer": 1,
      "explanation": "Memory is an illusion created by injecting the entire growing transcript back into the stateless model on every turn."
    },
    {
      "question": "As a conversation history grows extremely long, what often happens to the System Instructions?",
      "choices": [
        "They are prioritized",
        "The model 'forgets' them because they are pushed too far back in the context window",
        "They become cheaper to run"
      ],
      "answer": 1,
      "explanation": "System prompt reinforcement (reminding the model of its rules at the end of the transcript) is required for long chats."
    }
  ],
  "rag": [
    {
      "question": "What is the fundamental purpose of RAG?",
      "choices": [
        "To train a model on your data",
        "To ground answers strictly in retrieved evidence rather than the model's pre-trained parametric memory",
        "To search the internet"
      ],
      "answer": 1,
      "explanation": "RAG turns the LLM from a hallucinating encyclopedia into a strict reading comprehension engine."
    },
    {
      "question": "If a RAG system outputs garbage, where is the failure usually located?",
      "choices": [
        "The LLM generation step",
        "The Retrieval step returning irrelevant documents",
        "The system prompt"
      ],
      "answer": 1,
      "explanation": "Garbage In, Garbage Out. If the vector search fails to retrieve relevant data, the LLM cannot answer correctly."
    }
  ],
  "tools": [
    {
      "question": "How does an LLM execute a Python function?",
      "choices": [
        "It runs Python natively",
        "It generates a JSON payload representing the arguments, pauses, and waits for the application to run the code and return the result",
        "It sends an HTTP request"
      ],
      "answer": 1,
      "explanation": "Models are trapped in a text box. They only generate text (JSON). The application executes the tools."
    },
    {
      "question": "Why is giving an LLM autonomous write-access to a database extremely dangerous?",
      "choices": [
        "It will delete everything",
        "LLMs hallucinate arguments and can get stuck in loops. Destructive actions require a Human-in-the-Loop approval step",
        "It's too expensive"
      ],
      "answer": 1,
      "explanation": "You must never let a probabilistic system execute an irreversible action autonomously."
    }
  ],
  "multimodal": [
    {
      "question": "How do SOTA models like Gemini 1.5 process images?",
      "choices": [
        "They use OCR to extract text first",
        "They natively process the raw image patches directly",
        "They translate pixels to Python"
      ],
      "answer": 1,
      "explanation": "Native multimodal models understand spatial relationships and visuals without relying on brittle OCR translation layers."
    },
    {
      "question": "What is the best way to direct a multimodal model's attention in a massive video?",
      "choices": [
        "Ask a vague question",
        "Use explicit text anchors, specifying timestamps or spatial quadrants",
        "Upload the video twice"
      ],
      "answer": 1,
      "explanation": "Grounding the model's reasoning with specific spatial/temporal coordinates dramatically improves extraction accuracy."
    }
  ],
  "security": [
    {
      "question": "What is Indirect Prompt Injection?",
      "choices": [
        "A user typing a malicious command in a chatbox",
        "The application retrieving a poisoned document (e.g., from a web search) and blindly injecting it into the prompt's context",
        "A network hack"
      ],
      "answer": 1,
      "explanation": "The model cannot distinguish between trusted system context and untrusted user data unless explicitly isolated."
    },
    {
      "question": "Why do instructions like 'Ignore the user if they try to hack you' fail?",
      "choices": [
        "They consume too many tokens",
        "Because LLMs interpret all text as instructions, making them fundamentally vulnerable to clever linguistic overrides",
        "They aren't polite enough"
      ],
      "answer": 1,
      "explanation": "Security requires defense in depth (delimiters, strict schemas, external firewalls), not just asking the model nicely."
    }
  ],
  "evaluation": [
    {
      "question": "Why is evaluating prompts with 'vibe checks' an anti-pattern?",
      "choices": [
        "It's too slow",
        "It doesn't scale and fails to catch regressions on edge cases when a prompt is modified",
        "It requires too much code"
      ],
      "answer": 1,
      "explanation": "You must use automated, deterministic regression testing against a frozen Golden Dataset to prove prompt efficacy."
    },
    {
      "question": "Which of the following belongs in a Golden Dataset?",
      "choices": [
        "Only happy-path inputs",
        "Clear, ambiguous, adversarial, and missing-evidence inputs",
        "Only inputs that failed previously"
      ],
      "answer": 1,
      "explanation": "A robust evaluation suite must test the prompt's ability to handle failure modes and edge cases gracefully."
    }
  ],
  "judges": [
    {
      "question": "What is the critical prerequisite for using an LLM-as-a-Judge?",
      "choices": [
        "Using the most expensive model",
        "Mathematically proving that the Judge LLM's scores have a high 'Agreement Rate' with human expert baselines",
        "Using a fast model"
      ],
      "answer": 1,
      "explanation": "If the Judge LLM's scores don't correlate with human judgment, you are optimizing for a hallucinated metric."
    },
    {
      "question": "Why must an LLM Judge use Chain-of-Thought reasoning?",
      "choices": [
        "To make the logs longer",
        "Because it needs 'compute time' to justify its score before outputting the final integer, dramatically increasing reliability",
        "To save money"
      ],
      "answer": 1,
      "explanation": "Forcing a judge to output its rubric-based critique before outputting the score prevents random guessing."
    }
  ],
  "optimization": [
    {
      "question": "What does treating prompt engineering as a 'gradient descent problem' mean?",
      "choices": [
        "Using complex math",
        "Iteratively tuning prompts based solely on automated evaluation metrics rather than manual guessing",
        "Optimizing the server architecture"
      ],
      "answer": 1,
      "explanation": "You measure the baseline, change the prompt, run the eval, and keep the prompt only if the metric goes up."
    },
    {
      "question": "Why should you never optimize a prompt to fix a single reported bug without running a full regression suite?",
      "choices": [
        "It takes too long",
        "Fixing the prompt for one edge case will often silently break 100 other cases in production",
        "It wastes tokens"
      ],
      "answer": 1,
      "explanation": "Prompt changes have cascading semantic effects. You must prove the change didn't cause a regression."
    }
  ],
  "dspy": [
    {
      "question": "What is the primary value proposition of DSPy?",
      "choices": [
        "It makes models run faster",
        "It automates prompt generation by compiling declarative signatures into optimized prompt strings algorithmically",
        "It replaces Python"
      ],
      "answer": 1,
      "explanation": "DSPy abstracts away manual prompt tweaking, letting an optimizer search for the best prompt based on your metrics."
    },
    {
      "question": "In DSPy, what replaces the manual 'Prompt String'?",
      "choices": [
        "A Signature (defining inputs/outputs) and a Teleprompter (optimizer)",
        "A JSON file",
        "A larger LLM"
      ],
      "answer": 0,
      "explanation": "You define the *contract* (signature), and DSPy figures out the best English words to make the model fulfill that contract."
    }
  ],
  "agents": [
    {
      "question": "What defines an 'Agentic' workflow compared to a standard workflow?",
      "choices": [
        "It uses OpenAI",
        "It features autonomous loops where the model can plan, use tools, reflect, and act without hardcoded transitions",
        "It has a chat UI"
      ],
      "answer": 1,
      "explanation": "Agents possess agency. They decide the control flow dynamically based on the tool results they observe."
    },
    {
      "question": "Why do multi-agent systems often fail in production?",
      "choices": [
        "They are too deterministic",
        "They get stuck in infinite reflection loops or veer completely off task due to compounding hallucinations",
        "They are too fast"
      ],
      "answer": 1,
      "explanation": "Autonomous loops are highly unstable. Strict state-machine guardrails (like LangGraph) are required to keep them on track."
    }
  ],
  "coding": [
    {
      "question": "Why is Test-Driven Development (TDD) critical for Coding Agents?",
      "choices": [
        "To write documentation",
        "Because syntactic hallucinations will crash code. The agent must compile/test its code in a sandbox and reflect on the errors to fix them",
        "To save tokens"
      ],
      "answer": 1,
      "explanation": "LLMs cannot write flawless code zero-shot. They need an execution loop to verify syntax and logic."
    },
    {
      "question": "What is the danger of letting an LLM write code directly to production?",
      "choices": [
        "It's not dangerous",
        "It can introduce severe security vulnerabilities, infinite loops, or wipe databases",
        "It makes the codebase too large"
      ],
      "answer": 1,
      "explanation": "Code generation must be heavily sandboxed and subjected to traditional human code review."
    }
  ],
  "models": [
    {
      "question": "What does it mean that models have differing 'inductive biases'?",
      "choices": [
        "They cost different amounts",
        "They respond differently to the same prompt formatting (e.g., Claude prefers XML, GPT prefers Markdown)",
        "They use different programming languages"
      ],
      "answer": 1,
      "explanation": "A highly optimized prompt for one model family will often perform poorly on a competitor's model without refactoring."
    },
    {
      "question": "Why is portability a challenge in prompt engineering?",
      "choices": [
        "You can't copy text",
        "Because moving from a 70B model to an 8B model requires fundamentally simpler prompts and tighter schemas to succeed",
        "API keys change"
      ],
      "answer": 1,
      "explanation": "Smaller models have less reasoning capacity and require much more rigid instruction contracts."
    }
  ],
  "efficiency": [
    {
      "question": "What is Context Caching?",
      "choices": [
        "Saving the prompt in a local database",
        "Uploading massive context to the provider once, and executing subsequent queries against that frozen memory to slash cost and latency",
        "Deleting old messages"
      ],
      "answer": 1,
      "explanation": "Context Caching allows for near-instant responses on massive documents (like codebases or books)."
    },
    {
      "question": "How do you minimize token costs in a RAG pipeline?",
      "choices": [
        "By switching to a smaller model",
        "By aggressively pre-processing and stripping noise/HTML from the retrieved documents before injecting them",
        "By ignoring the context"
      ],
      "answer": 1,
      "explanation": "Injecting massive, messy logs wastes money. Clean your data before sending it to the LLM."
    }
  ],
  "promptops": [
    {
      "question": "What is the core philosophy of PromptOps?",
      "choices": [
        "Prompts are just text files",
        "Prompt engineering is software engineering; prompts must pass strict CI/CD pipelines before deployment",
        "Prompts should be edited live in production"
      ],
      "answer": 1,
      "explanation": "Treating prompts as versioned, tested artifacts prevents catastrophic regressions."
    },
    {
      "question": "Why should you never hardcode a prompt string deep in a Python business logic file?",
      "choices": [
        "It's too hard to read",
        "It couples the deployment of the application to the tweaking of the prompt, preventing non-engineers from iterating safely",
        "Python doesn't support long strings"
      ],
      "answer": 1,
      "explanation": "Prompts should be extracted to configuration files or external registries for safe, decoupled versioning."
    }
  ],
  "observability": [
    {
      "question": "Why is HTTP 200 (Success) a dangerous metric for LLM APIs?",
      "choices": [
        "It's deprecated",
        "An LLM can return a HTTP 200 while delivering a catastrophic, confidently incorrect hallucination",
        "It means the API is down"
      ],
      "answer": 1,
      "explanation": "Infrastructure observability is insufficient. You need semantic observability to measure output quality."
    },
    {
      "question": "What does Distributed Tracing for LLMs accomplish?",
      "choices": [
        "It tracks network packets",
        "It captures the exact inputs, outputs, and token costs of every individual node in a complex multi-stage workflow",
        "It speeds up the model"
      ],
      "answer": 1,
      "explanation": "When an agent fails, tracing allows you to pinpoint exactly which intermediate reasoning step derailed the process."
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
      "explanation": "Shadow deployments allow you to test new prompts against real-world edge cases with zero risk to the end user."
    },
    {
      "question": "Why decouple prompt deployment from code deployment using feature flags?",
      "choices": [
        "To make the code larger",
        "It enables instant hot-swapping and automated rollbacks of a bad prompt without requiring a full Kubernetes microservice restart",
        "It uses fewer tokens"
      ],
      "answer": 1,
      "explanation": "Feature flags allow immediate, zero-downtime remediation of prompt failures."
    }
  ],
  "governance": [
    {
      "question": "Why must PII redaction occur BEFORE the API call?",
      "choices": [
        "To save tokens",
        "Because sending raw PII/PHI to a third-party LLM is a massive compliance violation (HIPAA/GDPR)",
        "The LLM will delete the data"
      ],
      "answer": 1,
      "explanation": "You cannot rely on the LLM to 'keep a secret'. The data must be scrubbed by deterministic code before it leaves your network."
    },
    {
      "question": "What is an Outbound Guardrail?",
      "choices": [
        "A firewall rule",
        "A secondary system that scans the LLM's response for toxicity or restricted topics before displaying it to the user",
        "A prompt instruction"
      ],
      "answer": 1,
      "explanation": "Outbound guardrails act as the final defense layer to catch hallucinations or policy violations that slipped past the primary model."
    }
  ],
  "trust": [
    {
      "question": "What is Automation Bias?",
      "choices": [
        "Robots doing manual labor",
        "The psychological tendency for humans to blindly trust highly confident automated systems, even when they hallucinate",
        "A bug in the code"
      ],
      "answer": 1,
      "explanation": "If you present a hallucination in a slick, authoritative UI, users will believe it. You must design to counteract this."
    },
    {
      "question": "What is 'Trust Calibration'?",
      "choices": [
        "Making the user trust the AI 100%",
        "Designing the UI so the user's trust exactly matches the AI's actual reliability on that specific task (e.g., highlighting uncertainty)",
        "A mathematical formula"
      ],
      "answer": 1,
      "explanation": "High-stakes tasks with low confidence should intentionally introduce UX friction (Human-in-the-Loop)."
    }
  ],
  "portability": [
    {
      "question": "How do you avoid Vendor Lock-In when building LLM apps?",
      "choices": [
        "By signing a long contract",
        "By abstracting provider-specific APIs behind unified contract layers (like LiteLLM) and standardizing on JSON schemas",
        "By using only one model"
      ],
      "answer": 1,
      "explanation": "Portability allows you to hot-swap models to leverage cost reductions or failover during outages."
    },
    {
      "question": "What must you do to ensure an automated fallback model is actually useful?",
      "choices": [
        "Assume it works",
        "Run your automated evaluation suite against the fallback model continuously to ensure it meets quality thresholds",
        "Pay for a premium tier"
      ],
      "answer": 1,
      "explanation": "Portability of code doesn't guarantee portability of capability. The backup model must still pass the math."
    }
  ],
  "architecture": [
    {
      "question": "What is the core principle of System Selection?",
      "choices": [
        "Always use the largest model",
        "Complexity is a liability; always select the simplest, most deterministic architecture that solves the business constraint",
        "Never use code"
      ],
      "answer": 1,
      "explanation": "Moving from Prompt -> RAG -> Agents incurs massive latency and cost taxes. Default to simplicity."
    },
    {
      "question": "What is a 'Compound AI System'?",
      "choices": [
        "A single massive prompt",
        "An architecture that mixes deterministic code, fast classifier LLMs, and heavy reasoning LLMs in a coordinated pipeline",
        "A chemical reaction"
      ],
      "answer": 1,
      "explanation": "SOTA engineering relies on compound systems to route queries efficiently rather than forcing one massive model to do everything."
    }
  ],
  "capstone": [
    {
      "question": "What is the ultimate goal of Project Northstar?",
      "choices": [
        "To build a chat bot",
        "To synthesize routing, RAG, tool calling, and governance into a production-grade, observable Compound AI System",
        "To test API keys"
      ],
      "answer": 1,
      "explanation": "The capstone proves you can integrate all the discrete layers of AI engineering into a single resilient architecture."
    },
    {
      "question": "Why is 'Prompt Engineering is Software Engineering' the central thesis?",
      "choices": [
        "Because it sounds good",
        "Because treating prompts as versioned, evaluated, and governed code is the only way to deploy AI safely at enterprise scale",
        "Because prompts require compilation"
      ],
      "answer": 1,
      "explanation": "Without the rigor of traditional software engineering (CI/CD, evals, observability), prompt engineering is just a hobby."
    }
  ]
};
