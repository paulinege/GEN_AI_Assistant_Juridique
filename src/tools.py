from src.rag_pipeline import ask_rag, retriever_instance
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import requests
from langchain_core.tools import StructuredTool

from src.config import OPENWEATHER_API_KEY, TAVILY_API_KEY, WEB_SEARCH_MAX_RESULTS
from src.schemas import CalcInput, WeatherInput, WebSearchInput, TodoInput, EmptyInput


def safe_eval_math(expression: str) -> float:
    if not re.fullmatch(r"[0-9\s\+\-\*/\(\)\.]+", expression):
        raise ValueError("Expression non autorisée.")
    result = eval(expression, {"__builtins__": {}}, {})
    if not isinstance(result, (int, float)):
        raise ValueError("Résultat non numérique.")
    return float(result)


def calculatrice_juridique(expression: str) -> str:
    value = safe_eval_math(expression)
    return f"Résultat du calcul : {value}"


def fetch_weather(city: str, api_key: str) -> Dict[str, Any]:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "fr",
    }
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    return response.json()


def meteo_ville(ville: str) -> str:
    if not OPENWEATHER_API_KEY:
        return "OPENWEATHER_API_KEY absente. L'outil météo n'est pas disponible."
    try:
        data = fetch_weather(ville, OPENWEATHER_API_KEY)
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        return (
            f"Météo actuelle à {ville} : {description}, "
            f"{temp}°C, ressenti {feels_like}°C, humidité {humidity}%."
        )
    except Exception as exc:
        return f"Erreur météo pour '{ville}' : {exc}"


def tavily_search(question: str, max_results: int = WEB_SEARCH_MAX_RESULTS) -> Dict[str, Any]:
    if not TAVILY_API_KEY:
        raise RuntimeError("TAVILY_API_KEY absente.")
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": question,
        "max_results": max_results,
        "search_depth": "advanced",
        "include_answer": True,
    }
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def recherche_web_juridique(question: str) -> str:
    if not TAVILY_API_KEY:
        return "TAVILY_API_KEY absente. L'outil de recherche web n'est pas disponible."
    try:
        data = tavily_search(question, max_results=WEB_SEARCH_MAX_RESULTS)
        answer = data.get("answer", "")
        results = data.get("results", [])

        lines = []
        if answer:
            lines.append(f"Résumé web : {answer}")

        if results:
            lines.append("Sources :")
            for idx, item in enumerate(results[:WEB_SEARCH_MAX_RESULTS], start=1):
                title = item.get("title", "Sans titre")
                url = item.get("url", "")
                content = (item.get("content", "") or "").replace("\n", " ").strip()
                snippet = content[:220] + ("..." if len(content) > 220 else "")
                lines.append(f"{idx}. {title} — {url}\n   Extrait : {snippet}")

        return "\n".join(lines) if lines else "Aucun résultat web exploitable."
    except Exception as exc:
        return f"Erreur recherche web : {exc}"


def date_du_jour() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def todo_dossier_local(action: str, item: str = "") -> str:
    todo_path = Path("todo_juridique.json")
    data = json.loads(todo_path.read_text(encoding="utf-8")) if todo_path.exists() else []

    action = action.strip().lower()

    if action == "ajouter":
        if not item.strip():
            return "Impossible d'ajouter un élément vide."
        data.append(item.strip())
        todo_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return f"Élément ajouté : {item.strip()}"

    if action == "lister":
        if not data:
            return "La todo est vide."
        return "Todo dossier :\n- " + "\n- ".join(data)

    if action == "supprimer":
        if item.strip() in data:
            data.remove(item.strip())
            todo_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            return f"Élément supprimé : {item.strip()}"
        return f"Élément introuvable : {item.strip()}"

    return "Action invalide. Utiliser : ajouter, lister, supprimer."


def build_tools():
    return [
        StructuredTool.from_function(
            func=lambda q: ask_rag(q, retriever_instance),
            name="recherche_documents_internes",
            description="RECHERCHE PRIORITAIRE. Utilise cet outil pour répondre aux questions sur le droit du travail en consultant les documents internes (Code du Travail).",
            args_schema=WebSearchInput, # On réutilise WebSearchInput car il prend une 'question' en entrée
        ),
        StructuredTool.from_function(
            func=calculatrice_juridique,
            name="calculatrice_juridique",
            description="Effectue un calcul numérique utile en contexte juridique.",
            args_schema=CalcInput,
        ),
        StructuredTool.from_function(
            func=meteo_ville,
            name="meteo_ville",
            description="Retourne la météo actuelle d'une ville.",
            args_schema=WeatherInput,
        ),
        StructuredTool.from_function(
            func=recherche_web_juridique,
            name="recherche_web_juridique",
            description="Recherche sur le web des informations juridiques récentes.",
            args_schema=WebSearchInput,
        ),
        StructuredTool.from_function(
            func=lambda: date_du_jour(),
            name="date_du_jour",
            description="Retourne la date et l'heure actuelles.",
            args_schema=EmptyInput,
        ),
        StructuredTool.from_function(
            func=todo_dossier_local,
            name="todo_dossier_local",
            description="Gère une todo locale liée à un dossier juridique.",
            args_schema=TodoInput,
        ),
    ]