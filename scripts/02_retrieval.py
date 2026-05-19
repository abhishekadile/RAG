#!/usr/bin/env python
"""Fallback script: retrieval (dense, sparse, hybrid)."""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.config import FALLBACK_DIR, print_config
from src.ingestion.chunker import chunk_documents
from src.ingestion.embedder import configure_embed_model
from src.ingestion.loader import load_documents
from src.retrieval.retriever import get_dense_retriever, get_hybrid_retriever
from src.retrieval.store import get_or_create_index
from src.utils.display import print_retrieval_results


def build_index():
    """Build or load index (self-contained for this script)."""
    documents = load_documents(FALLBACK_DIR / "squad_sample.json")
    embed_model = configure_embed_model()
    nodes = chunk_documents(documents, strategy="sentence")
    index = get_or_create_index(nodes=nodes, embed_model=embed_model, force_rebuild=True)
    return index, nodes


def main():
    print("=" * 60)
    print("  02 — Retrieval Pipeline")
    print("=" * 60)
    print_config()

    index, nodes = build_index()
    query = "Who was the first president of the United States?"

    print(f"\nQuery: {query}\n")

    print("[Dense retrieval]")
    dense = get_dense_retriever(index, top_k=5)
    dense_results = dense.retrieve(query)
    print_retrieval_results(dense_results, "Dense (Vector) Results")

    print("\n[Hybrid retrieval (Dense + BM25)]")
    hybrid = get_hybrid_retriever(index, nodes, top_k=5)
    hybrid_results = hybrid.retrieve(query)
    print_retrieval_results(hybrid_results, "Hybrid Results")

    print("\n  [OK] Retrieval pipeline complete")


if __name__ == "__main__":
    main()
