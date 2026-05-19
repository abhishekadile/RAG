"""
RAGAS evaluation wrapper.

Metrics explained:
  - Faithfulness: Is the answer grounded in the retrieved context?
  - Answer Relevancy: Does the answer actually address the question?
  - Context Precision: Are the retrieved chunks relevant?
  - Context Recall: Did we retrieve the chunks needed to answer?
"""
from typing import Dict, List

from datasets import Dataset


def evaluate_rag(
    questions: List[str],
    answers: List[str],
    contexts: List[List[str]],
    ground_truths: List[str],
    llm=None,
    embed_model=None,
) -> Dict:
    """
    Run RAGAS evaluation on a list of QA pairs.

    Args:
        questions: List of questions
        answers: List of generated answers
        contexts: List of retrieved context lists (one per question)
        ground_truths: List of ground truth answers
        llm: LLM for judge-based metrics (uses default if None)
        embed_model: Embedding model for relevancy metrics

    Returns:
        Dict with metric scores + per-sample results
    """
    from ragas import evaluate
    from ragas.metrics import (
        answer_relevancy,
        context_precision,
        context_recall,
        faithfulness,
    )

    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    }
    dataset = Dataset.from_dict(data)

    try:
        result = evaluate(
            dataset=dataset,
            metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        )
        scores = result.to_pandas()
        summary = {
            "faithfulness": float(scores["faithfulness"].mean()),
            "answer_relevancy": float(scores["answer_relevancy"].mean()),
            "context_precision": float(scores["context_precision"].mean()),
            "context_recall": float(scores["context_recall"].mean()),
            "per_sample": scores.to_dict(orient="records"),
        }
        return summary
    except Exception as e:
        print(f"  [WARN] RAGAS evaluation failed: {e}")
        print("  Falling back to simple string-match metrics...")
        from src.evaluation.metrics import compute_simple_metrics

        return compute_simple_metrics(questions, answers, contexts, ground_truths)


def print_eval_summary(scores: Dict):
    """Pretty print evaluation scores with interpretation."""
    from rich.console import Console
    from rich.table import Table

    c = Console()
    t = Table(title="RAGAS Evaluation Results", show_header=True)
    t.add_column("Metric", style="cyan")
    t.add_column("Score", style="white")
    t.add_column("Interpretation", style="dim")

    interpretations = {
        "faithfulness": (
            "< 0.7: Hallucination risk",
            "0.7-0.9: Good",
            "> 0.9: Excellent — low hallucination",
        ),
        "answer_relevancy": (
            "< 0.6: Off-topic answers",
            "0.6-0.8: Reasonable",
            "> 0.8: Answers are on-point",
        ),
        "context_precision": (
            "< 0.5: Too much noise in retrieved chunks",
            "0.5-0.8: OK",
            "> 0.8: Retrieval is precise",
        ),
        "context_recall": (
            "< 0.5: Missing key information",
            "0.5-0.8: Partial coverage",
            "> 0.8: Good coverage",
        ),
    }
    for metric, score in scores.items():
        if metric in ("per_sample", "fallback_metrics"):
            continue
        thresholds = interpretations.get(metric, ("", "", ""))
        if score < 0.6:
            interp = thresholds[0]
            style = "red"
        elif score < 0.8:
            interp = thresholds[1]
            style = "yellow"
        else:
            interp = thresholds[2]
            style = "green"
        t.add_row(metric, f"[{style}]{score:.3f}[/{style}]", interp)
    c.print(t)
