from typing import List, Any, Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class ToolResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str
    name: str
    args: dict
    results: Any
    exception: Optional[Exception]


class MemoryStore(BaseModel):
    user_id: Optional[UUID | int]
    agent_id: UUID
    metadata: dict
    user_query: str
    facts: List[str]