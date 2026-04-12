def classify_query(query: str) -> str:
    q = query.lower()

    rag_patterns = [
        "selon le pdf",
        "dans le document",
        "dans le code",
        "dans la loi",
        "article ",
        "texte de loi",
        "fichier pdf",
        "dans le corpus",
        "selon le corpus",
    ]

    tool_patterns = [
        "calcule",
        "calcule-moi",
        "pourcentage",
        "intérêt",
        "pénalité",
        "météo",
        "temps à",
        "fait-il à",
        "aujourd'hui",
        "jurisprudence récente",
        "actualité juridique",
        "réforme récente",
        "todo",
        "checklist",
        "liste ma todo",
    ]

    if any(p in q for p in rag_patterns):
        return "rag"
    if any(p in q for p in tool_patterns):
        return "tool"
    return "chat"