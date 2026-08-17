# 09 — Conversation and Long-Context Engineering

## Learning Objectives
- **Manage Conversational State:** Understand that LLM "memory" is simply appending previous messages to the current prompt.
- **Implement Sliding Windows:** Build programmatic logic to drop older messages when a conversation exceeds token limits.
- **Summarize History:** Use a secondary model call to compress long conversation histories into dense context blocks.
- **Maintain Instruction Adherence:** Prevent early system instructions from being "forgotten" as the chat history grows massively long.

## Core Concepts & Workflow

Chatbots seem magical because they "remember" what you said three turns ago. In reality, there is no magic memory. Every time you send a new message, the application developer is appending your new message to a massive array of *all previous messages* and sending the entire transcript back to the stateless LLM.

This creates a compounding problem: every turn of the conversation costs more tokens, takes longer to process, and pushes the foundational System Instructions further away from the model's immediate attention. Long-Context Engineering is the practice of managing this growing transcript—deciding when to prune old messages, when to summarize the history, and how to constantly remind the model of its core constraints.

![Conversation Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Appending messages to an array until the API throws a `TokenLimitExceeded` error, breaking the application.

**Current State of the Art:**
1. **SDK Chat Abstractions:** Modern SDKs (like the `google-genai` `chats` service) handle the basic array-appending automatically.
2. **Semantic Memory Systems:** Advanced chatbots use systems like **[Zep](https://www.getzep.com/)** or **Mem0** to extract facts from conversations, store them in a vector database, and dynamically inject them into the system prompt, rather than relying solely on raw transcript history.
3. **Context Caching for Chat:** For incredibly long sessions, developers use Context Caching to freeze the early parts of the conversation in memory, dramatically reducing the latency and cost of subsequent turns.

## Lab and Production

### The Lab
The [notebook](09_conversation_and_long_context_engineering.ipynb) builds a stateful conversation loop from scratch. It demonstrates how to append user and model roles to a history array, and implements a basic "sliding window" pruning algorithm that drops the oldest turns of the conversation once a specific token threshold is reached.

### Production Best Practices
- **System Prompt Reinforcement:** As history grows, models "forget" their system instructions. For critical constraints, dynamically append a short reminder (e.g., "Remember to output JSON") to the very last user message.
- **Summarization over Deletion:** Instead of just deleting old messages (which causes the bot to develop amnesia), trigger a background process to summarize the dropped messages into a dense `<historical_summary>` block injected into the context.
- **Isolate State:** The LLM's conversation history is untrusted user data. Do not rely on the chat history to store authorized state (like whether a user is authenticated). Track that in your application database.
