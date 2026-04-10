"""
Partie 3 — Routeur intelligent
Décide si la question → RAG, Agent, ou LLM direct
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory

from rag_pipeline import load_vectorstore, get_retriever
from agents import get_agent_executor

# ─── LLM de base ─────────────────────────────────────────────────────────────

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# ─── Mémoire conversationnelle ───────────────────────────────────────────────

memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history"
)

# ─── Classifier de routage ───────────────────────────────────────────────────

ROUTER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Tu es un routeur pour un assistant juridique.
Analyse la question et réponds UNIQUEMENT par un de ces mots :
- RAG : si la question porte sur les textes de loi, articles, droits, obligations du Code du Travail
- AGENT : si la question nécessite un calcul (indemnités, préavis, salaires) ou une recherche web récente
- LLM : si c'est une salutation, une question générale, ou hors sujet juridique

Réponds uniquement par RAG, AGENT ou LLM."""),
    ("human", "{question}")
])

router_chain = ROUTER_PROMPT | llm | StrOutputParser()

# ─── Chaîne RAG ──────────────────────────────────────────────────────────────

RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Tu es un assistant juridique expert en droit du travail français.
Réponds à la question en te basant UNIQUEMENT sur les extraits du Code du Travail fournis.
Si l'information n'est pas dans les extraits, dis-le clairement.
Cite les articles pertinents quand possible.

Extraits du Code du Travail :
{context}

Historique de conversation :
{chat_history}"""),
    ("human", "{question}")
])


def rag_chain(question: str, retriever, chat_history: str) -> str:
    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])
    chain = RAG_PROMPT | llm | StrOutputParser()
    return chain.invoke({
        "context": context,
        "question": question,
        "chat_history": chat_history
    })


# ─── Chaîne LLM direct ───────────────────────────────────────────────────────

LLM_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Tu es un assistant juridique aimable spécialisé en droit du travail français. Réponds en français."),
    ("human", "{question}")
])

llm_chain = LLM_PROMPT | llm | StrOutputParser()

# ─── Routeur principal ────────────────────────────────────────────────────────

def route(question: str) -> str:
    """Route la question vers le bon système et retourne la réponse"""

    # Chargement vectorstore et agent
    vectorstore = load_vectorstore()
    retriever = get_retriever(vectorstore)
    agent_executor = get_agent_executor()

    # Historique mémoire
    chat_history = memory.load_memory_variables({}).get("chat_history", "")

    # Classification
    route_decision = router_chain.invoke({"question": question}).strip().upper()
    print(f"[Routeur] → {route_decision}")

    # Dispatch
    if route_decision == "RAG":
        response = rag_chain(question, retriever, str(chat_history))
    elif route_decision == "AGENT":
        result = agent_executor.invoke({"input": question})
        response = result["output"]
    else:
        response = llm_chain.invoke({"question": question})

    # Sauvegarde mémoire
    memory.save_context({"input": question}, {"output": response})

    return response


if __name__ == "__main__":
    questions = [
        "Bonjour, comment ça va ?",
        "Quelles sont les conditions du licenciement pour faute grave ?",
        "Calcule mon indemnité pour 4000€ de salaire et 12 ans d'ancienneté.",
        "Et pour une faute simple, c'est quoi la différence ?",  # Test mémoire
    ]
    for q in questions:
        print(f"\n{'='*60}")
        print(f"Q: {q}")
        print(f"R: {route(q)}")
