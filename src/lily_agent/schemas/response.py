from pydantic import BaseModel
from typing import Any, Literal, Optional, List

from .tool_call import ToolCall

class LLMResponse(BaseModel):
    response_type: Literal["text", "tool_call", "stop"]  
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    raw: Any = None