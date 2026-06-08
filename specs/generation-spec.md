# Spec: Generation Functions

**File:** `generator.py`
**Status:** Specification — implement these functions in Milestone 5.

---

## `generate_response(query, retrieved_chunks)`

**Status:** Not yet implemented.

### Purpose

Assemble a grounded prompt from the retrieved chunks and the user's query, then call the Groq LLM to produce a response.

**System prompt behaviour:**
- The LLM must answer strictly from the content in the retrieved chunks. It must not use its training data or outside knowledge under any circumstances.
- If no retrieved chunks are provided, the LLM must explicitly admit it does not have enough context to answer and ask the user to rephrase their question.
- Every factual point in the response must be annotated with its source document (e.g. `Official: World Wonder`, `Unofficial: Combat Basics`). For complex questions drawing from multiple sources, all relevant sources must be annotated.

### Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's query string |
| `retrieved_chunks` | `list[dict]` | List of chunk dicts as returned by `retriever.retrieve()` — each must contain `"text"`, `"metadata"`, and `"distance"` keys, where `"metadata"` contains `"type"` and `"source"` |

Each chunk is formatted into the prompt as:

```
(source: {source}, type: {type}, distance: {distance}) - {text}
```

**Output:** `str`

The generated response grounded in the provided chunks, with every factual point annotated with its source document. If no chunks are provided, returns a message stating the LLM does not have enough context to answer and asks the user to rephrase their question.
