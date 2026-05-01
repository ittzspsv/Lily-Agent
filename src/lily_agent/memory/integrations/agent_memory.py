from typing import Any, Dict, List, Optional, Type

from ..core.memory import MemoryBase
from ...agents.core.agent_base import AgentBase
from ...embedder.core.embedder import Embedder
from ...vectorstore.core.vector_store import VectorStore, VectorRetrieval
from ...agents.events.event_classes import MemoryStore

from ast import literal_eval

class AgentMemory(MemoryBase):
    """
    ### Definition
    - Agent level memory implementation that contains
       - `llm` (For fact retrieval)
       - `embedder` (Embedding Model)
       - `vector_store` (For storing embeddings)
    
    """
    def __init__(
            self, 
            llm: AgentBase,
            embedder: Embedder, 
            vector_store: VectorStore
    ) -> None:

        self.llm = llm
        self.embedder = embedder
        self.vector_store = vector_store

    @classmethod
    async def create(
        cls,
        embedder: Embedder,
        vector_store: Type[VectorStore],
        llm: AgentBase,
        *args,
        **kwargs
    ):
        vector_store_ = await vector_store.new(
            *args,
            dimensions=embedder.dimensions,
            **kwargs
        )

        return cls(
            llm=llm,
            embedder=embedder,
            vector_store=vector_store_
        )

    async def push(
            self,
            text: str,
            agent_id: str,
            user_id: Optional[str] = None,
            metadata: Optional[dict] = {}
        ) -> MemoryStore:
        response = await self.llm.run(text)
        facts: List[str] = literal_eval(response)

        for fact in facts:
            embedding = await self.embedder.embed(text)

            await self.vector_store.push(
                text=fact, 
                embedding=embedding,
                user_id=user_id,
                agent_id=agent_id,
                metadata=metadata
            )

        return MemoryStore(
            user_id=user_id or "__default__",
            agent_id=agent_id,
            metadata=metadata or {},
            user_query=text,
            facts=facts
        )
    
    async def retrieve(self, query: str, filters: Optional[Dict[str, Any]] = None, k: int = 5) -> List[VectorRetrieval]:
        query_embedding = await self.embedder.embed(query)

        results: List[VectorRetrieval] = await self.vector_store.retrieve(
            query_embedding=query_embedding,
            k=k,
            filters=filters
        )

        return results
    
    async def delete(self, filters: Optional[Dict[str, Any]] = None) -> None:
        if filters is not None:
            await self.vector_store.delete(filters=filters)
    
    async def clear(self, **kwargs) -> None:
        await self.vector_store.clear()