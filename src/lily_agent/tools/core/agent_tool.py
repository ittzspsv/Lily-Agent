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

    def execute_sync(self, tool_args: dict, runtime_args: dict) -> str:
        input_ = tool_args["input"]

        return self.agent.run_sync(
            str(input_),
            **runtime_args
        )
    
    
    async def execute(self, tool_args: dict, runtime_args: dict) -> str:
        input_ = tool_args["input"]
        return await self.agent.run(str(input_), **runtime_args)
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        schema = AgentToolInput.model_json_schema()
        schema.pop("title", None)
        for prop in schema.get("properties", {}).values():
            prop.pop("title", None)
        return schema