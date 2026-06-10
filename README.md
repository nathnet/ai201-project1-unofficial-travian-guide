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
Travian is a classic, browser-based massively multiplayer online real-time strategy (MMORTS) game originally released in 2004. The game has gone through several iterations and updates and have released over 4 versions and is still evolving on a regular basis. The game features several tribes, specializing in different strategic placements and combat abilities. The ever evolving nature has left the game with less up-to-date documents, combined with the deletion of official documents, the information becomes more difficult for players to find through just official channels.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Official: The Tribes and Their Advantages | Official | ./documents/official_the-tribes-and-their-advantages.md |
| 2 | Official: Interacting with Other Players | Official | ./documents/official_interacting-with-other-players.md |
| 3 | Official: Beginner's Protection | Official | ./documents/official_beginners-protection.md |
| 4 | Official: Troop Upgrades and Smithy | Official | ./documents/official_troop-upgrades-and-smithy.md |
| 5 | Official: Culture Points (CP) | Official | ./documents/official_culture-points-cp.md |
| 6 | Unofficial: Combat Basics (written by kirilloid) | Unofficial | ../documents/unofficial_game-secrets-combat-basics-written-by-kirilloid.md |
| 7 | Unofficial: Sniping waves | Unofficial | ../documents/unofficial_game-secrets-sniping-waves.md |
| 8 | Unofficial: Your very first steps in the game | Unofficial | ../documents/unofficial_game-secrets-your-very-first-steps-in-the-game.md |
| 9 | Unofficial: How to avoid getting farmed? | Unofficial | ../documents/unofficial_how-to-avoid-getting-farmed.md |
| 10 | Unofficial: Developing your first villages | Unofficial | ../documents/unofficial_developing-your-first-villages.md |
| 11-202 | Official guides | Official | Refer to /scraped.md |
| 203-266 | Unofficial guides | Unofficial | Refer to /scraped.md |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunking strategy:** Semantic chunking using chonkie-ai/chonkie's `SemanticChunker` with `bge-base-en-v1.5` via sentence-transformers

**Chunk size:** Up to 512 tokens (bge-base-en-v1.5 max token window)

**Overlap:** None — chonkie places boundaries at semantic similarity drops, so consecutive chunks are already semantically distinct

**Chunker parameters:**
- `threshold=0.6`: splits wherever cosine similarity drops below 0.6; selected by sweeping 0.3–0.7 across sample docs — 0.6 produces near one-chunk-per-Q&A on FAQ docs without over-fragmenting formula-heavy content
- `min_sentences_per_chunk=2`: prevents single-sentence orphan chunks
- `min_characters_per_sentence=50`: filters short bullet lines (e.g. `- Loyalty is not reduced.`) from being split candidates, reducing list fragmentation

**Pre-processing applied inside `clean_document()` before chunking:**
- `_attach_table_headers()`: removes the markdown separator row and repeats the header row before each data row, so every chunk containing a table row is self-contained for retrieval

**Why these choices fit your documents:** Fixed-size chunking is inflexible considering each document tends to have differing writing styles, and can also have references across multiple files. Some documents have all the answers within 200-300 characters, while other span across paragraphs (1000-1500 characters.) Semantic chunking is chosen over recursive chunking in this case since there are a lot of documents that may have answers for different parts of the the question across different documents. It is better to chunk the text semantically to retain its meaning. While recursive chunking can still remain a good fallback as the documents are already formated with hierarchical structure. bge-base-en-v1.5 is chosen over all-MiniLM-L6-v2 in this case to handle higher token windows (256 tokens vs 512 tokens)

**Final chunk count:** 1839 chunks

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** bge-base-en-v1.5

**Production tradeoff reflection:** `bge-base-en-v1.5` was chosen over `all-MiniLM-L6-v2` primarily for its 512-token context window — double the 256-token limit of MiniLM. This matters because Travian documents contain long, semantically cohesive sections (combat formulas, tribe comparisons) where semantic chunking can produce chunks that exceed 256 tokens, causing MiniLM to silently truncate and lose meaning at the embedding stage. The trade-off is that bge-base produces 768-dimensional vectors vs. MiniLM's 384, increasing storage size and vector similarity computation cost at query time, which adds latency. Both models are English-only, which is a real constraint given Travian's globally distributed player base. For production without cost constraints, Gemini Embedding 2 would be the choice: it supports 100+ languages to serve non-English players who form a large share of the player base; it is multimodal, so players could attach screenshots of their game state alongside text queries; its larger model capacity better handles niche gaming terminology (troop names like Praetorian or Druidrider that carry no inherent semantic meaning); and it is API-hosted with low latency optimized for real-time use. The main trade-offs versus a local model would be API cost per query, network dependency, and data leaving the local environment.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** The LLM is instructed to answer strictly using the context chunks provided in the user message and to not use training data or any outside knowledge under any circumstances. Each retrieved chunk is prefixed with its source document name, type (Official/Unofficial), and similarity distance before being injected into the prompt. If none of the provided chunks contain information relevant to the question, the model is told to explicitly state that the available guides don't cover the topic rather than hallucinating an answer.

