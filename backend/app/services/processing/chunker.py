"""
Text Chunker — Split text into overlapping chunks for embedding.

Uses LangChain's RecursiveCharacterTextSplitter for intelligent
text splitting that respects sentence and paragraph boundaries.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


class TextChunker:
    """Splits text content into chunks suitable for embedding and retrieval."""

    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None,
    ):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def chunk_text(self, text: str, metadata: dict = None) -> list[dict]:
        """
        Split text into overlapping chunks with metadata.

        Args:
            text: The text content to split
            metadata: Optional metadata to attach to each chunk
                      (e.g., url, title, section)

        Returns:
            List of dicts with:
            {
                "content": str,
                "metadata": dict,
                "chunk_index": int,
            }
        """
        if not text or not text.strip():
            return []

        base_metadata = metadata or {}
        documents = self.splitter.create_documents(
            texts=[text],
            metadatas=[base_metadata],
        )

        chunks = []
        for idx, doc in enumerate(documents):
            chunk = {
                "content": doc.page_content,
                "metadata": {
                    **doc.metadata,
                    "chunk_index": idx,
                    "total_chunks": len(documents),
                },
                "chunk_index": idx,
            }
            chunks.append(chunk)

        return chunks
