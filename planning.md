# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Travian is a classic, browser-based massively multiplayer online real-time strategy (MMORTS) game originally released in 2004. The game has gone through several iterations and updates and have released over 4 versions and is still evolving on a regular basis. The game features several tribes, specializing in different strategic placements and combat abilities. The ever evolving nature has left the game with less up-to-date documents, combined with the deletion of official documents, the information becomes more difficult for players to find through just official channels.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Official: The Tribes and Their Advantages | Tribes comparison before beginning the game | https://support.travian.com/en/articles/3-the-tribes-and-their-advantages |
| 2 | Official: Interacting with Other Players | Basic interaction with other players | https://support.travian.com/en/articles/11-interacting-with-other-players |
| 3 | Official: Beginner's Protection
 | Protection at the start of the server | https://support.travian.com/en/articles/12-beginner-s-protection |
| 4 | Official: Troop Upgrades and Smithy
 | Troop upgrades information | https://support.travian.com/en/articles/40-troop-upgrades-and-smithy |
| 5 | Official: Culture Points (CP) | Village expansion system and how to grow | https://support.travian.com/en/articles/51-culture-points-cp |
| 6 | Unofficial: Combat Basics (written by kirilloid) | Combat system formula | https://unofficialtravian.com/2025/01/game-secrets-combat-basics-written-by-kirilloid/ |
| 7 | Unofficial: Sniping waves | Advanced gameplay technique against offenders | https://unofficialtravian.com/2025/01/game-secrets-sniping-waves/ |
| 8 | Unofficial: Your very first steps in the game | First steps guide for first timers | https://unofficialtravian.com/2025/01/game-secrets-your-very-first-steps-in-the-game/ |
| 9 | Unofficial: How to avoid getting farmed? | Top tricks to avoid survive early gameworld | https://unofficialtravian.com/2025/01/how-to-avoid-getting-farmed/ |
| 10 | Unofficial: Developing your first villages | Development guide for first timers | https://unofficialtravian.com/2025/01/developing-your-first-villages/ |
| 11-203 | Official guides | The rest of official gameplay guides | Refer to /scraped.md |
| 203-267 | Unofficial guides | The rest of unofficial gameplay guides | Refer to /scraped.md |

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
