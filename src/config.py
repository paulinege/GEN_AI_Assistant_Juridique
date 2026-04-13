from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
<<<<<<< HEAD
DOCS_DIR = os.getenv("DOCS_DIR", "./data")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
=======
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

DOCS_DIR = os.getenv("DOCS_DIR", "./data")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")

WEB_SEARCH_MAX_RESULTS = int(os.getenv("WEB_SEARCH_MAX_RESULTS", "5"))
>>>>>>> 481b128e398b93d166d11ad98c0388a190eeaebb
