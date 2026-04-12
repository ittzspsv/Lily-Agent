from ..tools.tool_base import Tool
from typing import Dict, Any
from abc import ABC, abstractmethod


class Formatter(ABC):
    @abstractmethod
    def format(self, tool: Tool) -> Dict[str, Any]:
        pass

    def format_many(self, tools: list[Tool]) -> list[Dict[str, Any]]:
        return [self.format(tool) for tool in tools]