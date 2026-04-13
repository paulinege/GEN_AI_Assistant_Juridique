import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from src.tools import build_tools

@cl.on_chat_start
async def start():
    """Initialisation de l'agent au démarrage du chat"""
    
    # 1. Configuration du modèle (LLM)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True)
    
    # 2. Récupération des outils (incluant votre RAG)
    tools = build_tools()
    
    # 3. Définition du Prompt (Système d'aiguillage)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Tu es un assistant juridique expert.
        - Si l'utilisateur te salue, réponds poliment sans outils.
        - Pour toute question sur le droit du travail, utilise l'outil de recherche documentaire[cite: 30].
        - Pour les calculs, la météo ou le web, utilise les outils correspondants[cite: 31].
        - Cite toujours tes sources quand tu utilises les documents internes.
        """),
        MessagesPlaceholder(variable_name="chat_history"), # Mémoire 
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # 4. Configuration de la mémoire
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # 5. Création de l'Agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        memory=memory, 
        verbose=True,
        handle_parsing_errors=True
    )
    
    # Stockage dans la session Chainlit
    cl.user_session.set("agent", agent_executor)
    await cl.Message(content="Bonjour ! Je suis votre assistant juridique. Comment puis-je vous aider aujourd'hui ?").send()

@cl.on_message
async def main(message: cl.Message):
    """Traitement de chaque message envoyé par l'utilisateur"""
    
    agent_executor = cl.user_session.get("agent")
    
    # Appel de l'agent avec le gestionnaire de callback Chainlit
    # Cela permet de voir les étapes de réflexion de l'agent en direct
    res = await agent_executor.ainvoke(
        {"input": message.content},
        config={"callbacks": [cl.LangchainCallbackHandler()]}
    )
    
    # Envoi de la réponse finale
    await cl.Message(content=res["output"]).send()