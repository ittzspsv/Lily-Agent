from typing import Optional

from ..agent import AgentBase
from ...adapters.adapter import AgentAdapter
from ...schemas.message import Message
from ...exceptions.agent import AgentError
from ...schemas import User, LLMResponse, MessageRole
from ...configs.prompts import FACT_RETRIEVAL_ROLE, FACT_RETRIEVER_PROMPT

class FactRetriever(AgentBase):
    def __init__(self, adapter: AgentAdapter) -> None:

        self.role = FACT_RETRIEVAL_ROLE
        self.prompt = FACT_RETRIEVER_PROMPT

        super().__init__(adapter=adapter, role=self.role, prompt=self.prompt, name=None, key=None)

    async def run(
        self,
        query: str,
        user: Optional[User] = None,
        **kwargs,
    ) -> LLMResponse:
        response = await self.adapter.complete(
            messages=[
                Message(role=MessageRole.System, content=self.me.system_prompt),
                Message(role=MessageRole.User, content=query),
            ],
            tools=[],
        )

        if response.content is None:
            raise AgentError("Failed to generate response")

        return response