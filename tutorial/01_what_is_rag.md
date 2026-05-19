# What is RAG?

Retrieval-Augmented Generation (RAG) combines a **retrieval system** with a **language model** to answer questions using your own data.

## The problem RAG solves

Large language models have three fundamental limitations:

1. **Knowledge cutoff** — Models don't know about events after their training date
2. **Hallucination** — Models confidently generate false information
3. **Private data** — Models can't access your internal documents, databases, or wikis

RAG addresses all three by retrieving relevant documents at query time and grounding the model's answer in that context.

## The RAG pipeline

```
User Question
     │
     ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Embed Query │────▶│  Retrieve    │────▶│  Rerank     │
│  (vector)    │     │  Top-K chunks│     │  Top-3      │
└─────────────┘     └──────────────┘     └─────────────┘
                                               │
                                               ▼
                                        ┌─────────────┐
                                        │  Generate   │
                                        │  Answer     │
                                        │  (LLM)      │
                                        └─────────────┘
                                               │
                                               ▼
                                          Final Answer
                                     (grounded in context)
```

### Step by step

1. **Ingestion** — Load documents, split into chunks, embed, store in vector DB
2. **Retrieval** — Find chunks most similar to the user's question
3. **Reranking** — Re-score retrieved chunks for true relevance
4. **Generation** — LLM answers using only the retrieved context

## RAG vs fine-tuning vs in-context learning

| Approach | Best for | Cost | Updates |
|----------|----------|------|---------|
| **RAG** | Dynamic knowledge, Q&A over docs | Low | Add/remove docs anytime |
| **Fine-tuning** | Style, format, domain behavior | High | Requires retraining |
| **In-context learning** | Few-shot examples in prompt | Medium | Limited by context window |

**Use RAG when:** You have documents that change frequently, need citations, or want to avoid retraining.

**Use fine-tuning when:** You need the model to follow a specific output format or speak in a particular domain dialect.

## Real-world use cases

- **Customer support bots** — Answer from product docs and FAQs
- **Legal research** — Search case law and statutes
- **Internal knowledge bases** — Company wikis, HR policies, engineering runbooks
- **Medical Q&A** — Ground answers in clinical guidelines (with human review)
- **Code assistants** — Retrieve from codebase + documentation

## Key insight

RAG doesn't make the LLM smarter — it gives the LLM **the right information at the right time**. The quality of your RAG system depends almost entirely on:

1. How you chunk documents (see [Chunking Deep Dive](02_chunking_deep_dive.md))
2. How you retrieve chunks (see [Retrieval Deep Dive](03_retrieval_deep_dive.md))
3. How you prompt the model (see [Generation & Prompting](05_generation_prompting.md))

## Try it yourself

```bash
make app    # Open the Gradio chat interface
make test   # Run the full pipeline on bundled SQuAD data
```

Next: [Chunking Deep Dive →](02_chunking_deep_dive.md)
