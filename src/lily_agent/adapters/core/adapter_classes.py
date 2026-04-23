from typing import List, Any, Optional, Literal
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str | list | dict
    tool_call_id: Optional[str] = None


class ToolCall(BaseModel):
    id: str
    name: str
    input: dict


class LLMResponse(BaseModel):
    response_type: Literal["text", "tool_call", "stop"]  
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    raw: Any = None