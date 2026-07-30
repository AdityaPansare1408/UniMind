from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Google Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Validate API key
if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. Please add it to your .env file."
    )