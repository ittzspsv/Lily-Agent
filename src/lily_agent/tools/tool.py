from abc import ABC, abstractmethod

from typing import Any, Dict, Optional
from ..configs.prompts import INTENT_DESCRIPTION
from copy import deepcopy


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
    describe_template: Optional[str] = None


    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    async def execute(self, tool_args: dict, runtime_args: dict) -> Any:
        raise NotImplementedError

    @abstractmethod
    def execute_sync(self, tool_args: dict, runtime_args: dict) -> Any:
        raise NotImplementedError


    @property
    def input_schema(self) -> Dict[str, Any]:
        return {} 

    @property
    def llm_input_schema(self) -> Dict[str, Any]:
        schema = deepcopy(self.input_schema)
        schema.setdefault("type", "object")
        props = schema.get("properties", {})


        if "intent" in props:
            raise ValueError(
                f"Tool '{self.name}' defines '{"intent"}', which is reserved for call descriptions"
            )
        
        schema["properties"] = {
            "intent": {"type": "string", "description": INTENT_DESCRIPTION},
            **props,
        }

        schema["required"] = ["intent", *schema.get("required", [])]
        return schema

    def describe(self, tool_args: dict) -> str:
        if self.describe_template:
            try:
                return self.describe_template.format(**tool_args)
            except (KeyError, IndexError, ValueError, AttributeError):
                pass
        return f"Running {self.name}"

