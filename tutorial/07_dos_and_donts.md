# Do's and Don'ts

A practical guide to common mistakes in RAG systems, organized by pipeline stage.

## Ingestion

### DO
- **Clean documents before ingesting** — Remove headers, footers, page numbers, navigation menus
- **Store source metadata with every chunk** — title, file path, page number, URL, timestamp
- **Test chunk sizes with eval metrics** — 512 tokens is a starting point, not a rule
- **Use the bundled fallback data for testing** — `data/fallback/squad_sample.json` always works

### DON'T
- **Ingest the same document twice** — Causes duplicate retrieval and inflated scores
- **Use enormous chunks (>2000 tokens)** — Dilutes relevance signal; the retriever can't pinpoint the answer
- **Skip metadata** — Without source info, you can't debug retrieval or show citations
- **Chunk PDFs without text extraction quality check** — Garbled OCR produces garbage chunks

## Retrieval

### DO
- **Start with top_k=10, rerank to top_k=3** — The standard production pattern
- **Use hybrid retrieval (dense + BM25)** — Catches both semantic and keyword matches
- **Log retrieved chunks for every query** — Use the Chunk Inspector or `print_retrieval_results()`
- **Test edge cases** — Rare terms, acronyms, numbers, proper nouns, misspellings

### DON'T
- **Use only cosine similarity for keyword-heavy queries** — "ISO 27001 compliance" needs BM25
- **Trust retrieval without inspecting chunks** — Always look at what's being retrieved
- **Set top_k too high (>20)** — More noise for the reranker and generator
- **Ignore empty retrieval** — Handle the case where no chunks pass the similarity threshold

## Generation

### DO
- **Constrain the model to context-only answers** — Explicit instructions in the prompt
- **Handle empty retrieval gracefully** — Return "I couldn't find relevant information"
- **Test out-of-domain questions** — "What's the weather?" should not hallucinate an answer
- **Use rate limit retry logic** — Our `fallback.py` handles 429 errors automatically

### DON'T
- **Let the model blend context with parametric knowledge** — This is the #1 RAG failure mode
- **Use the same prompt for all document types** — Legal docs vs chat logs need different instructions
- **Forget streaming for UX** — Enable `streaming=True` for chat interfaces
- **Ignore latency** — If generation takes >5s, users will leave

## Evaluation

### DO
- **Build a golden test set before shipping** — Minimum 20 diverse QA pairs
- **Run evals after every pipeline change** — Chunk size, top_k, prompt, model
- **Include hard questions** — Not just easy factoid lookups
- **Manual spot checks alongside metrics** — Faithfulness 0.95 can still miss subtle errors

### DON'T
- **Evaluate only on easy questions** — "What is the capital of France?" is too easy
- **Trust faithfulness > 0.9 without manual checks** — RAGAS can miss nuanced hallucinations
- **Compare scores across different test sets** — Keep the same test set for A/B comparisons
- **Skip evaluation because "it looks fine"** — Looks fine on 3 queries ≠ works on 1000

## Checklist summary

```
Before shipping:
  □ 20+ test questions with ground truth
  □ faithfulness ≥ 0.7
  □ context_recall ≥ 0.5
  □ Out-of-domain questions return "I don't know"
  □ Retrieval logged and inspectable
  □ Works with zero API keys (local fallback)
```

See also: [Validation Checklist](../docs/VALIDATION_CHECKLIST.md)

Next: [Advanced Patterns →](08_advanced_patterns.md)
