from unittest.mock import patch

from src.agents.executor import run_agent


def _fake_invoke_weather(_payload):
    return {
        "messages": [
            {
                "role": "assistant",
                "tool_calls": [{"name": "weather_tool"}],
                "content": "",
            },
            {
                "role": "assistant",
                "content": "À Paris, il fait 18°C avec un ciel dégagé.",
            },
        ]
    }


def _fake_invoke_calculator(_payload):
    return {
        "messages": [
            {
                "role": "assistant",
                "tool_calls": [{"name": "calculator_tool"}],
                "content": "",
            },
            {
                "role": "assistant",
                "content": "Le résultat est 12.",
            },
        ]
    }


def _fake_invoke_todo(_payload):
    return {
        "messages": [
            {
                "role": "assistant",
                "tool_calls": [{"name": "todo_reader_tool"}],
                "content": "",
            },
            {
                "role": "assistant",
                "content": "Tu as 2 tâches prévues aujourd'hui.",
            },
        ]
    }


@patch("src.agents.executor.AGENT.invoke", side_effect=_fake_invoke_weather)
def test_run_agent_extracts_weather_tool(mock_invoke):
    result = run_agent("Quelle est la météo à Paris ?")

    assert "Paris" in result["answer"]
    assert "weather_tool" in result["used_tools"]
    mock_invoke.assert_called_once()


@patch("src.agents.executor.AGENT.invoke", side_effect=_fake_invoke_calculator)
def test_run_agent_extracts_calculator_tool(mock_invoke):
    result = run_agent("Calcule 5 + 7")

    assert "12" in result["answer"]
    assert "calculator_tool" in result["used_tools"]
    mock_invoke.assert_called_once()


@patch("src.agents.executor.AGENT.invoke", side_effect=_fake_invoke_todo)
def test_run_agent_extracts_todo_tool(mock_invoke):
    result = run_agent("Quelles sont mes tâches du jour ?")

    assert "tâches" in result["answer"]
    assert "todo_reader_tool" in result["used_tools"]
    mock_invoke.assert_called_once()