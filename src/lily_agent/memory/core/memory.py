from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from ...vectorstore.core.vector_store import VectorRetrieval
from ...agents.events.event_classes import MemoryStore

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
        agent_id: str,
        user_id: Optional[str] = None,
        metadata: Optional[dict] = {}
    ) -> MemoryStore:
        ...

    def push_sync(
            self, 
            text: str, 
            agent_id: str,
            user_id: Optional[str] = None,
            metadata: Optional[dict] = {}
    ) -> MemoryStore:
        return self._run_sync(self.push(text=text, agent_id=agent_id, user_id=user_id, metadata=metadata))

    @abstractmethod
    async def retrieve(self, query: str, filters: Optional[Dict[str, Any]] = None, k: int = 5) -> List[VectorRetrieval]:
        pass

    def retrieve_sync(self, query: str, filters: Optional[Dict[str, Any]] = None ,k: int = 5) -> List[VectorRetrieval]:
        return self._run_sync(self.retrieve(query=query, filters=filters ,k=k))

    @abstractmethod
    async def delete(self, filters: Optional[Dict[str, Any]] = None) -> None:
        pass

    def delete_sync(self, filters: Optional[Dict[str, Any]] = None) -> None:
        return self._run_sync(self.delete(filters=filters))

    @abstractmethod
    async def clear(self, **kwargs) -> None:
        pass

    def clear_sync(self, **kwargs) -> None:
        return self._run_sync(self.clear(**kwargs))