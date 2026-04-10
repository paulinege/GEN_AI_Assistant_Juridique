"""
Partie 2 — Agents & Outils
Calculatrice juridique, recherche web, calcul de délais légaux
"""

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate


# ─── Outil 1 : Calculatrice juridique ───────────────────────────────────────

@tool
def calculatrice_juridique(expression: str) -> str:
    """
    Effectue des calculs juridiques simples.
    Exemples : indemnités de licenciement, montant de préavis, heures supplémentaires.
    Entrée : expression mathématique en texte (ex: '2500 * 5 * 0.25')
    """
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"Résultat : {result:.2f}"
    except Exception as e:
        return f"Erreur de calcul : {str(e)}"


# ─── Outil 2 : Calcul d'indemnité de licenciement ───────────────────────────

@tool
def calcul_indemnite_licenciement(salaire_mensuel: float, annees_anciennete: float) -> str:
    """
    Calcule l'indemnité légale de licenciement selon le Code du Travail français.
    - 1/4 de mois de salaire par année pour les 10 premières années
    - 1/3 de mois de salaire par année au-delà de 10 ans
    Paramètres : salaire_mensuel (en euros), annees_anciennete (nombre d'années)
    """
    if annees_anciennete < 1:
        return "Ancienneté insuffisante (moins d'1 an) : pas d'indemnité légale."

    if annees_anciennete <= 10:
        indemnite = salaire_mensuel * annees_anciennete * (1 / 4)
    else:
        indemnite = salaire_mensuel * 10 * (1 / 4)
        indemnite += salaire_mensuel * (annees_anciennete - 10) * (1 / 3)

    return (
        f"Indemnité légale de licenciement :\n"
        f"  - Salaire mensuel : {salaire_mensuel:.2f} €\n"
        f"  - Ancienneté : {annees_anciennete} ans\n"
        f"  - Montant : {indemnite:.2f} €\n"
        f"  (Article L1234-9 du Code du Travail)"
    )


# ─── Outil 3 : Recherche web (jurisprudence) ────────────────────────────────

@tool
def recherche_jurisprudence(query: str) -> str:
    """
    Recherche des informations juridiques récentes sur le web.
    Utile pour la jurisprudence, les actualités du droit du travail,
    ou des questions dépassant le contenu des PDFs.
    Paramètre : question ou mots-clés à rechercher
    """
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(
                f"droit du travail France {query}",
                max_results=3
            ))
        if not results:
            return "Aucun résultat trouvé."
        output = f"Résultats pour '{query}' :\n\n"
        for r in results:
            output += f"• {r['title']}\n  {r['body'][:200]}...\n  Source : {r['href']}\n\n"
        return output
    except ImportError:
        return "Module duckduckgo_search non installé. Faire : pip install duckduckgo-search"
    except Exception as e:
        return f"Erreur de recherche : {str(e)}"


# ─── Création de l'agent ─────────────────────────────────────────────────────

TOOLS = [calculatrice_juridique, calcul_indemnite_licenciement, recherche_jurisprudence]

AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Tu es un assistant juridique spécialisé en droit du travail français.
Tu as accès à des outils pour :
- Effectuer des calculs (indemnités, préavis, salaires)
- Calculer l'indemnité légale de licenciement
- Rechercher des informations juridiques récentes

Utilise les outils quand c'est pertinent. Réponds toujours en français.
Cite les articles du Code du Travail quand tu les connais."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])


def get_agent_executor():
    """Crée et retourne l'agent avec ses outils"""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent = create_tool_calling_agent(llm, TOOLS, AGENT_PROMPT)
    return AgentExecutor(agent=agent, tools=TOOLS, verbose=True)


if __name__ == "__main__":
    executor = get_agent_executor()

    # Tests
    tests = [
        "Calcule l'indemnité de licenciement pour un salaire de 3000€ et 7 ans d'ancienneté.",
        "Quelle est la jurisprudence récente sur le télétravail ?",
        "Combien vaut 35 * 52 * 1.25 ?",
    ]
    for question in tests:
        print(f"\n{'='*60}")
        print(f"Question : {question}")
        result = executor.invoke({"input": question})
        print(f"Réponse : {result['output']}")
