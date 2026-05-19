# Tutorial Index

Welcome to the **RAG From Scratch** seminar tutorial series. These guides complement the Jupyter notebooks with deeper explanations, tradeoffs, and best practices.

## Reading order

| # | Guide | What you'll learn |
|---|-------|-------------------|
| 00 | [Setup Guide](00_setup.md) | Codespace setup, API keys, verification |
| 01 | [What is RAG?](01_what_is_rag.md) | RAG fundamentals and when to use it |
| 02 | [Chunking Deep Dive](02_chunking_deep_dive.md) | Chunking strategies and tradeoffs |
| 03 | [Retrieval Deep Dive](03_retrieval_deep_dive.md) | Dense, sparse, and hybrid retrieval |
| 04 | [Reranking](04_reranking.md) | Why reranking matters and how it works |
| 05 | [Generation & Prompting](05_generation_prompting.md) | Prompt engineering for RAG |
| 06 | [Evaluation](06_evaluation.md) | RAGAS metrics and validation |
| 07 | [Do's and Don'ts](07_dos_and_donts.md) | Common mistakes and best practices |
| 08 | [Advanced Patterns](08_advanced_patterns.md) | HyDE, query rewriting, agentic RAG |

## Quick reference

```bash
make keys   # Check which API keys are configured
make nb     # Start Jupyter Lab
make app    # Start Gradio demo
make test   # Run all pipeline scripts
make eval   # Run evaluation on SQuAD subset
```

## Need help?

1. Run `make keys` to verify API configuration
2. Check [Do's and Don'ts](07_dos_and_donts.md) for common pitfalls
3. Use bundled fallback data in `data/fallback/` — no download required
