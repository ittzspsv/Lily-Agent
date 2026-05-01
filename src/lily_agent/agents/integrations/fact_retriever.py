from typing import Optional

from ..core.agent_base import AgentBase
from ...adapters.core.adapter import AgentAdapter
from ...adapters.core.adapter_classes import Message
from ..errors.agent_exceptions import AgentError

from ...configs.prompts import FACT_RETRIEVAL_ROLE, FACT_RETRIEVER_PROMPT

class FactRetriever(AgentBase):
    def __init__(self, adapter: AgentAdapter) -> None:

        self.role = FACT_RETRIEVAL_ROLE
        self.prompt = FACT_RETRIEVER_PROMPT

        super().__init__(adapter=adapter, role=self.role, prompt=self.prompt, name=None, key=None)

    async def run(self, query: str, user_id: Optional[str]=None) -> str:
        response = await self.adapter.complete(messages=[Message(role="system", content=self.system_prompt), Message(role="user", content=query)], tools=[])
        if response.content is not None:
            return response.content
        
        raise AgentError("Failed to generate response")