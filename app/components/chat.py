"""Chat interface component."""
import gradio as gr


def build_chat_tab():
    """Build the Chat tab."""
    with gr.Tab("Chat"):
        gr.Markdown("Ask questions about the indexed SQuAD corpus.")
        model = gr.Dropdown(
            choices=["auto", "gemini", "groq", "local"],
            value="auto",
            label="Model",
        )
        chatbot = gr.Chatbot(label="Conversation", height=400)
        question = gr.Textbox(label="Your question", placeholder="Ask something...")
        sources = gr.Markdown(label="Sources used")
        with gr.Row():
            submit = gr.Button("Send", variant="primary")
            clear = gr.Button("Clear")

        def respond(q, m, h):
            from app.utils import chat

            new_h, src = chat(q, m, h or [])
            return new_h, src, ""

        submit.click(respond, [question, model, chatbot], [chatbot, sources, question])
        question.submit(respond, [question, model, chatbot], [chatbot, sources, question])
        clear.click(lambda: ([], "", ""), outputs=[chatbot, sources, question])
