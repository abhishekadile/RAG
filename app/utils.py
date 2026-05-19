"""App-level helpers for the Gradio frontend."""
import tempfile
from pathlib import Path

from src.config import FALLBACK_DIR
from src.generation.generator import build_query_engine, query_with_sources
from src.ingestion.chunker import chunk_documents
from src.ingestion.embedder import configure_embed_model
from src.ingestion.loader import load_documents
from src.retrieval.reranker import build_reranker
from src.retrieval.retriever import get_dense_retriever, get_hybrid_retriever
from src.retrieval.store import get_or_create_index

# Module-level cache for the demo index
_cached = {"index": None, "nodes": None, "embed_model": None}


def ensure_index(force_rebuild: bool = False):
    """Load or build the default SQuAD index."""
    if _cached["index"] is not None and not force_rebuild:
        return _cached["index"], _cached["nodes"]

    documents = load_documents(FALLBACK_DIR / "squad_sample.json")
    embed_model = configure_embed_model()
    nodes = chunk_documents(documents, strategy="sentence")
    index = get_or_create_index(
        nodes=nodes,
        embed_model=embed_model,
        force_rebuild=force_rebuild,
    )
    _cached.update({"index": index, "nodes": nodes, "embed_model": embed_model})
    return index, nodes


def chat(question: str, model_provider: str, history: list) -> tuple:
    """Handle chat tab queries."""
    if not question.strip():
        return history, ""

    try:
        from src.utils.fallback import get_llm

        index, nodes = ensure_index()
        llm = get_llm(provider=model_provider if model_provider != "auto" else None)
        engine = build_query_engine(index, nodes=nodes, llm=llm)
        result = query_with_sources(engine, question)

        sources_text = ""
        if result["sources"]:
            parts = []
            for i, s in enumerate(result["sources"]):
                score = s.get("score")
                score_str = f" (score: {score:.3f})" if score is not None else ""
                parts.append(f"**Source {i + 1}{score_str}:**\n{s['text'][:400]}...")
            sources_text = "\n\n".join(parts)

        history = history + [(question, result["answer"])]
        return history, sources_text
    except Exception as e:
        err = f"Error: {e}. Check API keys with `make keys` or use local fallback."
        history = history + [(question, err)]
        return history, err


def index_uploaded_files(files, url: str, strategy: str, chunk_size: int) -> str:
    """Index uploaded files or URL into ChromaDB."""
    try:
        paths = []
        if files:
            for f in files:
                paths.append(f.name if hasattr(f, "name") else str(f))

        documents = []
        if paths:
            for p in paths:
                documents.extend(load_documents(p))

        if url and url.strip().startswith("http"):
            documents.extend(load_documents(url.strip()))

        if not documents:
            return "No documents to index. Upload files or provide a URL."

        embed_model = configure_embed_model()
        nodes = chunk_documents(
            documents,
            strategy=strategy,
            chunk_size=int(chunk_size),
        )
        get_or_create_index(
            nodes=nodes,
            embed_model=embed_model,
            force_rebuild=True,
        )
        _cached.update({"index": None, "nodes": None})
        ensure_index(force_rebuild=False)
        return f"[OK] Indexed {len(documents)} documents into {len(nodes)} chunks."
    except Exception as e:
        return f"Indexing failed: {e}"


def inspect_chunks(query: str) -> tuple:
    """Return chunks before and after reranking."""
    if not query.strip():
        return "Enter a query.", "Enter a query."

    try:
        index, nodes = ensure_index()
        retriever = get_hybrid_retriever(index, nodes, top_k=10)
        before = retriever.retrieve(query)

        before_text = ""
        for i, n in enumerate(before[:10]):
            score = f"{n.score:.4f}" if n.score is not None else "—"
            before_text += f"**{i + 1}. Score: {score}**\n{n.node.get_content()[:300]}...\n\n"

        reranker = build_reranker(top_n=3)
        after = reranker.postprocess_nodes(before, query_str=query)

        after_text = ""
        for i, n in enumerate(after):
            score = f"{n.score:.4f}" if n.score is not None else "—"
            after_text += f"**{i + 1}. Score: {score}**\n{n.node.get_content()[:300]}...\n\n"

        return before_text or "No results.", after_text or "No results after reranking."
    except Exception as e:
        msg = f"Inspection failed: {e}"
        return msg, msg
