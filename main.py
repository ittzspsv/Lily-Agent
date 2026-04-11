from src.adapters.integrations.ollama_adapter import OllamaAdapter
from src.agents.agent import LilyAgent

# Create an agent
agent = LilyAgent(OllamaAdapter("qwen2.5:7b")) # We use OLLAMA qwen2.5:7b Model

# Run the agent
while True:
    print(agent.run(input("Enter an prompt: ")))