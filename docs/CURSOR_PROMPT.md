# Cursor IDE Implementation Prompt
# RAG Seminar — Full GitHub Codespace Repo

> Paste this entire prompt into Cursor's AI chat (Composer mode, Agent enabled).
> It will build the complete repo from scratch.

---

## CONTEXT

You are building a complete, production-quality RAG (Retrieval-Augmented Generation) seminar
repository that runs entirely inside GitHub Codespaces. This repo is used to teach a live
seminar where attendees code along in Jupyter notebooks.

**Core requirements:**
- One-click GitHub Codespace setup (devcontainer.json handles everything)
- UV for package management (pyproject.toml, NOT requirements.txt)
- LlamaIndex as the RAG framework
- ChromaDB as the local vector store (no external services)
- Gemini API for embeddings + generation (free tier, no credit card)
- Groq API as fast generation fallback (free tier, no credit card)
- Cohere API for reranking (free tier, no credit card)
- sentence-transformers all-MiniLM-L6-v2 as local embedding fallback
- SQuAD 2.0 Wikipedia subset as the validated corpus
- Gradio frontend (chat + file upload + chunk inspector + eval dashboard)
- Jupyter notebooks (.ipynb) for code-along with skeleton cells
- Pre-written .py fallback files that compile if notebooks aren't used
- Tutorial folder with deep educational content
- RAGAS + LlamaIndex eval for automated scoring
- Do's and Don'ts guide, eval guide, validation guide

---

## REPO STRUCTURE TO CREATE

```
rag-from-scratch/
├── .devcontainer/
│   ├── devcontainer.json          # One-click Codespace config
│   └── post-create.sh             # Post-creation setup script
├── .github/
│   └── workflows/
│       └── test.yml               # CI: runs fallback .py files end-to-end
├── src/
│   ├── __init__.py
│   ├── config.py                  # Centralised config: API keys, model names, paths
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── loader.py              # Document loading: PDF, MD, TXT, URL, SQuAD JSON
│   │   ├── chunker.py             # Fixed, sentence, semantic chunking strategies
│   │   └── embedder.py            # Gemini / sentence-transformers embedder
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── store.py               # ChromaDB vector store wrapper
│   │   ├── retriever.py           # Dense + BM25 hybrid retriever
│   │   └── reranker.py            # Cohere reranker + local cross-encoder fallback
│   ├── generation/
│   │   ├── __init__.py
│   │   ├── generator.py           # Gemini / Groq / Ollama generator
│   │   └── prompts.py             # RAG prompt templates
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── evaluator.py           # RAGAS wrapper: faithfulness, relevance, precision
│   │   ├── testset.py             # SQuAD test set builder
│   │   └── metrics.py             # Custom metrics + scoring utils
│   └── utils/
│       ├── __init__.py
│       ├── fallback.py            # API key detection + graceful fallback logic
│       └── display.py             # Pretty printing for notebooks
├── notebooks/
│   ├── 01_ingestion.ipynb         # Code-along: load, chunk, embed
│   ├── 02_retrieval.ipynb         # Code-along: dense, sparse, hybrid retrieval
│   ├── 03_generation.ipynb        # Code-along: prompting, RAG pipeline
│   ├── 04_evaluation.ipynb        # Code-along: RAGAS, test sets, metrics
│   └── 05_advanced.ipynb          # Code-along: HyDE, reranking, query rewriting
├── scripts/
│   ├── 01_ingestion.py            # Fallback: runs if notebook not used
│   ├── 02_retrieval.py
│   ├── 03_generation.py
│   ├── 04_evaluation.py
│   ├── 05_advanced.py
│   └── run_all.py                 # Runs all scripts in order, validates output
├── app/
│   ├── main.py                    # Gradio app entry point
│   ├── components/
│   │   ├── chat.py                # Chat interface component
│   │   ├── uploader.py            # File upload + ingestion component
│   │   ├── inspector.py           # Chunk inspector component
│   │   └── eval_dashboard.py      # Live eval scores component
│   └── utils.py                   # App-level helpers
├── data/
│   ├── fallback/
│   │   ├── squad_sample.json      # 50 SQuAD QA pairs (bundled, always available)
│   │   └── articles/              # 5 Wikipedia articles from SQuAD corpus (bundled)
│   └── squad/                     # Full SQuAD 2.0 download (gitignored, downloaded on setup)
├── tutorial/
│   ├── README.md                  # Tutorial index
│   ├── 00_setup.md                # API key setup guide with screenshots
│   ├── 01_what_is_rag.md          # RAG fundamentals
│   ├── 02_chunking_deep_dive.md   # Chunking strategies + tradeoffs
│   ├── 03_retrieval_deep_dive.md  # Dense vs sparse vs hybrid
│   ├── 04_reranking.md            # Why reranking matters + how it works
│   ├── 05_generation_prompting.md # Prompt engineering for RAG
│   ├── 06_evaluation.md           # How to evaluate a RAG system
│   ├── 07_dos_and_donts.md        # Common mistakes and best practices
│   └── 08_advanced_patterns.md    # HyDE, parent-child, query rewriting
├── docs/
│   └── VALIDATION_CHECKLIST.md   # Pre-ship RAG validation checklist
├── pyproject.toml                 # UV package management
├── .env.example                   # Example env file (never commit .env)
├── .gitignore
├── Makefile                       # make setup / make app / make eval / make test
└── README.md                      # Main README with Codespace badge
```

---

## FILE IMPLEMENTATIONS

### 1. `.devcontainer/devcontainer.json`

