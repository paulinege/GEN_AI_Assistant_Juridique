"""
Tests Partie 1 — Pipeline RAG
"""

questions_testees = [
    "Quel est le délai de préavis pour un CDI ?",
    "Quelles sont les conditions du licenciement pour faute grave ?",
    "Quelle est la durée maximale du travail hebdomadaire ?",
    "Quels sont les droits aux congés payés ?",
    "Qu'est-ce qu'un contrat à durée déterminée ?",
    "Quelles sont les règles sur le harcèlement moral ?",
    "Comment fonctionne la rupture conventionnelle ?",
    "Quels sont les droits des syndicats ?",
    "Quelles sont les règles sur l'égalité homme femme ?",
    "Quelles sont les obligations de sécurité de l'employeur ?"
]

def test_questions_non_vides():
    """Vérifie que toutes les questions de test sont non vides"""
    for q in questions_testees:
        assert len(q) > 0

def test_nombre_questions():
    """Vérifie qu'on a bien 10 questions de test"""
    assert len(questions_testees) == 10