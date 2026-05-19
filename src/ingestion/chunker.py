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
    HierarchicalNodeParser,
    SemanticSplitterNodeParser,
    SentenceSplitter,
)
from llama_index.core.schema import BaseNode

from src.config import CHUNK_OVERLAP, CHUNK_SIZE

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
        parser = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            paragraph_separator="\n\n",
        )

    elif strategy == "sentence":
        parser = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            paragraph_separator="\n\n",
        )

    elif strategy == "semantic":
        if embed_model is None:
            raise ValueError("embed_model required for semantic chunking")
        parser = SemanticSplitterNodeParser(
            embed_model=embed_model,
            breakpoint_percentile_threshold=95,
        )

    elif strategy == "hierarchical":
        parser = HierarchicalNodeParser.from_defaults(chunk_sizes=[2048, 512, 128])
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    nodes = parser.get_nodes_from_documents(documents, show_progress=True)
    print(f"  Chunked {len(documents)} documents into {len(nodes)} nodes")
    print(f"  Strategy: {strategy} | Chunk size: {chunk_size} | Overlap: {chunk_overlap}")
    return nodes
