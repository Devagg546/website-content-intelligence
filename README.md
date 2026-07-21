# 🧠 Website Content Intelligence Assistant

An AI-powered RAG (Retrieval-Augmented Generation) platform that crawls websites, indexes their content into a searchable knowledge base, and enables natural language Q&A with source citations — along with automated SEO analysis, content gap detection, and AI-generated insights.

---

## 🏗️ Architecture

```
Frontend (React + Tailwind)
        │
        ▼
FastAPI Backend  ──────────────►  Indexing Pipeline  ──────►  ChromaDB (Vector Store)
        │                                                            │
        │                                                            │
        ▼                                                            ▼
  SQLite (Pages, Crawl Jobs,                              RAG Query Pipeline
  Internal Links)                                                    │
                                                                      ▼
                                                        LLM (Ollama / Groq / OpenAI)
```

**Indexing Pipeline (on crawl):** Crawl → Clean → Chunk → Embed → Store in ChromaDB + SQLite
**RAG Query Pipeline (on question):** Embed question → Semantic search in ChromaDB → Build prompt with retrieved context → Generate answer via LLM → Return with citations

---

## ✨ Features

| Module | Description |
|---|---|
| 🕷️ **Web Crawler** | BFS crawling of any website (up to 500 pages), extracts titles, meta descriptions, H1s, body text, canonical URLs, and internal link structure |
| 🧹 **Content Processing** | Cleans HTML noise (scripts, nav, footers) and splits content into overlapping chunks for embedding |
| 🗂️ **Vector Database** | Stores content chunks as embeddings in ChromaDB for fast semantic similarity search |
| 🤖 **AI Q&A (RAG)** | Ask natural language questions about crawled content and get accurate, cited answers — no hallucinations, answers are grounded only in the crawled data |
| 🔍 **Content Search** | Keyword, semantic, and hybrid (reciprocal rank fusion) search across all crawled pages |
| 📎 **Source Citations** | Every AI answer includes source page title, URL, text snippet, and a relevance/confidence score |
| 📊 **Content Inventory Dashboard** | Total pages, total words, average content length, top keywords, largest/smallest pages |
| ⚠️ **Content Gap Detection** | Flags missing titles, missing meta descriptions, missing H1 tags, thin content, duplicate content, and orphan pages |
| 💡 **AI Content Insights** | Automatically identifies topics covered (Dining, Wellness, Weddings, etc.), content distribution by topic, and frequently mentioned entities (brands, locations, services, products) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Tailwind CSS |
| Backend | Python, FastAPI, Uvicorn |
| Crawling | Requests, BeautifulSoup4 |
| Chunking | LangChain (RecursiveCharacterTextSplitter) |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Vector DB | ChromaDB |
| Relational DB | SQLite |
| LLM Providers | Ollama (local, free), Groq (cloud, fast), OpenAI (cloud) — configurable |

---

## 📦 Project Structure

```
website-content-intelligence/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # FastAPI route handlers (crawl, ask, search, inventory, gaps, insights, pages)
│   │   ├── db/                # SQLite + ChromaDB connection management
│   │   ├── models/            # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── crawler/       # Web crawler, HTML parser, link extractor
│   │   │   ├── processing/    # Content cleaner, chunker, embedder
│   │   │   ├── rag/           # Retriever, prompt builder, LLM generator
│   │   │   └── *_service.py   # Business logic for gaps, search, inventory, insights
│   │   ├── config.py          # Environment-based settings
│   │   └── main.py            # FastAPI app factory
│   ├── data/                  # SQLite DB + ChromaDB storage (gitignored)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/                # Axios API client modules
│   │   ├── components/         # Reusable UI components (crawl, chat, dashboard, gaps, insights, search)
│   │   ├── context/             # Global app state (React Context)
│   │   ├── pages/                # Page-level components (Crawl, Ask AI, Search, Dashboard, Gaps, Insights)
│   │   └── App.jsx
│   └── package.json
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- (Optional) [Ollama](https://ollama.ai) for free local LLM, or a Groq/OpenAI API key for cloud LLM

### Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows

pip install -r requirements.txt

cp .env.example .env
# Edit .env with your LLM provider settings (see below)

uvicorn app.main:app --reload --port 8000
```

Backend runs at `http://127.0.0.1:8000` — API docs available at `http://127.0.0.1:8000/docs`.

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend runs at `http://localhost:5173`.

### LLM Provider Configuration

Set `LLM_PROVIDER` in `backend/.env` to one of:

```dotenv
# Option 1: Ollama (free, local, requires Ollama app running)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Option 2: Groq (free tier, cloud, fast — OpenAI-compatible API)
LLM_PROVIDER=groq
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.3-70b-versatile

# Option 3: OpenAI (paid, cloud)
LLM_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
```

If using Ollama, install it from [ollama.ai](https://ollama.ai) and pull a model:
```bash
ollama pull llama3
```
Ollama must be running in the background for `/api/ask` requests to work.

---

## 📖 API Overview

| Endpoint | Method | Description |
|---|---|---|
| `/api/crawl` | POST | Start a new website crawl job |
| `/api/crawl/status/{job_id}` | GET | Check crawl job progress |
| `/api/crawl/history` | GET | List past crawl jobs |
| `/api/pages` | GET | List crawled pages (paginated, searchable) |
| `/api/ask` | POST | Ask a question, get an AI answer with citations |
| `/api/search` | POST | Search content (keyword / semantic / hybrid) |
| `/api/inventory` | GET | Content inventory statistics |
| `/api/gaps` | GET | Content gap / SEO issue report |
| `/api/insights` | GET | AI-generated topic and entity insights |

Full interactive API documentation is available at `/docs` once the backend is running.

---

## 🧠 How It Works

1. **Crawl** — Enter a website URL. The crawler follows internal links (BFS) and extracts structured data from each page.
2. **Index** — Each page's content is cleaned, split into overlapping chunks, converted into vector embeddings, and stored in ChromaDB. Page metadata and internal link structure are stored in SQLite.
3. **Ask** — Ask a question in plain English. The question is embedded and matched against stored chunks using semantic similarity. The most relevant chunks are passed to an LLM, which generates an answer grounded strictly in that content — with citations back to the source pages.
4. **Analyze** — The Dashboard, Content Gaps, and AI Insights pages run analytics directly over the crawled data (no LLM required for these) to surface SEO issues, content statistics, and topic/entity intelligence automatically.

---

## 📄 License

Internal project — not licensed for public distribution.
