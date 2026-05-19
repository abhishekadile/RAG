"""Evaluation dashboard component."""
import gradio as gr
import pandas as pd


def build_eval_tab():
    """Build the Eval Dashboard tab."""
    with gr.Tab("Eval Dashboard"):
        gr.Markdown(
            "Run RAGAS evaluation on a SQuAD subset. "
            "Requires API keys for best results; falls back to simple metrics."
        )
        sample_size = gr.Slider(3, 20, value=5, step=1, label="Sample size")
        run_btn = gr.Button("Run Evaluation", variant="primary")
        progress = gr.Textbox(label="Progress", interactive=False)
        scores_md = gr.Markdown(label="Scores")
        table = gr.Dataframe(label="Per-question breakdown")

        def run_eval(n):
            try:
                from src.config import FALLBACK_DIR
                from src.evaluation.evaluator import evaluate_rag
                from src.evaluation.testset import load_squad_testset
                from src.generation.generator import build_query_engine, query_with_sources
                from src.ingestion.chunker import chunk_documents
                from src.ingestion.embedder import configure_embed_model
                from src.ingestion.loader import load_documents
                from src.retrieval.store import get_or_create_index

                testset = load_squad_testset(sample_size=int(n))
                documents = load_documents(FALLBACK_DIR / "squad_sample.json")
                embed_model = configure_embed_model()
                nodes = chunk_documents(documents, strategy="sentence")
                index = get_or_create_index(nodes=nodes, embed_model=embed_model)
                engine = build_query_engine(index, nodes=nodes)

                questions, answers, contexts, gts = [], [], [], []
                for i, item in enumerate(testset):
                    progress_val = f"Evaluating {i + 1}/{len(testset)}..."
                    result = query_with_sources(engine, item["question"])
                    questions.append(item["question"])
                    answers.append(result["answer"])
                    contexts.append([s["text"] for s in result["sources"]] or [item["context"]])
                    gts.append(item["ground_truth"])

                scores = evaluate_rag(questions, answers, contexts, gts)
                fallback = scores.get("fallback_metrics", False)
                md = "## Evaluation Results\n\n"
                for k in ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]:
                    if k in scores:
                        md += f"- **{k}**: {scores[k]:.3f}\n"
                if fallback:
                    md += "\n*Using fallback metrics (RAGAS unavailable)*"

                df = pd.DataFrame(scores.get("per_sample", []))
                return progress_val, md, df
            except Exception as e:
                return f"Failed: {e}", f"## Error\n\n{e}", pd.DataFrame()

        run_btn.click(run_eval, sample_size, [progress, scores_md, table])
