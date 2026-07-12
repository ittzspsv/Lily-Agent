from typing import Optional
from pydantic import BaseModel
from enum import Enum

class MessageRole(Enum):
    System = "system"
    User = "user"
    Assistant = "assistant"

class Message(BaseModel):
    role: MessageRole
    content: str | list | dict
    tool_call_id: Optional[str] = None

