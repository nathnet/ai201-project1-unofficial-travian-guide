import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Paths
DOCUMENTS_DIR = Path(__file__).parent / "documents"
CHROMA_DB_DIR = Path(__file__).parent / "chroma_db"

# ChromaDB
COLLECTION_NAME = "travian_guide"

# Embedding model (shared by ingest and chroma_store)
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

# Chunking
CHUNK_SIZE = 512
CHUNK_THRESHOLD = 0.6
MIN_SENTENCES_PER_CHUNK = 2
MIN_CHARACTERS_PER_SENTENCE = 50

# Retrieval
N_RESULTS = 10
DISTANCE_THRESHOLD = 0.4

# Generation
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
HISTORY_TURNS = 3
