import os
import chainlit as cl
from fastapi.staticfiles import StaticFiles
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langgraph.prebuilt import create_react_agent
from src.tools import build_tools
import json

# --- Monte le dossier 'data' comme fichiers statiques accessibles via /data/<file>
# Exécuter une seule fois au démarrage
if os.path.isdir("data"):
    try:
        cl.app.mount("/data", StaticFiles(directory="data"), name="data")
    except Exception:
        # Si déjà monté ou erreur, on ignore silencieusement
        pass

def build_sources_from_files(sources_list_from_agent=None):
    """
    Si l'agent renvoie une liste de sources (avec 'title' et éventuellement 'filename' ou 'url'),
    on complète les URLs vers /data/<filename>. Sinon, on retourne une liste vide.
    """
    results = []
    if not sources_list_from_agent:
        return results

    for src in sources_list_from_agent:
        title = src.get("title", "Source")
        # Priorité : url fournie par l'agent
        url = src.get("url")
        # Si l'agent a donné un nom de fichier correspondant à data/, on construit l'URL
        filename = src.get("filename") or src.get("file") or src.get("path")
        if not url and filename:
            # sécuriser le nom de fichier
            filename = os.path.basename(filename)
            if os.path.exists(os.path.join("data", filename)):
                url = f"/data/{filename}"
        # Si aucune url trouvée, on peut inclure le contenu inline (optionnel)
        results.append({"title": title, "url": url, "content": src.get("content", "")})
    return results

@cl.on_chat_start
async def start():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, streaming=True)
    tools = build_tools()
    agent = create_react_agent(llm, tools)
    cl.user_session.set("agent", agent)
    cl.user_session.set("chat_history", [])
    cl.user_session.set("pending_sources", None)
    await cl.Message(content="Bonjour ! Je suis votre assistant juridique. Comment puis-je vous aider aujourd'hui ?").send()

@cl.on_message
async def main(message: cl.Message):
    text = message.content.strip()

    # --- Gestion d'un clic sur un bouton qui renvoie une URL (si vous utilisez cl.Button)
    # Si le message reçu est une URL vers /data/..., on renvoie un message avec le lien (ou on laisse le navigateur ouvrir)
    if text.startswith("/data/") or text.startswith("http://") or text.startswith("https://"):
        # On renvoie un message confirmant l'ouverture (optionnel)
        await cl.Message(content=f"Ouvrir la ressource : {text}").send()
        return

    agent = cl.user_session.get("agent")
    chat_history = cl.user_session.get("chat_history", [])
    chat_history.append(HumanMessage(content=text))

    try:
        # Appel de l'agent
        res = await agent.ainvoke({"messages": chat_history})
        final_answer = res["messages"][-1].content
        sources_list = []

        # Extraction du JSON des sources si présent (votre logique existante)
        for msg in reversed(res["messages"]):
            if isinstance(msg, ToolMessage) and "📚 SOURCES UTILISÉES :" in msg.content:
                parts = msg.content.split("📚 SOURCES UTILISÉES :")
                if len(parts) > 1:
                    try:
                        sources_list = json.loads(parts[1].strip())
                    except:
                        sources_list = []
                break

        response_clean = final_answer.split("📚 SOURCES UTILISÉES :")[0].strip()

        # Envoi de la réponse principale
        await cl.Message(content=response_clean).send()

        # Construire la liste de sources enrichie (ajoute les URLs /data/<file> si possible)
        enriched = build_sources_from_files(sources_list)

        # Si on a des URLs, envoyer des liens cliquables Markdown (n'ouvre pas la sidebar)
        if enriched:
            # Construire la liste Markdown
            md_lines = []
            for src in enriched:
                title = src["title"]
                url = src.get("url")
                if url:
                    # lien cliquable qui ouvrira le PDF dans un nouvel onglet
                    md_lines.append(f"- [{title}]({url})")
                else:
                    # pas d'URL : afficher titre et (optionnellement) extrait
                    content_preview = src.get("content", "")
                    preview = content_preview[:400].replace("\n", " ") if content_preview else "Aucun aperçu disponible."
                    md_lines.append(f"- **{title}** — {preview}")

            await cl.Message(content="**Sources consultées :**\n\n" + "\n".join(md_lines)).send()

            # Stocker en session si vous voulez un affichage ultérieur via boutons
            cl.user_session.set("pending_sources", enriched)
        else:
            cl.user_session.set("pending_sources", None)

        # Mise à jour historique
        chat_history.append(AIMessage(content=response_clean))
        cl.user_session.set("chat_history", chat_history)

    except Exception as e:
        print(f"Erreur : {e}")
        await cl.Message(content=f"Erreur technique : {str(e)}").send()
