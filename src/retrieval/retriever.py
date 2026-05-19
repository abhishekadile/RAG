"""
Hybrid retriever: dense (vector) + sparse (BM25).
Dense retrieval finds semantically similar chunks.
Sparse retrieval finds exact keyword matches.
Combining both is almost always better than either alone.
"""
from typing import List

from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import QueryFusionRetriever, VectorIndexRetriever
from llama_index.core.schema import BaseNode
from llama_index.retrievers.bm25 import BM25Retriever

from src.config import TOP_K_RETRIEVE
from src.utils.fallback import get_llm


def get_dense_retriever(index: VectorStoreIndex, top_k: int = TOP_K_RETRIEVE):
    """Pure vector similarity retriever."""
    return index.as_retriever(similarity_top_k=top_k)


def get_hybrid_retriever(
    index: VectorStoreIndex,
    nodes: List[BaseNode],
    top_k: int = TOP_K_RETRIEVE,
    mode: str = "reciprocal_rerank",
):
    """
    Hybrid retriever combining dense + sparse (BM25).

    Why hybrid?
    - Dense: great for paraphrases, semantic similarity
    - BM25: great for exact matches, rare terms, names, numbers
    - Combined: catches what either alone would miss

    Args:
        index: VectorStoreIndex (for dense)
        nodes: All nodes (for BM25)
        top_k: Number of results to retrieve
        mode: Fusion mode for combining results

    Returns:
        QueryFusionRetriever combining both
    """
    dense = VectorIndexRetriever(index=index, similarity_top_k=top_k)
    sparse = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=top_k)

    return QueryFusionRetriever(
        retrievers=[dense, sparse],
        similarity_top_k=top_k,
        num_queries=1,
        mode=mode,
        use_async=False,
        llm=get_llm(),
    )