```json
{
  "name": "RAG From Scratch",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "features": {
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "forwardPorts": [7860, 8888],
  "portsAttributes": {
    "7860": { "label": "Gradio App", "onAutoForward": "openPreview" },
    "8888": { "label": "Jupyter", "onAutoForward": "notify" }
  },
  "postCreateCommand": "bash .devcontainer/post-create.sh",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-toolsai.jupyter",
        "ms-toolsai.jupyter-keymap",
        "charliermarsh.ruff",
        "ms-python.vscode-pylance",
        "GitHub.copilot"
      ],
      "settings": {
        "python.defaultInterpreterPath": ".venv/bin/python",
        "jupyter.kernelProviderPriority": ["ms-toolsai.jupyter-local"],
        "editor.formatOnSave": true
      }
    }
  },
  "remoteEnv": {
    "GEMINI_API_KEY": "${localEnv:GEMINI_API_KEY}",
    "GROQ_API_KEY": "${localEnv:GROQ_API_KEY}",
    "COHERE_API_KEY": "${localEnv:COHERE_API_KEY}"
  }
}
```

### 2. `.devcontainer/post-create.sh`

```bash
#!/bin/bash
set -e

echo "=========================================="
echo "  RAG From Scratch — Codespace Setup"
echo "=========================================="

# Install UV
echo "[1/6] Installing UV..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc

# Create virtualenv and install deps
echo "[2/6] Installing Python dependencies with UV..."
uv venv .venv --python 3.11
uv sync

# Copy env example if .env doesn't exist
echo "[3/6] Setting up environment file..."
if [ ! -f .env ]; then
  cp .env.example .env
  echo "  → .env created from .env.example. Add your API keys!"
fi

# Download SQuAD 2.0 fallback data
echo "[4/6] Downloading SQuAD fallback corpus..."
python scripts/download_data.py

# Register Jupyter kernel
echo "[5/6] Registering Jupyter kernel..."
uv run python -m ipykernel install --user --name=rag-seminar --display-name="RAG Seminar (Python 3.11)"

# Run smoke test
echo "[6/6] Running smoke test..."
uv run python -c "
import chromadb
from sentence_transformers import SentenceTransformer
print('  ✓ ChromaDB OK')
print('  ✓ sentence-transformers OK')
print('')
print('========================================')
print('  Setup complete!')
print('  Run: make app    → start Gradio UI')
print('  Run: make nb     → start Jupyter')
print('  Run: make test   → run all scripts')
print('========================================')
"
```

### 3. `pyproject.toml`

```toml
[project]
name = "rag-from-scratch"
version = "0.1.0"
description = "RAG seminar — build a complete RAG system from scratch"
requires-python = ">=3.11"
dependencies = [
  # RAG framework
  "llama-index>=0.11.0",
  "llama-index-vector-stores-chroma>=0.2.0",
  "llama-index-embeddings-gemini>=0.2.0",
  "llama-index-llms-gemini>=0.3.0",
  "llama-index-llms-groq>=0.2.0",
  "llama-index-postprocessor-cohere-rerank>=0.2.0",
  "llama-index-embeddings-huggingface>=0.3.0",

  # Vector store
  "chromadb>=0.5.0",

  # Embeddings (local fallback)
  "sentence-transformers>=3.0.0",

  # Sparse retrieval
  "rank-bm25>=0.2.2",

  # Evaluation
  "ragas>=0.2.0",

  # LLM clients
  "google-generativeai>=0.8.0",
  "groq>=0.11.0",
  "cohere>=5.0.0",
  "openai>=1.40.0",  # Used for Groq OpenAI-compatible calls

  # Frontend
  "gradio>=5.0.0",

  # Notebooks
  "jupyter>=1.0.0",
  "ipykernel>=6.0.0",
  "nbformat>=5.0.0",

  # Data + utilities
  "datasets>=2.20.0",    # SQuAD download
  "pandas>=2.0.0",
  "numpy>=1.26.0",
  "tqdm>=4.66.0",
  "python-dotenv>=1.0.0",
  "rich>=13.0.0",        # Pretty terminal output
  "httpx>=0.27.0",

  # Dev
  "ruff>=0.5.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.uv]
dev-dependencies = [
  "pytest>=8.0.0",
  "pytest-asyncio>=0.23.0",
]
```

### 4. `src/config.py`

