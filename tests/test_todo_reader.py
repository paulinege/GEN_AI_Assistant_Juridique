import json
from src.tools.todo_reader import read_todos


def test_read_todos_all(tmp_path, monkeypatch):
    todo_file = tmp_path / "todo.json"
    todo_file.write_text(
        json.dumps(
            [
                {"title": "Faire rapport", "date": "2026-04-12", "status": "open"},
                {"title": "Réviser cours", "date": "2026-04-13", "status": "done"},
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr("src.tools.todo_reader.settings.TODO_FILE_PATH", str(todo_file))
    result = read_todos()

    assert result["status"] == "success"
    assert len(result["output"]["todos"]) == 2


def test_read_todos_filtered(tmp_path, monkeypatch):
    todo_file = tmp_path / "todo.json"
    todo_file.write_text(
        json.dumps(
            [
                {"title": "Faire rapport", "date": "2026-04-12", "status": "open"},
                {"title": "Réviser cours", "date": "2026-04-13", "status": "done"},
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr("src.tools.todo_reader.settings.TODO_FILE_PATH", str(todo_file))
    assert result["output"]["todos"][0]["title"] == "Faire rapport"