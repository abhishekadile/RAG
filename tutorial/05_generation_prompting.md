# Generation & Prompting

The generation step takes retrieved context and a user question, then asks the LLM to produce a grounded answer. Prompt design is the most impactful knob you control.

## RAG prompt structure

```
┌─────────────────────────────────────────┐
│ SYSTEM: Answer ONLY from context.       │
│         Say "I don't know" if unsure.   │
├─────────────────────────────────────────┤
│ CONTEXT:                                │
│ [Chunk 1 text...]                       │
│ [Chunk 2 text...]                       │
│ [Chunk 3 text...]                       │
├─────────────────────────────────────────┤
│ USER: {question}                        │
├─────────────────────────────────────────┤
│ ASSISTANT: {answer}                     │
└─────────────────────────────────────────┘
```

Our template in `src/generation/prompts.py`:

```python
RAG_QA_TEMPLATE = PromptTemplate(
    "Context passages:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n\n"
    "Question: {query_str}\n\n"
    "Answer (based only on the context above):"
)
```

## Preventing hallucination

The model's parametric knowledge is vast and will leak into answers unless explicitly constrained:

**Bad prompt:**
> Answer the question based on the documents.

**Good prompt:**
> Answer ONLY using the provided context. If the answer is NOT in the context, respond with: "I cannot answer this question based on the provided context." Never use your general knowledge.

## Handling "I don't know"

Test with out-of-domain questions:

```python
result = query_with_sources(engine, "What is the stock price of Apple?")
# Expected: "I cannot answer this question based on the provided context."
```

If the model answers from general knowledge instead, tighten your prompt.

## Citations and grounding

Ask the model to cite supporting context:

```
5. When possible, cite which part of the context supports your answer.
```

In the Gradio app, the **Sources used** panel shows retrieved chunks alongside the answer.

## Model selection

| Provider | Model | Speed | Quality | Cost |
|----------|-------|-------|---------|------|
| Gemini | gemini-2.5-flash | Fast | High | Free tier |
| Groq | llama-3.3-70b | Very fast | High | Free tier |
| Ollama | llama3.2:3b | Slow (CPU) | Moderate | Free, local |

```python
llm = get_llm(provider="gemini")  # Force specific provider
```

## DO / DON'T

**DO:**
- Explicitly instruct context-only answers
- Test with questions NOT in your corpus
- Keep system prompts focused (under 200 words)
- Handle empty retrieval (no chunks above similarity threshold)

**DON'T:**
- Let the model blend context with parametric knowledge
- Use the same prompt for all document types
- Put instructions after the context (model may ignore them)
- Make prompts so long they dilute the context

Next: [Evaluation →](06_evaluation.md)
