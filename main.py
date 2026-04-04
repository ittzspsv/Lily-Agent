from src.tools.tool import tool
from pydantic import BaseModel, Field
from src.tool_builder.tool_builder import ToolBuilder


class WeatherInformation(BaseModel):
    location: str = Field(description="Location of that area")
    latitude: int = Field(description="Latitude of that area")
    longitude: int = Field(description="Longitude of that area")
    

class WeatherAgentTools(ToolBuilder):
    def __init__(self) -> None:
        super().__init__()
    
    @tool(description="Gets Weather Information")
    def get_weather_information(self, location: int, latitude: int, longitude: int):
        pass

tools = WeatherAgentTools()
print(tools.schemas)