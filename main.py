from src.tool.tool import tool
from src.adapters.integrations.ollama_adapter import OllamaAdapter
from src.agents.agent import LilyAgent
from pydantic import BaseModel, Field

import httpx
from typing import Dict

class WeatherModel(BaseModel):
    name: str = Field(description="Name of the city, state, or country to fetch weather information for (e.g., 'Chennai', 'India')")

@tool(name="get_weather", description="Fetch weather for a location. If location is not provided, you MUST first call get_location tool.", parameters=WeatherModel)
def get_weather(name: str) -> Dict:
    """
    Get current weather data for a given location.

    Args:
        name (str): Name of the city, state, or country (e.g., 'Chennai').

    Returns:
        dict: Contains temperature, windspeed, and weather condition.
    """

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_res = httpx.get(geo_url, params={"name": name, "count": 1}).json()

    if "results" not in geo_res:
        return {"error": f"Location '{name}' not found"}

    lat = geo_res["results"][0]["latitude"]
    lon = geo_res["results"][0]["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_res = httpx.get(
        weather_url,
        params={
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }
    ).json()

    return weather_res.get("current_weather", {})

@tool(
    name="get_location",
    description=(
        "Retrieves the user's approximate current location based on their public IP address. "
        "Returns country, region/state, city, latitude, longitude, timezone, and ISP information. "
        "This is not GPS-based and may be inaccurate for fine-grained positioning."
    ))
def get_location() -> Dict:
    try:
        response = httpx.get("http://ip-api.com/json", timeout=5.0)
        response.raise_for_status()
        data = response.json()

        return {
            "success": True,
            "ip": data.get("query"),
            "country": data.get("country"),
            "country_code": data.get("countryCode"),
            "region": data.get("regionName"),
            "city": data.get("city"),
            "zip": data.get("zip"),
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
            "timezone": data.get("timezone"),
            "isp": data.get("isp"),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

agent = LilyAgent(
            OllamaAdapter("qwen2.5:7b"), 
            tools=[get_weather, get_location], 
            role="You are an intelligent assistant that can answer questions and use tools when needed", 
            prompt="You are a weather assistant that provides accurate weather information. You can use tools to fetch real-time data when required.", 
            max_iter=10
    )

while True:
    print(agent.run(input("Enter an prompt: ")))