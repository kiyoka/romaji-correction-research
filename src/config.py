"""Configuration settings for the typo correction experiment."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "src" / "data"
RESULTS_DIR = PROJECT_ROOT / "results"

# Data files
REAL_TYPOS_FILE = DATA_DIR / "real_typos.json"
VIRTUAL_TYPOS_FILE = DATA_DIR / "virtual_typos.json"

# OpenAI API settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-5.2"  # GPT-5.2 for improved accuracy

# Create results directory if it doesn't exist
RESULTS_DIR.mkdir(exist_ok=True)
