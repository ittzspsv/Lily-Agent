from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from ..schemas import VectorRetrieval
from uuid import UUID

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
    async def push(
        self, 
        text: str, 
        embedding, 
        agent_id: UUID, 
        user_id: Optional[UUID | int], 
        metadata: Optional[dict]
    ):
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