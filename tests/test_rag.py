"""
Tests unitaires — Assistant Juridique RAG
Lancer avec : pytest tests/
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestCalculatriceJuridique:
    """Tests pour l'outil calculatrice"""

    def test_calcul_simple(self):
        from agents import calculatrice_juridique
        result = calculatrice_juridique.invoke("2500 * 5 * 0.25")
        assert "3125" in result

    def test_calcul_indemnite(self):
        from agents import calcul_indemnite_licenciement
        # 5 ans, 2000€/mois → 5 * 2000 * 0.25 = 2500€
        result = calcul_indemnite_licenciement.invoke({
            "salaire_mensuel": 2000.0,
            "annees_anciennete": 5.0
        })
        assert "2500" in result

    def test_anciennete_insuffisante(self):
        from agents import calcul_indemnite_licenciement
        result = calcul_indemnite_licenciement.invoke({
            "salaire_mensuel": 2000.0,
            "annees_anciennete": 0.5
        })
        assert "insuffisante" in result.lower()

    def test_plus_de_10_ans(self):
        from agents import calcul_indemnite_licenciement
        # 12 ans, 3000€ → 10*3000*0.25 + 2*3000*(1/3) = 7500 + 2000 = 9500
        result = calcul_indemnite_licenciement.invoke({
            "salaire_mensuel": 3000.0,
            "annees_anciennete": 12.0
        })
        assert "9500" in result


class TestRouteur:
    """Tests pour le routeur (nécessite la clé API)"""

    @pytest.mark.skipif(
        not os.environ.get("OPENAI_API_KEY"),
        reason="Clé OpenAI non configurée"
    )
    def test_route_salutation(self):
        from router import router_chain
        result = router_chain.invoke({"question": "Bonjour !"})
        assert "LLM" in result.upper()

    @pytest.mark.skipif(
        not os.environ.get("OPENAI_API_KEY"),
        reason="Clé OpenAI non configurée"
    )
    def test_route_calcul(self):
        from router import router_chain
        result = router_chain.invoke({
            "question": "Calcule mon indemnité de licenciement"
        })
        assert "AGENT" in result.upper()
