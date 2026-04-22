from ..tools.core.function_tool import FunctionTool
from typing import List
from ..tools.base.tool_exceptions import ToolValidationError, ToolRuntimeError
from .agent_exceptions import ToolNotFoundError
from ..adapters.adapter_classes import Message, ToolCall

class ToolExecutor:
    def __init__(self, tools: List[FunctionTool]) -> None:
        self._tool_registry = {tool.name: tool for tool in tools}

    def execute(self, tool_calls: List[ToolCall] | None) -> List[Message]:
        results: List[Message] = []

        if tool_calls is None:
            raise ValueError

        for tool_call in tool_calls:
            print(f"[ToolExecutor] Calling tool: {tool_call.name}")
            if tool_call.name not in self._tool_registry:
                raise ToolNotFoundError(tool_call.name)
            
            tool = self._tool_registry[tool_call.name]
            try:
                result = tool.execute(**tool_call.input)
            except ToolValidationError as e:
                result = f"Validation error: {e}"  
            except ToolRuntimeError as e:
                result = f"Runtime error: {e}"
            except Exception as e:
                result = f"Unexpected error: {e}"


            results.append(Message(
                role="tool_result",
                content=str(result),
                tool_call_id=tool_call.id
            ))

        return results 
    
    async def aexecute(self, tool_calls: List[ToolCall] | None)-> List[Message]:
        results: List[Message] = []

        if tool_calls is None:
            raise ValueError
        
        for tool_call in tool_calls:
            print(f"[ToolExecutor] Calling tool: {tool_call.name}")

            if tool_call.name not in self._tool_registry:
                raise ToolNotFoundError(tool_call.name)
            
            tool = self._tool_registry[tool_call.name]

            try:
                if hasattr(tool, "aexecute"):
                    result = await tool.aexecute(**tool_call.input)
                else:
                    result = tool.execute(**tool_call.input)
            except ToolValidationError as e:
                result = f"Validation error: {e}"  
            except ToolRuntimeError as e:
                result = f"Runtime error: {e}"
            except Exception as e:
                result = f"Unexpected error: {e}"

            results.append(Message(
                role="tool_result",
                content=str(result),
                tool_call_id=tool_call.id
            ))

        return results 