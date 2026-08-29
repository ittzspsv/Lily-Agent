from pydantic import BaseModel
from typing import Any, Optional, List
from enum import Enum
from .agents import AgentInfo
from .tool_call import ToolCallResult

from .tool_call import ToolCall

class ResponseType(str, Enum):
    Text = "text"
    ToolCall = "tool_call"
    Stop = "stop"

class LLMResponse(BaseModel):
    type: ResponseType
    content: Optional[str] = None
    raw: Any = None
    tool_calls: Optional[List[ToolCall]] = None

class AgentResponse(LLMResponse):
    agent: AgentInfo
    tool_call_result: list[ToolCallResult] | None = None