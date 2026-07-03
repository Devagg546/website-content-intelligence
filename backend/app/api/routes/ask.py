"""
Ask AI routes — RAG-powered question answering with citations.

Endpoints:
    POST /api/ask — Ask a natural language question about crawled content
"""

from fastapi import APIRouter, Depends

from app.models.ask import AskRequest, AskResponse
from app.api.dependencies import get_db, get_chroma

router = APIRouter()


@router.post("", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    db=Depends(get_db),
):
    """
    Ask a natural language question about the crawled website content.

    Pipeline:
    1. Embed the question using Sentence Transformers
    2. Semantic search in ChromaDB for top-K relevant chunks
    3. Build prompt with question + relevant context
    4. Generate answer using LLM (Ollama / OpenAI)
    5. Return answer with source citations

    Every answer MUST include source citations — no hallucinated answers.
    """
    # TODO: Implement RAG pipeline
    # 1. Embed question
    # 2. Search ChromaDB
    # 3. Build prompt
    # 4. Call LLM
    # 5. Format response with citations
    return AskResponse(
        answer="",
        citations=[],
    )
