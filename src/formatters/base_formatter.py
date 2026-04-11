from .formatter import Formatter
from ..tool.tool_base import Tool
from typing import Dict, Any


class BaseFormatter(Formatter):
    def __init__(self, strict: bool = True) -> None:
        super().__init__()
        self.strict: bool = strict

    def format(self, tool: Tool) -> Dict[str, Any]:
        schema = tool.input_schema.copy()

        if self.strict:
            schema.setdefault("additionalProperties", False)

        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": schema,
            }
        }