"""Configuration loaded from the local environment."""

import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Jarvis"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
