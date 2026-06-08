# Spec: Retrieval Functions

**File:** `retriever.py`
**Status:** Specification — implement these functions in Milestone 4.

---

## `retrieve(query, n_results)`

**Status:** Not yet implemented.

### Purpose

Entry point for retrieval called by `generator.py`. Calls `chroma_store.query()`, applies a distance threshold to filter out low-relevance results, and reshapes the raw ChromaDB response into clean chunk dicts ready for prompt assembly. Owns all post-retrieval logic — if hybrid search (BM25 + semantic + RRF merge) is added in the future, it belongs here.

### Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's query string |
| `n_results` | `int` | Number of top chunks to retrieve, defaults to `5` |

**Output:** `list[dict]`

Each dict contains exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"metadata"` | `dict` | Contains `"type"` and `"source"` for citation in the generated response |
| `"distance"` | `float` | Cosine distance score — lower means more similar |

Only chunks with a distance below the threshold (default `0.7`) are included. Returns an empty list `[]` if the collection is empty or no chunks pass the threshold.
