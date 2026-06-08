# Spec: ChromaDB Store Functions

**File:** `chroma_store.py`
**Status:** Specification — implement these functions in Milestone 4.

---

## `get_collection_size()`

**Status:** Not yet implemented.

### Purpose

Return the number of chunks currently stored in the ChromaDB collection. Used by `app.py` to check whether ingestion has already been run, without exposing the collection object outside of `chroma_store.py`.

### Input / Output Contract

**Inputs:** None

**Output:** `int`

The total number of chunks stored in the collection. Returns `0` if the collection is empty or does not exist.

---

## `embed_and_store(chunks)`

**Status:** Not yet implemented.

### Purpose

Embed each chunk using `bge-base-en-v1.5` and write the resulting vectors, texts, and metadata into ChromaDB. Called once during ingestion after all documents have been chunked. Skips storing if the collection already contains documents, so re-running ingestion does not produce duplicates.

### Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `chunks` | `list[dict]` | List of chunk dicts as returned by `chunk_document()` — each must contain `"text"`, `"chunk_id"`, and `"metadata"` keys |

**Output:** None

Each chunk is stored in ChromaDB as:

| ChromaDB field | Source |
|----------------|--------|
| `id` | `chunk["chunk_id"]` |
| `document` | `chunk["text"]` |
| `embedding` | `bge-base-en-v1.5` embedding of `chunk["text"]`, handled automatically by ChromaDB |
| `metadata` | `chunk["metadata"]` — contains `"type"` and `"source"` |

---

## `query(query, n_results)`

**Status:** Not yet implemented.

### Purpose

Embed the query using `bge-base-en-v1.5` and run a cosine similarity search against the ChromaDB collection. Returns the raw ChromaDB response without filtering or reshaping — all result parsing is handled by `retriever.py`.

### Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's query string |
| `n_results` | `int` | Number of top chunks to return |

**Output:** `dict`

A raw ChromaDB query response with exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"documents"` | `list[list[str]]` | Chunk texts — use index `[0]` to get results for the single query |
| `"metadatas"` | `list[list[dict]]` | Chunk metadatas — use index `[0]` to get results for the single query |
| `"distances"` | `list[list[float]]` | Cosine distance scores — use index `[0]` to get results for the single query |

Returns `None` if the collection is empty.
