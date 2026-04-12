import requests
from src.config.setting import settings
from src.schemas.tool_outputs import build_tool_response


def get_weather(city: str):
    try:
        if not city or not city.strip():
            raise ValueError("City name is required")

        city_clean = city.strip().title()

        if settings.OPENWEATHER_API_KEY:
            try:
                url = "https://api.openweathermap.org/data/2.5/weather"
                params = {
                    "q": city_clean,
                    "appid": settings.OPENWEATHER_API_KEY,
                    "units": "metric",
                    "lang": "fr",
                }
                response = requests.get(url, params=params, timeout=settings.WEATHER_TIMEOUT)
                response.raise_for_status()
                data = response.json()

                return build_tool_response(
                    tool_name="weather",
                    status="success",
                    input_data={"city": city_clean},
                    output_data={
                        "city": city_clean,
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"],
                        "humidity": data["main"]["humidity"],
                        "source": "api",
                    },
                )
            except Exception:
                pass

        mock_weather = {
            "Paris": {"temperature": 18, "description": "ciel dégagé"},
            "Lyon": {"temperature": 20, "description": "ensoleillé"},
            "Marseille": {"temperature": 24, "description": "chaud et sec"},
        }

        data = mock_weather.get(
            city_clean,
            {"temperature": 22, "description": "données simulées indisponibles pour cette ville"},
        )

        return build_tool_response(
            tool_name="weather",
            status="success",
            input_data={"city": city_clean},
            output_data={
                "city": city_clean,
                "temperature": data["temperature"],
                "description": data["description"],
                "source": "mock",
            },
        )
    except Exception as e:
        return build_tool_response(
            tool_name="weather",
            status="error",
            input_data={"city": city},
            error=str(e),
        )