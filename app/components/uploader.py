"""File upload and ingestion component."""
import gradio as gr


def build_upload_tab():
    """Build the Upload Your Data tab."""
    with gr.Tab("Upload Your Data"):
        gr.Markdown("Upload PDF, TXT, or MD files — or paste a URL — to index into ChromaDB.")
        files = gr.File(
            label="Upload files",
            file_count="multiple",
            file_types=[".pdf", ".txt", ".md"],
        )
        url = gr.Textbox(label="Or enter a URL", placeholder="https://...")
        strategy = gr.Dropdown(
            choices=["fixed", "sentence", "semantic"],
            value="sentence",
            label="Chunk strategy",
        )
        chunk_size = gr.Slider(128, 1024, value=512, step=64, label="Chunk size")
        index_btn = gr.Button("Index documents", variant="primary")
        status = gr.Textbox(label="Status", interactive=False)

        def do_index(f, u, s, cs):
            from app.utils import index_uploaded_files

            return index_uploaded_files(f, u, s, cs)

        index_btn.click(do_index, [files, url, strategy, chunk_size], status)
