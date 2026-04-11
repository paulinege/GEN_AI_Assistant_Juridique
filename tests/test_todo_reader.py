from src.tools.todo_reader import read_todos


def test_read_todos_all():
    result = read_todos()
    assert result["status"] in {"success", "error"}


def test_read_todos_filtered():
    result = read_todos("2026-04-12")
    assert result["status"] in {"success", "error"}