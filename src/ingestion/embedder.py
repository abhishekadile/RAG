"""Embedding utilities for the ingestion pipeline."""

from llama_index.core import Settings

from src.utils.fallback import get_embed_model


def configure_embed_model():
    """Set the global LlamaIndex embedding model with automatic fallback."""
    embed_model = get_embed_model()
    Settings.embed_model = embed_model
    return embed_model
