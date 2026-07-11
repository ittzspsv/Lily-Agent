from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str | list | dict
    tool_call_id: Optional[str] = None