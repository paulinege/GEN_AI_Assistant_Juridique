from unittest.mock import patch, Mock
from src.tools.weather import get_weather

@patch("src.tools.weather.requests.get")
def test_weather_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "main": {"temp": 20, "humidity": 40},
        "weather": [{"description": "ciel dégagé"}],
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    with patch("src.tools.weather.settings.OPENWEATHER_API_KEY", "fake_key"):
        result = get_weather("Paris")

    assert result["status"] == "success"
    assert result["output"]["city"] == "Paris"
    assert result["output"]["temperature"] == 20


def test_weather_missing_city():
    result = get_weather("")
    assert result["status"] == "error"