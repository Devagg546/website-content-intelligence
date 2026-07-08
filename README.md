# 🧠 Website Content Intelligence Assistant

An AI-powered RAG (Retrieval-Augmented Generation) platform that crawls websites, indexes content into a searchable knowledge base, and enables natural language Q&A with source citations.

## 🏗️ Architecture

```
Frontend (React + Tailwind)  →  FastAPI Backend  →  Indexing Pipeline  →  ChromaDB
                                      ↕
                              RAG Query Pipeline  →  LLM (Ollama / OpenAI)
```

## 🛠️ Tech Stack

| Layer       | Technology                                     |
|-------------|------------------------------------------------|
| Frontend    | React, Vite, Tailwind CSS                      |
| Backend     | Python, FastAPI, Uvicorn                        |
| Crawling    | Playwright, BeautifulSoup4                      |
| Processing  | LangChain (Text Splitter)                       |
| Embeddings  | Sentence Transformers                           |
| Vector DB   | ChromaDB                                        |
| LLM         | Ollama (Llama 3 / Mistral) → OpenAI / Claude   |
| Database    | SQLite                                          |

## 📦 Project Structure

```
Content_Intelligence_Assistant/
├── backend/          # FastAPI Python backend
├── frontend/         # React + Vite frontend
├── docs/             # Documentation
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Ollama (for local LLM)

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### Install Ollama & Pull Model
```bash
# Download from https://ollama.ai
ollama pull llama3
```

## 📖 Documentation
- [Architecture Overview](docs/architecture.md)
- [API Reference](docs/api-reference.md)

## 📋 Features
- 🕷️ **Web Crawler** — BFS crawling with Playwright (up to 500 pages)
- 🤖 **AI Q&A** — RAG-powered answers with source citations
- 🔍 **Content Search** — Keyword + semantic search
- 📊 **Dashboard** — Content inventory & statistics
- ⚠️ **Gap Detection** — Missing metadata, thin/duplicate content
- 💡 **AI Insights** — Topic distribution & entity extraction
