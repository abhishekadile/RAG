"""
ChromaDB vector store wrapper.
Handles collection creation, upserting nodes, and returning a LlamaIndex index.
"""
from pathlib import Path
from typing import List

import chromadb
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.schema import BaseNode
from llama_index.vector_stores.chroma import ChromaVectorStore

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
        metadata={"hnsw:space": "cosine"},
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
        print(f"  [OK] Index built. ChromaDB collection has {count} vectors.")
    else:
        print(f"  Loading existing index from {persist_dir}...")
        index = VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model=embed_model,
        )

    return index
