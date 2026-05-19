"""
Reranking: takes top-K retrieved chunks and re-scores them.

Why rerank?
- Vector similarity is a proxy for relevance, not relevance itself
- Rerankers (cross-encoders) jointly process query + document — much more accurate
- Cohere's reranker is trained specifically for retrieval tasks
- Reranking is cheap: you only rerank the top-K, not the whole corpus

The typical pipeline:
  Query → Retrieve top-20 (fast, approximate)
         → Rerank to top-3 (slow, accurate)
         → Generate answer from top-3
"""
from llama_index.core.postprocessor.types import BaseNodePostprocessor

from src.utils.fallback import get_reranker


def build_reranker(top_n: int = 3) -> BaseNodePostprocessor:
    """
    Build reranker with automatic fallback.
    - If COHERE_API_KEY is set: uses Cohere rerank-english-v3.5
    - Otherwise: uses local sentence-transformers cross-encoder
    """
    reranker = get_reranker()
    reranker.top_n = top_n
    return reranker
