import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Base directory: product-support-bot/
BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset CSV path
DATA_CSV_PATH = os.getenv(
    "DATA_CSV_PATH",
    str(BASE_DIR / "data" / "DatafinitiElectronicsProductsPricingData.csv"),
)

# API key for Gemini 
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")