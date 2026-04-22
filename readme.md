<div align="center" style="display: flex; align-items: center; justify-content: center; gap: 16px;">
  <img src=".github/images/Chiaki.png" width="80" />
  <h1 style="margin: 0;">Lily Agent</h1>
</div>



A lightweight python framework for building modular LLM-powered AI agents.

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.8-pink" />
</p>

## Installation
### venv
```bash
python -m venv .venv

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

git clone https://github.com/ittzspsv/lily-agent.git

cd lily-agent

pip install -e .
```

## Quick Start
Get started by running your first AI agent. 

**Synchronous version**
```python
from lily_agent import LilyAgent
from lily_agent.adapters import OllamaAdapter

# Create an agent
agent = LilyAgent(
    adapter=OllamaAdapter("qwen2.5:7b")
)  

# Run the agent
while True:
    print(agent.run_sync(input("Enter a prompt: ")))
```

**Asynchronous Version**
```python
from lily_agent import LilyAgent
from lily_agent.adapters import OllamaAdapter
import asyncio

# Create an agent
agent = LilyAgent(
    adapter=OllamaAdapter("qwen2.5:7b")
)

async def main():
    while True:
        response = await agent.run(input("Enter a prompt: "))

        print(response)

asyncio.run(main())

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

print(agent.run_sync("What do you know about me?"))
```


### Why Lily-Agent over other options
- Minimal abstraction
- Easier to learn, if you are new to developing Ai Agents (code based)
- Both sync/async support 
- Easy integration with local models (ollama)



### Documentation
Work in progress....

> **Note:** Package not yet released on PyPI. Stay tuned!
>
> Work in progress
