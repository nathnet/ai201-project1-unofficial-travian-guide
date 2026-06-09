import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))
from ingest import load_documents, clean_document, chunk_document

docs = load_documents()
by_key = {d["metadata"]["type"] + "_" + d["metadata"]["source"]: d for d in docs}

samples = [
    "official_the-tribes-and-their-advantages.md",
    "unofficial_game-secrets-sniping-waves.md",
    "official_battle-mechanics.md",
    "official_culture-points-cp.md",
]

for name in samples:
    d = by_key.get(name)
    if not d:
        print(f"NOT FOUND: {name}")
        continue
    cleaned = clean_document(d["text"])
    chunks = chunk_document(cleaned, d["metadata"])
    print(f"=== {name} => {len(chunks)} chunk(s) ===")
    for c in chunks:
        word_count = len(c["text"].split())
        print(f"  [{c['chunk_id']}] ~{word_count} words")
        print(f"  {c['text'][:200]}")
        print()
