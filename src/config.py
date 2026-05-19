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
TOP_K_RETRIEVE = 10  # retrieve this many before reranking
TOP_K_RERANK = 3  # keep this many after reranking
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
    t.add_row(
        "Gemini API",
        GEMINI_MODEL if HAS_GEMINI else "—",
        "OK Available" if HAS_GEMINI else "X Using local fallback",
    )
    t.add_row(
        "Groq API",
        GROQ_MODEL if HAS_GROQ else "—",
        "OK Available" if HAS_GROQ else "X Not configured",
    )
    t.add_row(
        "Cohere API",
        COHERE_RERANK_MODEL if HAS_COHERE else "—",
        "OK Available" if HAS_COHERE else "X Using local rerank fallback",
    )
    t.add_row(
        "Embeddings",
        GEMINI_EMBED_MODEL if HAS_GEMINI else LOCAL_EMBED_MODEL,
        "API" if HAS_GEMINI else "Local",
    )
    t.add_row("Chunk size", str(CHUNK_SIZE), "")
    t.add_row("Top-K retrieve", str(TOP_K_RETRIEVE), "")
    t.add_row("Top-K rerank", str(TOP_K_RERANK), "")
    c.print(t)