```python
"""
Centralised configuration. All settings read from environment variables.
Graceful fallbacks when API keys are not present.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
FALLBACK_DIR = DATA_DIR / "fallback"
CHROMA_DIR = ROOT / ".chroma_db"

# ── API Keys (all optional — graceful fallback if missing) ─────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")

# ── Model names ────────────────────────────────────────────────────────────
# Generation
GEMINI_MODEL = "gemini-2.5-flash"
GROQ_MODEL = "llama-3.3-70b-versatile"
LOCAL_MODEL = "ollama/llama3.2:3b"

# Embeddings
GEMINI_EMBED_MODEL = "models/text-embedding-004"
LOCAL_EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBED_DIM = 384  # all-MiniLM-L6-v2 dimension

# Reranking
COHERE_RERANK_MODEL = "rerank-english-v3.5"
LOCAL_RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ── RAG Settings ───────────────────────────────────────────────────────────
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64
TOP_K_RETRIEVE = 10   # retrieve this many before reranking
TOP_K_RERANK = 3      # keep this many after reranking
COLLECTION_NAME = "rag_seminar"

# ── Evaluation ─────────────────────────────────────────────────────────────
EVAL_SAMPLE_SIZE = 20  # number of SQuAD QA pairs to evaluate on

# ── Capability detection ───────────────────────────────────────────────────
HAS_GEMINI = bool(GEMINI_API_KEY)
HAS_GROQ = bool(GROQ_API_KEY)
HAS_COHERE = bool(COHERE_API_KEY)

def print_config():
    """Print current configuration and detected capabilities."""
    from rich.console import Console
    from rich.table import Table
    c = Console()
    t = Table(title="RAG Seminar Configuration", show_header=True)
    t.add_column("Setting", style="cyan")
    t.add_column("Value", style="white")
    t.add_column("Status", style="green")
    t.add_row("Gemini API", GEMINI_MODEL if HAS_GEMINI else "—", "✓ Available" if HAS_GEMINI else "✗ Using local fallback")
    t.add_row("Groq API", GROQ_MODEL if HAS_GROQ else "—", "✓ Available" if HAS_GROQ else "✗ Not configured")
    t.add_row("Cohere API", COHERE_RERANK_MODEL if HAS_COHERE else "—", "✓ Available" if HAS_COHERE else "✗ Using BM25 rerank fallback")
    t.add_row("Embeddings", GEMINI_EMBED_MODEL if HAS_GEMINI else LOCAL_EMBED_MODEL, "API" if HAS_GEMINI else "Local")
    t.add_row("Chunk size", str(CHUNK_SIZE), "")
    t.add_row("Top-K retrieve", str(TOP_K_RETRIEVE), "")
    t.add_row("Top-K rerank", str(TOP_K_RERANK), "")
    c.print(t)
```

### 5. `src/utils/fallback.py`

```python
"""
Graceful fallback logic. Detects which API keys are available
and returns the appropriate LLM / embedder / reranker.
"""
from src.config import (
    HAS_GEMINI, HAS_GROQ, HAS_COHERE,
    GEMINI_API_KEY, GROQ_API_KEY, COHERE_API_KEY,
    GEMINI_MODEL, GROQ_MODEL,
    GEMINI_EMBED_MODEL, LOCAL_EMBED_MODEL,
    COHERE_RERANK_MODEL, LOCAL_RERANK_MODEL,
    TOP_K_RERANK,
)

def get_llm():
    """Return the best available LLM."""
    if HAS_GEMINI:
        from llama_index.llms.gemini import Gemini
        return Gemini(model=GEMINI_MODEL, api_key=GEMINI_API_KEY)
    elif HAS_GROQ:
        from llama_index.llms.groq import Groq
        return Groq(model=GROQ_MODEL, api_key=GROQ_API_KEY)
    else:
        # Local Ollama fallback
        from llama_index.llms.ollama import Ollama
        print("⚠ No API keys found. Using Ollama local model (slow on CPU).")
        print("  Run: ollama pull llama3.2:3b")
        return Ollama(model="llama3.2:3b", request_timeout=120.0)

def get_embed_model():
    """Return the best available embedding model."""
    if HAS_GEMINI:
        from llama_index.embeddings.gemini import GeminiEmbedding
        return GeminiEmbedding(model_name=GEMINI_EMBED_MODEL, api_key=GEMINI_API_KEY)
    else:
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
        print("⚠ No Gemini key. Using local sentence-transformers (all-MiniLM-L6-v2).")
        return HuggingFaceEmbedding(model_name=LOCAL_EMBED_MODEL)

def get_reranker():
    """Return the best available reranker."""
    if HAS_COHERE:
        from llama_index.postprocessor.cohere_rerank import CohereRerank
        return CohereRerank(api_key=COHERE_API_KEY, model=COHERE_RERANK_MODEL, top_n=TOP_K_RERANK)
    else:
        from llama_index.core.postprocessor import SentenceTransformerRerank
        print("⚠ No Cohere key. Using local cross-encoder reranker.")
        return SentenceTransformerRerank(model=LOCAL_RERANK_MODEL, top_n=TOP_K_RERANK)
```

### 6. `src/ingestion/loader.py`

```python
"""
Document loader. Supports: PDF, Markdown, TXT, URL, SQuAD JSON.
Returns LlamaIndex Document objects in all cases.
"""
import json
from pathlib import Path
from typing import List
from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core.readers.base import BaseReader

class SQuADLoader(BaseReader):
    """Load SQuAD 2.0 format JSON into LlamaIndex Documents."""

    def load_data(self, file_path: str | Path) -> List[Document]:
        with open(file_path) as f:
            squad = json.load(f)

        documents = []
        for article in squad["data"]:
            title = article["title"]
            for paragraph in article["paragraphs"]:
                context = paragraph["context"]
                # Store QA pairs as metadata for eval
                qas = [
                    {"question": qa["question"], "answer": qa["answers"][0]["text"] if qa["answers"] else ""}
                    for qa in paragraph["qas"]
                    if not qa["is_impossible"]
                ]
                documents.append(Document(
                    text=context,
                    metadata={"title": title, "source": "squad", "qas": qas}
                ))
        return documents

def load_documents(source: str | Path) -> List[Document]:
    """
    Universal document loader.
    - Directory: loads all files recursively
    - .json: tries SQuAD format
    - URL (starts with http): fetches webpage
    - Single file: loads based on extension
    """
    source = str(source)

    if source.startswith("http"):
        from llama_index.readers.web import SimpleWebPageReader
        return SimpleWebPageReader(html_to_text=True).load_data([source])

    path = Path(source)
    if path.is_dir():
        return SimpleDirectoryReader(str(path), recursive=True).load_data()

    if path.suffix == ".json":
        return SQuADLoader().load_data(path)

    return SimpleDirectoryReader(input_files=[str(path)]).load_data()
```

