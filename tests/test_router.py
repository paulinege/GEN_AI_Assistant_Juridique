from src.agents.router import route_query, extract_city

def test_extract_city_paris():
    city = extract_city("Quelle est la météo à Paris ?")
    assert city.lower() == "paris"

def test_router_weather():
    result = route_query("Quelle est la météo à Paris ?")
    assert result["tool_name"] == "weather"


def test_router_todo():
    result = route_query("Montre mes tâches pour 2026-04-12")
    assert result["tool_name"] == "todo_reader"


def test_router_web_search():
    result = route_query("Cherche sur le web les dernières infos sur le télétravail")
    assert result["tool_name"] == "web_search"


def test_router_calculator():
    result = route_query("2 + 2")
    assert result["tool_name"] == "calculator"