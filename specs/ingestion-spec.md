# Spec: Ingestion Functions

**File:** `ingest.py`
**Status:** Specification — implement these functions in Milestone 3.

---

## `load_documents()`

**Status:** Not yet implemented.

### Purpose

Load all markdown documents from the `documents/` directory into memory, along with their metadata. Each document is returned as a dict so downstream functions have both the raw text and the source information needed to populate chunk metadata.

### Input / Output Contract

**Inputs:** None

**Output:** `list[dict]`

Each dict contains exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | Full raw markdown text of the document |
| `"metadata"` | `dict` | Source metadata for the document (see below) |

**`metadata` keys:**

| Key | Type | Description |
|-----|------|-------------|
| `"type"` | `str` | Either `"official"` or `"unofficial"`, derived from filename prefix |
| `"source"` | `str` | Filename excluding its prefix (e.g., `"the-tribes-and-their-advantages.md"`) |

Returns an empty list `[]` if the `documents/` directory is empty or does not exist.

---

## `clean_document(text)`

**Status:** Not yet implemented.

### Purpose

Strip markdown syntax from a document's raw text while preserving the readable content and section header text. This includes removing the header quoteblock that appears between the document title and the main content, which contains only source metadata (URL, source name) and carries no semantic value. The output is plain text suitable for sentence splitting and embedding — free of formatting noise like `**`, `#`, `[]()`, HTML tags, and the header quoteblock.

### Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Raw markdown text of a single document |

**Output:** `str`

The cleaned plain text of the document with markdown formatting removed. Returns an empty string `""` if the input is empty.

---

## `chunk_document(text, metadata)`

**Status:** Not yet implemented.

### Purpose

Orchestrate the chunking of a single document's cleaned text by delegating to a chunking strategy. Each chunk is returned as a dict containing the chunk text and the document's metadata, so every chunk is self-contained and traceable back to its source when retrieved. Currently delegates to `semantic_chunking()` — any additional chunking strategy (e.g. `recursive_chunking()`) must follow the same `(text, metadata)` signature and return the same `list[dict]` output shape.

### Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Cleaned plain text of a single document (output of `clean_document()`) |
| `metadata` | `dict` | Metadata for the source document — must contain `"type"` and `"source"` keys |

**Output:** `list[dict]`

Each dict contains exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"chunk_id"` | `str` | Unique identifier formatted as `{type}_{source}_{order}` (e.g., `"official_the-tribes-and-their-advantages.md_0"`) — used as the vector ID in the store |
| `"metadata"` | `dict` | Source metadata for the chunk (see below) |

**`metadata` keys:**

| Key | Type | Description |
|-----|------|-------------|
| `"type"` | `str` | Passed through from `metadata["type"]` |
| `"source"` | `str` | Passed through from `metadata["source"]` |

Returns an empty list `[]` if the input text is empty or produces no valid chunks.

---

## `semantic_chunking(text, metadata)`

**Status:** Not yet implemented.

### Purpose

Apply LangChain's `SemanticChunker` to a cleaned document text and return chunks ready for storage. This is the concrete chunking strategy called by `chunk_document()` — it groups consecutive sentences by cosine similarity using `bge-base-en-v1.5` as the embedding model, inserting a boundary wherever similarity drops below the threshold.

### Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | `str` | Cleaned plain text of a single document |
| `metadata` | `dict` | Source metadata — must contain `"type"` and `"source"` keys |

**Output:** `list[dict]`

Each dict contains exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"chunk_id"` | `str` | Unique identifier formatted as `{type}_{source}_{order}` (e.g., `"official_the-tribes-and-their-advantages.md_0"`) — used as the vector ID in the store |
| `"metadata"` | `dict` | Contains `"type"` and `"source"` passed through from `metadata` |

Returns an empty list `[]` if the input text is empty or too short to produce any chunks.
