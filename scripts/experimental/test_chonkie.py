from chonkie import SemanticChunker
from chonkie.embeddings import SentenceTransformerEmbeddings

embeddings = SentenceTransformerEmbeddings("BAAI/bge-base-en-v1.5")
chunker = SemanticChunker(embedding_model=embeddings, max_chunk_size=512, threshold=0.5)

test_text = """Do artefact effects stack?

No. Artefact effects of the same type do not stack.

If you own multiple artefacts with the same effect a village-scope artefact overrides an account-scope artefact for that specific village.

Does the Stronger Buildings artefact affect walls?

Yes. The Stronger Buildings artefact also applies to walls.

How many artefacts can I own and use?

You can own any number of artefacts on your account. However at any given time a maximum of three artefacts can be active and only one account-scope artefact can be active."""

chunks = chunker.chunk(test_text)
print(f"{len(chunks)} chunks")
for c in chunks:
    print(f"  [{c.token_count} tokens] {c.text[:120]}")