### 7. `src/ingestion/chunker.py`

```python
"""
Chunking strategies. This is one of the most important decisions in RAG.

Strategies implemented:
  - Fixed size: simple, predictable, fast
  - Sentence window: preserves sentence boundaries
  - Semantic: groups semantically similar sentences (best quality, slowest)
  - Hierarchical: parent + child nodes (for parent-child retrieval)
"""
from typing import List, Literal
from llama_index.core import Document
from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
    HierarchicalNodeParser,
)
from llama_index.core.schema import BaseNode
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

ChunkStrategy = Literal["fixed", "sentence", "semantic", "hierarchical"]

def chunk_documents(
    documents: List[Document],
    strategy: ChunkStrategy = "sentence",
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
    embed_model=None,
) -> List[BaseNode]:
    """
    Chunk documents into nodes using the specified strategy.

    Args:
        documents: List of LlamaIndex Documents
        strategy: Chunking strategy to use
        chunk_size: Target chunk size in tokens (fixed/sentence)
        chunk_overlap: Overlap between chunks in tokens
        embed_model: Required for semantic chunking

    Returns:
        List of LlamaIndex nodes ready for embedding
    """
    if strategy == "fixed":
        # Simple fixed-size chunks. Fast but ignores sentence boundaries.
        # DO: Use for uniform, structured text (tables, code)
        # DON'T: Use for narrative text — cuts mid-sentence
        parser = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            paragraph_separator="\n\n",
        )

    elif strategy == "sentence":
        # Respects sentence boundaries. Good default choice.
        # DO: Use as your starting point for most corpora
        parser = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            paragraph_separator="\n\n",
        )

    elif strategy == "semantic":
        # Groups sentences by semantic similarity. Best quality.
        # DON'T: Use without an embed_model — it will fail
        # DON'T: Use on large corpora without caching — slow
        if embed_model is None:
            raise ValueError("embed_model required for semantic chunking")
        parser = SemanticSplitterNodeParser(
            embed_model=embed_model,
            breakpoint_percentile_threshold=95,
        )

    elif strategy == "hierarchical":
        # Creates parent + child nodes. Use with ParentDocumentRetriever.
        # DO: Use when you want to retrieve small chunks but return large context
        parser = HierarchicalNodeParser.from_defaults(
            chunk_sizes=[2048, 512, 128]
        )
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    nodes = parser.get_nodes_from_documents(documents, show_progress=True)
    print(f"  Chunked {len(documents)} documents into {len(nodes)} nodes")
    print(f"  Strategy: {strategy} | Chunk size: {chunk_size} | Overlap: {chunk_overlap}")
    return nodes
```

### 8. `src/retrieval/store.py`

```python
"""
ChromaDB vector store wrapper.
Handles collection creation, upserting nodes, and returning a LlamaIndex index.
"""
import chromadb
from pathlib import Path
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.schema import BaseNode
from typing import List
from src.config import CHROMA_DIR, COLLECTION_NAME

def get_or_create_index(
    nodes: List[BaseNode] | None = None,
    embed_model=None,
    collection_name: str = COLLECTION_NAME,
    persist_dir: str | Path = CHROMA_DIR,
    force_rebuild: bool = False,
) -> VectorStoreIndex:
    """
    Get existing index from ChromaDB or create a new one.

    Args:
        nodes: If provided, creates/rebuilds the index with these nodes
        embed_model: Embedding model to use
        collection_name: ChromaDB collection name
        persist_dir: Where ChromaDB persists data
        force_rebuild: Delete and recreate if collection exists

    Returns:
        LlamaIndex VectorStoreIndex backed by ChromaDB
    """
    persist_dir = Path(persist_dir)
    persist_dir.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(persist_dir))

    if force_rebuild:
        try:
            client.delete_collection(collection_name)
            print(f"  Deleted existing collection: {collection_name}")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )

    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    if nodes:
        print(f"  Building index with {len(nodes)} nodes...")
        index = VectorStoreIndex(
            nodes,
            storage_context=storage_context,
            embed_model=embed_model,
            show_progress=True,
        )
        count = collection.count()
        print(f"  ✓ Index built. ChromaDB collection has {count} vectors.")
    else:
        print(f"  Loading existing index from {persist_dir}...")
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model=embed_model,
        )

    return index
```

### 9. `src/retrieval/retriever.py`

```python
"""
Hybrid retriever: dense (vector) + sparse (BM25).
Dense retrieval finds semantically similar chunks.
Sparse retrieval finds exact keyword matches.
Combining both is almost always better than either alone.
"""
from typing import List
from llama_index.core import VectorStoreIndex
from llama_index.core.schema import BaseNode, NodeWithScore
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever
from src.config import TOP_K_RETRIEVE

def get_dense_retriever(index: VectorStoreIndex, top_k: int = TOP_K_RETRIEVE):
    """Pure vector similarity retriever."""
    return index.as_retriever(similarity_top_k=top_k)

def get_hybrid_retriever(
    index: VectorStoreIndex,
    nodes: List[BaseNode],
    top_k: int = TOP_K_RETRIEVE,
    mode: str = "reciprocal_rerank",  # "simple" | "reciprocal_rerank"
):
    """
    Hybrid retriever combining dense + sparse (BM25).

    Why hybrid?
    - Dense: great for paraphrases, semantic similarity
    - BM25: great for exact matches, rare terms, names, numbers
    - Combined: catches what either alone would miss

    Args:
        index: VectorStoreIndex (for dense)
        nodes: All nodes (for BM25)
        top_k: Number of results to retrieve
        mode: Fusion mode for combining results

    Returns:
        QueryFusionRetriever combining both
    """
    dense = VectorIndexRetriever(index=index, similarity_top_k=top_k)
    sparse = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=top_k)

    return QueryFusionRetriever(
        retrievers=[dense, sparse],
        similarity_top_k=top_k,
        num_queries=1,  # set > 1 to enable query expansion (advanced)
        mode=mode,
        use_async=False,
    )
```

