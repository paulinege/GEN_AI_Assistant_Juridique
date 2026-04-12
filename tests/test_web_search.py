from src.tools.web_search import search_web


class DummyDDGS:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def text(self, query, max_results=5):
        return [
            {
                "title": "Résultat 1",
                "href": "https://example.com",
                "body": "Résumé test",
            }
        ]

@patch("src.tools.web_search.DDGS", return_value=DummyDDGS())
def test_web_search_success(_mock_ddgs):
    result = search_web("télétravail en France")
    assert result["status"] == "success"
    assert len(result["output"]["results"]) == 1
    assert result["output"]["results"][0]["title"] == "Résultat 1"


def test_web_search_empty_query():
    result = search_web("")
    assert result["status"] == "error"