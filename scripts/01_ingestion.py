#!/usr/bin/env python
"""Fallback script: ingestion pipeline (load → chunk → embed → index)."""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.config import FALLBACK_DIR, print_config
from src.ingestion.chunker import chunk_documents
from src.ingestion.embedder import configure_embed_model
from src.ingestion.loader import load_documents
from src.retrieval.store import get_or_create_index
from src.utils.display import print_documents, print_nodes


def main():
    print("=" * 60)
    print("  01 — Ingestion Pipeline")
    print("=" * 60)
    print_config()

    print("\n[1/4] Loading documents...")
    documents = load_documents(FALLBACK_DIR / "squad_sample.json")
    print_documents(documents)

    print("\n[2/4] Chunking documents...")
    embed_model = configure_embed_model()
    nodes = chunk_documents(documents, strategy="sentence")
    print_nodes(nodes)

    print("\n[3/4] Building vector index...")
    index = get_or_create_index(
        nodes=nodes,
        embed_model=embed_model,
        force_rebuild=True,
    )

    print("\n[4/4] Verification...")
    print(f"  [OK] Index ready with {len(nodes)} nodes")
    print(f"  [OK] Documents loaded: {len(documents)}")
    return index, nodes, embed_model


if __name__ == "__main__":
    main()
