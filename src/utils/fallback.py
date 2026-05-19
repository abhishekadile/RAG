"""
Graceful fallback logic. Detects which API keys are available
and returns the appropriate LLM / embedder / reranker.
Includes exponential backoff for rate limit (429) errors.
"""
import functools
import time
import warnings

from src.config import (
    COHERE_API_KEY,
    COHERE_RERANK_MODEL,
    GEMINI_API_KEY,
    GEMINI_EMBED_MODEL,
    GEMINI_MODEL,
    GROQ_API_KEY,
    GROQ_MODEL,
    HAS_COHERE,
    HAS_GEMINI,
    HAS_GROQ,
    LOCAL_EMBED_MODEL,
    LOCAL_RERANK_MODEL,
    TOP_K_RERANK,
)


def with_rate_limit_retry(max_retries: int = 3, base_delay: float = 2.0):
    """Decorator: retry on 429 rate limit errors with exponential backoff."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    err_str = str(e).lower()
                    if "429" in err_str or "rate" in err_str or "quota" in err_str:
                        delay = base_delay * (2**attempt)
                        warnings.warn(
                            f"Rate limited on {func.__name__}. "
                            f"Retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})",
                            stacklevel=2,
                        )
                        time.sleep(delay)
                    else:
                        raise
            raise last_error

        return wrapper

    return decorator


def _ollama_available() -> bool:
    """Check if Ollama server is reachable."""
    try:
        import httpx

        resp = httpx.get("http://localhost:11434/api/tags", timeout=2.0)
        return resp.status_code == 200
    except Exception:
        return False


def _get_ollama_or_mock():
    """Return Ollama LLM if server is running, else MockLLM."""
    if _ollama_available():
        from llama_index.llms.ollama import Ollama

        print("[WARN] Using Ollama local model (slow on CPU).")
        print("  Run: ollama pull llama3.2:3b")
        return Ollama(model="llama3.2:3b", request_timeout=30.0)

    from llama_index.core.llms.mock import MockLLM

    print("[WARN] Ollama unavailable. Using MockLLM for testing.")
    return MockLLM(max_tokens=256)


@with_rate_limit_retry()
def get_llm(provider: str | None = None):
    """Return the best available LLM, optionally forced to a provider."""
    if provider == "gemini" and HAS_GEMINI:
        from llama_index.llms.gemini import Gemini

        return Gemini(model=GEMINI_MODEL, api_key=GEMINI_API_KEY)
    if provider == "groq" and HAS_GROQ:
        from llama_index.llms.groq import Groq

        return Groq(model=GROQ_MODEL, api_key=GROQ_API_KEY)
    if provider == "local":
        return _get_ollama_or_mock()

    if HAS_GEMINI:
        from llama_index.llms.gemini import Gemini

        return Gemini(model=GEMINI_MODEL, api_key=GEMINI_API_KEY)
    if HAS_GROQ:
        from llama_index.llms.groq import Groq

        return Groq(model=GROQ_MODEL, api_key=GROQ_API_KEY)

    print("[WARN] No API keys found.")
    return _get_ollama_or_mock()


@with_rate_limit_retry()
def get_embed_model():
    """Return the best available embedding model."""
    if HAS_GEMINI:
        from llama_index.embeddings.gemini import GeminiEmbedding

        return GeminiEmbedding(model_name=GEMINI_EMBED_MODEL, api_key=GEMINI_API_KEY)

    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    print("[WARN] No Gemini key. Using local sentence-transformers (all-MiniLM-L6-v2).")
    return HuggingFaceEmbedding(model_name=LOCAL_EMBED_MODEL)


@with_rate_limit_retry()
def get_reranker():
    """Return the best available reranker."""
    if HAS_COHERE:
        from llama_index.postprocessor.cohere_rerank import CohereRerank

        return CohereRerank(
            api_key=COHERE_API_KEY,
            model=COHERE_RERANK_MODEL,
            top_n=TOP_K_RERANK,
        )

    from llama_index.core.postprocessor import SentenceTransformerRerank

    print("[WARN] No Cohere key. Using local cross-encoder reranker.")
    return SentenceTransformerRerank(model=LOCAL_RERANK_MODEL, top_n=TOP_K_RERANK)
