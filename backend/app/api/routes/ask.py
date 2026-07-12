"""
Ask AI routes — RAG-powered question answering with citations.
"""

from fastapi import APIRouter, Depends

from app.models.ask import AskRequest, AskResponse, Citation
from app.api.dependencies import get_db
from app.services.rag.retriever import Retriever
from app.services.rag.prompt_builder import PromptBuilder
from app.services.rag.generator import get_generator

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
    5. Return answer with source citations and confidence score
    """

    # Step 1 & 2 — Retrieve relevant chunks from ChromaDB
    retriever = Retriever()
    chunks = retriever.retrieve(request.question)

    if not chunks:
        return AskResponse(
            answer="I couldn't find any relevant content to answer your question. Please make sure the website has been crawled first.",
            citations=[],
            confidence_score=0.0,
        )

    # Step 3 — Build prompt with context
    prompt_builder = PromptBuilder()
    prompt = prompt_builder.build_prompt(request.question, chunks)

    # Step 4 — Generate answer using LLM
    generator = get_generator()
    answer = await generator.generate(
        system_prompt=prompt["system"],
        user_prompt=prompt["user"],
    )

    # Step 5 — Build citations from retrieved chunks
    citations = []
    for chunk in chunks:
        metadata = chunk.get("metadata", {})
        citations.append(Citation(
            page_title=metadata.get("title", "Unknown Page"),
            url=metadata.get("url", "Unknown URL"),
            snippet=chunk.get("content", "")[:200] + "...",
            relevance_score=round(chunk.get("relevance_score", 0.0), 3),
        ))

    # Calculate overall confidence score as average of top chunks
    confidence = sum(c.relevance_score for c in citations) / len(citations) if citations else 0.0

    return AskResponse(
        answer=answer,
        citations=citations,
        confidence_score=round(confidence, 3),
    )