# Pre-Ship RAG Validation Checklist

Use this checklist before deploying any RAG system to production or presenting your seminar demo.

## Data & Ingestion

- [ ] Documents are cleaned (headers, footers, page numbers removed)
- [ ] No duplicate documents in the corpus
- [ ] Every chunk has source metadata (title, file, page, URL)
- [ ] Chunk size tested with evaluation metrics (512 tokens ≈ 350 words is a good start)
- [ ] Fallback data works with zero API keys

## Retrieval

- [ ] Hybrid retrieval (dense + BM25) tested against dense-only
- [ ] Top-K retrieve set to 10, rerank to 3
- [ ] Retrieved chunks logged for sample queries
- [ ] Edge cases tested: rare terms, acronyms, numbers, names
- [ ] Empty retrieval handled gracefully

## Generation

- [ ] Prompt explicitly constrains answers to provided context only
- [ ] "I don't know" response works when context is insufficient
- [ ] No hallucination on out-of-domain questions (manual spot check)
- [ ] Rate limit handling tested (429 errors don't crash the app)

## Evaluation

- [ ] Golden test set created (minimum 20 QA pairs)
- [ ] RAGAS scores recorded as baseline
- [ ] Faithfulness ≥ 0.7 (or fallback F1 ≥ 0.5 without API keys)
- [ ] Context recall ≥ 0.5 (retrieval finds answer-bearing chunks)
- [ ] Eval re-run after every pipeline change

## Application

- [ ] Gradio app starts on port 7860
- [ ] File upload indexes successfully (PDF, TXT, MD)
- [ ] Chunk inspector shows before/after reranking
- [ ] Eval dashboard runs without crashing
- [ ] Error messages are user-friendly

## CI & Codespaces

- [ ] `make test` passes with no API keys (local fallback)
- [ ] Codespace post-create script completes in < 5 minutes
- [ ] Jupyter kernel "RAG Seminar" registered
- [ ] All 5 notebooks run independently

## Sign-off

| Check | Owner | Date | Pass/Fail |
|-------|-------|------|-----------|
| Ingestion | | | |
| Retrieval | | | |
| Generation | | | |
| Evaluation | | | |
| App | | | |
| CI | | | |
