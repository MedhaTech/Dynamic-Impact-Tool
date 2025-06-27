import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Groq API Settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Default LLM Model
DEFAULT_MODEL = "llama3-8b-8192"

# Temperature and behavior settings
DEFAULT_TEMPERATURE = 0.3

# Number of rows to sample from dataset if not explicitly given
DEFAULT_SAMPLE_SIZE = 1000

if not GROQ_API_KEY or "xxxx" in GROQ_API_KEY:
    raise ValueError("🚨 Missing or invalid GROQ_API_KEY in .env")
