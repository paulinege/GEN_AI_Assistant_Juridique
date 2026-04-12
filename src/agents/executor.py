from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from src.tools.calculator import calculate
from src.tools.weather import get_weather
from src.tools.web_search import search_web
from src.tools.todo_reader import read_todos


@tool
def calculator_tool(a: float, b: float, op: str) -> dict:
    """Effectue un calcul simple entre deux nombres.
    A utiliser pour les additions, soustractions, multiplications, divisions et puissances.
    """
    return calculate(a, b, op)


@tool
def weather_tool(city: str) -> dict:
    """Retourne la météo d'une ville.
    A utiliser pour les questions sur la météo, la température ou le temps.
    """
    return get_weather(city)


@tool
def web_search_tool(query: str) -> dict:
    """Effectue une recherche web.
    A utiliser pour les questions qui demandent des informations récentes ou Internet.
    """
    return search_web(query)


@tool
def todo_reader_tool(date: str = None) -> dict:
    """Lit les tâches locales depuis le fichier todo.
    A utiliser pour les questions sur les tâches, le planning, l'agenda ou les todos.
    """
    return read_todos(date)


def _build_agent():
    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0,
    )

    tools = [
        calculator_tool,
        weather_tool,
        web_search_tool,
        todo_reader_tool,
    ]

    system_prompt = """
Tu es un assistant intelligent multi-outils.

Tu dois choisir le bon outil quand c'est nécessaire :
- calculator_tool pour les calculs.
- weather_tool pour la météo.
- web_search_tool pour les recherches web et les informations récentes.
- todo_reader_tool pour les tâches, l'agenda ou les todos.

Si aucun outil n'est nécessaire, réponds directement.
Quand un outil renvoie un dictionnaire, reformule la réponse clairement pour l'utilisateur en français.
"""

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )
    return agent


def run_agent(user_query: str):
    agent = _build_agent()
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_query,
                }
            ]
        }
    )
    return result