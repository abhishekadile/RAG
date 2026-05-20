"""Evaluation dashboard component."""
import gradio as gr
import pandas as pd


def build_eval_tab():
    """Build the Eval Dashboard tab."""
    with gr.Tab("Eval Dashboard"):
        gr.Markdown(
            "## Eval Dashboard\n\n"
            "Run RAGAS evaluation on a SQuAD subset. "
            "Falls back to token-F1 / exact-match if no API keys."
        )
        with gr.Row():
            sample_size = gr.Slider(3, 20, value=5, step=1, label="Sample size")
            run_btn = gr.Button("Run Evaluation", variant="primary", scale=0)

        progress = gr.Textbox(
            label="Status",
            value="Click 'Run Evaluation' to start.",
            interactive=False,
            lines=2,
        )
        with gr.Row():
            faith_md = gr.Markdown("**Faithfulness** —")
            rel_md = gr.Markdown("**Answer relevancy** —")
            prec_md = gr.Markdown("**Context precision** —")
            rec_md = gr.Markdown("**Context recall** —")

        scores_md = gr.Markdown()
        table = gr.Dataframe(label="Per-question breakdown")

        def run_eval(n):
            # Generator: yields after each step so the UI updates in real time
            yield "Loading pipeline...", "—", "—", "—", "—", "", pd.DataFrame()
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
                yield "Building index...", "—", "—", "—", "—", "", pd.DataFrame()

                documents = load_documents(FALLBACK_DIR / "squad_sample.json")
                embed_model = configure_embed_model()
                nodes = chunk_documents(documents, strategy="sentence")
                index = get_or_create_index(nodes=nodes, embed_model=embed_model)
                engine = build_query_engine(index, nodes=nodes)

                questions, answers, contexts, gts = [], [], [], []
                for i, item in enumerate(testset):
                    status = f"Evaluating {i + 1}/{len(testset)}: {item['question'][:55]}..."
                    yield status, "—", "—", "—", "—", "", pd.DataFrame()
                    result = query_with_sources(engine, item["question"])
                    questions.append(item["question"])
                    answers.append(result["answer"])
                    contexts.append([s["text"] for s in result["sources"]] or [item["context"]])
                    gts.append(item["ground_truth"])

                yield "Computing RAGAS scores...", "—", "—", "—", "—", "", pd.DataFrame()
                scores = evaluate_rag(questions, answers, contexts, gts)
                fallback = scores.get("fallback_metrics", False)

                def fmt(k):
                    v = scores.get(k)
                    return f"**{k}**: {v:.3f}" if v is not None else f"**{k}**: —"

                note = "\n\n*Using fallback metrics (RAGAS unavailable)*" if fallback else ""
                md = f"## Results ({len(questions)} samples){note}"
                df = pd.DataFrame(scores.get("per_sample", []))

                yield (
                    f"Done — {len(questions)} samples evaluated.",
                    fmt("faithfulness"),
                    fmt("answer_relevancy"),
                    fmt("context_precision"),
                    fmt("context_recall"),
                    md,
                    df,
                )
            except Exception as e:
                yield (
                    f"Failed: {e}",
                    "—",
                    "—",
                    "—",
                    "—",
                    f"## Error\n\n```\n{e}\n```",
                    pd.DataFrame(),
                )

        run_btn.click(
            fn=run_eval,
            inputs=[sample_size],
            outputs=[progress, faith_md, rel_md, prec_md, rec_md, scores_md, table],
        )
