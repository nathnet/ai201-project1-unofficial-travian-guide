import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from chonkie import SemanticChunker
from chonkie.embeddings import SentenceTransformerEmbeddings
from ingest import load_documents, clean_document

SAMPLES = [
    "official_artefacts-faq.md",
    "official_adventures.md",
    "official_alliance-management.md",
    "unofficial_developing-your-first-villages.md",
    "unofficial_game-secrets-combat-basics-written-by-kirilloid.md",
]

THRESHOLDS = [0.3, 0.4, 0.5, 0.6, 0.7]

docs = load_documents()
by_key = {d["metadata"]["type"] + "_" + d["metadata"]["source"]: d for d in docs}

print(f"\n{'Doc':<52} " + "  ".join(f"t={t}" for t in THRESHOLDS))
print("-" * 90)

embeddings = SentenceTransformerEmbeddings("BAAI/bge-base-en-v1.5")

for name in SAMPLES:
    d = by_key.get(name)
    if not d:
        print(f"NOT FOUND: {name}")
        continue
    cleaned = clean_document(d["text"])

    counts = []
    for t in THRESHOLDS:
        chunker = SemanticChunker(
            embedding_model=embeddings,
            threshold=t,
            chunk_size=512,
            min_sentences_per_chunk=2,
            min_characters_per_sentence=50,
        )
        chunks = [c for c in chunker.chunk(cleaned) if c.text.strip()]
        counts.append(len(chunks))

    label = name.replace("official_", "").replace("unofficial_", "")[:50]
    print(f"{label:<52} " + "  ".join(f"{c:>5}" for c in counts))
