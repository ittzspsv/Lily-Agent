from dataclasses import dataclass
from typing import List, Any, Optional

@dataclass
class TextResponse:
    content: str


@dataclass
class ToolResult:
    id: str
    name: str
    args: dict
    results: Any
    exception: Optional[Exception]

@dataclass
class MemoryStore:
    user_id: str
    agent_id: str
    metadata: dict
    user_query: str
    facts: List[str]