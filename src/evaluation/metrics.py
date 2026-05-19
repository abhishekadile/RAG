"""Custom evaluation metrics and scoring utilities."""
import re
from typing import Dict, List


def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return re.sub(r"\s+", " ", text)


def exact_match(prediction: str, ground_truth: str) -> float:
    """Return 1.0 if normalized strings match, else 0.0."""
    return 1.0 if normalize_text(prediction) == normalize_text(ground_truth) else 0.0


def token_f1(prediction: str, ground_truth: str) -> float:
    """Compute token-level F1 between prediction and ground truth."""
    pred_tokens = set(normalize_text(prediction).split())
    truth_tokens = set(normalize_text(ground_truth).split())
    if not pred_tokens or not truth_tokens:
        return 0.0
    common = pred_tokens & truth_tokens
    if not common:
        return 0.0
    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(truth_tokens)
    return 2 * precision * recall / (precision + recall)


def context_contains_answer(contexts: List[str], ground_truth: str) -> float:
    """Return 1.0 if any context contains the ground truth answer."""
    norm_truth = normalize_text(ground_truth)
    for ctx in contexts:
        if norm_truth in normalize_text(ctx):
            return 1.0
    return 0.0


def compute_simple_metrics(
    questions: List[str],
    answers: List[str],
    contexts: List[List[str]],
    ground_truths: List[str],
) -> Dict:
    """
    Fallback metrics when RAGAS is unavailable (no API keys, rate limits, etc.).
    """
    per_sample = []
    em_scores = []
    f1_scores = []
    recall_scores = []

    for q, a, ctx, gt in zip(questions, answers, contexts, ground_truths, strict=True):
        em = exact_match(a, gt)
        f1 = token_f1(a, gt)
        recall = context_contains_answer(ctx, gt)
        em_scores.append(em)
        f1_scores.append(f1)
        recall_scores.append(recall)
        per_sample.append(
            {
                "question": q,
                "answer": a,
                "ground_truth": gt,
                "exact_match": em,
                "token_f1": f1,
                "context_recall": recall,
            }
        )

    n = len(questions) or 1
    return {
        "faithfulness": sum(f1_scores) / n,
        "answer_relevancy": sum(em_scores) / n,
        "context_precision": sum(recall_scores) / n,
        "context_recall": sum(recall_scores) / n,
        "per_sample": per_sample,
        "fallback_metrics": True,
    }
