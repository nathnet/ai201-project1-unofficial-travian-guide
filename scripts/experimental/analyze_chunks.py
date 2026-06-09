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

SMALL = 40

for name in samples:
    d = by_key.get(name)
    if not d:
        print(f"NOT FOUND: {name}")
        continue
    cleaned = clean_document(d["text"])
    chunks = chunk_document(cleaned, d["metadata"])
    words = [len(c["text"].split()) for c in chunks]
    small = [(i, chunks[i]) for i, w in enumerate(words) if w < SMALL]

    print(f"\n=== {name}: {len(chunks)} chunks, {len(small)} under {SMALL} words ===")
    print(f"  sizes: {words}")
    for i, c in small:
        print(f"  [chunk {i}, {words[i]}w] {c['text'][:150].replace(chr(10), ' / ')!r}")
