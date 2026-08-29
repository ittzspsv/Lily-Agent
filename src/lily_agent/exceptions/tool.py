from typing import List
from pydantic_core import ErrorDetails

class ToolError(Exception):
    """Base exception for all Tool related errors."""
    pass

class ToolValidationError(ToolError):
    def __init__(self, tool_name: str, errors: List[ErrorDetails]):
        self.tool_name = tool_name
        self.errors = errors
        super().__init__(f"Validation failed for tool '{tool_name}'")


class ToolRuntimeError(ToolError):
    def __init__(self, tool_name: str, message: str):
        self.tool_name = tool_name
        self.message = message
        super().__init__(f"Execution failed for tool '{tool_name}': {message}")