### 10. `src/retrieval/reranker.py`

```python
"""
Reranking: takes top-K retrieved chunks and re-scores them.

Why rerank?
- Vector similarity is a proxy for relevance, not relevance itself
- Rerankers (cross-encoders) jointly process query + document — much more accurate
- Cohere's reranker is trained specifically for retrieval tasks
- Reranking is cheap: you only rerank the top-K, not the whole corpus

The typical pipeline:
  Query → Retrieve top-20 (fast, approximate)
         → Rerank to top-3 (slow, accurate)
         → Generate answer from top-3
"""
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from src.utils.fallback import get_reranker

def build_reranker(top_n: int = 3) -> BaseNodePostprocessor:
    """
    Build reranker with automatic fallback.
    - If COHERE_API_KEY is set: uses Cohere rerank-english-v3.5
    - Otherwise: uses local sentence-transformers cross-encoder
    """
    reranker = get_reranker()
    reranker.top_n = top_n
    return reranker
```

### 11. `src/generation/prompts.py`

```python
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

# ── Base RAG prompt ────────────────────────────────────────────────────────
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

# ── HyDE prompt (Hypothetical Document Embedding) ─────────────────────────
HYDE_TEMPLATE = PromptTemplate(
    "Write a detailed paragraph that would answer the following question. "
    "Do not reference that this is hypothetical.\n\n"
    "Question: {query_str}\n\n"
    "Hypothetical answer paragraph:"
)

# ── Query rewriting prompt ─────────────────────────────────────────────────
QUERY_REWRITE_TEMPLATE = PromptTemplate(
    "You are a search query optimizer. Rewrite the user's question to be "
    "more specific and retrieval-friendly, without changing its intent. "
    "Return only the rewritten query.\n\n"
    "Original question: {query_str}\n\n"
    "Rewritten query:"
)

# ── Step-back prompt ───────────────────────────────────────────────────────
STEP_BACK_TEMPLATE = PromptTemplate(
    "Given a specific question, generate a more general 'step-back' question "
    "that would help retrieve broader context useful for answering the original.\n\n"
    "Specific question: {query_str}\n\n"
    "Step-back question:"
)
```

### 12. `src/generation/generator.py`

```python
"""
RAG query engine. Wires together: retriever + reranker + LLM + prompt.
"""
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from src.generation.prompts import RAG_QA_TEMPLATE, RAG_SYSTEM_PROMPT
from src.utils.fallback import get_llm, get_embed_model, get_reranker
from src.config import TOP_K_RETRIEVE, TOP_K_RERANK

def build_query_engine(
    index: VectorStoreIndex,
    nodes=None,
    use_hybrid: bool = True,
    use_reranker: bool = True,
    top_k_retrieve: int = TOP_K_RETRIEVE,
    top_k_rerank: int = TOP_K_RERANK,
    streaming: bool = False,
):
    """
    Build a complete RAG query engine.

    Args:
        index: ChromaDB-backed VectorStoreIndex
        nodes: All nodes (required for hybrid retrieval)
        use_hybrid: Use BM25 + dense hybrid retrieval
        use_reranker: Apply reranking after retrieval
        top_k_retrieve: How many chunks to retrieve initially
        top_k_rerank: How many chunks to keep after reranking
        streaming: Enable streaming responses

    Returns:
        LlamaIndex QueryEngine
    """
    llm = get_llm()
    Settings.llm = llm

    # Build retriever
    if use_hybrid and nodes:
        from src.retrieval.retriever import get_hybrid_retriever
        retriever = get_hybrid_retriever(index, nodes, top_k=top_k_retrieve)
    else:
        from src.retrieval.retriever import get_dense_retriever
        retriever = get_dense_retriever(index, top_k=top_k_retrieve)

    # Build postprocessors
    postprocessors = []
    if use_reranker:
        reranker = get_reranker()
        reranker.top_n = top_k_rerank
        postprocessors.append(reranker)
    else:
        # At minimum filter by similarity score
        postprocessors.append(SimilarityPostprocessor(similarity_cutoff=0.3))

    # Build query engine
    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        node_postprocessors=postprocessors,
        text_qa_template=RAG_QA_TEMPLATE,
        streaming=streaming,
        llm=llm,
    )
    return query_engine
```

### 13. `src/evaluation/testset.py`

```python
"""
Build evaluation test sets from SQuAD 2.0.
SQuAD gives us ground-truth questions + answers — perfect for RAG eval.
"""
import json
import random
from pathlib import Path
from typing import List, Dict
from src.config import FALLBACK_DIR, EVAL_SAMPLE_SIZE

def load_squad_testset(
    path: str | Path | None = None,
    sample_size: int = EVAL_SAMPLE_SIZE,
    seed: int = 42,
) -> List[Dict]:
    """
    Load SQuAD QA pairs as a test set.

    Returns list of dicts with keys:
      - question: str
      - ground_truth: str
      - context: str (the passage the answer comes from)
    """
    if path is None:
        path = FALLBACK_DIR / "squad_sample.json"

    with open(path) as f:
        squad = json.load(f)

    pairs = []
    for article in squad["data"]:
        for paragraph in article["paragraphs"]:
            context = paragraph["context"]
            for qa in paragraph["qas"]:
                if qa["is_impossible"] or not qa["answers"]:
                    continue
                pairs.append({
                    "question": qa["question"],
                    "ground_truth": qa["answers"][0]["text"],
                    "context": context,
                    "title": article["title"],
                })

    random.seed(seed)
    sample = random.sample(pairs, min(sample_size, len(pairs)))
    print(f"  Loaded {len(sample)} QA pairs from SQuAD")
    return sample
```

