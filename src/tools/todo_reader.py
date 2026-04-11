import json
from pathlib import Path
from src.config.setting import settings
from src.schemas.tool_outputs import build_tool_response


def read_todos(date: str | None = None):
    try:
        todo_path = Path(settings.TODO_FILE_PATH)

        if not todo_path.exists():
            raise FileNotFoundError(f"Todo file not found: {todo_path}")

        with open(todo_path, "r", encoding="utf-8") as f:
            todos = json.load(f)

        if date:
            todos = [item for item in todos if item.get("date") == date]

        return build_tool_response(
            tool_name="todo_reader",
            status="success",
            input_data={"date": date},
            output_data={"todos": todos},
        )
    except Exception as e:
        return build_tool_response(
            tool_name="todo_reader",
            status="error",
            input_data={"date": date},
            error=str(e),
        )