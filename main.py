from lily_agent import LilyAgent
from lily_agent.adapters import OllamaAdapter
from lily_agent import tool

# Define a simple tool
@tool(description="Retrieve basic user information such as name, preferences, or profile details.")
def user_details():
    return {
        "name" : "shree",
        "hobby" : ["loves coding", "loves hearing stories..."],
    }

# Create an agent
agent = LilyAgent(
    adapter=OllamaAdapter("qwen2.5:7b"),
    tools=[user_details],
    role="",
    prompt=""
)

print(agent.run("What do you know about me?"))