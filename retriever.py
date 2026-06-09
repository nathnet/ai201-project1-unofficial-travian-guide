import bm25s
import Stemmer

import chroma_store
from config import N_RESULTS, DISTANCE_THRESHOLD, RRF_K

_bm25_index = None
_bm25_corpus: list[dict] = []
_stemmer = Stemmer.Stemmer("english")


def build_bm25_index() -> None:
    """Fetch all chunks from ChromaDB and build an in-memory BM25 index.

    Called once at app startup after ingestion. Stores the index and corpus
    in module-level variables for use by bm25_search(). Uses an English
    Snowball stemmer so query tokens like 'win' match 'wins' and 'winning'.
    """
    global _bm25_index, _bm25_corpus

    _bm25_corpus = chroma_store.get_all_chunks()
    if not _bm25_corpus:
        print("Warning: BM25 index not built — no chunks in collection.")
        return

    texts = [chunk["text"] for chunk in _bm25_corpus]
    tokenized = bm25s.tokenize(texts, stemmer=_stemmer, show_progress=False)

    _bm25_index = bm25s.BM25()
    _bm25_index.index(tokenized)
    print(f"BM25 index built over {len(_bm25_corpus)} chunks.")


def bm25_search(query: str, n_results: int = N_RESULTS, source_type: str | None = None) -> list[dict]:
    """Search the in-memory BM25 index and return top-n chunks by keyword relevance.

    Filters by source_type after retrieval if specified. Returns [] if the index
    has not been built or no results are found. Each result contains 'text',
    'metadata', and 'score' (higher = more relevant).
    """
    if _bm25_index is None or not _bm25_corpus:
        return []

    query_tokens = bm25s.tokenize([query], stemmer=_stemmer, show_progress=False)
    k = min(50, len(_bm25_corpus))
    results, scores = _bm25_index.retrieve(query_tokens, k=k)

    chunks = []
    for idx, score in zip(results[0], scores[0]):
        chunk = _bm25_corpus[idx]
        if source_type and chunk["metadata"]["type"] != source_type:
            continue
        chunks.append({
            "text": chunk["text"],
            "metadata": chunk["metadata"],
            "score": float(score),
        })
        if len(chunks) == n_results:
            break

    return chunks


def hybrid_retrieve(query: str, n_results: int = N_RESULTS, source_type: str | None = None) -> list[dict]:
    """Merge semantic and BM25 results using Reciprocal Rank Fusion (RRF).

    RRF score = Σ 1 / (k + rank) across both result lists. Chunks are deduped
    by text. Returns the same list[dict] shape as retrieve(), with 'distance'
    included only for chunks that appeared in semantic results.
    """
    semantic_results = retrieve(query, n_results * 2, source_type, threshold=None)
    bm25_results = bm25_search(query, n_results, source_type)

    rrf_scores: dict[str, float] = {}
    chunk_map: dict[str, dict] = {}

    for rank, chunk in enumerate(semantic_results):
        key = chunk["text"]
        rrf_scores[key] = rrf_scores.get(key, 0.0) + 1.0 / (RRF_K + rank + 1)
        chunk_map[key] = chunk

    for rank, chunk in enumerate(bm25_results):
        key = chunk["text"]
        rrf_scores[key] = rrf_scores.get(key, 0.0) + 1.0 / (RRF_K + rank + 1)
        if key not in chunk_map:
            chunk_map[key] = {"text": chunk["text"], "metadata": chunk["metadata"]}

    ranked = sorted(rrf_scores, key=lambda k: rrf_scores[k], reverse=True)
    return [chunk_map[key] for key in ranked[:n_results]]


def retrieve(query: str, n_results: int = N_RESULTS, source_type: str | None = None, threshold: float | None = DISTANCE_THRESHOLD) -> list[dict]:
    """Query ChromaDB and return filtered, reshaped chunks for prompt assembly.

    Applies a distance threshold (default 0.4) — pass None to skip filtering,
    which is used by hybrid_retrieve() so RRF acts as the quality signal instead.
    Optionally filters by source type ('official' or 'unofficial').
    Returns [] if the collection is empty or no chunks pass the threshold.
    """
    raw = chroma_store.query(query, n_results, source_type)
    if raw is None:
        return []

    documents = raw["documents"][0]
    metadatas = raw["metadatas"][0]
    distances = raw["distances"][0]

    chunks = []
    for text, metadata, distance in zip(documents, metadatas, distances):
        if threshold is None or distance < threshold:
            chunks.append({
                "text": text,
                "metadata": metadata,
                "distance": distance,
            })

    return chunks
