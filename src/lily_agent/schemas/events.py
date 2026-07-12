from typing import List, Any, Optional
from pydantic import BaseModel


class TextResponse(BaseModel):
    content: str

class ToolResult(BaseModel):
    id: str
    name: str
    args: dict
    results: Any
    exception: Optional[Exception]


class MemoryStore(BaseModel):
    user_id: str
    agent_id: str
    metadata: dict
    user_query: str
    facts: List[str]