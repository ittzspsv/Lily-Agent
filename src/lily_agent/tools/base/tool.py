from typing import Callable, Type, Optional
from pydantic import BaseModel
from ..core.function_tool import FunctionTool


def tool(name: Optional[str]=None, description: Optional[str] = None, parameters: Optional[Type[BaseModel]]=None):
    def decorator(func: Callable):
        return FunctionTool(func=func, name=name,description=description, parameters=parameters)
    return decorator