# Reranking

Reranking is the step that takes your top-K retrieved chunks and re-orders them by true relevance. It's often the highest-ROI improvement you can make to a RAG system.

## Why retrieved order ≠ relevance order

Vector similarity (bi-encoder) compares query and document **independently**:

```
Bi-encoder (retrieval):
  Query  → [encoder] → vector_q
  Doc    → [encoder] → vector_d
  score = cosine(vector_q, vector_d)    ← fast, approximate

Cross-encoder (reranking):
  [Query + Doc together] → [encoder] → relevance score    ← slow, accurate
```

Bi-encoders are fast (can compare against millions of docs) but less accurate. Cross-encoders jointly process query + document and are much more accurate but too slow for full-corpus search.

**Solution:** Retrieve top-20 with bi-encoder (fast), rerank to top-3 with cross-encoder (accurate).

```
Retrieve 10-20 chunks (milliseconds)
         │
         ▼
Rerank to top 3 (50-200ms)
         │
         ▼
Generate answer from top 3
```

## Cohere reranker

When `COHERE_API_KEY` is set, we use `rerank-english-v3.5`:

```python
reranker = CohereRerank(api_key=KEY, model="rerank-english-v3.5", top_n=3)
reranked = reranker.postprocess_nodes(retrieved, query_str=query)
```

Cohere's reranker is trained on search relevance tasks and typically improves context precision by 10-30%.

## Local fallback: cross-encoder

Without Cohere, we use `cross-encoder/ms-marco-MiniLM-L-6-v2`:

```python
reranker = SentenceTransformerRerank(model="cross-encoder/ms-marco-MiniLM-L-6-v2", top_n=3)
```

Runs locally on CPU — slower but free and private.

## Measuring improvement

Compare eval scores with and without reranking:

```python
# Without reranker
engine_no_rerank = build_query_engine(index, nodes, use_reranker=False)

# With reranker
engine_rerank = build_query_engine(index, nodes, use_reranker=True)
```

Typical improvements:

| Metric | Without rerank | With rerank |
|--------|---------------|-------------|
| context_precision | 0.55 | 0.78 |
| faithfulness | 0.72 | 0.85 |

## DO / DON'T

**DO:**
- Always rerank if latency budget allows (< 200ms added)
- Retrieve 2-3x more than you rerank (retrieve 10, rerank to 3)
- Use the Chunk Inspector to visualize reranking impact

**DON'T:**
- Skip reranking and wonder why context is noisy
- Rerank the entire corpus (only rerank top-K)
- Set top_n too high (3-5 is optimal for generation)

Next: [Generation & Prompting →](05_generation_prompting.md)
