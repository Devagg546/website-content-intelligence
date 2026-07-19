"""
Search Service — Keyword and semantic content search.

Supports:
- Keyword search: Traditional text matching in SQLite
- Semantic search: Vector similarity search via ChromaDB
- Hybrid search: Combined ranking from both methods
"""

from pydoc import text
import re

from app.models.search import SearchRequest, SearchResponse, SearchResult
from app.services.processing.embedder import get_embedder
from app.db.vector_store import get_vector_store


class SearchService:
    """Handles content search across crawled website pages."""

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def search(self, request: SearchRequest) -> SearchResponse:
        """Execute a search based on the request type."""
        if request.search_type == "keyword":
            return self._keyword_search(request)
        elif request.search_type == "semantic":
            return self._semantic_search(request)
        else:
            return self._hybrid_search(request)
        
    def _make_snippet(self, text: str, query: str, context_chars: int = 80) -> str:
        """Build a snippet around a match of the query, skipping likely boilerplate at the start."""
        if not text:
            return ""

        lower_text = text.lower()
        lower_query = query.lower()

        idx = lower_text.find(lower_query, 300)
        if idx == -1:
            idx = lower_text.find(lower_query)

        if idx == -1:
            return text[:160].strip() + ("..." if len(text) > 160 else "")

        start = max(0, idx - context_chars)
        end = min(len(text), idx + len(query) + context_chars)
        snippet = text[start:end].strip()

        if start > 0:
            snippet = "..." + snippet
        if end < len(text):
            snippet = snippet + "..."
        return snippet

    

    def _keyword_search(self, request: SearchRequest) -> SearchResponse:
        """Keyword-based search using SQLite LIKE queries."""
        cursor = self.db_conn.cursor()
        search_term = f"%{request.query}%"

        cursor.execute(
            """
            SELECT url, title, body_text FROM pages
            WHERE title LIKE ? OR body_text LIKE ? OR meta_description LIKE ?
            LIMIT ?
            """,
            (search_term, search_term, search_term, request.limit),
        )
        rows = cursor.fetchall()

        results = []
        for row in rows:
            title = row["title"] or "Untitled"
            body = row["body_text"] or ""
            snippet = self._make_snippet(body, request.query)

            occurrences = body.lower().count(request.query.lower())
            score = min(1.0, occurrences / 30)

            results.append(SearchResult(
                page_title=title,
                url=row["url"],
                snippet=snippet,
                score=round(score, 3),
            ))

        results.sort(key=lambda r: r.score, reverse=True)

        return SearchResponse(
            results=results, total=len(results), query=request.query, search_type="keyword"
        )

    def _semantic_search(self, request: SearchRequest) -> SearchResponse:
        """Semantic search using ChromaDB vector similarity."""
        embedder = get_embedder()
        query_embedding = embedder.embed_query(request.query)

        collection = get_vector_store()
        if collection is None:
            return SearchResponse(results=[], total=0, query=request.query, search_type="semantic")

        chroma_results = collection.query(
            query_embeddings=[query_embedding],
            n_results=request.limit,
            include=["documents", "metadatas", "distances"],
        )

        results = []
        seen_urls = set()

        if chroma_results and chroma_results["documents"]:
            for i, doc in enumerate(chroma_results["documents"][0]):
                metadata = chroma_results["metadatas"][0][i] if chroma_results["metadatas"] else {}
                url = metadata.get("url", "")

                if url in seen_urls:
                    continue
                seen_urls.add(url)

                distance = chroma_results["distances"][0][i] if chroma_results["distances"] else 1.0
                score = round(1 - distance, 3)

                results.append(SearchResult(
                    page_title=metadata.get("title", "Untitled"),
                    url=url,
                    snippet=doc[:200] + "..." if len(doc) > 200 else doc,
                    score=score,
                ))

        return SearchResponse(
            results=results, total=len(results), query=request.query, search_type="semantic"
        )

    def _hybrid_search(self, request: SearchRequest) -> SearchResponse:
        """Hybrid search combining keyword and semantic results using reciprocal rank fusion."""
        keyword_response = self._keyword_search(request)
        semantic_response = self._semantic_search(request)

        k = 60
        fused_scores = {}
        result_map = {}

        for rank, result in enumerate(keyword_response.results):
            fused_scores[result.url] = fused_scores.get(result.url, 0) + 1 / (k + rank + 1)
            result_map[result.url] = result

        for rank, result in enumerate(semantic_response.results):
            fused_scores[result.url] = fused_scores.get(result.url, 0) + 1 / (k + rank + 1)
            if result.url not in result_map:
                result_map[result.url] = result

        sorted_urls = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for url, fused_score in sorted_urls[:request.limit]:
            result = result_map[url]
            results.append(SearchResult(
                page_title=result.page_title,
                url=result.url,
                snippet=result.snippet,
                score=round(fused_score, 4),
            ))

        return SearchResponse(
            results=results, total=len(results), query=request.query, search_type="hybrid"
        )