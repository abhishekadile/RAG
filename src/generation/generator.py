"""
RAG query engine. Wires together: retriever + reranker + LLM + prompt.
"""
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.query_engine import RetrieverQueryEngine

from src.config import TOP_K_RERANK, TOP_K_RETRIEVE
from src.generation.prompts import RAG_QA_TEMPLATE
from src.utils.fallback import get_embed_model, get_llm, get_reranker


def build_query_engine(
    index: VectorStoreIndex,
    nodes=None,
    use_hybrid: bool = True,
    use_reranker: bool = True,
    top_k_retrieve: int = TOP_K_RETRIEVE,
    top_k_rerank: int = TOP_K_RERANK,
    streaming: bool = False,
    llm=None,
):
    """
    Build a complete RAG query engine.

    Args:
        index: ChromaDB-backed VectorStoreIndex
        nodes: All nodes (required for hybrid retrieval)
        use_hybrid: Use BM25 + dense hybrid retrieval
        use_reranker: Apply reranking after retrieval
        top_k_retrieve: How many chunks to retrieve initially
        top_k_rerank: How many chunks to keep after reranking
        streaming: Enable streaming responses
        llm: Optional LLM override (Gemini/Groq/Ollama)

    Returns:
        LlamaIndex QueryEngine
    """
    if llm is None:
        llm = get_llm()
    Settings.llm = llm
    Settings.embed_model = get_embed_model()

    if use_hybrid and nodes:
        from src.retrieval.retriever import get_hybrid_retriever

        retriever = get_hybrid_retriever(index, nodes, top_k=top_k_retrieve)
    else:
        from src.retrieval.retriever import get_dense_retriever

        retriever = get_dense_retriever(index, top_k=top_k_retrieve)

    postprocessors = []
    if use_reranker:
        reranker = get_reranker()
        reranker.top_n = top_k_rerank
        postprocessors.append(reranker)
    else:
        postprocessors.append(SimilarityPostprocessor(similarity_cutoff=0.3))

    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        node_postprocessors=postprocessors,
        text_qa_template=RAG_QA_TEMPLATE,
        streaming=streaming,
        llm=llm,
    )
    return query_engine


def query_with_sources(query_engine, question: str) -> dict:
    """Run a query and return answer plus source nodes."""
    response = query_engine.query(question)
    sources = []
    if hasattr(response, "source_nodes") and response.source_nodes:
        for node in response.source_nodes:
            sources.append(
                {
                    "text": node.node.get_content(),
                    "score": getattr(node, "score", None),
                    "metadata": node.node.metadata,
                }
            )
    return {"answer": str(response), "sources": sources}
