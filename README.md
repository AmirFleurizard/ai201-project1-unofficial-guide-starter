# The Unofficial Guide — Project 1

---

## Domain

This Unofficial Guide covers student experiences with on-campus dining at UNC Charlotte — including the two main all-you-care-to-eat dining halls (SoVi and Social 704), retail locations, meal plan options, dietary accommodations, hours, and food quality. This knowledge is valuable because students making decisions about meal plans, dietary needs, or which dining hall to visit have to piece together information from scattered Reddit threads, Yelp reviews, the student newspaper, and word-of-mouth. The official university dining website only provides marketing-level information and lacks honest student perspectives on food quality, wait times, and overall value.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | UNC Charlotte Official Dining Halls Page | Official university page | https://aux.charlotte.edu/dining/dining-map/dining-halls |
| 2 | UNC Charlotte Dining Options Overview | Official university page | https://dining.charlotte.edu/dining-options/ |
| 3 | Dine on Campus – UNCC Menu & Hours | Official menu/hours portal | https://dineoncampus.com/unccharlotte/ |
| 4 | Niner Times – "Dining Options on Campus" (2023) | Student newspaper article | https://www.ninertimes.com/arts_and_culture/dining-options-on-campus/article_1643389a-f39b-11ed-9c0c-1b317a3db9ed.html |
| 5 | Niner Nation Guide – On-Campus Dining (2021) | Student-written guide | https://issuu.com/midasmag/docs/niner_nation_guide_2021_numba_3/s/12418952 |
| 6 | Niner Nation Guide – Off-Campus Dining (2021) | Student-written guide | https://issuu.com/midasmag/docs/niner_nation_guide_2021_numba_3/10 |
| 7 | Arcadia UNCC – Meal Plans & On-Campus Dining Guide | Student blog post | https://arcadiauncc.com/blog/meal-plan-uncc-arcadia/ |
| 8 | r/UNCCharlotte Reddit – Dining & Meal Plan Threads | Student Reddit posts | https://www.reddit.com/r/UNCCharlotte/ |
| 9 | Yelp Reviews – UNC Charlotte Campus Dining | Student reviews | https://www.yelp.com/biz/university-of-north-carolina-at-charlotte-charlotte |
| 10 | Google Reviews – SoVi and Social 704 | Student reviews | https://maps.google.com (search "SoVi UNC Charlotte" and "Social 704 UNC Charlotte") |

---

## Chunking Strategy

**Chunk size:** 400 characters

**Overlap:** 50 characters

**Why these choices fit your documents:**
My document corpus is a mix of short opinion-based reviews (Reddit, Yelp, Google Reviews) and medium-length articles (Niner Times, student guides, official pages). The most valuable content — individual student opinions about food quality, wait times, and meal plan value — tends to appear in 1–3 sentences, which is roughly 200–400 characters. Using 400-character chunks keeps individual opinions intact without merging unrelated topics into a single embedding. The 50-character overlap ensures that any key opinion or fact that falls at a chunk boundary is still captured in at least one of the adjacent chunks, preventing important context from being lost.

Before chunking, documents were cleaned to remove HTML tags, navigation menus, cookie banners, boilerplate footers, phone numbers, email addresses, and ad content. This was handled by the `clean_text()` function in `ingest.py` using regex patterns.

**Final chunk count:** 136 chunks across 10 documents

**Sample chunks:**

