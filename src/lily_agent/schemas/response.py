from pydantic import BaseModel
from typing import Any, Literal, Optional, List
from enum import Enum

from .tool_call import ToolCall

class ResponseType(str, Enum):
    Text = "text",
    ToolCall = "tool_call",
    Stop = "stop"

class LLMResponse(BaseModel):
    response_type: ResponseType
    content: Optional[str] = None
    raw: Any = None

class AgentResponse(LLMResponse):
    tool_calls: Optional[List[ToolCall]] = None