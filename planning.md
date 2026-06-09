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

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

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

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