**How source attribution is surfaced in the response:** The model is instructed to annotate every factual point inline with its source document in the format `(Official: <source>)` or `(Unofficial: <source>)`, with the `.md` extension stripped. It is told to cite only one source when the answer comes from a single document, and to expand to multiple citations only when the answer genuinely spans across documents.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

Note: all responses below were generated using semantic (vector) search only, without BM25 hybrid search. 

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What is a wave sniping? | Defensive troops land in the small time gap between two attacks, literally one second apart. | Correctly described wave sniping as a defensive technique where troops land between two incoming attack waves within the same second, preventing building damage and killing siege units. | Relevant | Accurate |
| 2 | Given Travian Plus is off, what tribe can build both resource fields and buildings simultaneously? | Romans | Correctly identified Romans and cited their "Simultaneous Construction" ability. | Relevant | Accurate |
| 3 | What is an operational hammer? | A mid-sized army trained in Barracks, Stables, and Workshop (without Great versions) used in everyday offense operations. | Correctly described it as a mid-sized offensive army for daily operations, and included typical troop composition numbers. | Relevant | Accurate |
| 4 | How do you win in normal Travian: Legends? | The first player or alliance to build their World Wonder to level 100 wins the server. | Failed to retrieve the relevant chunk — responded that the guides don't cover the topic. | Off-target | Inaccurate |
| 5 | What are the strengths of Mongolian troops? | No information could be found within the game guides. | Correctly returned a "not covered" response, as Mongolian troops do not exist in Travian: Legends. | Relevant | Accurate |

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

**Question that failed:** How do you win in normal Travian: Legends?

**What the system returned:** "The available guides don't cover that topic. Can you rephrase or ask something more specific about Travian: Legends?"

**Root cause (tied to a specific pipeline stage):** The failure occurred at the retrieval stage. The embedding model encoded "How do you win" as a concept semantically closer to strategy and tactics — steps and actions a player takes to succeed — so it retrieved chunks about troop building, resource management, and combat instead. The actual win condition ("build a World Wonder to level 100") is framed in the documents as a server end condition, not gameplay advice, and its vocabulary ("Wonder of the World", "level 100", "server ends") shares almost no semantic overlap with the query. The retrieved chunks all fell below the distance threshold, triggering the no-context fallback.

**What you would change to fix it:** Add BM25 hybrid search with a Snowball stemmer (as implemented in the Hybrid Search stretch feature), so that "win", "wins", and "winning" are all reduced to the same stem before matching. Alternatively, query expansion could rewrite the query to include "World Wonder level 100 victory condition" before embedding, increasing the chance of a semantic hit.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Writing separate spec sections for each pipeline stage — with explicit input/output contracts, expected function signatures, and sample results — made it possible to feed each section directly to Claude Code and get cohesive, on-spec implementations. Because the contracts were precise (e.g. what `chunk_document()` accepts and returns, what distance threshold filters), the generated code consistently matched the expected behavior without needing major corrections.

**One way your implementation diverged from the spec, and why:** The planning spec was intended to be complete before any code was written, but in practice it was patched incrementally as implementation revealed gaps. For example, chunking parameters like threshold, min_sentences_per_chunk, and min_characters_per_sentence were not in the original spec — they were added after observing over-fragmented chunks during early test runs. This meant some Claude Code prompts were fed an incomplete spec and produced code that had to be revised once the spec caught up. The lesson was that a living spec works better than a frozen one for a pipeline with this many interdependent tuning parameters.

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

- *What I gave the AI:* An instructional comment inside `scripts/scrape_articles.py` describing the target websites (official Travian support and unofficialtravian.com), the expected output format (one markdown file per article), and the naming convention for output files.
- *What it produced:* A working web scraper that fetched article content from both sites, stripped HTML, and saved each article as a markdown file with the correct naming scheme. It also generated a `scraped.md` index listing every scraped document.
- *What I changed or overrode:* Adjusted the markdown cleaning logic to better preserve hierarchical structure (headings, tables, bullet lists) that semantic chunking later depended on, since the initial output flattened some nested content.

**Instance 2**

- *What I gave the AI:* Draft sections of `planning.md` — chunking strategy, retrieval approach, and architecture diagram — as a spec to review and help refine, iterating back and forth like a pair programming session.
- *What it produced:* Suggestions for filling gaps in the spec: adding chunker parameters (`threshold`, `min_sentences_per_chunk`), clarifying the distance threshold rationale, and flagging that the token window mismatch between MiniLM and the chunker would silently truncate chunks.
- *What I changed or overrode:* Incorporated most suggestions directly into the spec, but pushed back on switching the embedding model mid-spec — kept bge-base-en-v1.5 and instead documented the MiniLM limitation as a rationale rather than switching models late in planning.

**Instance 3**

