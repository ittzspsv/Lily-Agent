from typing import Any, Dict, List, Optional, Type

from ..core.memory import MemoryBase
from ...agents.core.agent_base import AgentBase
from ...embedder.core.embedder import Embedder
from ...vectorstore.core.vector_store import VectorStore

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

    async def push(self, text: str, role: str, metadata: Dict[str, Any] | None = None) -> None:

        facts = await self.llm.run(text)

        for fact in literal_eval(facts):
            embedding = await self.embedder.embed(text)

            await self.vector_store.push(
                text=fact, 
                embedding=embedding, 
                metadata={
                    "role": role,
                    **(metadata or {})
                }
            )
    
    async def retrieve(self, query: str, role: str | None = None, k: int = 5) -> List[str]:
        query_embedding = await self.embedder.embed(query)

        filters = {}
        if role:
            filters["role"] = role

        results: List[str] = await self.vector_store.retrieve(
            query_embedding=query_embedding,
            k=k,
            filters=filters
        )

        return results
    
    async def delete(self, filters: Dict[str, Any]) -> None:
        await self.vector_store.delete(filters=filters)
    
    async def clear(self) -> None:
        await self.vector_store.clear()