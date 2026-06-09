import chroma_store
from config import N_RESULTS, DISTANCE_THRESHOLD


def retrieve(query: str, n_results: int = N_RESULTS) -> list[dict]:
    """Query ChromaDB and return filtered, reshaped chunks for prompt assembly.

    Applies a distance threshold of 0.7 — chunks with a cosine distance at or
    above the threshold are excluded. Returns [] if the collection is empty or
    no chunks pass the threshold.
    """
    raw = chroma_store.query(query, n_results)
    if raw is None:
        return []

    documents = raw["documents"][0]
    metadatas = raw["metadatas"][0]
    distances = raw["distances"][0]

    chunks = []
    for text, metadata, distance in zip(documents, metadatas, distances):
        if distance < DISTANCE_THRESHOLD:
            chunks.append({
                "text": text,
                "metadata": metadata,
                "distance": distance,
            })

    return chunks
