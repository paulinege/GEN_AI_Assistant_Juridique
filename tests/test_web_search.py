from src.tools.web_search import search_web


def test_web_search_empty_query():
    result = search_web("")
    assert result["status"] == "error"