# tool_base.py

from abc import ABC, abstractmethod
from typing import Any, Dict

class Tool(ABC):
    """
    ### Definition
    Base Class for defining a tool.
    - This Class wraps a callable function and converts that into a structured tool with JSON Schema
    - This can be reused for AI

    ### Constructor
    - **name**: `str` (name of the tool)
    - **description**: `Optional[str]` ((description of what the tool does and when it should be used)
    """
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        raise NotImplementedError

    @abstractmethod
    def execute_sync(self, **kwargs) -> Any:
        raise NotImplementedError


    @property
    def input_schema(self) -> Dict[str, Any]:
        return {} 