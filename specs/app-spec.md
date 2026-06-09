# Spec: App Functions

**File:** `app.py`
**Status:** Complete.

---

## `run_ingestion()`

**Status:** Implemented.

### Purpose

Check whether the ChromaDB collection already contains chunks via `chroma_store.get_collection_size()`. If the collection is empty, run the full ingestion pipeline — load, clean, chunk, embed, and store all documents. Called once at app startup before the Gradio UI is launched so the vector store is always ready before the first query.

### Input / Output Contract

**Inputs:** None

**Output:** None

---

## `chat(message, history)`

**Status:** Implemented.

### Purpose

Handle a single chat turn. Calls `retriever.retrieve()` with the user's message, then passes the query and retrieved chunks to `generator.generate_response()` and returns the response string to the Gradio UI.

### Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `message` | `str` | The user's current message |
| `history` | `list` | The conversation history managed by Gradio — not currently passed to the LLM (see Future Improvements) |

**Output:** `str`

The generated response string returned by `generator.generate_response()`.

---

## `build_ui()`

**Status:** Implemented.

### Purpose

Construct and return the Gradio `Blocks` UI. Called from the main function after `run_ingestion()` completes. The UI consists of a chat interface on the left and a sidebar on the right listing loaded game guides, following the same two-column layout as the reference implementation.

### Layout

```
┌─────────────────────────────────────────────────────┐
│  Header: app title + tagline                        │
├──────────────────────────────┬──────────────────────┤
│  ChatInterface (scale=3)     │  Sidebar (scale=1)   │
│                              │                      │
│  • gr.Chatbot                │  Loaded Guides list  │
│  • Textbox                   │  (derived from       │
│  • Example questions         │  documents/ at       │
│                              │  startup)            │
└──────────────────────────────┴──────────────────────┘
```

**Example questions** should cover a variety of query types drawn from the Evaluation Plan, including tribe comparisons, combat mechanics, and advanced techniques.

**Output:** `gr.Blocks`

The fully constructed Gradio app instance, ready to be launched.

---

## Future Improvements

- **Chat history:** Pass `history` from `chat()` to `generator.generate_response()` so the LLM can answer follow-up questions with awareness of prior turns in the conversation.
