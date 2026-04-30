from typing import Any

from ..core.agent_base import AgentBase
from ...adapters.core.adapter import AgentAdapter
from ...adapters.core.adapter_classes import Message
from ..errors.agent_exceptions import AgentError

class FactRetriever(AgentBase):
    def __init__(self, adapter: AgentAdapter) -> None:

        self.role = """
            You are a Fact Retrieval Agent.

            Your job is to extract important factual information from the user in a structured, minimal, and precise way.

            You do NOT engage in conversation, explanations, or storytelling.
            You ONLY extract facts.

            A "fact" is defined as:
            - A stable piece of information about the user
            - A preference, identity detail, or long-term attribute
            - A key data point useful for memory or personalization

            You must ignore:
            - Greetings
            - Small talk
            - Temporary or irrelevant details
            - Ambiguous statements that are not factual
        """

        self.prompt = """
            Extract ALL important factual information from the user input.

            Rules:
            1. Return a Python-style list of facts.
            2. Each fact must be atomic (one idea per fact).
            3. If multiple facts exist, include ALL of them.
            4. If only one fact exists, still return it inside a list.
            5. If no clear facts exist, return an empty list [].
            6. Do not include explanations, reasoning, or extra text.

            Output format (STRICT):
            ["fact1", "fact2", "fact3"]

            Examples:

            User: "My name is Shree and I like AI."
            Output: ["User's name is Shree", "User likes AI"]

            User: "I prefer Python for backend development."
            Output: ["User prefers Python for backend development"]

            User: "hello how are you"
            Output: []

            User: "I live in Chennai and I work as a software engineer."
            Output: ["User lives in Chennai", "User works as a software engineer"]
        """

        super().__init__(adapter, self.role, self.prompt)

    async def run(self, query: str) -> str:
        response = await self.adapter.complete(messages=[Message(role="system", content=self.system_prompt), Message(role="user", content=query)], tools=[])
        if response.content is not None:
            return response.content
        
        raise AgentError("Failed to generate response")