"""
Embedding Generator — Generate vector embeddings using Sentence Transformers.

Used for both indexing (content chunks) and query embedding (user questions).
Same model must be used for both to ensure consistent vector space.
"""

from typing import Union

from app.config import settings


class EmbeddingGenerator:
    """
    Generates text embeddings using Sentence Transformers.
    Lazily loads the model on first use to avoid startup overhead.
    """

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.embedding_model
        self._model = None

    @property
    def model(self):
        """Lazy-load the Sentence Transformers model."""
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed_text(self, text: str) -> list[float]:
        """
        Generate embedding for a single text string.

        Args:
            text: The text to embed

        Returns:
            List of floats representing the embedding vector
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts in a batch.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        embeddings = self.model.encode(texts, convert_to_numpy=True, batch_size=32)
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        """
        Generate embedding for a search query.
        Uses the same model as content embedding for consistency.

        Args:
            query: The search query to embed

        Returns:
            Embedding vector for the query
        """
        return self.embed_text(query)


# Singleton instance to avoid loading the model multiple times
_embedder_instance = None


def get_embedder() -> EmbeddingGenerator:
    """Get or create the singleton EmbeddingGenerator instance."""
    global _embedder_instance
    if _embedder_instance is None:
        _embedder_instance = EmbeddingGenerator()
    return _embedder_instance
