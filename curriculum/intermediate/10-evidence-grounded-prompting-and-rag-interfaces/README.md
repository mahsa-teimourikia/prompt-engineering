# 10 — Evidence-Grounded Prompting and RAG Interfaces

## Learning Objectives
- **Mitigate Hallucinations:** Ground LLM responses strictly in retrieved data rather than its pre-trained parametric memory.
- **Architect RAG Pipelines:** Understand the separation between the Retrieval phase (database search) and the Generation phase (prompting).
- **Enforce Citation Contracts:** Force the model to explicitly cite the document IDs it used to generate its answer.
- **Design Fallback States:** Program the model to safely say "I don't know" when the retrieved evidence is insufficient.

## Core Concepts & Workflow

LLMs are prone to hallucination because they are designed to predict plausible text, not to retrieve facts. If you ask an LLM a question about your private company policy, it will confidently guess.

Retrieval-Augmented Generation (RAG) solves this by splitting the problem. 
1. **Retrieval:** The application searches a database (often a Vector DB) for documents relevant to the user's query.
2. **Generation:** The application injects those documents into the prompt as `<evidence>` and strictly instructs the LLM: "Answer the user's query using *only* the provided evidence. If the answer is not in the evidence, output 'UNKNOWN'."

The LLM is no longer acting as an encyclopedia; it is acting as a reading comprehension engine.

![RAG Workflow](./diagram-1.svg)

## Technology Landscape and State of the Art

**Foundational:** Hoping the model knows the answer, or blindly appending a single text file to the prompt.

**Current State of the Art:**
1. **Vector Databases:** Tools like **Pinecone**, **Milvus**, or **Weaviate** are used to perform semantic similarity searches across massive document corpuses in milliseconds.
2. **Orchestration Frameworks:** Libraries like **[LlamaIndex](https://www.llamaindex.ai/)** or LangChain provide the pipeline logic to chunk documents, embed them, retrieve them, and format the final RAG prompt.
3. **Advanced Retrieval:** Simple RAG often fails on complex queries. SOTA systems use Hybrid Search (keyword + vector), Re-ranking models (like Cohere Rerank), and query-rewriting to ensure the injected evidence is actually relevant.
4. **Citation Extraction:** Modern RAG prompts require the model to output a structured JSON response containing both the `answer` and an array of `source_ids` to prove where it got the information.

## Lab and Production

### The Lab
The [notebook](10_evidence_grounded_prompting_and_rag_interfaces.ipynb) simulates the Generation phase of RAG. It passes a strict instruction contract, a user query, and a block of simulated retrieved evidence. It demonstrates a success case where the model cites the evidence, and crucially, a failure case where the evidence is missing, proving that the strict contract forces the model to safely abstain rather than hallucinate.

### Production Best Practices
- **Data Access Control:** The LLM cannot enforce security. Your retrieval code must filter the vector search so that Customer A's documents are never retrieved and injected into a prompt for Customer B.
- **Garbage In, Garbage Out:** If your retrieval step returns irrelevant documents, the LLM will fail. RAG optimization usually requires fixing the search algorithm, not rewriting the prompt.
- **Measure Groundedness:** Use evaluation frameworks (like Ragas) to score whether the LLM's answer is factually grounded in the provided context or if it hallucinated external information.
