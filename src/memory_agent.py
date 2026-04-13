from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from src.tools import build_tools

SYSTEM_PROMPT = """
Tu es un assistant juridique conversationnel.

Règles :
- conserve le contexte de la conversation ;
- utilise les tools si nécessaire ;
- si l'utilisateur fait référence à un élément mentionné plus tôt, tiens-en compte ;
- n'invente jamais de base légale ;
- si une question relève du corpus PDF local, indique que le module RAG devra être utilisé dans l'intégration finale.
"""

def build_memory_agent():
    project_root = Path(__file__).resolve().parents[1]
    env_path = project_root / ".env"

    load_dotenv(env_path, override=True)
    openai_api_key = os.getenv("OPENAI_API_KEY")

    print("env_path =", env_path)
    print("env existe ?", env_path.exists())
    print("clé chargée ?", bool(openai_api_key))

    if not openai_api_key:
        raise ValueError(f"OPENAI_API_KEY manquant. .env attendu ici : {env_path}")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=openai_api_key,
    )

    tools = build_tools()
    checkpointer = InMemorySaver()

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )

    return agent