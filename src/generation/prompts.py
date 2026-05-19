"""
RAG prompt templates. The prompt is one of the most impactful knobs in RAG.

DO:
  - Include explicit instructions to use ONLY the provided context
  - Tell the model to say "I don't know" if context is insufficient
  - Ask for citations or source references
  - Keep system prompts focused on the task

DON'T:
  - Let the model use prior knowledge without grounding
  - Use vague instructions like "answer based on the documents"
  - Forget to handle the "no relevant context" case
  - Make prompts so long they dilute the context
"""
from llama_index.core import PromptTemplate

RAG_SYSTEM_PROMPT = """\
You are a precise question-answering assistant. You answer questions
ONLY using the provided context passages. Follow these rules strictly:

1. If the answer is clearly present in the context, answer directly and concisely.
2. If the answer is partially in the context, provide what you can and note limitations.
3. If the answer is NOT in the context, respond with:
   "I cannot answer this question based on the provided context."
4. Never use your general knowledge to supplement the context.
5. When possible, cite which part of the context supports your answer.
"""

RAG_QA_TEMPLATE = PromptTemplate(
    "Context passages:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n\n"
    "Question: {query_str}\n\n"
    "Answer (based only on the context above):"
)

HYDE_TEMPLATE = PromptTemplate(
    "Write a detailed paragraph that would answer the following question. "
    "Do not reference that this is hypothetical.\n\n"
    "Question: {query_str}\n\n"
    "Hypothetical answer paragraph:"
)

QUERY_REWRITE_TEMPLATE = PromptTemplate(
    "You are a search query optimizer. Rewrite the user's question to be "
    "more specific and retrieval-friendly, without changing its intent. "
    "Return only the rewritten query.\n\n"
    "Original question: {query_str}\n\n"
    "Rewritten query:"
)

STEP_BACK_TEMPLATE = PromptTemplate(
    "Given a specific question, generate a more general 'step-back' question "
    "that would help retrieve broader context useful for answering the original.\n\n"
    "Specific question: {query_str}\n\n"
    "Step-back question:"
)
