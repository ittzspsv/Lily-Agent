from __future__ import annotations

from ..core.memory import AgentMemory
from typing import List, Optional, TYPE_CHECKING, Dict, Any
from ...embedder.core.embedder import Embedder
from lancedb.index import IvfFlat

import uuid
import json

if TYPE_CHECKING:
    import lancedb
    import pyarrow
    from lancedb import AsyncConnection, AsyncTable

class LanceMemory(AgentMemory):
    def __init__(
            self, 
            embedder: Embedder,
            uri: str, 
            table_name: str = 'memory',
            **kwargs
    ) -> None:
        super().__init__(embedder=embedder)

        if not uri:
            raise ValueError("Database path isn't specified.")

        '''Identifier (Can be local, or cloud endpoint url)'''
        self.uri = uri

        self.table_name = table_name
        self.kwargs = kwargs
        self._table: Optional["AsyncTable"] = None

        self._db: Optional["AsyncConnection"] = None
        self._schema = None

        self._index_initialized: bool = False

        
    async def _init(self):
        '''Check if the package is installed, else raise an ImportError'''
        try:
            import lancedb
            import pyarrow
        except ImportError:
            raise ImportError("Install lancedb and pyarrow to use LanceMemory")

        
        '''Let's define a schema for our vectorstore'''
        self._schema = pyarrow.schema([
            ('id', pyarrow.string()),
            ('text', pyarrow.string()),
            ('embedding', pyarrow.list_(pyarrow.float32(), self.embedder.dimensions)),
            ('role', pyarrow.string()),
            ('metadata', pyarrow.string())
        ])


        '''Let's connect to lance db'''
        self._db = await lancedb.connect_async(uri=self.uri, **self.kwargs)

        '''Fetch all table names from the database'''
        table_names = await self._db.table_names()

        '''
        Check if the database contains the table name
        If not raise an runtime exception.
        '''
        if self.table_name in table_names:
            self._table = await self._db.open_table(self.table_name)

        else:
            '''Create a table with default parameter required for the agent.'''
            self._table = await self._db.create_table(
                self.table_name,
                data=[],
                schema=self._schema
            )


    async def push(self, text: str, role: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        if self._table is not None:

            embedding = await self.embedder.embed(text=text)


            await self._table.add([
                {
                    "id": str(uuid.uuid4()),
                    "text": text,
                    "embedding": embedding,
                    "role": role,
                    "metadata": json.dumps(metadata or {})
                }
            ])

            if not self._index_initialized:
                await self._table.create_index(column="embedding", config=IvfFlat(distance_type="cosine"))

        else:
            raise RuntimeError("Memory not initialized. Call create() first.")

    async def retrieve(self, query: str, role: Optional[str] = None ,k: int = 5) -> List[str]:
        if self._table is None:
            raise RuntimeError("Memory not initialized. Call create() first.")

        query_embedding: list[float] = await self.embedder.embed(text=query)

        cursor = await self._table.search(query_embedding, vector_column_name="embedding")
        
        if role is not None:
            cursor = cursor.where(f"role = '{role}'")

        rows = await cursor.limit(k).to_list()

        return [row["text"] for row in rows]
    
    async def delete(self, filters: Dict[str, Any]) -> None:
        pass
    
    async def clear(self) -> None:
        pass
