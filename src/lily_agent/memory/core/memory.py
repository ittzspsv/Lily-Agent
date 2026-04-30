from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from ...embedder.core.embedder import Embedder

import asyncio


class MemoryBase(ABC):
    def _run_sync(self, coro):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coro)
        else:
            raise RuntimeError(
                "Cannot call sync method inside a running loop. Use async version."
            )
    
    @abstractmethod
    async def push(
        self,
        text: str,
        role: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        pass

    def push_sync(
            self, 
            text: str, 
            role: str, 
            metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        return self._run_sync(self.push(text=text, role=role, metadata=metadata))

    @abstractmethod
    async def retrieve(self, query: str, role: Optional[str] = None, k: int = 5) -> List[str]:
        pass

    def retrieve_sync(self, query: str, k: int = 5) -> List[str]:
        return self._run_sync(self.retrieve(query=query, k=k))

    @abstractmethod
    async def delete(self, filters: Dict[str, Any]) -> None:
        pass

    def delete_sync(self, filters: Dict[str, Any]) -> None:
        return self._run_sync(self.delete(filters=filters))

    @abstractmethod
    async def clear(self) -> None:
        pass

    def clear_sync(self) -> None:
        return self._run_sync(self.clear())