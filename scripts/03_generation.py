#!/usr/bin/env python
"""Fallback script: RAG generation pipeline."""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.config import FALLBACK_DIR, print_config
from src.generation.generator import build_query_engine, query_with_sources
from src.ingestion.chunker import chunk_documents
from src.ingestion.embedder import configure_embed_model
from src.ingestion.loader import load_documents
from src.retrieval.store import get_or_create_index
from src.utils.display import print_qa_result


def build_index():
    documents = load_documents(FALLBACK_DIR / "squad_sample.json")
    embed_model = configure_embed_model()
    nodes = chunk_documents(documents, strategy="sentence")
    index = get_or_create_index(nodes=nodes, embed_model=embed_model, force_rebuild=True)
    return index, nodes


def main():
    print("=" * 60)
    print("  03 — Generation Pipeline")
    print("=" * 60)
    print_config()

    index, nodes = build_index()
    query_engine = build_query_engine(index, nodes=nodes, use_hybrid=True, use_reranker=True)

    questions = [
        "When was George Washington born?",
        "What is the capital of France?",
        "Who wrote Romeo and Juliet?",
    ]

    for question in questions:
        print(f"\n--- Question: {question} ---")
        try:
            result = query_with_sources(query_engine, question)
            print_qa_result(question, result["answer"], result["sources"])
        except Exception as e:
            print(f"  [WARN] Generation failed: {e}")
            print("  Tip: Set GEMINI_API_KEY or GROQ_API_KEY, or run Ollama locally.")
            continue

    print("\n  [OK] Generation pipeline complete")


if __name__ == "__main__":
    main()
