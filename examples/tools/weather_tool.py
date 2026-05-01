from lily_agent import LilyAgent, tool
from lily_agent.adapters import OllamaAdapter
from pydantic import BaseModel, Field

agent = LilyAgent(
    adapter=OllamaAdapter(model="qwen2.5:7b"),
    role = "You are an supportive agent",
    prompt = "Use available tools when needed to complete tasks accurately"
)

class Weather(BaseModel):
    city: str = Field(..., description="The name of the city / place provided by the user") # Detailed description of the parameter

import httpx



@tool(description="Get weather information of the given city", parameters=Weather) # Pass in your pydantic model as parameters argument
def get_weather(city: str) -> str | dict:
    """ We first need to get the city coordinates using geographic api """
    with httpx.Client(timeout=30.0) as client:
        geo_response = client.get(
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

        weather_response = client.get(
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
    
agent.register_tool(get_weather)
print(agent.run_sync("What is the weather in new york."))
