import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.graph import START, StateGraph
from src.tools import build_tools

@cl.on_chat_start
async def start():
    """Initialisation de l'agent au démarrage du chat"""
    
    # 1. Configuration du modèle (LLM)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True)
    
    # 2. Récupération des outils
    tools = build_tools()
    
    # 3. Définition du Prompt (Système d'aiguillage)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Tu es un assistant juridique expert.
        - Si l'utilisateur te salue, réponds poliment sans outils.
        - Pour toute question sur le droit du travail, utilise l'outil de recherche documentaire.
        - Pour les calculs, la météo ou le web, utilise les outils correspondants.
        - Cite toujours tes sources quand tu utilises les documents internes.
        """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # 4. Création de l'Agent avec LangGraph (nouvelle API)
    agent = create_react_agent(llm, tools, prompt=prompt)
    
    # Stockage dans la session Chainlit
    cl.user_session.set("agent", agent)
    cl.user_session.set("chat_history", [])
    
    await cl.Message(content="Bonjour ! Je suis votre assistant juridique. Comment puis-je vous aider aujourd'hui ?").send()

@cl.on_message
async def main(message: cl.Message):
    """Traitement de chaque message envoyé par l'utilisateur"""
    
    agent = cl.user_session.get("agent")
    chat_history = cl.user_session.get("chat_history", [])
    
    # Ajouter le message utilisateur à l'historique
    chat_history.append(HumanMessage(content=message.content))
    
    # Appel de l'agent avec le gestionnaire de callback Chainlit
    res = await agent.ainvoke(
        {
            "input": message.content,
            "chat_history": chat_history
        },
        config={"callbacks": [cl.LangchainCallbackHandler()]}
    )
    
    # Extraire la réponse
    output = res.get("output", "")
    
    # Mettre à jour l'historique
    from langchain_core.messages import AIMessage
    chat_history.append(AIMessage(content=output))
    cl.user_session.set("chat_history", chat_history)
    
    # Envoi de la réponse finale
    await cl.Message(content=output).send()
