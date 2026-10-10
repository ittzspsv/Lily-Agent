from typing import Callable, Type, Optional
from pydantic import BaseModel
from .function_tool import FunctionTool


def tool(
        name: Optional[str]=None, 
        description: Optional[str] = None, 
        parameters: Optional[Type[BaseModel]]=None,
        describe_template: Optional[str] = None,
        overload: bool = False
    ):
    def decorator(func: Callable):
        return FunctionTool(
            func=func, 
            name=name,
            description=description, 
            parameters=parameters, 
            describe_template=describe_template,
            overload=overload
        )
    return decorator