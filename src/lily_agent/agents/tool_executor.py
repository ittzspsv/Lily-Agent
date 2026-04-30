# tool_executor.py

from ..tools.base.tool_base import Tool
from typing import List, Optional
from ..tools.errors.tool_exceptions import ToolValidationError, ToolRuntimeError
from .errors.agent_exceptions import ToolNotFoundError
from ..adapters.core.adapter_classes import Message, ToolCall
from .events.event_dispatcher import EventDispatcher
from .events.agent_events import AgentEvents
from .events.event_classes import ToolResult

class ToolExecutor:
    def __init__(self, tools: List[Tool], event_handler: Optional[EventDispatcher]) -> None:
        self._tool_registry = {tool.name: tool for tool in tools}
        self._event_handler: Optional[EventDispatcher] = event_handler

    def execute_sync(self, tool_calls: List[ToolCall] | None) -> List[Message]:
        results: List[Message] = []

        if tool_calls is None:
            raise ValueError

        for tool_call in tool_calls:
            print(f"[ToolExecutor] Calling tool: {tool_call.name}")
            if tool_call.name not in self._tool_registry:
                raise ToolNotFoundError(tool_call.name)
            
            tool = self._tool_registry[tool_call.name]
            try:
                result = tool.execute_sync(**tool_call.input)
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
    
    async def execute(self, tool_calls: List[ToolCall] | None)-> List[Message]:
        results: List[Message] = []

        if tool_calls is None:
            raise ValueError("tool_calls cannot be None")
        
        for tool_call in tool_calls:
            if self._event_handler is not None:
                await self._event_handler.invoke(AgentEvents.ON_TOOL_EXECUTION_STARTED, ToolResult(
                    id=tool_call.id, 
                    name=tool_call.name,
                    args=tool_call.input,
                    results={},
                    exception=None
                ))
            
            if tool_call.name not in self._tool_registry:
                raise ToolNotFoundError(tool_call.name)
            
            tool = self._tool_registry[tool_call.name]

            try:
                result = await tool.execute(**tool_call.input)

                if self._event_handler is not None:
                    await self._event_handler.invoke(AgentEvents.ON_TOOL_EXECUTION_COMPLETED, ToolResult(
                        id=tool_call.id, 
                        name=tool_call.name,
                        args=tool_call.input,
                        results=result,
                        exception=None
                    ))
            
            except ToolValidationError as e:
                result = f"Validation error: {e}"
                
                if self._event_handler is not None:
                    await self._event_handler.invoke(AgentEvents.ON_TOOL_EXECUTION_FAILED, ToolResult(
                        id=tool_call.id,
                        name=tool_call.name,
                        args=tool_call.input,
                        results={},
                        exception=e
                    ))  
            
            except ToolRuntimeError as e:
                result = f"Runtime error: {e}"

                if self._event_handler is not None:
                    await self._event_handler.invoke(AgentEvents.ON_TOOL_EXECUTION_FAILED, ToolResult(
                        id=tool_call.id,
                        name=tool_call.name,
                        args=tool_call.input,
                        results={},
                        exception=e
                    ))
            
            except Exception as e:
                result = f"Unexpected error: {e}"

                if self._event_handler is not None:
                    await self._event_handler.invoke(AgentEvents.ON_TOOL_EXECUTION_FAILED, ToolResult(
                        id=tool_call.id,
                        name=tool_call.name,
                        args=tool_call.input,
                        results={},
                        exception=e
                    ))

            results.append(Message(
                role="tool_result",
                content=str(result),
                tool_call_id=tool_call.id
            ))

        return results 