### 14. `src/evaluation/evaluator.py`

```python
"""
RAGAS evaluation wrapper.

Metrics explained:
  - Faithfulness: Is the answer grounded in the retrieved context?
      Score 1.0 = every claim in the answer is supported by context
      Score 0.0 = answer contains hallucinated claims
  - Answer Relevancy: Does the answer actually address the question?
      Score 1.0 = answer directly answers the question
      Score 0.0 = answer is off-topic
  - Context Precision: Are the retrieved chunks relevant?
      Score 1.0 = all retrieved chunks are useful
      Score 0.0 = retrieved chunks are noise
  - Context Recall: Did we retrieve the chunks needed to answer?
      Score 1.0 = all needed information was retrieved
      Score 0.0 = key information was not retrieved

The ideal RAG system scores high on ALL four.
Typical tradeoffs:
  - High precision, low recall: retriever is conservative (safe but incomplete)
  - High recall, low precision: retriever casts too wide a net (noisy)
"""
from typing import List, Dict
from datasets import Dataset

def evaluate_rag(
    questions: List[str],
    answers: List[str],
    contexts: List[List[str]],
    ground_truths: List[str],
    llm=None,
    embed_model=None,
) -> Dict:
    """
    Run RAGAS evaluation on a list of QA pairs.

    Args:
        questions: List of questions
        answers: List of generated answers
        contexts: List of retrieved context lists (one per question)
        ground_truths: List of ground truth answers
        llm: LLM for judge-based metrics (uses default if None)
        embed_model: Embedding model for relevancy metrics

    Returns:
        Dict with metric scores + per-sample results
    """
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    )
    from ragas.llms import LangchainLLMWrapper
    from ragas.embeddings import LangchainEmbeddingsWrapper

    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    }
    dataset = Dataset.from_dict(data)

    result = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    )

    scores = result.to_pandas()
    summary = {
        "faithfulness": float(scores["faithfulness"].mean()),
        "answer_relevancy": float(scores["answer_relevancy"].mean()),
        "context_precision": float(scores["context_precision"].mean()),
        "context_recall": float(scores["context_recall"].mean()),
        "per_sample": scores.to_dict(orient="records"),
    }
    return summary

def print_eval_summary(scores: Dict):
    """Pretty print evaluation scores with interpretation."""
    from rich.console import Console
    from rich.table import Table
    c = Console()
    t = Table(title="RAGAS Evaluation Results", show_header=True)
    t.add_column("Metric", style="cyan")
    t.add_column("Score", style="white")
    t.add_column("Interpretation", style="dim")

    interpretations = {
        "faithfulness": ("< 0.7: Hallucination risk", "0.7-0.9: Good", "> 0.9: Excellent — low hallucination"),
        "answer_relevancy": ("< 0.6: Off-topic answers", "0.6-0.8: Reasonable", "> 0.8: Answers are on-point"),
        "context_precision": ("< 0.5: Too much noise in retrieved chunks", "0.5-0.8: OK", "> 0.8: Retrieval is precise"),
        "context_recall": ("< 0.5: Missing key information", "0.5-0.8: Partial coverage", "> 0.8: Good coverage"),
    }
    for metric, score in scores.items():
        if metric == "per_sample":
            continue
        thresholds = interpretations.get(metric, ("", "", ""))
        if score < 0.6:
            interp = thresholds[0]
            style = "red"
        elif score < 0.8:
            interp = thresholds[1]
            style = "yellow"
        else:
            interp = thresholds[2]
            style = "green"
        t.add_row(metric, f"[{style}]{score:.3f}[/{style}]", interp)
    c.print(t)
```

### 15. `scripts/run_all.py`

```python
#!/usr/bin/env python
"""
Run all pipeline scripts in order. Used when notebooks are not available.
This is the fallback path — attendees who don't use Jupyter can run:

    make test
    # or
    uv run python scripts/run_all.py

Each script is self-contained and can be run independently.
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS = [
    "scripts/01_ingestion.py",
    "scripts/02_retrieval.py",
    "scripts/03_generation.py",
    "scripts/04_evaluation.py",
    "scripts/05_advanced.py",
]

def run_script(path: str) -> bool:
    print(f"\n{'='*60}")
    print(f"  Running: {path}")
    print(f"{'='*60}")
    result = subprocess.run(
        [sys.executable, path],
        capture_output=False,
        text=True,
    )
    if result.returncode != 0:
        print(f"\n✗ FAILED: {path}")
        return False
    print(f"\n✓ PASSED: {path}")
    return True

if __name__ == "__main__":
    results = []
    for script in SCRIPTS:
        if not Path(script).exists():
            print(f"  Skipping {script} (not found)")
            continue
        results.append(run_script(script))

    print(f"\n{'='*60}")
    passed = sum(results)
    total = len(results)
    print(f"  Results: {passed}/{total} scripts passed")
    if passed == total:
        print("  ✓ All scripts passed!")
    else:
        print("  ✗ Some scripts failed. Check output above.")
    sys.exit(0 if passed == total else 1)
```

