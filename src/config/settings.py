from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# =========================
# API Keys
# =========================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. Please add it to your .env file."
    )

# =========================
# Gemini Models
# =========================

GOOGLE_CHAT_MODELS = [
    model.strip()
    for model in os.getenv(
        "GOOGLE_CHAT_MODELS",
        "models/gemini-3.5-flash-lite,models/gemini-3.6-flash",
    ).split(",")
]

GOOGLE_EMBEDDING_MODEL = os.getenv(
    "GOOGLE_EMBEDDING_MODEL",
    "models/gemini-embedding-001",
)

CHROMA_DB_PATH = "data/chroma_db"

# =========================
# Retry Configuration
# =========================

MAX_RETRIES = 3

REQUEST_TIMEOUT = 60