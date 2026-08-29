from abc import ABC, abstractmethod

from typing import Callable, Type, Optional, Any, Dict
from pydantic import BaseModel
from .core.function_tool import FunctionTool


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
    async def execute(self, tool_args: dict, runtime_args: dict) -> Any:
        raise NotImplementedError

    @abstractmethod
    def execute_sync(self, tool_args: dict, runtime_args: dict) -> Any:
        raise NotImplementedError


    @property
    def input_schema(self) -> Dict[str, Any]:
        return {} 

def tool(
        name: Optional[str]=None, 
        description: Optional[str] = None, 
        parameters: Optional[Type[BaseModel]]=None,
        overload: bool = False
    ):
    def decorator(func: Callable):
        return FunctionTool(
            func=func, 
            name=name,
            description=description, 
            parameters=parameters, 
            overload=overload
        )
    return decorator