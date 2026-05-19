"""
Build evaluation test sets from SQuAD 2.0.
SQuAD gives us ground-truth questions + answers — perfect for RAG eval.
"""
import json
import random
from pathlib import Path
from typing import Dict, List

from src.config import EVAL_SAMPLE_SIZE, FALLBACK_DIR


def load_squad_testset(
    path: str | Path | None = None,
    sample_size: int = EVAL_SAMPLE_SIZE,
    seed: int = 42,
) -> List[Dict]:
    """
    Load SQuAD QA pairs as a test set.

    Returns list of dicts with keys:
      - question: str
      - ground_truth: str
      - context: str (the passage the answer comes from)
    """
    if path is None:
        path = FALLBACK_DIR / "squad_sample.json"

    with open(path) as f:
        squad = json.load(f)

    pairs = []
    for article in squad["data"]:
        for paragraph in article["paragraphs"]:
            context = paragraph["context"]
            for qa in paragraph["qas"]:
                if qa["is_impossible"] or not qa["answers"]:
                    continue
                pairs.append(
                    {
                        "question": qa["question"],
                        "ground_truth": qa["answers"][0]["text"],
                        "context": context,
                        "title": article["title"],
                    }
                )

    random.seed(seed)
    sample = random.sample(pairs, min(sample_size, len(pairs)))
    print(f"  Loaded {len(sample)} QA pairs from SQuAD")
    return sample
