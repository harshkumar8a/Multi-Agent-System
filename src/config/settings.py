from dotenv import load_dotenv
import os

load_dotenv()

OLLAMA_MODEL = "llama3.2"

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

LANGCHAIN_PROJECT = os.getenv(
    "LANGCHAIN_PROJECT"
)