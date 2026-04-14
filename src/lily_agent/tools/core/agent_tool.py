from __future__ import annotations
from typing import TYPE_CHECKING
from ..base.tool_base import Tool

from typing import Dict, Any

if TYPE_CHECKING:
    from ...agents.agent import LilyAgent

from .agent_classes import AgentToolInput

class AgentTool(Tool):
    def __init__(self, name: str, agent: "LilyAgent", description: str):
        super().__init__(
            name=name,
            description=description,
        )
        
        self.agent = agent

    def execute(self, **kwargs) -> str:
        input_ = kwargs["input"]
        result = self.agent.run(str(input_))
        return result
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return AgentToolInput.model_json_schema()