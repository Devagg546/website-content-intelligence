# Architecture Overview

## System Architecture

The platform follows a **three-tier architecture** with clear separation between the presentation layer (React frontend), application layer (FastAPI backend), and data layer (SQLite + ChromaDB).

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
│  Crawl Input │ Ask AI │ Search │ Dashboard │ Insights    │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP / REST
┌──────────────────────▼──────────────────────────────────┐
│                  API LAYER (FastAPI)                      │
│  /crawl  /ask  /search  /inventory  /gaps  /insights     │
└─────┬───────────────────────────────────────┬───────────┘
      │                                       │
┌─────▼──────────────┐             ┌─────────▼───────────┐
│  INDEXING PIPELINE  │             │  RAG QUERY PIPELINE  │
│                     │             │                      │
│  1. Crawler         │             │  1. Embed Question   │
│  2. Content Proc.   │             │  2. Semantic Search  │
│  3. Embeddings      │             │  3. Build Prompt     │
│  4. Store → ChromaDB│             │  4. LLM Generation   │
└─────────┬───────────┘             │  5. Citations        │
          │                         └──────────┬──────────┘
          │                                    │
┌─────────▼────────────────────────────────────▼──────────┐
│                    DATA LAYER                            │
│         SQLite (pages metadata)                          │
│         ChromaDB (embeddings + chunks)                   │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

### Indexing Pipeline
1. **Crawler** — Playwright visits pages, BeautifulSoup extracts content
2. **Content Processor** — Cleans HTML, extracts text
3. **Chunker** — LangChain RecursiveCharacterTextSplitter creates chunks
4. **Embedder** — Sentence Transformers generates vectors
5. **Storage** — Chunks + embeddings + metadata stored in ChromaDB; page metadata in SQLite

### RAG Query Pipeline
1. **Embed Question** — Same Sentence Transformers model embeds the user query
2. **Semantic Search** — ChromaDB returns top-K relevant chunks
3. **Prompt Builder** — Assembles context + question into LLM prompt
4. **LLM** — Ollama (Phase 1) or cloud API (Phase 2) generates answer
5. **Citations** — Response includes source URLs, page titles, and content snippets

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Vector DB | ChromaDB | Open-source, lightweight, zero infra cost |
| Crawling | Playwright | Handles JS-rendered pages |
| Chunking | LangChain RecursiveTextSplitter | Smart, context-aware splitting |
| Embeddings | Sentence Transformers | Free, local, high quality |
| LLM Phase 1 | Ollama (Llama 3) | Free, local, no API costs |
| Database | SQLite | Zero setup, sufficient for MVP |
| Frontend | React + Tailwind | Modern, fast, great DX |
