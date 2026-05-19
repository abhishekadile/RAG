# RAG From Scratch 🔍

> A complete, hands-on RAG seminar that runs entirely in GitHub Codespaces.
> No local setup. No paid APIs required. Everything works out of the box.

## One-click setup

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/abhishekadile/RAG?quickstart=1)

Click the button above. The Codespace will:

1. Install Python 3.11 + UV
2. Install all dependencies (locked versions)
3. Download the SQuAD corpus
4. Register the Jupyter kernel
5. Run a smoke test

**Total setup time: ~3 minutes**

## Getting API keys (all free, no credit card)

| Service | Purpose | Get key at |
|---------|---------|------------|
| Google Gemini | Embeddings + Generation | [aistudio.google.com](https://aistudio.google.com) → Get API key |
| Groq | Fast generation fallback | [console.groq.com](https://console.groq.com) → API Keys |
| Cohere | Neural reranking | [dashboard.cohere.com](https://dashboard.cohere.com) → API Keys |

After getting keys, edit `.env` in the Codespace:

```bash
GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
COHERE_API_KEY=your_key_here
```

**All keys are optional.** The system falls back to local models automatically.

## Code-along notebooks

| Notebook | Topics |
|----------|--------|
| [01_ingestion.ipynb](notebooks/01_ingestion.ipynb) | Loading docs, chunking strategies, embedding |
| [02_retrieval.ipynb](notebooks/02_retrieval.ipynb) | Dense, sparse, hybrid retrieval |
| [03_generation.ipynb](notebooks/03_generation.ipynb) | RAG prompt engineering, query engine |
| [04_evaluation.ipynb](notebooks/04_evaluation.ipynb) | RAGAS metrics, test sets, scoring |
| [05_advanced.ipynb](notebooks/05_advanced.ipynb) | HyDE, reranking, query rewriting |

## Running the app

```bash
make app    # Gradio UI on port 7860
make nb     # Jupyter on port 8888
make test   # Run fallback scripts
make eval   # Run RAGAS evaluation
make keys   # Check API key status
```

## Project structure

```
rag-from-scratch/
├── src/           # Core RAG pipeline modules
├── notebooks/     # Code-along Jupyter notebooks
├── scripts/       # Fallback .py scripts (mirror notebooks)
├── app/           # Gradio frontend
├── tutorial/      # Deep-dive educational content
├── data/fallback/ # Bundled SQuAD sample (always available)
└── .devcontainer/ # One-click Codespace config
```

## Tutorial

See [`tutorial/`](tutorial/) for deep dives on every concept:

- What is RAG and why does it work?
- Chunking strategies and when to use each
- Dense vs sparse vs hybrid retrieval
- Why reranking matters
- How to evaluate a RAG system
- Do's and don'ts
- Advanced patterns (HyDE, parent-child, query rewriting)

## Local development (without Codespaces)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
cp .env.example .env
uv run python scripts/download_data.py
make test
```

## License

MIT — use freely for teaching and learning.
