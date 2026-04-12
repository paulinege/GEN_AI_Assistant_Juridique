from src.router import classify_query


def test_classify_query_rag():
    assert classify_query("Selon le PDF du code civil, que dit l'article 1240 ?") == "rag"


def test_classify_query_tool():
    assert classify_query("Quel temps fait-il à Marseille aujourd'hui ?") == "tool"


def test_classify_query_chat():
    assert classify_query("Bonjour maître") == "chat"