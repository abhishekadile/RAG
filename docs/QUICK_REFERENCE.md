# RAG Seminar — Quick Reference Card
# Print this or keep it open during the seminar

## Repo URL
https://github.com/YOUR_USERNAME/rag-from-scratch

## One-click Codespace
https://codespaces.new/YOUR_USERNAME/rag-from-scratch

---

## API Key URLs (all free, no credit card)

| Key | URL | Env var |
|-----|-----|---------|
| Gemini | aistudio.google.com → Get API key | GEMINI_API_KEY |
| Groq | console.groq.com → API Keys | GROQ_API_KEY |
| Cohere | dashboard.cohere.com → API Keys | COHERE_API_KEY |

Add to `.env` file in the Codespace root.

---

## Commands

```bash
make keys    # Check API key status
make nb      # Start Jupyter (port 8888)
make app     # Start Gradio UI (port 7860)
make test    # Run all fallback scripts
make eval    # Run RAGAS evaluation
make clean   # Reset ChromaDB
```

---

## Notebook order

```
01_ingestion.ipynb   → Load + chunk + embed
02_retrieval.ipynb   → Dense + sparse + hybrid
03_generation.ipynb  → Prompt + query engine
04_evaluation.ipynb  → RAGAS + scoring
05_advanced.ipynb    → HyDE + reranking + rewriting
```

---

## If notebooks don't work → run scripts instead

```bash
uv run python scripts/run_all.py
# OR individually:
uv run python scripts/01_ingestion.py
uv run python scripts/02_retrieval.py
uv run python scripts/03_generation.py
uv run python scripts/04_evaluation.py
uv run python scripts/05_advanced.py
```

---

## RAGAS score guide

| Metric | < 0.6 | 0.6–0.8 | > 0.8 |
|--------|-------|---------|-------|
| Faithfulness | 🔴 Hallucinating | 🟡 OK | 🟢 Grounded |
| Answer relevancy | 🔴 Off-topic | 🟡 Reasonable | 🟢 On-point |
| Context precision | 🔴 Noisy retrieval | 🟡 Acceptable | 🟢 Precise |
| Context recall | 🔴 Missing info | 🟡 Partial | 🟢 Good coverage |

---

## Fallback tiers (automatic)

```
Tier 1 (best):     Gemini API + Cohere reranker
Tier 2 (fast):     Groq API + local cross-encoder reranker
Tier 3 (no keys):  sentence-transformers + Ollama (local only)
```

---

## Tutorial docs location

```
tutorial/
  00_setup.md          → API keys + Codespace setup
  01_what_is_rag.md    → RAG fundamentals
  02_chunking.md       → Chunking strategies
  03_retrieval.md      → Dense vs sparse vs hybrid
  04_reranking.md      → Why reranking matters
  05_generation.md     → Prompt engineering for RAG
  06_evaluation.md     → RAGAS metrics explained
  07_dos_and_donts.md  → Common mistakes
  08_advanced.md       → HyDE, query rewriting, etc.
```
