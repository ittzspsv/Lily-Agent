from typing import Callable, Type, Optional
from pydantic import BaseModel
from .tool_base import Tool


def tool(description: Optional[str] = None, parameters: Optional[Type[BaseModel]]=None, strict: bool=True):
    def decorator(func: Callable):
        return Tool(func=func, description=description, parameters=parameters)
    return decorator