### 16. `Makefile`

```makefile
.PHONY: setup app nb test eval clean help

help:
	@echo "RAG From Scratch — Available commands"
	@echo ""
	@echo "  make setup    Install dependencies (UV)"
	@echo "  make app      Start Gradio frontend (port 7860)"
	@echo "  make nb       Start Jupyter (port 8888)"
	@echo "  make test     Run all fallback .py scripts"
	@echo "  make eval     Run RAGAS evaluation on SQuAD"
	@echo "  make clean    Delete ChromaDB and cached data"
	@echo "  make keys     Check which API keys are configured"

setup:
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv sync
	cp -n .env.example .env || true
	uv run python scripts/download_data.py

app:
	uv run python app/main.py

nb:
	uv run jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token=''

test:
	uv run python scripts/run_all.py

eval:
	uv run python scripts/04_evaluation.py

clean:
	rm -rf .chroma_db
	rm -rf data/squad/*.json
	find . -type d -name __pycache__ -exec rm -rf {} +

keys:
	uv run python -c "from src.config import print_config; print_config()"

download:
	uv run python scripts/download_data.py
```

### 17. `.env.example`

```bash
# ─────────────────────────────────────────────────
# RAG From Scratch — Environment Variables
# Copy this file to .env and fill in your keys
# NEVER commit .env to git
# ─────────────────────────────────────────────────

# REQUIRED for best experience (free, no credit card):
# Get at: https://aistudio.google.com → Get API key
GEMINI_API_KEY=

# OPTIONAL — fast inference fallback (free, no credit card):
# Get at: https://console.groq.com → API Keys
GROQ_API_KEY=

# OPTIONAL — neural reranking (free trial, no credit card):
# Get at: https://dashboard.cohere.com → API Keys
COHERE_API_KEY=

# If ALL keys above are empty, the system uses:
#   Embeddings: sentence-transformers/all-MiniLM-L6-v2 (local)
#   Generation: Ollama llama3.2:3b (local — run: ollama pull llama3.2:3b)
#   Reranking:  cross-encoder/ms-marco-MiniLM-L-6-v2 (local)
```

### 18. `README.md`

```markdown
# RAG From Scratch 🔍

> A complete, hands-on RAG seminar that runs entirely in GitHub Codespaces.
> No local setup. No paid APIs required. Everything works out of the box.

## One-click setup

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/YOUR_USERNAME/rag-from-scratch?quickstart=1)

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
\`\`\`bash
GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
COHERE_API_KEY=your_key_here
\`\`\`

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

\`\`\`bash
make app    # Gradio UI on port 7860
make nb     # Jupyter on port 8888
make test   # Run fallback scripts
make eval   # Run RAGAS evaluation
make keys   # Check API key status
\`\`\`

## Tutorial

See [`tutorial/`](tutorial/) for deep dives on every concept:
- What is RAG and why does it work?
- Chunking strategies and when to use each
- Dense vs sparse vs hybrid retrieval
- Why reranking matters
- How to evaluate a RAG system
- Do's and don'ts
- Advanced patterns (HyDE, parent-child, query rewriting)
```

---

## NOTEBOOK IMPLEMENTATION PATTERN

Each notebook follows this exact pattern. Implement all 5 notebooks:

```python
# Cell 1: Header + learning objectives (Markdown)
# Cell 2: Setup + imports (Code)
# Cell 3: Section intro (Markdown)
# Cell 4: EXERCISE cell — skeleton with # YOUR CODE HERE comments
# Cell 5: SOLUTION cell — complete implementation (hidden by default)
# Cell 6: Visualization / verification
# Repeat for each major concept
```

**EXERCISE cells look like this:**
```python
# ── EXERCISE ──────────────────────────────────────────────────────────────
# Load the SQuAD fallback corpus and print:
#   - Number of documents loaded
#   - First document's text (first 200 chars)
#   - First document's metadata

# YOUR CODE HERE
documents = ???

print(f"Loaded: {???} documents")
print(f"First doc preview: {???}")
print(f"Metadata: {???}")
```

**SOLUTION cells look like this:**
```python
# ── SOLUTION (expand to see) ──────────────────────────────────────────────
from src.ingestion.loader import load_documents
from src.config import FALLBACK_DIR

documents = load_documents(FALLBACK_DIR / "squad_sample.json")

print(f"Loaded: {len(documents)} documents")
print(f"First doc preview: {documents[0].text[:200]}")
print(f"Metadata: {documents[0].metadata}")
```

---

## TUTORIAL CONTENT TO WRITE

### `tutorial/00_setup.md`
Complete step-by-step setup guide:
1. Fork the repo on GitHub
2. Open in Codespace (with screenshots)
3. Get Gemini API key (with screenshots of aistudio.google.com)
4. Get Groq API key (with screenshots of console.groq.com)
5. Get Cohere API key (with screenshots of dashboard.cohere.com)
6. Add keys to .env
7. Verify with `make keys`
8. Start Jupyter with `make nb`

### `tutorial/01_what_is_rag.md`
- The problem RAG solves (LLM knowledge cutoff, hallucination, private data)
- The RAG pipeline end-to-end
- When to use RAG vs fine-tuning vs in-context learning
- Real-world RAG use cases

### `tutorial/02_chunking_deep_dive.md`
- Why chunking matters (the goldilocks problem)
- Fixed size: pros, cons, when to use
- Sentence-aware: pros, cons, when to use
- Semantic chunking: pros, cons, when to use
- Hierarchical / parent-child: pros, cons, when to use
- How to choose chunk size (experiments with eval scores)
- DO: Test multiple chunk sizes with eval metrics
- DON'T: Use the same chunk size for all document types

