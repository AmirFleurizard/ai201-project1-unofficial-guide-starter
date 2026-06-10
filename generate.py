# generate.py
# Uses retrieved chunks as context to generate a grounded response via Groq.

import os
from groq import Groq
from dotenv import load_dotenv
from retrieve import retrieve

load_dotenv()

# ── Configuration ──────────────────────────────────────────────
GROQ_MODEL = "llama-3.3-70b-versatile"
MAX_TOKENS = 1024

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# ── Prompt Template ────────────────────────────────────────────
def build_prompt(query: str, chunks: list[dict]) -> str:
    """Build a grounded prompt from retrieved chunks."""
    context_blocks = []
    for i, chunk in enumerate(chunks):
        context_blocks.append(
            f"[Document {i+1} | Source: {chunk['source']}]\n{chunk['text']}"
        )
    context = "\n\n".join(context_blocks)

    return f"""You are a helpful assistant for UNC Charlotte students looking for information about campus dining.

Answer the question using ONLY the information provided in the documents below.
Do NOT use any outside knowledge or make assumptions beyond what is written.
Do NOT include a Sources section in your response — sources are handled separately.
If the documents do not contain enough information to answer the question, respond with:
"I don't have enough information in my sources to answer that question."

Documents:
{context}

Question: {query}

Answer:"""


# ── Generation ─────────────────────────────────────────────────
def ask(query: str, k: int = 5) -> dict:
    """
    Full RAG pipeline: retrieve chunks, generate grounded response.
    Returns dict with keys: answer, sources, chunks.
    """
    # Retrieve relevant chunks
    chunks = retrieve(query, k=k)

    # Build grounded prompt
    prompt = build_prompt(query, chunks)

    # Generate response
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    # Extract unique sources from retrieved chunks
    sources = list(dict.fromkeys(chunk["source"] for chunk in chunks))

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks
    }


# ── Test ───────────────────────────────────────────────────────
if __name__ == "__main__":
    test_queries = [
        "What dining halls are available at UNC Charlotte and where are they located?",
        "Does SoVi have options for students with dietary restrictions or allergies?",
        "What is the best restaurant on Mars?"  # out-of-scope test
    ]

    for query in test_queries:
        print("\n" + "=" * 60)
        print(f"QUERY: {query}")
        print("=" * 60)
        result = ask(query)
        print(f"\nANSWER:\n{result['answer']}")
        print(f"\nSOURCES: {', '.join(result['sources'])}")