import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from src.tools import build_tools

@cl.on_chat_start
async def start():
    """Initialisation de l'agent au démarrage du chat"""
    
    # 1. Configuration du modèle (LLM)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True)
    
    # 2. Récupération des outils
    tools = build_tools()
    
    # 3. Création de l'Agent (LangGraph gère le prompt automatiquement)
    agent = create_react_agent(llm, tools)
    
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
    
    # Appel de l'agent
    try:
        res = await agent.ainvoke(
            {"messages": chat_history},
            config={"callbacks": [cl.LangchainCallbackHandler()]}
        )
        
        # Extraire la réponse (dernier message de l'agent)
        output = res["messages"][-1].content
        
        # Mettre à jour l'historique
        chat_history.append(AIMessage(content=output))
        cl.user_session.set("chat_history", chat_history)
        
        # Envoi de la réponse finale
        await cl.Message(content=output).send()
        
    except Exception as e:
        await cl.Message(content=f"Erreur : {str(e)}").send()