### `tutorial/03_retrieval_deep_dive.md`
- How vector similarity works (cosine similarity, dot product)
- What BM25 is and why it complements dense retrieval
- When hybrid beats dense-only (keyword queries, rare terms)
- HNSW: how ChromaDB actually stores and searches vectors
- Retrieval failure modes and how to diagnose them

### `tutorial/04_reranking.md`
- Why retrieved order ≠ relevance order
- Bi-encoders vs cross-encoders (speed vs accuracy tradeoff)
- Cohere reranker internals
- How to measure reranking improvement with eval metrics
- DO: Always rerank if latency allows
- DON'T: Skip reranking and wonder why context is noisy

### `tutorial/05_generation_prompting.md`
- The RAG prompt structure (system + context + question)
- How to prevent the model from using prior knowledge
- Handling "I don't know" gracefully
- Citation and grounding techniques
- DO: Explicitly instruct the model to cite context
- DON'T: Let the model answer from general knowledge

### `tutorial/06_evaluation.md`
- Why "it seems good" is not enough
- The 4 RAGAS metrics explained with examples
- How to build a ground-truth test set
- SQuAD as a validation corpus (why it's ideal)
- Acceptable score ranges and what low scores mean
- How to use eval scores to tune your pipeline

### `tutorial/07_dos_and_donts.md`
Complete Do's and Don'ts covering:
**Ingestion:**
- DO: Clean your documents before ingesting (remove headers, page numbers)
- DON'T: Ingest the same document twice (causes duplicate retrieval)
- DO: Store source metadata with every chunk
- DON'T: Use enormous chunks (>2000 tokens) — dilutes relevance

**Retrieval:**
- DO: Start with top_k=10, rerank to top_k=3
- DON'T: Use only cosine similarity for keyword-heavy queries
- DO: Log what's being retrieved for every query
- DON'T: Trust retrieval without inspecting chunks

**Generation:**
- DO: Constrain the model to context-only answers
- DON'T: Let the model blend context with parametric knowledge
- DO: Handle empty retrieval gracefully
- DON'T: Use the same prompt for all document types

**Evaluation:**
- DO: Build a golden test set before shipping
- DON'T: Evaluate only on easy questions
- DO: Run evals after every pipeline change
- DON'T: Trust faithfulness > 0.9 without manual spot checks

### `tutorial/08_advanced_patterns.md`
- HyDE (Hypothetical Document Embedding): how and when to use
- Parent-child retrieval: retrieve child, return parent
- Query rewriting: making vague queries more retrieval-friendly
- Step-back prompting: generating broader context queries
- Multi-query retrieval: query expansion for robustness
- Agentic RAG: tool-calling RAG systems

---

## GRADIO APP IMPLEMENTATION

### `app/main.py`

Build a Gradio app with 4 tabs:

**Tab 1: Chat**
- Text input for user questions
- Chat history display
- "Sources used" expander showing retrieved chunks
- Model selector (Gemini / Groq / Local)

**Tab 2: Upload Your Data**
- File upload (PDF, TXT, MD — multiple files)
- URL input
- Chunk strategy selector (fixed / sentence / semantic)
- Chunk size slider (128 to 1024)
- "Index documents" button
- Progress display + chunk count

**Tab 3: Chunk Inspector**
- Query input
- Shows retrieved chunks with similarity scores
- Shows chunks BEFORE and AFTER reranking
- Highlights why reranking changes the order

**Tab 4: Eval Dashboard**
- "Run Evaluation" button (runs on SQuAD subset)
- Progress bar
- Score cards for all 4 RAGAS metrics
- Per-question breakdown table
- Score interpretation guide

---

## GITHUB ACTIONS CI

### `.github/workflows/test.yml`

```yaml
name: Test fallback scripts

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Install dependencies
        run: uv sync
      - name: Download data
        run: uv run python scripts/download_data.py
      - name: Run all scripts (no API keys — local fallback)
        run: uv run python scripts/run_all.py
        env:
          GEMINI_API_KEY: ""
          GROQ_API_KEY: ""
          COHERE_API_KEY: ""
```

---

## IMPORTANT IMPLEMENTATION NOTES

1. **Every src/ module must work with zero API keys** — always use `get_llm()`, `get_embed_model()`, `get_reranker()` from `fallback.py`, never instantiate models directly.

2. **Notebooks must be independently runnable** — each notebook should work even if previous notebooks haven't been run. Use the bundled fallback data by default.

3. **The fallback .py scripts must be identical in logic to the notebooks** — copy-paste equivalents, not simplified versions.

4. **The Gradio app must handle errors gracefully** — show user-friendly messages when API keys are missing, when files fail to load, when evaluation fails.

5. **ChromaDB persists between sessions** — the `.chroma_db` folder is gitignored but persists in the Codespace across restarts.

6. **All tutorial markdown files must be self-contained** — include code examples, diagrams (ASCII), and concrete numbers (e.g., "a chunk size of 512 tokens ≈ 350 words").

7. **The SQuAD fallback bundle must be committed to the repo** — `data/fallback/squad_sample.json` with 50 QA pairs and 5 articles. Students must be able to run everything without downloading anything.

8. **Add rate limit handling** — wrap all API calls with exponential backoff for 429 errors. Show a warning when rate limited, don't crash.

Now implement the entire repository. Start with the devcontainer and pyproject.toml, then src/ modules, then notebooks, then scripts, then app, then tutorial docs.
```
