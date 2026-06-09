import os
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Paths
DOCUMENTS_DIR = Path(__file__).parent / "documents"
CHROMA_DB_DIR = Path(__file__).parent / "chroma_db"

# Embedding model (shared by ingest and chroma_store)
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"

# Chunking — change CHUNKING_STRATEGY to switch between strategies
class ChunkingStrategy(Enum):
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"

CHUNKING_STRATEGY = ChunkingStrategy.SEMANTIC

CHUNK_SIZE = 512
CHUNK_THRESHOLD = 0.6
MIN_SENTENCES_PER_CHUNK = 2
MIN_CHARACTERS_PER_SENTENCE = 50

# ChromaDB — collection name is derived from CHUNKING_STRATEGY
COLLECTION_NAME = f"travian_guide_{CHUNKING_STRATEGY.value}"

# Retrieval
N_RESULTS = 10
DISTANCE_THRESHOLD = 0.4
# Reciprocal Rank Fusion constant — dampens the influence of top-ranked results,
# preventing a single list from dominating the merged ranking. Standard value is 60.
RRF_K = 60

# Generation
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
HISTORY_TURNS = 3

# UI options
class SourceFilter(Enum):
    ALL = "All"
    OFFICIAL = "Official"
    UNOFFICIAL = "Unofficial"

class SearchMode(Enum):
    VECTOR = "Vector Search"
    HYBRID = "Hybrid Search"
