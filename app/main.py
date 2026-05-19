#!/usr/bin/env python
"""Gradio app entry point — RAG seminar frontend."""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import gradio as gr

from app.components.chat import build_chat_tab
from app.components.eval_dashboard import build_eval_tab
from app.components.inspector import build_inspector_tab
from app.components.uploader import build_upload_tab
from src.config import print_config


def create_app() -> gr.Blocks:
    """Create the Gradio application with four tabs."""
    with gr.Blocks(title="RAG From Scratch", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            "# RAG From Scratch 🔍\n"
            "Interactive demo for the RAG seminar. "
            "Chat, upload data, inspect chunks, and run evaluation."
        )

        with gr.Tabs():
            build_chat_tab()
            build_upload_tab()
            build_inspector_tab()
            build_eval_tab()

        gr.Markdown("---\nRun `make keys` to check API key status.")

    return demo


if __name__ == "__main__":
    print_config()
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
