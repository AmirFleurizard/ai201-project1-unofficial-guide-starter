# embed.py
# Embeds all chunks from the ingestion pipeline and stores them in ChromaDB.

import chromadb
from sentence_transformers import SentenceTransformer
from ingest import run_pipeline

# ── Configuration ──────────────────────────────────────────────
CHROMA_DIR = "chroma_db"   # where ChromaDB will store its files
COLLECTION_NAME = "uncc_dining"

def build_vector_store():
    """Embed all chunks and store them in ChromaDB with source metadata."""

    # Step 1: Run ingestion pipeline to get chunks
    print("Running ingestion pipeline...")
    chunks = run_pipeline()

    if not chunks:
        print("No chunks found. Make sure your docs/ folder has .txt files.")
        return

    # Step 2: Load embedding model
    print("\nLoading embedding model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Step 3: Set up ChromaDB
    print("Setting up ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Delete existing collection if it exists (clean rebuild)
    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted existing collection '{COLLECTION_NAME}' for clean rebuild.")

    collection = client.create_collection(COLLECTION_NAME)

    # Step 4: Embed and store in batches
    print(f"\nEmbedding {len(chunks)} chunks...")
    texts = [chunk["text"] for chunk in chunks]
    sources = [chunk["source"] for chunk in chunks]
    chunk_indices = [str(chunk["chunk_index"]) for chunk in chunks]
    ids = [f"{source}_{idx}" for source, idx in zip(sources, chunk_indices)]

    # Embed all at once (MiniLM is fast enough for 136 chunks)
    embeddings = model.encode(texts, show_progress_bar=True)

    # Store in ChromaDB
    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[
            {"source": source, "chunk_index": int(idx)}
            for source, idx in zip(sources, chunk_indices)
        ]
    )

    print(f"\nDone! {collection.count()} chunks stored in ChromaDB at '{CHROMA_DIR}/'")
    return collection


if __name__ == "__main__":
    build_vector_store()