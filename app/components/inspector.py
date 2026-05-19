"""Chunk inspector component."""
import gradio as gr


def build_inspector_tab():
    """Build the Chunk Inspector tab."""
    with gr.Tab("Chunk Inspector"):
        gr.Markdown("See retrieved chunks **before** and **after** reranking.")
        query = gr.Textbox(
            label="Query",
            placeholder="Who was the first president?",
        )
        inspect_btn = gr.Button("Inspect", variant="primary")
        with gr.Row():
            before = gr.Markdown(label="Before reranking (top 10)")
            after = gr.Markdown(label="After reranking (top 3)")

        def do_inspect(q):
            from app.utils import inspect_chunks

            return inspect_chunks(q)

        inspect_btn.click(do_inspect, query, [before, after])
        query.submit(do_inspect, query, [before, after])
