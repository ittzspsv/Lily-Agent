from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class VectorRetrieval:
    id: str
    text: str
    embedding: Optional[List[float]]
    user_id: str
    agent_id: str
    metadata: Optional[dict]

class VectorStore(ABC):
    def __init__(self, dimensions: int) -> None:
        self.dimensions = dimensions

    @classmethod
    @abstractmethod
    async def new(cls, *args, **kwargs) -> Any:
        ...

    def initialize(self, dimensions: int):
        self.dimensions = dimensions
    
    
    @abstractmethod
    async def push(self, text, embedding, agent_id: str, user_id: Optional[str], metadata: Optional[dict]):
        ...

    @abstractmethod
    async def retrieve(self, query_embedding, k, filters) -> List[VectorRetrieval]:
        ...

    @abstractmethod
    async def delete(self, filters: Dict[str, Any]) -> None:
        ...

    @abstractmethod
    async def clear(self) -> None:
        ...