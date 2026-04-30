from abc import ABC, abstractmethod
from typing import Any, Dict, List

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
    async def push(self, text, embedding, metadata):
        ...

    @abstractmethod
    async def retrieve(self, query_embedding, k, filters) -> List[str]:
        ...

    @abstractmethod
    async def delete(self, filters: Dict[str, Any]) -> None:
        ...

    @abstractmethod
    async def clear(self) -> None:
        ...