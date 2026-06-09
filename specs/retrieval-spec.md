# Spec: Retrieval Functions

**File:** `retriever.py`
**Status:** Complete — extended with hybrid search (BM25 + semantic + RRF) as a stretch feature.

---

## `retrieve(query, n_results)`

**Status:** Implemented.

### Purpose

Entry point for retrieval called by `generator.py`. Calls `chroma_store.query()`, applies a distance threshold to filter out low-relevance results, and reshapes the raw ChromaDB response into clean chunk dicts ready for prompt assembly. Owns all post-retrieval logic — if hybrid search (BM25 + semantic + RRF merge) is added in the future, it belongs here.

### Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's query string |
| `n_results` | `int` | Number of top chunks to retrieve, defaults to `10` |

**Output:** `list[dict]`

Each dict contains exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"metadata"` | `dict` | Contains `"type"` and `"source"` for citation in the generated response |
| `"distance"` | `float` | Cosine distance score — lower means more similar |

Only chunks with a distance below the threshold (default `0.4`) are included. Pass `threshold=None` to skip filtering (used internally by `hybrid_retrieve()`). Returns an empty list `[]` if the collection is empty or no chunks pass the threshold.

---

## Stretch Feature: Hybrid Search

### `build_bm25_index()`

**Status:** Implemented.

Fetches all chunks from ChromaDB and builds an in-memory BM25 index using `bm25s` with an English Snowball stemmer (via `PyStemmer`). Called once at app startup after ingestion. Stores the index and corpus in module-level variables.

### `bm25_search(query, n_results, source_type)`

**Status:** Implemented.

Searches the BM25 index by keyword relevance. Applies the same Snowball stemmer to the query so tokens like "win", "wins", and "winning" match correctly. Fetches up to 50 candidates then filters by `source_type` and returns the top `n_results`. Each result contains `"text"`, `"metadata"`, and `"score"` (higher = more relevant).

### `hybrid_retrieve(query, n_results, source_type)`

**Status:** Implemented.

Merges semantic and BM25 results using Reciprocal Rank Fusion (RRF). Semantic search bypasses the distance threshold (`threshold=None`) and fetches `n_results * 3` candidates so rare matches aren't cut early. RRF score = Σ `1 / (RRF_K + rank + 1)` across both lists. Chunks appearing in both lists receive a boosted score. Returns the same `list[dict]` shape as `retrieve()`, with `"distance"` included only for chunks that appeared in semantic results.
