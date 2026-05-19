#!/usr/bin/env python
"""Fallback script: advanced RAG patterns (HyDE, reranking, query rewriting)."""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from llama_index.core import Settings

from src.config import FALLBACK_DIR, print_config
from src.generation.prompts import HYDE_TEMPLATE, QUERY_REWRITE_TEMPLATE
from src.ingestion.chunker import chunk_documents
from src.ingestion.embedder import configure_embed_model
from src.ingestion.loader import load_documents
from src.retrieval.reranker import build_reranker
from src.retrieval.retriever import get_hybrid_retriever
from src.retrieval.store import get_or_create_index
from src.utils.display import print_retrieval_results
from src.utils.fallback import get_llm


def build_index():
    documents = load_documents(FALLBACK_DIR / "squad_sample.json")
    embed_model = configure_embed_model()
    nodes = chunk_documents(documents, strategy="sentence")
    index = get_or_create_index(nodes=nodes, embed_model=embed_model, force_rebuild=True)
    return index, nodes


def main():
    print("=" * 60)
    print("  05 — Advanced RAG Patterns")
    print("=" * 60)
    print_config()

    index, nodes = build_index()
    llm = get_llm()
    Settings.llm = llm

    original_query = "Who led the American Revolution?"
    print(f"\nOriginal query: {original_query}")

    # Query rewriting
    print("\n[Query Rewriting]")
    try:
        rewrite_prompt = QUERY_REWRITE_TEMPLATE.format(query_str=original_query)
        rewritten = llm.complete(rewrite_prompt).text.strip()
        print(f"  Rewritten: {rewritten}")
        search_query = rewritten
    except Exception as e:
        print(f"  [WARN] Rewrite failed: {e}. Using original query.")
        search_query = original_query

    # HyDE
    print("\n[HyDE — Hypothetical Document Embedding]")
    try:
        hyde_prompt = HYDE_TEMPLATE.format(query_str=original_query)
        hypothetical = llm.complete(hyde_prompt).text.strip()
        print(f"  Hypothetical doc: {hypothetical[:200]}...")
        search_query = hypothetical[:500]
    except Exception as e:
        print(f"  [WARN] HyDE failed: {e}")

    # Retrieve + rerank
    print("\n[Retrieve -> Rerank]")
    retriever = get_hybrid_retriever(index, nodes, top_k=10)
    retrieved = retriever.retrieve(search_query)
    print_retrieval_results(retrieved[:5], "Before Reranking (top 5)")

    reranker = build_reranker(top_n=3)
    reranked = reranker.postprocess_nodes(retrieved, query_str=original_query)
    print_retrieval_results(reranked, "After Reranking (top 3)")

    print("\n  [OK] Advanced patterns demo complete")


if __name__ == "__main__":
    main()
