import requests
from src.config.setting import settings
from src.schemas.tool_outputs import build_tool_response


def get_weather(city: str):
    try:
        if not city or not city.strip():
            raise ValueError("City name is required")

        if not settings.OPENWEATHER_API_KEY:
            return build_tool_response(
                tool_name="weather",
                status="error",
                input_data={"city": city},
                error="Missing OPENWEATHER_API_KEY",
            )

        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "fr",
        }

        response = requests.get(url, params=params, timeout=settings.WEATHER_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        output = {
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
        }

        return build_tool_response(
            tool_name="weather",
            status="success",
            input_data={"city": city},
            output_data=output,
        )
    except Exception as e:
        return build_tool_response(
            tool_name="weather",
            status="error",
            input_data={"city": city},
            error=str(e),
        )