from src.tools.web_search import search_web


def test_web_search_empty_query():
    result = search_web("")
    assert result["status"] == "error"

def test_web_search_valid_query_structure():
    result = search_web("télétravail en France")
    assert result["tool_name"] == "web_search"
    assert result["status"] in {"success", "error"}