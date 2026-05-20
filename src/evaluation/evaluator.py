"""
RAGAS evaluation wrapper — compatible with ragas ~=0.2.0

Metrics:
  - Faithfulness:      answer claims supported by context (no hallucination)
  - Answer Relevancy:  answer addresses the question
  - Context Precision: retrieved chunks are relevant
  - Context Recall:    retrieved chunks contain the needed information
"""
from typing import Dict, List


def evaluate_rag(
    questions: List[str],
    answers: List[str],
    contexts: List[List[str]],
    ground_truths: List[str],
    llm=None,
    embed_model=None,
) -> Dict:
    """Run RAGAS evaluation, falling back to simple metrics if unavailable."""
    try:
        return _evaluate_with_ragas(questions, answers, contexts, ground_truths)
    except ImportError:
        print("  [WARN] RAGAS not installed. Using simple fallback metrics.")
        from src.evaluation.metrics import compute_simple_metrics

        return compute_simple_metrics(questions, answers, contexts, ground_truths)
    except Exception as e:
        print(f"  [WARN] RAGAS evaluation failed: {e}")
        print("  Falling back to simple string-match metrics...")
        from src.evaluation.metrics import compute_simple_metrics

        return compute_simple_metrics(questions, answers, contexts, ground_truths)


def _evaluate_with_ragas(
    questions: List[str],
    answers: List[str],
    contexts: List[List[str]],
    ground_truths: List[str],
) -> Dict:
    """Internal: handles both ragas 0.2.x (new API) and 0.1.x (old API)."""
    try:
        # ragas 0.2.x API — metrics are classes, dataset is EvaluationDataset
        from ragas import EvaluationDataset, SingleTurnSample, evaluate
        from ragas.metrics import (
            AnswerRelevancy,
            ContextPrecision,
            ContextRecall,
            Faithfulness,
        )

        samples = [
            SingleTurnSample(
                user_input=q,
                response=a,
                retrieved_contexts=c,
                reference=gt,
            )
            for q, a, c, gt in zip(questions, answers, contexts, ground_truths, strict=True)
        ]
        dataset = EvaluationDataset(samples=samples)
        result = evaluate(
            dataset=dataset,
            metrics=[Faithfulness(), AnswerRelevancy(), ContextPrecision(), ContextRecall()],
        )

    except (ImportError, AttributeError):
        # ragas 0.1.x API fallback — metrics are module-level instances
        from datasets import Dataset
        from ragas import evaluate
        from ragas.metrics import (
            answer_relevancy,
            context_precision,
            context_recall,
            faithfulness,
        )

        dataset = Dataset.from_dict(
            {
                "question": questions,
                "answer": answers,
                "contexts": contexts,
                "ground_truth": ground_truths,
            }
        )
        result = evaluate(
            dataset=dataset,
            metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        )

    scores_df = result.to_pandas()
    metric_cols = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]
    summary = {col: float(scores_df[col].mean()) for col in metric_cols if col in scores_df.columns}
    summary["per_sample"] = scores_df.to_dict(orient="records")
    return summary


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
