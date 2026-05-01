# Agent Tools
- An tool is a function that the LLM can use to perform tasks beyond generating text. 
- A Tool Can be Anything.  For example
  - weather_tool => a function that is capable of **extracting weather** information and returns the output
  - web_search_tool => a function that is capable of **searching the web** for information
  - email_tool => a tool that sends **email**

  ## Tool Creation
  - Defining a tool is straightforward. 
    1. You simply declare a decorator over a function
    2. Register the tool to an particular agent.
  - The agent can invoke the tool whenever it's necessary.

### Prerequisites
- Let us first create an agent to work with
```python
from lily_agent import LilyAgent
from lily_agent.adapters import OllamaAdapter

agent = LilyAgent(
    adapter=OllamaAdapter(model="qwen2.5:7b"),
    role = "You are an supportive agent",
    prompt = "Use available tools when needed to complete tasks accurately"
)

print(agent.run_sync("Hello!"))
```
- We will use this agent all across our guide.


## Creating a Simple Tool
- Let us create a very simple tool that is capable of returning our personal details.
- The tool decorator takes in
   - name: **str** =>  Name of the tool
   - description: **str** => description of the tool
   - paramters: **pydantic.BaseModel** => A pydantic model to define schemas.

- **name**, **description** and **parameters** are optional, but it's necessary to pass them for high accruacy.
- If **parameters** are not passed as an argument it is crucial for you to define python **type hints** for all the function arguments.
- The function can also be defined any **formal arguments**, if no inputs are required.

### 1. Tool Definition
```python
from lily_agent import tool

@tool(description=("Retrive basic user information such as name preferences or profile details"))
async def user_details():
    return {
        "name": "Shree",
        "hobby": "coding, reading books",
        "likes": "anime"
    }
```
### 2. Registering the tool.
- You can register an tool in 2 ways 
#### 1. while creating an agent.
```python
agent = LilyAgent(
    adapter=OllamaAdapter(model="qwen2.5:7b"),
    role = "You are an supportive agent",
    prompt = "Use available tools when needed to complete tasks accurately",
    tools=[user_details] # Takes in a list of Tools
)
```
#### 2. Registering tools at runtime
```python
agent.register_tool(user_details) # Can also be a list of tools too.
```

## Creating an Structured tool
- Let us define a tool with an pydantic class validation with proper description for each arguments using field.

### 1. Tool Definition
- Let us create a tool that fetches weather from a location.

```python
from pydantic import BaseModel, Field

""" Let us create a pydantic class """
class Weather(BaseModel):
    city: str = Field(..., description="The name of the city / place provided by the user") # Detailed description of the parameter
```
### 2. Tool Implementation
- Let us implement the tool 
```python
import httpx

@tool(description="Get weather information of the given city", parameters=Weather) # Pass in your pydantic model as argument
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
```

### 3. Registering the tool
```python
agent.register_tool(get_weather)
```

### 4. Testing the result.
```python
print(agent.run_sync("What is the weather in new york."))
```

### Final Implementation
- Here is the [final implementation](../../examples/tools/weather_tool.py) for your reference.

## Notes
- Tools can either be async or sync.  If you use an asynchronous tool, ensure your agent also runs asynchronously.