from typing import Callable, Type, Optional
from pydantic import BaseModel
from .tool_base import Tool


def tool(name: Optional[str]=None, description: Optional[str] = None, parameters: Optional[Type[BaseModel]]=None):
    def decorator(func: Callable):
        return Tool(func=func, name=name,description=description, parameters=parameters)
    return decorator