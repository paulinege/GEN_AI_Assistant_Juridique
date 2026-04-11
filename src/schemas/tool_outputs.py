from typing import Any, Dict, Optional


def build_tool_response(
    tool_name: str,
    status: str,
    input_data: Dict[str, Any],
    output_data: Optional[Any] = None,
    error: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "tool_name": tool_name,
        "status": status,
        "input": input_data,
        "output": output_data,
        "error": error,
    }