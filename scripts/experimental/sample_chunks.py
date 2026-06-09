import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))
from ingest import load_documents, clean_document, chunk_document

docs = load_documents()
by_key = {d["metadata"]["type"] + "_" + d["metadata"]["source"]: d for d in docs}

samples = [
    "official_artefacts-faq.md",
    "official_adventures.md",
    "official_alliance-management.md",
    "official_buildings-and-resource-fields-statistics.md",
    "unofficial_game-secrets-combat-basics-written-by-kirilloid.md",
    "unofficial_developing-your-first-villages.md",
]

for name in samples:
    d = by_key.get(name)
    if not d:
        print(f"NOT FOUND: {name}")
        continue
    cleaned = clean_document(d["text"])
    chunks = chunk_document(cleaned, d["metadata"])
    print(f"\n=== {name} => {len(chunks)} chunks ===")
    for c in chunks:
        words = len(c["text"].split())
        preview = c["text"][:200].replace("\n", " ")
        print(f"  [{c['chunk_id'].split('_')[-1]}] {words}w | {preview}")