| # | Source | Chunk text |
|---|--------|------------|
| 1 | acardia_uncc.txt | "UNCC Meal Plans & On-Campus Dining: A Student Guide — Kyle Knutsen, May 30th, 2025. Table of Contents: Understanding UNCC Meal Plan Options, Cost of Meal Plans at UNCC, Exploring On-Campus Dining Locations..." |
| 2 | acardia_uncc.txt | "Einstein Bros. Bagels serves coffee and breakfast, while Thoughtful Cup provides a quiet spot for coffee and pastries. Most campus cafes and convenience stores UNCC frequently accept DB, ODA, and card payments..." |
| 3 | niner_nation_guide_off_campus.txt | "All UNC Charlotte students must go here before graduating. Recommend going late at night since it is open until 4:30am. Offers both breakfast and dinner options. Designed as an old-fashioned retro-style diner..." |
| 4 | niner_times.txt | "Soup and salad station offering protein cooked to order. Between the Bread offered a customizable deli section. Chef's Table offered flavors from around the world. Hot Flats served burgers, hotdogs and other grilled favorites..." |
| 5 | google_reviews.txt | "5/5 - We love the healthy food options and the cleanliness. The staff is awesome. You can always find what you like and there is plenty to eat. We cannot resist the pizza bar or the dessert..." |

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`. This model runs entirely locally with no API key or rate limits, produces 384-dimensional embeddings, and handles short-to-medium English text well — a strong fit for the review and article content in this corpus.

**Production tradeoff reflection:**
If deploying this system for real users, I would weigh the following tradeoffs when choosing an embedding model:
- **Context length:** `all-MiniLM-L6-v2` handles up to 256 tokens. For longer documents like detailed dining guides, a model with a longer context window (e.g., OpenAI's `text-embedding-3-small` at 8191 tokens) would be better suited.
- **Accuracy on domain-specific text:** MiniLM is a general-purpose model. A model fine-tuned on review-style text would likely improve retrieval relevance for opinion-based queries like "is the food good?"
- **Cost:** MiniLM is free and local. OpenAI embeddings cost per token but offer higher accuracy and are actively maintained.
- **Latency:** Local models like MiniLM have no network latency. API-based models add round-trip time, which matters for a real-time query interface serving many concurrent users.
- **Multilingual support:** MiniLM is English-only. A model like `paraphrase-multilingual-MiniLM-L12-v2` would be needed if serving non-English-speaking students.

---

## Grounded Generation

**System prompt grounding instruction:**
The following instruction is passed to the LLM in every query: You are a helpful assistant for UNC Charlotte students looking for information
about campus dining. Answer the question using ONLY the information provided in
the documents below. Do NOT use any outside knowledge or make assumptions beyond
what is written. Do NOT include a Sources section in your response — sources are
handled separately. If the documents do not contain enough information to answer
the question, respond with: "I don't have enough information in my sources to
answer that question."

Each retrieved chunk is labeled with its source filename and passed as numbered
document blocks, for example:
[Document 1 | Source: acardia_uncc.txt]
<chunk text>
[Document 2 | Source: google_reviews.txt]
<chunk text>

**How source attribution is surfaced in the response:**
Source attribution is handled programmatically — after generation, the code extracts the unique source filenames from the retrieved chunks and appends them to the response in a "Retrieved From" section in the Gradio interface. This ensures sources are always shown regardless of what the LLM produces.

**Out-of-scope query example:**
Query: "What is the best restaurant on Mars?"
Response: "I don't have enough information in my sources to answer that question."
Retrieved From: dining_options_overview.txt, google_reviews.txt, reddit_uncc_dining.txt, niner_times.txt

---

## Retrieval Test Examples

**Query 1: "What dining halls are available at UNC Charlotte and where are they located?"**

Top retrieved chunks:
- `official_dining_page.txt` (distance: 0.43) — "Charlotte has two dining halls..."
- `acardia_uncc.txt` (distance: 0.47) — "Dining at UNC Charlotte centers around two buffet-style dining halls: SoVi UNCC and Crown Commons UNCC. SoVi, located at South Village Crossing..."

These chunks are relevant because they directly name the dining halls and their locations, which is exactly what the query asks for.

**Query 2: "Does SoVi have options for students with dietary restrictions or allergies?"**

Top retrieved chunks:
- `dining_options_overview.txt` (distance: 0.66) — "in an area for those with gluten intolerance. Dietary Assistance..."
- `acardia_uncc.txt` (distance: 0.86) — "vegan options UNCC students can rely on, along with gluten-free dining labels..."

The top result is relevant because it directly mentions dietary accommodations at SoVi. The remaining results have high distance scores (0.86+), indicating weak semantic matches — this query exposed a retrieval gap where allergen-specific content is sparse across the corpus.

**Query 3: "What do students say about food quality at the dining halls?"**

Top retrieved chunks:
- `google_reviews.txt` (distance: 0.69) — "5/5 - We love the healthy food options... 3/5 - Good choice if you want a burger and fries..."
- `google_reviews.txt` (distance: 0.80) — "1/5 - Genuinely hate this place, there's always flies..."

These chunks are relevant because they are direct student reviews expressing opinions about food quality, which is exactly what the query asks for. The retrieval correctly prioritized the review documents over the official dining pages.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What dining halls are available at UNC Charlotte and where are they located? | SoVi (South Village Crossing) and Social 704 (Popp Martin Student Union), both all-you-care-to-eat buffet style | Correctly identified SoVi and Crown Commons but incorrectly listed them as three separate halls and did not provide Social 704's location | Relevant | Partially accurate |
| 2 | Does SoVi have options for students with dietary restrictions or allergies? | Yes — vegan, gluten-free, and allergen-free stations available | Correctly answered yes, mentioned vegan options and gluten-free labels at both SoVi and Crown Commons | Partially relevant | Accurate |
| 3 | Is the meal plan worth it at UNC Charlotte according to students? | Mixed opinions — some find it worth it, others say it is overpriced | Refused to answer: "I don't have enough information in my sources to answer that question" | Partially relevant | Inaccurate |
| 4 | What do students say about food quality at the dining halls? | Mixed reviews — quality has declined, grill and pizza are highlights | Well-rounded answer citing specific student comments about declining quality, flies at Social 704, and occasional praise for specific stations | Relevant | Accurate |
| 5 | What are some food options near campus? | Boardwalk Billy's, Midnight Diner, Cava, and other off-campus restaurants | Listed on-campus chains (Chick-fil-A, Subway, Starbucks) instead of off-campus restaurants | Partially relevant | Partially accurate |

---

## Failure Case Analysis

**Question that failed:**
"Is the meal plan worth it at UNC Charlotte according to students?"

**What the system returned:**
"I don't have enough information in my sources to answer that question."

**Root cause (tied to a specific pipeline stage):**
This failure occurred at the retrieval stage. The relevant information about meal plan value does exist in the corpus — Reddit Thread 3 contains a sarcastic post about the meal plan with 83 upvotes and comments about cost and value, and `acardia_uncc.txt` contains a section on meal plan costs and tips. However, the query phrase "is the meal plan worth it" uses evaluative language that does not semantically match the way this information is written in the documents. The Reddit content uses sarcasm ("Why starve to death for free when you can pay for it?") and the Arcadia guide uses neutral descriptive language about plan types — neither phrasing produces a strong embedding similarity to a direct value-judgment query. As a result, the retrieved chunks did not contain enough direct student opinion about meal plan value for the LLM to generate a grounded answer, so it correctly refused rather than fabricating a response.

**What you would change to fix it:**
Adding more explicit student opinion documents about meal plan value — such as additional Reddit threads where students directly say "the meal plan is/isn't worth it" — would give the retrieval stage better matching chunks. Alternatively, query expansion (rephrasing the query into multiple variants before retrieval) could help surface relevant content that uses different vocabulary.

---

## Spec Reflection

**One way the spec helped you during implementation:**
Writing the chunking strategy in `planning.md` before touching any code forced me to think carefully about document structure upfront. Because I had already decided on 400-character chunks with 50-character overlap and written down the reasoning, I was able to give Claude a precise spec when generating `ingest.py` — and the output matched what I needed without having to iterate much. The spec also made it easy to verify the generated code was correct: I could check the chunk size and overlap values against what I had written and immediately spot any discrepancies.

**One way your implementation diverged from the spec, and why:**
The spec anticipated that the Niner Nation Guide documents would be loaded directly from URLs or clean text. In practice, the off-campus guide (`niner_nation_guide_off_campus.txt`) was heavily corrupted from PDF copy-paste encoding errors — garbled characters, split words, and merged lines made it unusable as-is. Rather than trying to clean it programmatically, I manually rewrote the content as clean plain text based on the original source. This diverged from the planned automated ingestion pipeline but produced much higher quality chunks for that document.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* The Documents section and Chunking Strategy section from `planning.md`, along with the Milestone 3 requirements describing what the ingestion script needed to do.
- *What it produced:* A complete `ingest.py` with a `clean_text()` function using regex patterns and a `chunk_text()` function using a fixed character split with the specified 400-character chunk size and 50-character overlap.
- *What I changed or overrode:* The initial `clean_text()` function did not catch all boilerplate — it missed cookie consent banners from `acardia_uncc.txt` and app store footer text from `dine_on_campus.txt`. I directed Claude to add additional regex patterns targeting those specific patterns after identifying them in the chunk inspection output.

**Instance 2**

- *What I gave the AI:* The Retrieval Approach section from `planning.md`, the pipeline architecture diagram, and the Milestone 4 requirements for embedding and retrieval.
- *What it produced:* A complete `embed.py` that loaded chunks from the ingestion pipeline, embedded them using `all-MiniLM-L6-v2`, and stored them in ChromaDB with source metadata. It also produced a `retrieve.py` with a `retrieve(query, k=5)` function and a test harness for 3 evaluation queries.
- *What I changed or overrode:* The generated code used `chromadb.Client()` which is the in-memory client — I directed Claude to change it to `chromadb.PersistentClient(path=CHROMA_DIR)` so the vector store persists to disk between runs instead of rebuilding every time the script is called.
