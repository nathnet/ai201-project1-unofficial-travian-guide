# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

## Chunking Strategy Comparison
|Query|Semantic Chunking Response|Recursive Chunking Response|
|-|-|-|
| What is a wave sniping? | Wave sniping, also referred to as "cutting waves" or "inserting waves," is a defensive technique in Travian: Legends where defensive troops are sent to land in the small time gap between two incoming attack waves, often within the same second or just one second apart (Official: sniping-waves). This tactic allows defenders to reduce or fully prevent building damage, kill parts of the attacking player's siege units, and protect important structures (Official: sniping-waves). The goal is to insert defensive troops between waves, making the second attack hit the defense instead of an empty village (Unofficial: game-secrets-sniping-waves). | Wave sniping, also known as sniping waves, cutting waves, or inserting waves, refers to the defensive technique of sending troops to land in the small time gap between two incoming attack waves, often within the same second or just one second apart (Official: sniping-waves). This tactic takes advantage of the game's first-in, first-out rule for events happening in the same second, allowing defensive troops to arrive immediately after a clearing wave but before the next catapult wave, thereby reducing or preventing building damage and killing parts of the attacker's siege units (Official: sniping-waves, Unofficial: game-secrets-sniping-waves). |
| Given Travian Plus is off, what tribe can build both resource fields and building simultaneously | The Romans can build one resource field and one building at the same time, thanks to their "Simultaneous Construction" ability (Official: the-romans-and-their-advantages). | The available guides don't cover that topic. They discuss the development of resource villages, settling a second village, and general strategies for playing Travian: Legends, but do not provide information on which tribe can build both resource fields and buildings simultaneously with Travian Plus off. Can you rephrase or ask something more specific about Travian: Legends? |
| What is an operational hammer? | An Operational (Working) Hammer is a mid-sized offensive army trained in the Barracks, Stables, and Workshop, used for daily offensive actions such as clearing nearby villages, supporting alliance operations, farming inactives, and participating in minor conquests (Official: building-an-operational-working-hammer). It typically consists of 25,000-35,000 offensive infantry, 6,000-12,000 offensive cavalry, 1,500-2,000 rams, and 1,500-2,000 catapults (Official: building-an-operational-working-hammer, Unofficial: game-secrets-the-path-of-the-warrior-an-operational-hammer). | An Operational Hammer, also known as a Working Hammer, is a mid-sized offensive army trained in the Barracks, Stables, and Workshop (without Great Barracks/Great Stables) (Official: building-an-operational-working-hammer). It is used for daily offensive actions, such as clearing nearby villages, supporting alliance operations, farming inactives, and participating in minor conquests (Official: building-an-operational-working-hammer, Unofficial: game-secrets-the-path-of-the-warrior-an-operational-hammer).

A typical Operational Hammer consists of 25,000-35,000 offensive infantry, 6,000-12,000 offensive cavalry, 1,500-2,000 rams, and 1,500-2,000 catapults (Official: building-an-operational-working-hammer, Unofficial: game-secrets-the-path-of-the-warrior-an-operational-hammer). |
| How do you win a Travian: Legends server? | The available guides don't cover that topic. Can you rephrase or ask something more specific about Travian: Legends? | To win a Travian: Legends server, you must build a level 100 Wonder of the World (Official: what-is-travian-legends, Unofficial: what-is-travian-legends). This requires cooperation with your alliance and strategic planning throughout the game (Official: what-is-travian-legends, Unofficial: what-is-travian-legends).|
| What are the strengths of Mongolian troops | The available guides don't cover that topic. Can you rephrase or ask something more specific about Travian: Legends? | The available guides don't cover that topic. They discuss the strengths and weaknesses of various tribes in Travian: Legends, such as Teutons, Huns, Egyptians, Gauls, and Spartans, but do not provide information on Mongolian troops (Official: the-tribes-and-their-advantages, Unofficial: the-huns-and-their-advantages). Can you rephrase or ask something more specific about Travian: Legends? |