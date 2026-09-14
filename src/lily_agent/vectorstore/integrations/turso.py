from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING, Dict
from ..vector_store import VectorStore
from ...schemas import VectorRetrieval

if TYPE_CHECKING:
    import turso

import uuid
import json


_METRIC_FUNCS = {
    "cosine": "vector_distance_cos",
    "l2": "vector_distance_l2",
    "euclidean": "vector_distance_l2",
    "dot": "vector_distance_dot",
}


def _to_vector_literal(embedding: List[float]) -> str:
    """Render a Python float list as a vector32() literal, e.g. '[1,2,3]'."""
    return "[" + ",".join(repr(float(x)) for x in embedding) + "]"


class Turso(VectorStore):
    def __init__(
            self,
            path: str,
            dimensions: int,
            table_name: str = 'memory',
            remote_url: Optional[str] = None,
            auth_token: Optional[str] = None,
            metric: str = 'cosine',
            **kwargs
        ) -> None:
        super().__init__(dimensions=dimensions)

        if not path:
            raise ValueError("Database path isn't specified.")
        
        self.path = path
        self.remote_url = remote_url
        self.auth_token = auth_token

        self.kwargs = kwargs

        self.dimensions = dimensions

        self.table_name = table_name
        self.metric = metric
        if metric not in _METRIC_FUNCS:
            raise ValueError(f"Unsupported metric '{metric}'; choose one of {sorted(_METRIC_FUNCS)}")
        self._distance_func = _METRIC_FUNCS[metric]

        self._conn: Optional[Any] = None

    @classmethod
    async def new(
        cls,
        dimensions: int,
        path: str,
        remote_url: Optional[str] = None,
        auth_token: Optional[str] = None,
    ) -> Any:
        self = cls(path=path, dimensions=dimensions, remote_url=remote_url, auth_token=auth_token)
        await self._init()
        return self

    async def _init(self):
        try:
            import turso
            import turso.aio.sync
        except ImportError:
            raise ImportError("Install pyturso to use TursoMemory")

        if self.remote_url:
            self._conn = await turso.aio.sync.connect(
                self.path,
                remote_url=self.remote_url,
                auth_token=self.auth_token,
                **self.kwargs
            )
            await self._conn.pull()
        else:
            self._conn = await turso.aio.connect(self.path, **self.kwargs)

        await self._conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id TEXT PRIMARY KEY,
                text TEXT,
                embedding BLOB,
                user_id TEXT,
                agent_id TEXT,
                metadata TEXT
            )
            """
        )

        await self._conn.commit()

    async def push(
            self,
            text: str,
            embedding,
            agent_id: uuid.UUID,
            user_id: Optional[uuid.UUID | int],
            metadata: Optional[dict]
        ) -> None:
        if self._conn is not None:
            if len(embedding) != self.dimensions:
                raise ValueError(
                    f"Embedding has {len(embedding)} dimensions, expected {self.dimensions}"
                )
            await self._conn.execute(
                f"""
                INSERT INTO {self.table_name} (id, text, embedding, user_id, agent_id, metadata)
                VALUES (?, ?, vector32(?), ?, ?, ?)
                """,
                (
                    str(uuid.uuid4()),
                    text,
                    _to_vector_literal(embedding),
                    str(user_id) if user_id is not None else "__default__",
                    str(agent_id),
                    json.dumps(metadata or {}),
                )
            )
            await self._conn.commit()
            if self.remote_url:
                await self._conn.push()

    async def retrieve(
        self,
        query_embedding: List[float],
        k: int = 5,
        filters: Dict[str, Any] | None = None
    ) -> List[VectorRetrieval]:

        if self._conn is None:
            raise RuntimeError("Memory not initialized. Call create() first.")

        allowed_keys = {"id", "text", "user_id", "agent_id"}

        vec_literal = _to_vector_literal(query_embedding)
        where_sql = ""
        params: List[Any] = [vec_literal]

        if filters:
            conditions = []
            for key, value in filters.items():
                if key in allowed_keys:
                    conditions.append(f"{key} == ?")
                    params.append(str(value))
            if conditions:
                where_sql = "WHERE " + " AND ".join(conditions)

        params.append(vec_literal)
        params.append(k)

        query = f"""
            SELECT id, text, embedding, user_id, agent_id, metadata,
                   {self._distance_func}(embedding, vector32(?)) AS distance
            FROM {self.table_name}
            {where_sql}
            ORDER BY {self._distance_func}(embedding, vector32(?)) ASC
            LIMIT ?
        """

        cursor = await self._conn.execute(query, params)
        rows = await cursor.fetchall()
        columns = [d[0] for d in cursor.description]

        results = []
        for row in rows:
            row_dict = dict(zip(columns, row))
            results.append(
                VectorRetrieval(
                    id=row_dict["id"],
                    text=row_dict["text"],
                    embedding=row_dict.get("embedding"),
                    user_id=row_dict["user_id"],
                    agent_id=row_dict["agent_id"],
                    metadata=json.loads(row_dict["metadata"] or "{}")
                )
            )
        return results

    async def delete(self, filters: Dict[str, Any]) -> None:
        if self._conn is None:
            raise RuntimeError("Connection not initialized.")

        if not filters:
            raise ValueError("Filters required for delete operation")

        allowed_keys = {"id", "text", "user_id", "agent_id"}

        conditions = []
        params: List[Any] = []

        for key, value in filters.items():
            if key in allowed_keys:
                conditions.append(f"{key} == ?")
                params.append(str(value))

        if not conditions:
            raise ValueError("No valid filters provided")

        where_clause = " AND ".join(conditions)

        await self._conn.execute(
            f"DELETE FROM {self.table_name} WHERE {where_clause}",
            params
        )
        await self._conn.commit()
        if self.remote_url:
            await self._conn.push()

    async def clear(self) -> None:
        if self._conn is None:
            raise RuntimeError("Connection not initialized.")

        await self._conn.execute(f"DELETE FROM {self.table_name}")
        await self._conn.commit()
        if self.remote_url:
            await self._conn.push()

    async def close(self) -> None:
        if self._conn is not None:
            await self._conn.close()