# Advanced RAG Patterns

Once you have a working baseline RAG pipeline, these patterns can significantly improve quality for specific use cases.

## HyDE — Hypothetical Document Embedding

**Problem:** Short queries don't embed well against long document chunks.

**Solution:** Generate a hypothetical answer, embed that instead.

```
Query: "Who led the American Revolution?"
         │
         ▼ LLM generates hypothetical paragraph
"George Washington served as commander of the Continental Army
 during the American Revolutionary War from 1775 to 1783..."
         │
         ▼ embed hypothetical paragraph (not the query)
         ▼ retrieve against corpus
    Better matches!
```

```python
from src.generation.prompts import HYDE_TEMPLATE

hyde_prompt = HYDE_TEMPLATE.format(query_str=query)
hypothetical = llm.complete(hyde_prompt).text.strip()
results = retriever.retrieve(hypothetical[:500])
```

**When to use:** Vague or short queries, question-answer style corpora.
**Cost:** One extra LLM call per query.

## Parent-child retrieval

**Problem:** Small chunks retrieve well but lack context for generation. Large chunks retrieve poorly but have full context.

**Solution:** Index small child chunks, retrieve children, return parent chunks for generation.

```
Document (2048 tokens) ← PARENT (returned to LLM)
├── Chunk A (512 tokens) ← CHILD (used for retrieval)
├── Chunk B (512 tokens) ← CHILD
└── Chunk C (512 tokens) ← CHILD

Query matches Chunk B → return Parent document
```

```python
nodes = chunk_documents(documents, strategy="hierarchical")
# chunk_sizes=[2048, 512, 128]
```

**When to use:** Long documents where you need both precision and context.

## Query rewriting

**Problem:** Users ask vague, conversational questions that don't match document language.

```
User: "who was the first prez?"
Rewritten: "Who was the first president of the United States?"
```

```python
from src.generation.prompts import QUERY_REWRITE_TEMPLATE

prompt = QUERY_REWRITE_TEMPLATE.format(query_str=original_query)
rewritten = llm.complete(prompt).text.strip()
results = retriever.retrieve(rewritten)
```

**When to use:** Chat interfaces, conversational queries, non-expert users.

## Step-back prompting

Generate a broader question to retrieve background context:

```
Specific: "What was Washington's role at the Constitutional Convention?"
Step-back: "What was the Constitutional Convention of 1787?"
```

Retrieve for both queries, combine results.

## Multi-query retrieval

Generate multiple query variants and fuse results:

```python
retriever = get_hybrid_retriever(index, nodes, top_k=10)
fusion = QueryFusionRetriever(
    retrievers=[retriever],
    num_queries=3,  # generates 3 query variants
    mode="reciprocal_rerank",
)
```

**When to use:** Ambiguous queries, multi-faceted questions.

## Agentic RAG

The LLM decides when and how to retrieve:

```
User question
     │
     ▼
┌─────────────┐     Need more info?
│  LLM Agent  │────▶ Retrieve → Read → Reason → Retrieve again
│  (tool use) │     or answer directly
└─────────────┘
```

Tools available to the agent:
- `search_documents(query)` — vector search
- `search_web(url)` — fetch live data
- `calculator(expr)` — precise computation

**When to use:** Complex multi-hop questions, dynamic data sources.
**Complexity:** High — start with basic RAG first.

## Pattern selection guide

| Pattern | Latency impact | Quality gain | Complexity |
|---------|---------------|--------------|------------|
| Query rewriting | +1 LLM call | Medium | Low |
| HyDE | +1 LLM call | High for short queries | Low |
| Reranking | +50-200ms | High | Low |
| Parent-child | None at query time | High for long docs | Medium |
| Multi-query | +2 LLM calls | Medium | Medium |
| Agentic RAG | Variable (multi-step) | Highest | High |

**Recommendation:** Start with hybrid retrieval + reranking. Add query rewriting next. Try HyDE if retrieval quality is still low. Consider agentic RAG only for complex use cases.

Try these patterns in [notebook 05](../notebooks/05_advanced.ipynb) and `scripts/05_advanced.py`.
