import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    TODO_FILE_PATH = os.getenv("TODO_FILE_PATH", "data/todo.json")
    WEATHER_TIMEOUT = int(os.getenv("WEATHER_TIMEOUT", "10"))
    WEB_SEARCH_MAX_RESULTS = int(os.getenv("WEB_SEARCH_MAX_RESULTS", "5"))


settings = Settings()