- *What I gave the AI:* The high-level planning spec and a request to generate more granular implementation specs for each pipeline module — explicit input/output contracts, expected function signatures, return types, and sample outputs.
- *What it produced:* Detailed per-function specs for `ingest.py`, `chroma_store.py`, `retriever.py`, and `generator.py`, each describing what arguments a function accepts, what it returns, and what a correct result looks like for a sample input.
- *What I changed or overrode:* Used these generated specs directly as Claude Code prompts for implementation, which meant the code generation had a tightly scoped target to hit. Occasionally tightened the contracts where the generated spec was too loose — for example, specifying that `query()` must return distances alongside chunks, not just chunk text, since the generator needed distance values for context formatting.

## Chunking Strategy Comparison
All responses below were generated using semantic (vector) search only, without BM25 hybrid search.  

|Query|Semantic Chunking Response|Recursive Chunking Response|Results|
|-|-|-|-|
| What is a wave sniping? | Wave sniping, also referred to as "cutting waves" or "inserting waves," is a defensive technique in Travian: Legends where defensive troops are sent to land in the small time gap between two incoming attack waves, often within the same second or just one second apart (Official: sniping-waves). This tactic allows defenders to reduce or fully prevent building damage, kill parts of the attacking player's siege units, and protect important structures (Official: sniping-waves). The goal is to insert defensive troops between waves, making the second attack hit the defense instead of an empty village (Unofficial: game-secrets-sniping-waves). | Wave sniping, also known as sniping waves, cutting waves, or inserting waves, refers to the defensive technique of sending troops to land in the small time gap between two incoming attack waves, often within the same second or just one second apart (Official: sniping-waves). This tactic takes advantage of the game's first-in, first-out rule for events happening in the same second, allowing defensive troops to arrive immediately after a clearing wave but before the next catapult wave, thereby reducing or preventing building damage and killing parts of the attacker's siege units (Official: sniping-waves, Unofficial: game-secrets-sniping-waves). | Similar response, favoring recursive chunking as it mentions first-in, first-out rule being used as a leverage to protect one's village
| Given Travian Plus is off, what tribe can build both resource fields and building simultaneously | The Romans can build one resource field and one building at the same time, thanks to their "Simultaneous Construction" ability (Official: the-romans-and-their-advantages). | The available guides don't cover that topic. They discuss the development of resource villages, settling a second village, and general strategies for playing Travian: Legends, but do not provide information on which tribe can build both resource fields and buildings simultaneously with Travian Plus off. Can you rephrase or ask something more specific about Travian: Legends? | Semantic chunking wins this one, being able to discern Romans as the tribe that can build simultaneously. |
| What is an operational hammer? | An Operational (Working) Hammer is a mid-sized offensive army trained in the Barracks, Stables, and Workshop, used for daily offensive actions such as clearing nearby villages, supporting alliance operations, farming inactives, and participating in minor conquests (Official: building-an-operational-working-hammer). It typically consists of 25,000-35,000 offensive infantry, 6,000-12,000 offensive cavalry, 1,500-2,000 rams, and 1,500-2,000 catapults (Official: building-an-operational-working-hammer, Unofficial: game-secrets-the-path-of-the-warrior-an-operational-hammer). | An Operational Hammer, also known as a Working Hammer, is a mid-sized offensive army trained in the Barracks, Stables, and Workshop (without Great Barracks/Great Stables) (Official: building-an-operational-working-hammer). It is used for daily offensive actions, such as clearing nearby villages, supporting alliance operations, farming inactives, and participating in minor conquests (Official: building-an-operational-working-hammer, Unofficial: game-secrets-the-path-of-the-warrior-an-operational-hammer). <br><br>A typical Operational Hammer consists of 25,000-35,000 offensive infantry, 6,000-12,000 offensive cavalry, 1,500-2,000 rams, and 1,500-2,000 catapults (Official: building-an-operational-working-hammer, Unofficial: game-secrets-the-path-of-the-warrior-an-operational-hammer). | Similar response, with semantic chunking being more concise and clear |
| How do you win a Travian: Legends server? | The available guides don't cover that topic. Can you rephrase or ask something more specific about Travian: Legends? | To win a Travian: Legends server, you must build a level 100 Wonder of the World (Official: what-is-travian-legends, Unofficial: what-is-travian-legends). This requires cooperation with your alliance and strategic planning throughout the game (Official: what-is-travian-legends, Unofficial: what-is-travian-legends).| Recursive chunking wins this one, being able to identify Wonder of the World as the victory condition |
| What are the strengths of Mongolian troops | The available guides don't cover that topic. Can you rephrase or ask something more specific about Travian: Legends? | The available guides don't cover that topic. They discuss the strengths and weaknesses of various tribes in Travian: Legends, such as Teutons, Huns, Egyptians, Gauls, and Spartans, but do not provide information on Mongolian troops (Official: the-tribes-and-their-advantages, Unofficial: the-huns-and-their-advantages). Can you rephrase or ask something more specific about Travian: Legends? | Similar response, but recursive chunking is clearer about the lack of Mongolian tribe.