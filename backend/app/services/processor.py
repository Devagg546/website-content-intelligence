import json
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

def clean_text(text):
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?;:()\-\'\"]+', ' ', text)
    
    # Remove very short words that add no meaning (single chars except 'a' and 'i')
    text = re.sub(r'\b[b-hj-z]\b', '', text)
    
    # Final strip
    text = text.strip()
    
    return text

def chunk_page(page_data, chunk_size=500, chunk_overlap=50):
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    cleaned_content = clean_text(page_data["content_body"])
    
    if len(cleaned_content) < 50:
        return []
    
    chunks = text_splitter.split_text(cleaned_content)
    
    result = []
    for i, chunk in enumerate(chunks):
        result.append({
            "chunk_id": f"{page_data['url']}#chunk{i}",
            "chunk_index": i,
            "text": chunk,
            "url": page_data["url"],
            "title": page_data["title"],
            "meta_description": page_data["meta_description"],
            "h1": page_data["h1"],
            "crawl_date": page_data["crawl_date"]
        })
    
    return result

def process_crawl_output(input_file="crawl_output.json", output_file="chunks_output.json"):
    
    # Load crawled pages
    with open(input_file, "r", encoding="utf-8") as f:
        pages = json.load(f)
    
    print(f"Loaded {len(pages)} pages from {input_file}")
    print("-" * 50)
    
    all_chunks = []
    skipped = 0
    
    for page in pages:
        chunks = chunk_page(page)
        
        if len(chunks) == 0:
            skipped += 1
            print(f"Skipped (thin content): {page['url']}")
            continue
        
        all_chunks.extend(chunks)
        print(f"Chunked ({len(chunks)} chunks): {page['url']}")
    
    print("-" * 50)
    print(f"Total pages processed: {len(pages) - skipped}")
    print(f"Total pages skipped: {skipped}")
    print(f"Total chunks created: {len(all_chunks)}")
    
    # Save chunks to file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(all_chunks)} chunks to {output_file}")
    return all_chunks


if __name__ == "__main__":
    import sys
    
    input_file = sys.argv[1] if len(sys.argv) > 1 else "crawl_output.json"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "chunks_output.json"
    
    process_crawl_output(input_file, output_file)