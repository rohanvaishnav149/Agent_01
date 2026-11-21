import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# Read the .env file that sits next to this Python file.
load_dotenv(Path(__file__).resolve().parent / ".env")

API_KEY = (os.getenv("OPENAI_API_KEY") or "").strip()
MODEL = (os.getenv("OPENAI_MODEL") or "gpt-6.2-sol").strip()

if not API_KEY or API_KEY.startswith("replace_this"):
    raise SystemExit("Please put your real OPENAI_API_KEY inside the .env file.")

# The AI model. Both Phase 1 and Phase 2 use this same object.
llm = ChatOpenAI(model=MODEL, api_key=API_KEY)
