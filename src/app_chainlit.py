import chainlit as cl
from src.chat_memory import ask_agent_with_memory
from src.session_manager import new_thread_id
from src.router import classify_query
from src.rag_pipeline import load_vectorstore, get_retriever, ask_rag

@cl.on_chat_start
async def on_chat_start():
    thread_id = new_thread_id("juridique")
    cl.user_session.set("thread_id", thread_id)

    await cl.Message(
        content=(
            "**Assistant Juridique — Code du Travail**\n\n"
            "Bonjour ! Je suis votre assistant spécialisé en droit du travail français.\n\n"
            "Je peux vous aider à :\n"
            "- Répondre à des questions sur le Code du Travail\n"
            "- Calculer des indemnités, préavis...\n"
            "- Rechercher des informations récentes\n\n"
            "Posez votre question !"
        )
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    thread_id = cl.user_session.get("thread_id")
    query = message.content

    route = classify_query(query)

    if route == "rag":
        async with cl.Step(name="Recherche dans le Code du Travail..."):
            vectorstore = load_vectorstore()
            retriever = get_retriever(vectorstore)
            reponse = ask_rag(query, retriever)

    elif route == "tool":
        async with cl.Step(name="Utilisation des outils..."):
            reponse = ask_agent_with_memory(query, thread_id=thread_id)

    else:
        async with cl.Step(name="Réflexion..."):
            reponse = ask_agent_with_memory(query, thread_id=thread_id)

    await cl.Message(content=reponse).send()