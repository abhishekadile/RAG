#!/usr/bin/env python
"""Fallback script: RAGAS evaluation on SQuAD subset."""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.config import EVAL_SAMPLE_SIZE, FALLBACK_DIR, print_config
from src.evaluation.evaluator import evaluate_rag, print_eval_summary
from src.evaluation.testset import load_squad_testset
from src.generation.generator import build_query_engine, query_with_sources
from src.ingestion.chunker import chunk_documents
from src.ingestion.embedder import configure_embed_model
from src.ingestion.loader import load_documents
from src.retrieval.store import get_or_create_index


def build_pipeline():
    documents = load_documents(FALLBACK_DIR / "squad_sample.json")
    embed_model = configure_embed_model()
    nodes = chunk_documents(documents, strategy="sentence")
    index = get_or_create_index(nodes=nodes, embed_model=embed_model, force_rebuild=True)
    query_engine = build_query_engine(index, nodes=nodes)
    return query_engine


def main():
    print("=" * 60)
    print("  04 — Evaluation Pipeline")
    print("=" * 60)
    print_config()

    testset = load_squad_testset(sample_size=min(EVAL_SAMPLE_SIZE, 5))
    query_engine = build_pipeline()

    questions, answers, contexts, ground_truths = [], [], [], []

    print(f"\nRunning evaluation on {len(testset)} samples...")
    for i, item in enumerate(testset):
        print(f"  [{i + 1}/{len(testset)}] {item['question'][:60]}...")
        try:
            result = query_with_sources(query_engine, item["question"])
            questions.append(item["question"])
            answers.append(result["answer"])
            contexts.append([s["text"] for s in result["sources"]] or [item["context"]])
            ground_truths.append(item["ground_truth"])
        except Exception as e:
            print(f"    [WARN] Skipped: {e}")

    if not questions:
        print("  [FAIL] No samples evaluated. Check API keys or Ollama setup.")
        sys.exit(1)

    scores = evaluate_rag(questions, answers, contexts, ground_truths)
    print_eval_summary(scores)
    print("\n  [OK] Evaluation complete")


if __name__ == "__main__":
    main()
