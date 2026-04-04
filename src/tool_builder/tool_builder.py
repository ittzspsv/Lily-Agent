from ..tools.tool import tool
from ..tools.tool_base import Tool

class ToolBuilder:
    """
    Base Class for Defining a tool builder
    - A Tool builder contains a collection of tools that can be passed to an AI Agent base class
    - Each tools contains:
       - Callable function that executes the logic of the tool
       - Schema metadata used for validation
    """
    _tools = {}
    def __init_subclass__(cls) -> None:
        cls._tools = {}

        for name, value in cls.__dict__.items():
            if isinstance(value, Tool):
                cls._tools[name] = value

    def __init__(self) -> None:
        self.tools = [
            tool.func.__get__(self, self.__class__)
            for tool in self._tools.values()
        ]

        self.schemas = [
            tool.schema
            for tool in self._tools.values()
        ]
