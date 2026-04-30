from dataclasses import dataclass
from typing import List, Any, Optional

@dataclass
class TextResponse:
    content: str

@dataclass
class MemoryRetrieval:
    last_k: int
    content: List[str]

@dataclass
class ToolResult:
    id: str
    name: str
    args: dict
    results: Any
    exception: Optional[Exception]