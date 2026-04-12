from pathlib import Path
from unittest.mock import patch

import pytest

from src.tools import (
    safe_eval_math,
    calculatrice_juridique,
    todo_dossier_local,
    meteo_ville,
    recherche_web_juridique,
)


def test_safe_eval_math_ok():
    assert safe_eval_math("(1200 * 0.1) + 300") == 420.0


def test_safe_eval_math_rejects_unsafe_code():
    with pytest.raises(ValueError):
        safe_eval_math("__import__('os').system('echo hacked')")


def test_calculatrice_juridique():
    out = calculatrice_juridique("100 + 25 * 2")
    assert "150" in out


def test_todo_cycle():
    todo_file = Path("todo_juridique.json")
    if todo_file.exists():
        todo_file.unlink()

    add_output = todo_dossier_local("ajouter", "vérifier la compétence territoriale")
    list_output = todo_dossier_local("lister")
    del_output = todo_dossier_local("supprimer", "vérifier la compétence territoriale")

    assert "ajouté" in add_output.lower()
    assert "compétence territoriale" in list_output.lower()
    assert "supprimé" in del_output.lower()


@patch("src.tools.fetch_weather")
def test_meteo_ville_mocked(mock_weather):
    mock_weather.return_value = {
        "weather": [{"description": "ciel dégagé"}],
        "main": {"temp": 21.5, "feels_like": 22.0, "humidity": 40},
    }
    output = meteo_ville("Paris")
    assert "Paris" in output
    assert "21.5" in output


@patch("src.tools.tavily_search")
def test_recherche_web_juridique_mocked(mock_search):
    mock_search.return_value = {
        "answer": "Une réforme récente a été annoncée.",
        "results": [
            {
                "title": "Actualité juridique",
                "url": "https://example.com/reforme",
                "content": "Le ministère a publié une mise à jour de la procédure..."
            }
        ],
    }
    output = recherche_web_juridique("réforme récente procédure civile")
    assert "Résumé web" in output
    assert "Sources" in output