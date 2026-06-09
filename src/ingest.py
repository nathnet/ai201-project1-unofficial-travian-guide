import re
from pathlib import Path

from chonkie import SemanticChunker
from chonkie.embeddings import SentenceTransformerEmbeddings


DOCUMENTS_DIR = Path(__file__).parent.parent / "documents"

_chunker = None


def _get_chunker():
    global _chunker
    if _chunker is None:
        embeddings = SentenceTransformerEmbeddings("BAAI/bge-base-en-v1.5")
        _chunker = SemanticChunker(
            embedding_model=embeddings,
            threshold=0.6,
            chunk_size=512,
            min_sentences_per_chunk=2,
            min_characters_per_sentence=50
        )
    return _chunker


def load_documents() -> list[dict]:
    """Load all markdown documents from documents/ into memory with metadata.

    Returns a list of dicts, each with:
      - "text": full raw markdown text
      - "metadata": {"type": "official"|"unofficial", "source": filename-without-prefix}

    Returns [] if documents/ is empty or does not exist.
    """
    if not DOCUMENTS_DIR.exists() or not DOCUMENTS_DIR.is_dir():
        return []

    documents = []
    for filepath in sorted(DOCUMENTS_DIR.glob("*.md")):
        filename = filepath.name

        if filename.startswith("official_"):
            doc_type = "official"
            source = filename[len("official_"):]
        elif filename.startswith("unofficial_"):
            doc_type = "unofficial"
            source = filename[len("unofficial_"):]
        else:
            continue

        text = filepath.read_text(encoding="utf-8")
        documents.append({
            "text": text,
            "metadata": {
                "type": doc_type,
                "source": source,
            },
        })

    return documents


def _attach_table_headers(lines: list[str]) -> list[str]:
    """Remove separator rows; prepend the header row before each data row.

    Detects the separator (e.g. | --- | --- |) to identify the header row above
    it, then skips the separator and inserts that header before every subsequent
    data row. This ensures each row is self-contained so any chunk the semantic
    chunker produces will include the column names alongside the values.

    Before:  | Col A | Col B |
             | ----- | ----- |   <- separator
             | val 1 | val 2 |   <- data rows
             | val 3 | val 4 |

    After:   | Col A | Col B |
             | Col A | Col B |   <- repeated before each data row
             | val 1 | val 2 |
             | Col A | Col B |
             | val 3 | val 4 |
    """
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        is_separator = bool(re.match(r"^\|[-:\s|]+\|$", line.strip()))
        prev_is_table_row = bool(
            result and re.match(r"^\|", result[-1].strip()))

        if is_separator and prev_is_table_row:
            header = result[-1]
            result.pop()  # remove the first header
            i += 1  # skip separator
            while i < len(lines) and re.match(r"^\|", lines[i].strip()):
                result.append(header)
                result.append(lines[i])
                i += 1
        else:
            result.append(line)
            i += 1
    return result


def clean_document(text: str) -> str:
    """Strip markdown syntax from raw document text, keeping readable content.

    Removes the header quoteblock (Source/URL metadata block before the first
    horizontal rule), heading markers, bold/italic markers, links, images, and
    table formatting. Content blockquotes ("> text") have the "> " prefix
    stripped but their text is preserved. Returns "" if input is empty.
    """
    if not text:
        return ""

    lines = text.split("\n")

    # Locate the first horizontal rule — everything before it is the header section
    first_hr = next(
        (i for i, line in enumerate(lines)
         if re.match(r"^-{3,}$", line.strip())),
        len(lines),
    )

    cleaned_lines = []
    for i, line in enumerate(lines):
        if i < first_hr and line.startswith(">"):
            # Header quoteblock (Source/URL metadata): drop entirely
            continue
        elif i >= first_hr and line.startswith(">"):
            # Content blockquote: strip the "> " prefix, keep the text
            cleaned_lines.append(re.sub(r"^>\s?", "", line))
        else:
            cleaned_lines.append(line)

    # Remove separator rows and prepend table header before each data row
    cleaned_lines = _attach_table_headers(cleaned_lines)

    text = "\n".join(cleaned_lines)

    # Remove horizontal rules
    text = re.sub(r"^-{3,}$", "", text, flags=re.MULTILINE)

    # Remove images: ![alt](url)
    text = re.sub(r"!\[[^\]]*\]\([^\)]*\)", "", text)

    # Convert links to plain text: [text](url) → text
    text = re.sub(r"\[([^\]]+)\]\([^\)]*\)", r"\1", text)

    # Strip heading markers, preserve text
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)

    # Remove bold/italic markers (* and _)
    text = re.sub(r"\*{1,3}([^*\n]+)\*{1,3}", r"\1", text)
    text = re.sub(r"_{1,3}([^_\n]+)_{1,3}", r"\1", text)

    # Normalize tab-indented sub-bullets to regular bullets so they embed consistently
    text = re.sub(r"^\t+([-*])", r"\1", text, flags=re.MULTILINE)

    # Remove inline code
    text = re.sub(r"`+[^`\n]+`+", "", text)

    # Collapse 3+ blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def chunk_document(text: str, metadata: dict) -> list[dict]:
    """Orchestrate chunking of a single document's cleaned text.

    Delegates to semantic_chunking(). Any alternative strategy must share
    the same (text, metadata) signature and list[dict] return shape.

    Returns [] if text is empty.
    """
    if not text:
        return []
    return semantic_chunking(text, metadata)


def semantic_chunking(text: str, metadata: dict) -> list[dict]:
    """Chunk cleaned document text using chonkie's SemanticChunker with bge-base-en-v1.5.

    Splits text at natural sentence/paragraph boundaries using peak detection
    on semantic similarity, respecting a 512-token maximum chunk size.

    Returns a list of dicts, each with:
      - "text": chunk text
      - "chunk_id": "{type}_{source}_{order}"
      - "metadata": {"type": ..., "source": ...}

    Returns [] if text is empty or too short to produce chunks.
    """
    if not text:
        return []

    chunker = _get_chunker()
    raw_chunks = chunker.chunk(text)

    doc_type = metadata["type"]
    source = metadata["source"]

    chunks = []
    for order, chunk in enumerate(raw_chunks):
        if chunk.text.strip():
            chunks.append({
                "text": chunk.text,
                "chunk_id": f"{doc_type}_{source}_{order}",
                "metadata": {"type": doc_type, "source": source},
            })

    return chunks
