from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING, Dict
from ..core.vector_store import VectorStore

if TYPE_CHECKING:
    import lancedb
    import pyarrow
    from lancedb.index import IvfFlat
    from lancedb import AsyncConnection, AsyncTable

import uuid
import json

class Lance(VectorStore):
    def __init__(
            self,
            uri: str, 
            dimensions: int,
            table_name: str = 'memory',
            **kwargs        
        ) -> None:
        super().__init__(dimensions=dimensions)

        if not uri:
            raise ValueError("Database path isn't specified.")
        
        '''Identifier (Can be local, or cloud endpoint url)'''
        self.uri = uri

        self.kwargs = kwargs

        self.dimensions = dimensions

        self.table_name = table_name
        self._table: Optional["AsyncTable"] = None

        self._db: Optional["AsyncConnection"] = None
        self._schema = None

        self._index_initialized: bool = False

    @classmethod
    async def new(cls, dimensions: int ,uri: str) -> Any:
        self = cls(uri=uri, dimensions=dimensions)
        await self._init()
        return self
    
    async def _init(self):
        """ Check if the package is installed, else raise an ImportError """
        try:
            import lancedb
            import pyarrow
        except ImportError:
            raise ImportError("Install lancedb and pyarrow to use LanceMemory")

        
        '''Let's define a schema for our vectorstore'''
        self._schema = pyarrow.schema([
            ('id', pyarrow.string()),
            ('text', pyarrow.string()),
            ('embedding', pyarrow.list_(pyarrow.float32(), self.dimensions)),
            ('role', pyarrow.string()),
            ('metadata', pyarrow.string())
        ])


        """ Let's connect to lance db """
        self._db = await lancedb.connect_async(uri=self.uri, **self.kwargs)

        """ Fetch all table names from the database """
        table_names = await self._db.table_names()

        """
        Check if the database contains the table name
        If not raise an runtime exception.
        """
        if self.table_name in table_names:
            self._table = await self._db.open_table(self.table_name)

        else:
            """ Create a table with default parameter required for the agent. """
            self._table = await self._db.create_table(
                self.table_name,
                data=[],
                schema=self._schema
            )

    async def push(self, text, embedding, metadata):
        if self._table is not None:
            await self._table.add([
                {
                    "id": str(uuid.uuid4()),
                    "text": text,
                    "embedding": embedding,
                    "metadata": json.dumps(metadata or {})
                }
            ])

    async def retrieve(
        self,
        query_embedding: List[float],
        k: int = 5,
        filters: Dict[str, Any] | None = None
    ) -> List[str]:

        if self._table is None:
            raise RuntimeError("Memory not initialized. Call create() first.")

        cursor = await self._table.search(
            query_embedding,
            vector_column_name="embedding"
        )

        if filters:
            conditions = []

            for key, value in filters.items():
                if key in {"id", "text", "role"}:
                    conditions.append(f"{key} = '{value}'")

                else:
                    conditions.append(f"metadata LIKE '%\"{key}\": \"{value}\"%'")

            if conditions:
                where_clause = " AND ".join(conditions)
                cursor = cursor.where(where_clause)

        rows = await cursor.limit(k).to_list()

        return [row["text"] for row in rows]
    
    async def delete(self, filters: Dict[str, Any]) -> None:
        if self._table is None:
            raise RuntimeError("Table not initialized.")

        if not filters:
            raise ValueError("Filters required for delete operation")

        conditions = []

        for key, value in filters.items():
            if key in {"id", "text", "role"}:
                conditions.append(f"{key} = '{value}'")
            else:
                conditions.append(f"metadata LIKE '%\"{key}\": \"{value}\"%'")

        where_clause = " AND ".join(conditions)

        await self._table.delete(where_clause)
    
    async def clear(self) -> None:
        if self._table is None:
            raise RuntimeError("Table not initialized.")

        await self._table.delete("TRUE")