# Evaluation

"It seems good" is not enough. You need quantitative metrics to know if your RAG system actually works — and to catch regressions when you change chunking, retrieval, or prompts.

## Why evaluate?

```
Change chunk size 512 → 256
         │
         ▼
Did context_recall improve? Did faithfulness drop?
         │
         ▼
Without eval → you're guessing
With eval    → data-driven decisions
```

## The 4 RAGAS metrics

### Faithfulness
**Question:** Is every claim in the answer supported by the retrieved context?

```
Context: "Paris is the capital of France."
Answer:  "Paris is the capital of France and has 12 million people."
Score:   0.5 — "12 million" is not in context (hallucination)
```

### Answer Relevancy
**Question:** Does the answer actually address the question?

```
Question: "What is the capital of France?"
Answer:  "France is in Western Europe."
Score:   0.3 — related but doesn't answer the question
```

### Context Precision
**Question:** Are the retrieved chunks actually relevant?

```
Retrieved: [France capital chunk, WWII chunk, Python chunk]
Relevant:  [France capital chunk]
Score:     0.33 — 1 of 3 chunks is useful
```

### Context Recall
**Question:** Did we retrieve the chunks needed to answer?

```
Ground truth: "Paris"
Retrieved chunks contain "Paris": Yes → 1.0
Retrieved chunks contain "Paris": No  → 0.0
```

## Building a test set

SQuAD 2.0 is ideal because it provides question + answer + context triples:

```python
testset = load_squad_testset(sample_size=20)
# Each item: {question, ground_truth, context, title}
```

Our bundled fallback has **50 QA pairs** across 5 Wikipedia articles — enough for seminar evaluation.

## Running evaluation

```bash
make eval
# or
uv run python scripts/04_evaluation.py
```

Or use the **Eval Dashboard** tab in the Gradio app.

## Acceptable score ranges

| Metric | Poor | OK | Good | Excellent |
|--------|------|-----|------|-----------|
| faithfulness | < 0.7 | 0.7-0.8 | 0.8-0.9 | > 0.9 |
| answer_relevancy | < 0.6 | 0.6-0.7 | 0.7-0.8 | > 0.8 |
| context_precision | < 0.5 | 0.5-0.7 | 0.7-0.8 | > 0.8 |
| context_recall | < 0.5 | 0.5-0.7 | 0.7-0.8 | > 0.8 |

## Fallback metrics (no API keys)

When RAGAS can't run (no LLM for judging), we fall back to:

- **Token F1** — overlap between predicted and ground truth answer
- **Exact match** — normalized string equality
- **Context recall** — ground truth appears in retrieved chunks

## Using scores to tune

```
Low context_recall → increase chunk overlap, try hybrid retrieval, increase top_k
Low context_precision → add reranking, reduce top_k, reduce chunk size
Low faithfulness → tighten prompt, reduce top_k after rerank
Low answer_relevancy → check if retrieval finds right topic at all
```

Next: [Do's and Don'ts →](07_dos_and_donts.md)
