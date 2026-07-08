"""
ChromaDB Vector Store — Client and collection management.

Manages the ChromaDB persistent client and collection for:
- Storing content chunk embeddings
- Semantic similarity search
"""

from pathlib import Path
from typing import Optional

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.config import settings

# Module-level references
_chroma_client: Optional[chromadb.ClientAPI] = None
_collection: Optional[chromadb.Collection] = None


def init_vector_store() -> None:
    """
    Initialize the ChromaDB persistent client and collection.
    Called during application startup via lifespan.
    """
    global _chroma_client, _collection

    persist_dir = Path(settings.chroma_persist_dir)
    persist_dir.mkdir(parents=True, exist_ok=True)

    _chroma_client = chromadb.PersistentClient(
        path=str(persist_dir),
        settings=ChromaSettings(anonymized_telemetry=False),
    )

    # Get or create the main collection
    _collection = _chroma_client.get_or_create_collection(
        name=settings.chroma_collection_name,
        metadata={"description": "Website content chunks with embeddings"},
    )


def get_vector_store() -> Optional[chromadb.Collection]:
    """
    Get the ChromaDB collection instance.

    Returns:
        ChromaDB Collection or None if not initialized
    """
    return _collection


def get_chroma_client() -> Optional[chromadb.ClientAPI]:
    """
    Get the ChromaDB client instance.

    Returns:
        ChromaDB Client or None if not initialized
    """
    return _chroma_client


def add_documents(
    ids: list[str],
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict],
) -> None:
    """
    Add documents with embeddings to the vector store.

    Args:
        ids: Unique identifiers for each document
        documents: Text content of each document
        embeddings: Pre-computed embedding vectors
        metadatas: Metadata dicts for each document
    """
    if _collection is None:
        raise RuntimeError("Vector store not initialized. Call init_vector_store() first.")

    _collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def query_similar(
    query_embedding: list[float],
    n_results: int = 5,
) -> dict:
    """
    Query the vector store for similar documents.

    Args:
        query_embedding: The query vector
        n_results: Number of results to return

    Returns:
        ChromaDB query results dict
    """
    if _collection is None:
        raise RuntimeError("Vector store not initialized. Call init_vector_store() first.")

    return _collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )
