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
            "Assistant Juridique — Code du Travail\n\n"
            "Bonjour ! Je suis votre assistant specialise en droit du travail francais.\n\n"
            "Je peux vous aider a :\n"
            "- Repondre a des questions sur le Code du Travail\n"
            "- Calculer des indemnites, preavis...\n"
            "- Rechercher des informations recentes\n\n"
            "Exemples de questions :\n"
            "- Quel est le delai de preavis pour un CDI ?\n"
            "- Calcule mon indemnite pour 3000 euros et 5 ans d anciennete\n"
            "- Quelles sont les regles sur le harcelement moral ?\n\n"
            "Posez votre question !"
        )
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    thread_id = cl.user_session.get("thread_id")
    query = message.content

    route = classify_query(query)

    if route == "rag":
        async with cl.Step(name="Recherche dans le Code du Travail...") as step:
            vectorstore = load_vectorstore()
            retriever = get_retriever(vectorstore)
            docs = retriever.invoke(query)
            reponse = ask_rag(query, retriever)

            sources = "\n".join([
                f"- {doc.metadata.get('source', '?').split('/')[-1]}"
                f" (page {doc.metadata.get('page', '?')})"
                for doc in docs
            ])
            step.output = f"Sources consultees :\n{sources}"

        await cl.Message(content=reponse).send()

    elif route == "tool":
        async with cl.Step(name="Utilisation des outils...") as step:
            reponse = ask_agent_with_memory(query, thread_id=thread_id)
            step.output = "Calcul ou recherche effectue"

        await cl.Message(content=reponse).send()

    else:
        async with cl.Step(name="Reflexion...") as step:
            reponse = ask_agent_with_memory(query, thread_id=thread_id)
            step.output = "Reponse generee"

        await cl.Message(content=reponse).send()