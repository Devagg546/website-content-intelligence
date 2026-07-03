"""
RAG Retriever — Semantic search in ChromaDB for relevant content chunks.

Embeds the user question and performs similarity search to find
the most relevant content chunks from the indexed website.
"""

from app.config import settings
from app.services.processing.embedder import get_embedder
from app.db.vector_store import get_vector_store


class Retriever:
    """Retrieves relevant content chunks from ChromaDB using semantic search."""

    def __init__(self, top_k: int = None):
        self.top_k = top_k or settings.top_k_results

    def retrieve(self, query: str) -> list[dict]:
        """
        Find the most relevant content chunks for a given query.

        Pipeline:
        1. Embed the query using the same model used for indexing
        2. Search ChromaDB for top-K similar chunks
        3. Return chunks with metadata and relevance scores

        Args:
            query: The user's natural language question

        Returns:
            List of dicts with:
            {
                "content": str,
                "metadata": dict,
                "relevance_score": float,
            }
        """
        # TODO: Implement semantic retrieval
        # 1. Get embedder and embed the query
        # 2. Get ChromaDB collection
        # 3. Query with embedding for top-K results
        # 4. Format and return results
        embedder = get_embedder()
        query_embedding = embedder.embed_query(query)

        collection = get_vector_store()
        if collection is None:
            return []

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k,
            include=["documents", "metadatas", "distances"],
        )

        # Format results
        retrieved_chunks = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                chunk = {
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "relevance_score": 1 - results["distances"][0][i]
                    if results["distances"]
                    else 0.0,
                }
                retrieved_chunks.append(chunk)

        return retrieved_chunks
