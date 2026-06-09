# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
This guide covers dining options at and around the University of North Carolina at Charlotte. As a student it can be daunting to find what to eat especially if you're in a new state or lack transportation. This knowledge is hard to find because student opinions are split between multiple different sources, while the official UNC Charlotte website only provides surface level information on the dining halls.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | UNC Charlotte Official Dining Halls Page | Official university page listing of the dining halls, SoVi and Social 704, with food station descriptions and payment options. | https://aux.charlotte.edu/dining/dining-map/dining-halls |
| 2 | UNC Charlotte Dining Options Overview | Official overview of all campus dining including retail locations, food trucks, and late-night dining. | https://dining.charlotte.edu/dining-options/ |
| 3 | Dine on Campus – UNCC Menu & Hours | Official menu and hours portal where students check daily food offerings at SoVi and Social 704. | https://dineoncampus.com/unccharlotte/ |
| 4 | Niner Times – "Dining Options on Campus" (2023) | Student newspaper article reviewing on-campus dining locations, food stations, and tips for navigating dining options. | https://www.ninertimes.com/arts_and_culture/dining-options-on-campus/article_1643389a-f39b-11ed-9c0c-1b317a3db9ed.html |
| 5 | Niner Nation Guide – On-Campus Dining (2021) | Student-written guide covering all on-campus dining locations including Crown Commons, SoVi, Prospector, and cafe spots. | https://issuu.com/midasmag/docs/niner_nation_guide_2021_numba_3/s/12418952 |
| 6 | Niner Nation Guide – Off-Campus Dining (2021) | Student-written guide recommending 10 off-campus restaurants near UNCC for when dining halls get repetitive. | https://issuu.com/midasmag/docs/niner_nation_guide_2021_numba_3/10 |
| 7 | Arcadia UNCC – Meal Plans & On-Campus Dining Guide | Student blog post explaining meal plan options, dining hall layouts, dietary accommodations, and practical tips. | https://arcadiauncc.com/blog/meal-plan-uncc-arcadia/ |
| 8 | r/UNCCharlotte Reddit – Dining & Meal Plan Threads | Student Reddit posts and comments about food quality, meal plan value, wait times, and dining hall tips. (Manually copied from r/UNCCharlotte) | https://www.reddit.com/r/UNCCharlotte/ |
| 9 | Yelp Reviews – SoVi Dining Hall | Student and visitor Yelp reviews of SoVi covering food quality, variety, hours, and overall experience. (Manually copied from Yelp) | https://www.yelp.com/search?find_desc=SoVi+Dining+UNC+Charlotte |
| 10 | Google Reviews – Social 704 / Crown Commons | Google Maps student reviews of Social 704 (formerly Crown Commons) covering food quality and dining experience. (Manually copied from Google Maps) | https://maps.google.com (search "Social 704 UNC Charlotte") |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->
I have a wide variety of different sources with different lengths ranging from short reviews to medium length articles. Because the most valuable content seems to be student reviews, which are usually shorter, I am going to use a chunk size of 400 characters with an overlap of 50. 

**Chunk size:**
400

**Overlap:**
50

**Reasoning:**
Based on my research the average student review is about 1-3 sentences which is typically around 300-400 characters. Since the content I'm using isn't structured and theirs a chance that I split t useful context, I went with an overlap of 50. This should catch and sentences I split and ensure that I gather enough context. I'll be able to tell if my chunks are too small if it returns fragmented text and too large if it shows a mix of unrelated topics.
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2

**Top-k:** 5 chunks per query

**Production tradeoff reflection:**
- Context length: all-MiniLM-L6-v2 handles up to 256 tokens. For longer documents, a model with longer context windows would be better.
- Accuracy on domain-specific text: MiniLM is general-purpose. For a production dining system, a fine-tuned model on review-style text might improve retrieval relevance.
- Latency: Local models like MiniLM have no network latency. API-based models add round-trip time, which matters for a real-time query interface.
- Cost: MiniLM is free and local. OpenAI embeddings cost per token but offer higher accuracy and multilingual support.
- Multilingual support: MiniLM is English-only. A model like paraphrase-multilingual-MiniLM-L12-v2 would be needed if serving non-English-speaking students.


---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What dining halls are available at UNC Charlotte and where are they located? | SoVi is located in South Village Crossing and Social 704 is located in the Popp Martin Student Union. Both are all-you-care-to-eat buffet-style dining halls. |
| 2 | Does SoVi have options for students with dietary restrictions or allergies? | Yes, SoVi has a "Delicious Without" station serving dishes free of the top 9 allergens, plus designated vegan and gluten-avoiding options. |
| 3 | Is the meal plan worth it at UNC Charlotte according to students? | Student opinions are mixed — some find it convenient and good value for resident students, while others feel it is overpriced for the food quality and variety offered. |
| 4 | What do students say about food quality at the dining halls? | Reviews are mixed — students note decent variety but inconsistent quality, with stations like the grill, pizza (Burning Stone), and the SoVi bakery frequently mentioned as highlights. |
| 5 | What are some food options near campus? | Nearby options include Boardwalk Billy's, Midnight Diner, Cava, and various chain restaurants accessible via light rail or a short drive from campus. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Noisy or inconsistent review documents: Articles, Reddit posts, and Yelp reviews are informal, inconsistent in length, and may contain slang, typos, or off-topic content. This could produce low-quality chunks that confuse retrieval.

2. Official sources vs. student opinion mismatch: The official dining pages describe stations and options in marketing language, while student reviews describe real experiences. A query like "is the food good?" might retrieve the official description ("fresh ingredients, rotating menus") instead of the honest student opinion, which could lead to an overly positive response.


---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

     

**Milestone 3 — Ingestion and chunking:**
I will give Claude the Documents section (file types, sources) and the Chunking Strategy section (400 chars, 50 overlap) and ask it to implement a script that loads all .txt files from a docs/ folder, cleans them (strips HTML, extra whitespace, boilerplate), and produces chunks using CharacterTextSplitter. I will verify the output by printing 5 sample chunks and confirming they are readable, self-contained, and match the specified chunk size.


**Milestone 4 — Embedding and retrieval:**
I will give Claude the Retrieval Approach section (all-MiniLM-L6-v2, top-k=5) and the Architecture diagram and ask it to implement code that embeds chunks using sentence-transformers and stores them in ChromaDB with source metadata. I will also ask it to implement a retrieve(query, k=5) function. I will verify by running 3 test queries and confirming the returned chunks are visibly relevant and have distance scores below 0.5.


**Milestone 5 — Generation and interface:**
I will give Claude the grounding requirements and the Gradio interface requirements and ask it to implement a generate() function using Groq's llama-3.3-70b-versatile with a strict grounding prompt, and a app.py Gradio Blocks UI with query input, answer output, and sources output fields. I will verify by testing an in-scope query (should cite a source) and an out-of-scope query (should decline to answer).
