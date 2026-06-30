from lily_agent import LilyAgent, tool
from lily_agent.adapters import OllamaAdapter
from pydantic import BaseModel, Field
import httpx


class Weather(BaseModel):
    city: str = Field(..., description="The name of the city / place provided by the user") # Detailed description of the parameter


@tool(description="Get weather information of the given city", parameters=Weather) # Pass in your pydantic model as parameters argument
async def get_weather(city: str) -> str | dict:
    """ We first need to get the city coordinates using geographic api """
    async with httpx.AsyncClient(timeout=30.0) as client:
        geo_response = await client.get(
            url="https://geocoding-api.open-meteo.com/v1/search",
            params = {
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            }
        )

        response_data = geo_response.json()
        if not response_data.get("results"):
            raise ValueError(f"City '{city}' not found.")
        
        location = response_data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]

        """ We then use that coordinates to fetch weather data. """

        weather_response = await client.get(
            url="https://api.open-meteo.com/v1/forecast",
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": True
            }
        )

        response_data = weather_response.json()
        return {
            "city": location["name"],
            "country": location["country"],
            "latitude": latitude,
            "longitude": longitude,
            "weather": response_data.get("current_weather", {})
        }