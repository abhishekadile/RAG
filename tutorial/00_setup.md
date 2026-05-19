# Setup Guide

This guide walks you through setting up the RAG seminar environment from zero to running notebooks.

## Step 1: Fork the repository

1. Go to the GitHub repository page
2. Click **Fork** in the top-right corner
3. Choose your account as the destination

```
GitHub Repo Page
┌─────────────────────────────────────────────┐
│  rag-from-scratch          [Fork ▼] [Star]  │
│  ─────────────────────────────────────────  │
│  A complete RAG seminar for Codespaces      │
└─────────────────────────────────────────────┘
```

## Step 2: Open in GitHub Codespaces

1. On your fork, click the green **Code** button
2. Select the **Codespaces** tab
3. Click **Create codespace on main**

The devcontainer will automatically:

- Install Python 3.11
- Install UV and sync dependencies
- Create `.env` from `.env.example`
- Download optional SQuAD data
- Register the Jupyter kernel
- Run a smoke test

Expected output:

```
==========================================
  RAG From Scratch — Codespace Setup
==========================================
[1/6] Installing UV...
[2/6] Installing Python dependencies with UV...
...
  ✓ ChromaDB OK
  ✓ sentence-transformers OK
  Setup complete!
```

## Step 3: Get a Gemini API key

1. Visit [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **Get API key** → **Create API key**
4. Copy the key

```
Google AI Studio
┌─────────────────────────────────────────────┐
│  Get API key                                │
│  ┌─────────────────────────────────────┐    │
│  │ AIza...your_key_here                │    │
│  └─────────────────────────────────────┘    │
│  [Copy]                                     │
└─────────────────────────────────────────────┘
```

## Step 4: Get a Groq API key (optional)

1. Visit [console.groq.com](https://console.groq.com)
2. Create an account
3. Go to **API Keys** → **Create API Key**
4. Copy the key

## Step 5: Get a Cohere API key (optional)

1. Visit [dashboard.cohere.com](https://dashboard.cohere.com)
2. Sign up for a free account
3. Go to **API Keys** → **Create Trial Key**
4. Copy the key

## Step 6: Add keys to `.env`

In the Codespace terminal:

```bash
nano .env
```

Add your keys:

```bash
GEMINI_API_KEY=AIza...your_key
GROQ_API_KEY=gsk_...your_key
COHERE_API_KEY=...your_key
```

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X` in nano).

## Step 7: Verify configuration

```bash
make keys
```

Expected output:

```
┌──────────────────── RAG Seminar Configuration ────────────────────┐
│ Setting      │ Value                    │ Status                 │
│ Gemini API   │ gemini-2.5-flash         │ ✓ Available            │
│ Groq API     │ llama-3.3-70b-versatile  │ ✓ Available            │
│ Cohere API   │ rerank-english-v3.5      │ ✓ Available            │
└───────────────────────────────────────────────────────────────────┘
```

## Step 8: Start Jupyter

```bash
make nb
```

Codespaces will notify you that port 8888 is forwarded. Click **Open in Browser**.

Select the kernel: **RAG Seminar (Python 3.11)**.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `make keys` shows no API keys | Edit `.env` and restart terminal |
| Ollama fallback is slow | Set `GEMINI_API_KEY` or `GROQ_API_KEY` |
| Jupyter kernel not found | Run post-create script: `bash .devcontainer/post-create.sh` |
| Port 7860 not opening | Run `make app` and check forwarded ports panel |

## Next steps

- Start with [notebook 01](../notebooks/01_ingestion.ipynb)
- Read [What is RAG?](01_what_is_rag.md)
