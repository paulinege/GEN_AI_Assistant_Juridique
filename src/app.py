"""
Partie 4 — Interface Chainlit
Lancer avec : chainlit run src/app.py -w
"""

import chainlit as cl
from router import route


@cl.on_chat_start
async def on_chat_start():
    """Message d'accueil au démarrage de la conversation"""
    await cl.Message(
        content=(
            "⚖️ **Assistant Juridique — Code du Travail**\n\n"
            "Bonjour ! Je suis votre assistant spécialisé en droit du travail français.\n\n"
            "Je peux vous aider à :\n"
            "- 📖 Répondre à des questions sur le **Code du Travail**\n"
            "- 🧮 **Calculer** des indemnités de licenciement, préavis…\n"
            "- 🔍 Rechercher des informations juridiques **récentes**\n\n"
            "Posez votre question !"
        )
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    """Traitement de chaque message utilisateur"""

    # Indicateur de chargement
    async with cl.Step(name="Analyse en cours…") as step:
        step.output = "Recherche dans le Code du Travail…"

    # Appel au routeur
    response = route(message.content)

    # Envoi de la réponse
    await cl.Message(content=response).send()
