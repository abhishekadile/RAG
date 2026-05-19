# Chunking Deep Dive

Chunking is the process of splitting documents into smaller pieces for retrieval. It's one of the most impactful decisions in any RAG system.

## The Goldilocks problem

```
Too small (50 tokens)          Just right (512 tokens)         Too large (4000 tokens)
┌────┐ ┌────┐ ┌────┐          ┌──────────────────┐          ┌────────────────────────────┐
│frag│ │ment│ │ed  │          │ Complete thought │          │ Multiple topics, diluted   │
│info│ │no  │ │ctx │          │ with context     │          │ relevance signal           │
└────┘ └────┘ └────┘          └──────────────────┘          └────────────────────────────┘
  High precision                 Balanced                      High recall, low precision
  Low recall
```

A chunk size of **512 tokens ≈ 350 words ≈ 1-2 paragraphs** is a good starting point for most text corpora.

## Strategies in this repo

### Fixed-size chunking

Splits text every N tokens regardless of content boundaries.

```python
nodes = chunk_documents(documents, strategy="fixed", chunk_size=512)
```

| Pros | Cons |
|------|------|
| Fast and predictable | Cuts mid-sentence |
| Simple to implement | Loses semantic coherence |
| Good for structured text | Poor for narrative text |

**Use when:** Tables, code, logs, uniformly structured data.

### Sentence-aware chunking (default)

Respects sentence boundaries while targeting a chunk size.

```python
nodes = chunk_documents(documents, strategy="sentence", chunk_size=512, chunk_overlap=64)
```

| Pros | Cons |
|------|------|
| Preserves readable units | Still may split related paragraphs |
| Good default for most corpora | Overlap adds storage cost |
| Fast | Not semantically aware |

**Use when:** General-purpose text — start here.

### Semantic chunking

Groups sentences by embedding similarity — splits where meaning shifts.

```python
nodes = chunk_documents(documents, strategy="semantic", embed_model=embed_model)
```

| Pros | Cons |
|------|------|
| Highest quality chunks | Slow (requires embedding each sentence) |
| Respects topic boundaries | Expensive at scale |
| Best for mixed-topic documents | Needs embed_model |

**Use when:** Long documents with multiple topics (research papers, legal docs).

### Hierarchical (parent-child)

Creates chunks at multiple sizes: 2048 → 512 → 128 tokens.

```python
nodes = chunk_documents(documents, strategy="hierarchical")
```

| Pros | Cons |
|------|------|
| Retrieve small, return large context | Complex to implement |
| Best of both precision and context | More storage |
| Great for long documents | Requires parent-child retriever |

**Use when:** You need precise retrieval but want rich context for generation.

## Choosing chunk size

Run an experiment:

```python
for size in [256, 512, 1024]:
    nodes = chunk_documents(docs, chunk_size=size)
    # build index, run eval
    scores = evaluate_rag(...)
    print(f"size={size}: recall={scores['context_recall']:.2f}")
```

Typical results:

| Chunk size | Context precision | Context recall |
|------------|-------------------|----------------|
| 256 | Higher | Lower |
| 512 | Balanced | Balanced |
| 1024 | Lower | Higher |

## DO / DON'T

**DO:**
- Test multiple chunk sizes with eval metrics
- Use overlap (64-128 tokens) to avoid losing context at boundaries
- Store source metadata with every chunk

**DON'T:**
- Use the same chunk size for all document types
- Create chunks larger than 2000 tokens
- Chunk before cleaning (remove headers, page numbers first)

Next: [Retrieval Deep Dive →](03_retrieval_deep_dive.md)
