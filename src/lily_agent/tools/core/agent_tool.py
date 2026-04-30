# agent_tool.py

from __future__ import annotations
from typing import TYPE_CHECKING
from ..base.tool_base import Tool

from typing import Dict, Any

if TYPE_CHECKING:
    from ...agents.integrations.agent import LilyAgent

from .agent_classes import AgentToolInput

class AgentTool(Tool):
    def __init__(self, name: str, agent: "LilyAgent", description: str):
        super().__init__(
            name=name,
            description=description,
        )
        
        self.agent = agent

    def execute_sync(self, **kwargs) -> str:
        input_ = kwargs["input"]
        return self.agent.run_sync(str(input_))
    
    
    async def execute(self, **kwargs) -> str:
        input_ = kwargs["input"]
        return await self.agent.run(str(input_))
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        schema = AgentToolInput.model_json_schema()
        schema.pop("title", None)
        for prop in schema.get("properties", {}).values():
            prop.pop("title", None)
        return schema