# ingest.py
# Loads all .txt files from the docs/ folder, cleans them, and splits into chunks.

import os
import re

# ── Configuration ──────────────────────────────────────────────
DOCS_DIR = "documents"
CHUNK_SIZE = 400      # characters
CHUNK_OVERLAP = 50    # characters


# ── Cleaning ───────────────────────────────────────────────────
def clean_text(text: str) -> str:
    """Remove HTML tags, extra whitespace, boilerplate, and navigation artifacts."""
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Decode common HTML entities
    text = text.replace("&amp;", "&").replace("&nbsp;", " ")
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&#39;", "'")
    # Remove URLs
    text = re.sub(r"http\S+", "", text)
    # Remove common boilerplate phrases
    boilerplate_patterns = [
        r"(?i)skip to content.*?\n",
        r"(?i)manage preferences.*?\n",
        r"(?i)privacy policy.*?\n",
        r"(?i)schedule a tour.*?\n",
        r"(?i)apply now.*?\n",
        r"(?i)this website utilizes technologies.*?advertising\.?",
        r"(?i)to learn more, view the following link.*?\n",
        r"(?i)explore floor plans.*?\n",
        r"(?i)follow us\s*(facebook|instagram|x|youtube|tiktok|\s)*",
        r"(?i)main menu.*?\n",
        r"\(\d{3}\)\s*\d{3}-\d{4}",  # phone numbers
        r"[\w\.-]+@[\w\.-]+\.\w+",    # email addresses
        r"(?i)download on the app store.*?\n",
        r"(?i)get it on google play.*?\n",
        r"(?i)terms of use.*?\n",
        r"(?i)all rights reserved.*?\n",
        r"(?i)copyright \d{4}.*?\n",
        r"(?i)registered trademark.*?\n",
        r"(?i)delete my account.*?\n",
        r"(?i)privacy request.*?\n",
    ]
    for pattern in boilerplate_patterns:
        text = re.sub(pattern, "", text)
    # Collapse multiple newlines into two
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Collapse multiple spaces
    text = re.sub(r" {2,}", " ", text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text


# ── Chunking ───────────────────────────────────────────────────
def chunk_text(text: str, source: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[dict]:
    """Split text into overlapping chunks and attach source metadata."""
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if len(chunk) > 0:
            chunks.append({
                "text": chunk,
                "source": source,
                "chunk_index": chunk_index
            })
            chunk_index += 1

        start += chunk_size - overlap  # slide forward with overlap

    return chunks


# ── Ingestion ──────────────────────────────────────────────────
def load_documents(docs_dir: str = DOCS_DIR) -> list[dict]:
    """Load all .txt files from the docs directory."""
    documents = []

    if not os.path.exists(docs_dir):
        print(f"ERROR: '{docs_dir}' folder not found. Create it and add your .txt files.")
        return documents

    txt_files = [f for f in os.listdir(docs_dir) if f.endswith(".txt")]

    if not txt_files:
        print(f"No .txt files found in '{docs_dir}'. Add your documents and try again.")
        return documents

    for filename in sorted(txt_files):
        filepath = os.path.join(docs_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()

        cleaned = clean_text(raw_text)
        documents.append({
            "filename": filename,
            "raw_length": len(raw_text),
            "cleaned_length": len(cleaned),
            "text": cleaned
        })
        print(f"Loaded: {filename} ({len(raw_text)} chars raw → {len(cleaned)} chars cleaned)")

    return documents


# ── Main ───────────────────────────────────────────────────────
def run_pipeline() -> list[dict]:
    """Run the full ingestion + chunking pipeline and return all chunks."""
    print("=" * 50)
    print("STEP 1: Loading documents")
    print("=" * 50)
    documents = load_documents()

    if not documents:
        return []

    print(f"\nLoaded {len(documents)} documents.\n")

    print("=" * 50)
    print("STEP 2: Chunking documents")
    print("=" * 50)
    all_chunks = []

    for doc in documents:
        chunks = chunk_text(doc["text"], source=doc["filename"])
        all_chunks.extend(chunks)
        print(f"{doc['filename']}: {len(chunks)} chunks")

    print(f"\nTotal chunks: {len(all_chunks)}")

    print("\n" + "=" * 50)
    print("STEP 3: Inspecting 5 sample chunks")
    print("=" * 50)

    # Print 5 evenly spaced sample chunks
    step = max(1, len(all_chunks) // 5)
    samples = [all_chunks[i] for i in range(0, min(len(all_chunks), step * 5), step)]

    for i, chunk in enumerate(samples):
        print(f"\n--- Sample Chunk {i+1} ---")
        print(f"Source:      {chunk['source']}")
        print(f"Chunk index: {chunk['chunk_index']}")
        print(f"Length:      {len(chunk['text'])} chars")
        print(f"Text:\n{chunk['text']}")

    return all_chunks


if __name__ == "__main__":
    chunks = run_pipeline()
    print(f"\nPipeline complete. {len(chunks)} chunks ready for embedding.")