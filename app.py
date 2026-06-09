import sys
sys.stdout.reconfigure(encoding="utf-8")

import gradio as gr

import chroma_store
from config import SourceFilter, SearchMode
from ingest import load_documents, clean_document, chunk_document
from retriever import retrieve, hybrid_retrieve, build_bm25_index
from generator import generate_response


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

def chat(message: str, history: list, source_filter: str = SourceFilter.ALL.value, search_mode: str = SearchMode.VECTOR.value) -> str:
    """Handle a single chat turn — retrieve relevant chunks and generate a grounded response."""
    if not message.strip():
        return "Please enter a question about Travian: Legends."
    source_type = None if source_filter == SourceFilter.ALL.value else source_filter.lower()
    if search_mode == SearchMode.HYBRID.value:
        chunks = hybrid_retrieve(message.strip(), source_type=source_type)
    else:
        chunks = retrieve(message.strip(), source_type=source_type)
    return generate_response(message.strip(), chunks, history)


def build_ui() -> gr.Blocks:
    """Construct and return the Gradio Blocks UI."""
    documents = load_documents()
    guide_items = []
    for doc in sorted(documents, key=lambda d: (d["metadata"]["type"], d["metadata"]["source"])):
        label = "Official" if doc["metadata"]["type"] == "official" else "Unofficial"
        name = doc["metadata"]["source"].replace(".md", "").replace("-", " ").title()
        guide_items.append(f"<li><b>{label}:</b> {name}</li>")
    guides_html = f"<ul style='padding-left:1rem'>{''.join(guide_items)}</ul>" if guide_items else "<p>No guides loaded.</p>"

    with gr.Blocks(title="The Unofficial Travian Guide") as demo:
        gr.Markdown("# The Unofficial Travian Guide\nAsk anything about Travian: Legends — tribes, combat, buildings, and more.")

        with gr.Row():
            with gr.Column(scale=3):
                gr.ChatInterface(
                    fn=chat,
                    chatbot=gr.Chatbot(height=500),
                    additional_inputs=[
                        gr.Radio(
                            choices=[f.value for f in SourceFilter],
                            value=SourceFilter.ALL.value,
                            label="Source Filter",
                        ),
                        gr.Radio(
                            choices=[m.value for m in SearchMode],
                            value=SearchMode.VECTOR.value,
                            label="Search Mode",
                        ),
                    ],
                    examples=[
                        ["What is wave sniping?", SourceFilter.ALL.value, SearchMode.VECTOR.value],
                        ["Which tribe can build resource fields and buildings at the same time without Travian Plus?", SourceFilter.ALL.value, SearchMode.VECTOR.value],
                        ["What is an operational hammer?", SourceFilter.ALL.value, SearchMode.VECTOR.value],
                        ["How do you win a Travian: Legends server?", SourceFilter.ALL.value, SearchMode.HYBRID.value],
                        ["What are the strengths of Gauls?", SourceFilter.ALL.value, SearchMode.VECTOR.value],
                    ],
                )
            with gr.Column(scale=2):
                gr.Markdown("### Loaded Game Guides")
                gr.HTML(f"<div style='height:500px; overflow-y:auto; border:1px solid #e0e0e0; border-radius:6px; padding:0.5rem'>{guides_html}</div>")

    return demo


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  TravianGuide — starting up")
    print("="*50 + "\n")
    run_ingestion()
    build_bm25_index()
    ui = build_ui()
    ui.launch()
