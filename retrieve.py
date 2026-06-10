# retrieve.py
# Retrieval function: given a query, returns the top-k most relevant chunks.

import chromadb
from sentence_transformers import SentenceTransformer

# ── Configuration ──────────────────────────────────────────────
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "uncc_dining"
DEFAULT_K = 5

# Load model and collection once at module level (reused across queries)
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection(COLLECTION_NAME)


def retrieve(query: str, k: int = DEFAULT_K) -> list[dict]:
    """
    Retrieve the top-k most relevant chunks for a given query.
    Returns a list of dicts with keys: text, source, chunk_index, distance.
    """
    # Embed the query
    query_embedding = model.encode(query).tolist()

    # Query ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    # Format results
    chunks = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks.append({
            "text": text,
            "source": metadata["source"],
            "chunk_index": metadata["chunk_index"],
            "distance": round(distance, 4)
        })

    return chunks


def test_retrieval():
    """Test retrieval with 3 evaluation plan queries."""
    test_queries = [
        "What dining halls are available at UNC Charlotte and where are they located?",
        "Does SoVi have options for students with dietary restrictions or allergies?",
        "What do students say about food quality at the dining halls?"
    ]

    for query in test_queries:
        print("\n" + "=" * 60)
        print(f"QUERY: {query}")
        print("=" * 60)
        results = retrieve(query)
        for i, chunk in enumerate(results):
            print(f"\n  Result {i+1} | Source: {chunk['source']} | Distance: {chunk['distance']}")
            print(f"  {chunk['text'][:300]}...")


if __name__ == "__main__":
    test_retrieval()