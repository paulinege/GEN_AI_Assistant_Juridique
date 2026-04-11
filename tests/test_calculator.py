from src.tools.calculator import calculate


def test_calculator_addition():
    result = calculate(2, 3, "+")
    assert result["status"] == "success"
    assert result["output"]["result"] == 5


def test_calculator_division_by_zero():
    result = calculate(10, 0, "/")
    assert result["status"] == "error"
    assert "Division by zero" in result["error"]