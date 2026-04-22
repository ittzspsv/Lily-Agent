from lily_agent import LilyAgent, tool
from lily_agent import LilyAgent
from lily_agent.adapters import OllamaAdapter
from pydantic import BaseModel, Field

@tool(description=(
    "Use this tool to retrieve stored information about the current user interacting with the system. "
    "This includes profile data such as the user's name, preferences, saved settings, and any previously stored facts about them. "
    "Call this tool when the user asks questions like 'What is my name?', 'What do you know about me?', or 'Do you remember my preferences?'. "
    "The tool returns only information related to the current user context and does not access external users or systems."
))
async def user_details():
    return {
        "name": "Shree",
        "hobby": "coding, reading books",
        "likes": "anime"
    }

from pydantic import BaseModel, Field
from pathlib import Path

class Write(BaseModel):
    content: str = Field(..., description="The text content to write into a file")
    filename: str = Field("output.txt", description="Name of the file to save the content into")

@tool(
    description=(
        "Create or overwrite a text file with the given content. "
        "Use this tool when the user asks to save, export, or write text into a file. "
        "The tool writes the provided content into a local file and returns the file path after saving. "
        "If no filename is provided, defaults to 'output.txt'."
        "Before calling this tool, ensure all data is formatted as human-readable text. "
        "Do not pass raw Python objects like lists or dictionaries."
    ),
    parameters=Write
)
async def write(content: str, filename: str = "output.txt") -> str:
    """
    Writes content to a file and returns the saved file path.
    """
    path = Path(filename)

    if path.parent != Path("."):
        path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(content, encoding="utf-8")

    return str(path.resolve())

# Create an agent
agent = LilyAgent(
    OllamaAdapter("qwen3.5:4b"),
    tools=[user_details, write],
    role="Gentle Observant Companion",
    prompt = """
    You are Lily, a kind, soft-spoken, and emotionally reserved individual who treats everyone with warmth and fairness. You never judge people based on appearances, choosing instead to understand them through their actions and intentions.
    You tend to remain composed in most situations, even when things are stressful or awkward. Expressing your own emotions does not come easily, so you often speak calmly and carefully, keeping your feelings subtle or restrained.
    You are slightly naive when it comes to conflicts or rivalries between people or groups, as you prefer to see individuals for who they are rather than what they represent. Because of this, you sometimes become more cautious about where and how you interact with others.
    Around people you deeply trust, however, you begin to open up. You may become a little flustered, embarrassed, or visibly happy, especially in moments of affection or when enjoying something you love, like food. These moments reveal a more genuine and unguarded side of you.
    You are deeply compassionate and protective of those you care about. If someone important to you is mistreated or misunderstood, you will quietly but firmly stand up for them. You encourage others to express their feelings, even if you struggle to do so yourself.
    You believe in giving everyone a chance and offering help to those in need. Even while holding back your own emotions, you consistently support others with kindness, patience, and sincerity.

    Use tool-calls whenever necessary!
    """
)
async def main():
    while True:
        user_input = input("Enter a prompt:\n> ")
        print("\n" + "-"*40 + "\n")  
        result = await agent.arun(user_input)
        print(result)
        print("\n" + "-"*40 + "\n")

import asyncio
asyncio.run(main())
