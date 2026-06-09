import sys
sys.stdout.reconfigure(encoding="utf-8")

import chroma_store
from ingest import load_documents, clean_document, chunk_document
from retriever import retrieve


def run_ingestion() -> None:
    """Run the full ingestion pipeline if the vector store is empty."""
    current_size = chroma_store.get_collection_size()
    if current_size > 0:
        print(f"ChromaDB already populated with {current_size} chunks, skipping ingestion.")
        return

    print("Starting ingestion...")
    documents = load_documents()
    print(f"Loaded {len(documents)} documents.")

    all_chunks = []
    for doc in documents:
        cleaned = clean_document(doc["text"])
        chunks = chunk_document(cleaned, doc["metadata"])
        all_chunks.extend(chunks)

    if not all_chunks:
        print("Warning: no chunks produced — check that documents/ is populated.")
        return

    print(f"Produced {len(all_chunks)} chunks. Embedding and storing...")
    chroma_store.embed_and_store(all_chunks)
    print("Ingestion completed.")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  TravianGuide — starting up")
    print("="*50 + "\n")
    run_ingestion()
