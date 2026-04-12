<div align="center" style="display: flex; align-items: center; justify-content: center; gap: 16px;">
  <img src=".github/images/Chiaki.png" width="80" />
  <h1 style="margin: 0;">Lily Agent</h1>
</div>



A lightweight minimal python framework for building modular LLM-powered AI agents.

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue" />
</p>

## Installation
### venv
```
python -m venv .venv

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install lily-agent
```

## Quick Start
Get started by running your first AI Agent.  
```python
from lily_agent import LilyAgent
from lily_agent.adapters import OllamaAdapter

# Create an agent
agent = LilyAgent(
    adapter=OllamaAdapter("qwen2.5:7b")
)  

# Run the agent
while True:
    print(agent.run(input("Enter a prompt: ")))
```
Defining a tool and making tool calls

```python
from lily_agent import LilyAgent, tool

# Define a simple tool
@tool(description="Retrieve basic user information such as name, preferences, or profile details.")
def user_details():
    return {
        "name" : "shree",
        "hobby" : ["coding", "reading books"]
    }

# Create an agent
agent = LilyAgent(
    OllamaAdapter("qwen2.5:7b"),
    tools=[user_details]
)

print(agent.run("What do you know about me?"))
```

### Documentation
Work in progress....

> **Note:** Package not yet released on PyPI. Stay tuned!
>
> Work in progress
