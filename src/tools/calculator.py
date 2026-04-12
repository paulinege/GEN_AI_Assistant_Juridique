import operator
from src.schemas.tool_outputs import build_tool_response

ALLOWED_OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "**": operator.pow,
}


def calculate(a: float, b: float, op: str):
    try:
        if op not in ALLOWED_OPERATORS:
            raise ValueError(f"Unsupported operator: {op}")
        if op == "/" and b == 0:
            raise ValueError("Division by zero is not allowed")

        result = ALLOWED_OPERATORS[op](a, b)

        return build_tool_response(
            tool_name="calculator",
            status="success",
            input_data={"a": a, "b": b, "op": op},
            output_data={"result": result},
        )
    except Exception as e:
        return build_tool_response(
            tool_name="calculator",
            status="error",
            input_data={"a": a, "b": b, "op": op},
            error=str(e),
        )