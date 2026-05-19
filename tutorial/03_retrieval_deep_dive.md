# Retrieval Deep Dive

Retrieval is the step that finds relevant document chunks for a given question. Getting this wrong means the LLM never sees the right information.

## How vector similarity works

Documents and queries are converted to vectors (lists of numbers). Similarity is measured by:

```
cosine_similarity(A, B) = (A · B) / (|A| × |B|)

Score range: -1 to 1 (typically 0.3 to 0.9 for relevant pairs)
```

For `all-MiniLM-L6-v2`, vectors are **384 dimensions**. For Gemini embeddings, **768 dimensions**.

```
Query: "When was Washington born?"
         │
         ▼ embed
    [0.12, -0.34, 0.56, ...]  ← 384-dim vector
         │
         ▼ cosine similarity against all chunk vectors
    ┌─────────────────────────────────────┐
    │ Chunk 42: 0.87  ← "born February 22"│
    │ Chunk 17: 0.71  ← "Virginia birth"  │
    │ Chunk 99: 0.31  ← "France capital"   │
    └─────────────────────────────────────┘
```

## What is BM25?

BM25 (Best Matching 25) is a sparse retrieval algorithm based on keyword matching with TF-IDF weighting.

```
BM25 score = f(term frequency, document length, corpus statistics)
```

**Strengths:** Exact matches, rare terms, names, numbers, acronyms
**Weaknesses:** No semantic understanding ("car" won't match "automobile")

## Dense vs sparse vs hybrid

| Method | "When was GW born?" | "February 22, 1732 birth date" | "first US president birth" |
|--------|---------------------|--------------------------------|----------------------------|
| Dense | Good | Good | Good |
| BM25 | Good (if "GW" in text) | Excellent (exact date) | Moderate |
| Hybrid | Best | Best | Best |

```python
# Dense only
dense = get_dense_retriever(index, top_k=10)

# Hybrid (recommended)
hybrid = get_hybrid_retriever(index, nodes, top_k=10)
```

Hybrid fusion uses **reciprocal rank fusion** — combines rankings from both retrievers without needing score normalization.

## How ChromaDB stores vectors (HNSW)

ChromaDB uses **HNSW** (Hierarchical Navigable Small World) graphs for approximate nearest neighbor search.

```
Layer 2:  A ────────────── D        (sparse, long jumps)
Layer 1:  A ─── B ─── C ── D        (medium density)
Layer 0:  A─B─C─D─E─F─G─H          (all vectors, precise)
```

- **Search:** Start at top layer, greedily move toward query, descend layers
- **Complexity:** O(log N) instead of O(N) brute force
- **Tradeoff:** ~99% recall at 10x speed vs exact search

## Failure modes and diagnosis

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Wrong topic retrieved | Chunk too large | Reduce chunk size |
| No results for keyword query | Dense-only retrieval | Enable hybrid (BM25) |
| Right doc, wrong section | Chunk overlap too low | Increase overlap to 128 |
| Slow retrieval | Too many vectors | Filter by metadata, reduce corpus |
| Identical scores | Embedding model mismatch | Re-embed with same model |

## Debugging retrieval

Always log what's retrieved:

```python
results = retriever.retrieve("your query")
for r in results:
    print(f"score={r.score:.3f} | {r.node.get_content()[:100]}")
```

Use the **Chunk Inspector** tab in the Gradio app to compare before/after reranking.

Next: [Reranking →](04_reranking.md)
