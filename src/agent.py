from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from src.tools import build_tools

SYSTEM_PROMPT = """
Tu es un assistant juridique.

- utilise les tools quand nécessaire
- n'invente jamais de lois
- si la question concerne des PDF -> dire que RAG sera utilisé
"""

def build_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    return create_agent(
        model=llm,
        tools=build_tools(),
        system_prompt=SYSTEM_PROMPT
    )


def ask_agent(query: str):
    agent = build_agent()

    result = agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })

    return result["messages"][-1].content