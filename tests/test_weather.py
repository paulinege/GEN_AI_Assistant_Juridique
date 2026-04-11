from src.tools.weather import get_weather


def test_weather_missing_city():
    result = get_weather("")
    assert result["status"] == "error"