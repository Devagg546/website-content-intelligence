import sys
sys.path.insert(0, 'backend')

from app.services.crawler.crawler import WebCrawler, CrawlJob
from app.services.processing.cleaner import ContentCleaner
from app.services.processing.chunker import TextChunker
from app.services.processing.embedder import get_embedder
from app.db.vector_store import init_vector_store, add_documents
from app.config import settings

def run(url, max_pages=10):
    print(f"Starting pipeline for: {url}")

    # Step 1 - Crawl
    job = CrawlJob(url=url, max_pages=max_pages)
    crawler = WebCrawler()
    pages = crawler.crawl(job)
    print(f"Crawled {len(pages)} pages")

    # Step 2 - Chunk and embed
    chunker = TextChunker()
    embedder = get_embedder()

    # Step 3 - Init ChromaDB
    init_vector_store()

    all_ids, all_docs, all_embeddings, all_metadatas = [], [], [], []

    for page in pages:
        body = page.get("body_text", "")
        if not body or len(body.strip()) < 50:
            continue

        metadata = {
            "url": page.get("url", ""),
            "title": page.get("title", ""),
            "h1": page.get("h1", ""),
            "meta_description": page.get("meta_description", ""),
            "crawl_date": page.get("crawl_date", ""),
        }

        chunks = chunker.chunk_text(body, metadata)

        for chunk in chunks:
            chunk_id = f"{page.get('url','')}#chunk{chunk['chunk_index']}"
            all_ids.append(chunk_id)
            all_docs.append(chunk["content"])
            all_metadatas.append(chunk["metadata"])

    print(f"Total chunks: {len(all_docs)}")
    print("Generating embeddings...")
    all_embeddings = embedder.embed_texts(all_docs)

    add_documents(
        ids=all_ids,
        documents=all_docs,
        embeddings=all_embeddings,
        metadatas=all_metadatas,
    )
    print(f"Pipeline complete! {len(all_ids)} chunks stored in ChromaDB.")

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.oberoihotels.com"
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    run(url, max_pages)