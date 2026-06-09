import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from config import CHROMA_DB_DIR, COLLECTION_NAME, EMBEDDING_MODEL

_client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
_embedding_fn = SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_collection = _client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=_embedding_fn,
    metadata={"hnsw:space": "cosine"},
)


def _get_collection():
    return _collection


def get_collection_size() -> int:
    """Return the number of chunks stored in the ChromaDB collection."""
    try:
        return _get_collection().count()
    except Exception:
        return 0


def embed_and_store(chunks: list[dict]) -> None:
    """Embed each chunk with bge-base-en-v1.5 and write to ChromaDB.

    Skips storing if the collection already contains documents to prevent
    duplicates on re-runs.
    """
    collection = _get_collection()
    if collection.count() > 0:
        return

    ids = [chunk["chunk_id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [chunk["metadata"] for chunk in chunks]

    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    print(f"Stored {collection.count()} chunks in ChromaDB.")


def query(query_text: str, n_results: int) -> dict | None:
    """Embed the query with bge-base-en-v1.5 and run a cosine similarity search.

    Returns the raw ChromaDB response with 'documents', 'metadatas', and
    'distances' keys, or None if the collection is empty.
    """
    collection = _get_collection()
    if collection.count() == 0:
        return None

    return collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )
