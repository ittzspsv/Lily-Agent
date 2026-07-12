from pydantic import BaseModel
from typing import Any, Optional, List
from enum import Enum
from .users import User
from .agents import AgentInfo

from .tool_call import ToolCall

class ResponseType(str, Enum):
    Text = "text"
    ToolCall = "tool_call"
    Stop = "stop"

class LLMResponse(BaseModel):
    response_type: ResponseType
    content: Optional[str] = None
    raw: Any = None
    tool_calls: Optional[List[ToolCall]] = None


class AgentResponse(LLMResponse):
    me: Optional[AgentInfo] = None