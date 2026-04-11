import re
from src.tools.calculator import calculate
from src.tools.weather import get_weather
from src.tools.web_search import search_web
from src.tools.todo_reader import read_todos


def extract_city(query: str) -> str:
    patterns = [
        r"météo à\s+([A-Za-zÀ-ÿ\- ]+)",
        r"meteo à\s+([A-Za-zÀ-ÿ\- ]+)",
        r"température à\s+([A-Za-zÀ-ÿ\- ]+)",
        r"temperature à\s+([A-Za-zÀ-ÿ\- ]+)",
        r"à\s+([A-Za-zÀ-ÿ\- ]+)$",
    ]

    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            city = match.group(1).strip(" ?!.,;:")
            return city

    return "Paris"

def extract_date(query: str) -> str | None:
    match = re.search(r"\d{4}-\d{2}-\d{2}", query)
    return match.group(0) if match else None


def extract_math_expression(query: str):
    match = re.search(r"(\d+(?:\.\d+)?)\s*([\+\-\*/]{1,2})\s*(\d+(?:\.\d+)?)", query)
    if not match:
        return None
    a, op, b = match.groups()
    return float(a), float(b), op


def route_query(user_query: str):
    q = user_query.lower()

    if "météo" in q or "meteo" in q or "température" in q or "temperature" in q:
        city = extract_city(user_query)
        return get_weather(city)

    if "tâche" in q or "tache" in q or "todo" in q or "agenda" in q or "calendrier" in q:
        date = extract_date(user_query)
        return read_todos(date)

    if "cherche" in q or "recherche" in q or "internet" in q or "web" in q:
        return search_web(user_query)

    math_expr = extract_math_expression(user_query)
    if math_expr:
        a, b, op = math_expr
        return calculate(a, b, op)

    return {
        "tool_name": "llm_direct",
        "status": "success",
        "input": {"query": user_query},
        "output": {"message": "No tool required. Direct LLM response can be used."},
        "error": None,
    }