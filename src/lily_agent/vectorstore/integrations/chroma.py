from lily_agent.vectorstore import VectorStore, VectorRetrieval
from typing import Dict, Any, Optional, List

class Qdrant(VectorStore):
    @classmethod
    async def new(cls, *args, **kwargs) -> Any:
        """ Method used to connect to a database, construct base database schema """

    async def push(self, text, embedding, agent_id: str, user_id: Optional[str], metadata: Optional[dict]):
        """ Method used to insert or add an embedding to a database """

    async def retrieve(self, query_embedding, k, filters) -> List[VectorRetrieval]:
        """ 
        Method used to retrive or fetch an embedding from a database 
        - Based on embeddings, top k amount (limit) and filters """
        ...


    async def delete(self, filters: Dict[str, Any]) -> None:
        """ Method used to delete an embedding from a database 
        - based on filters passed as an argument """


    async def clear(self) -> None:
        """ Method used to clear the entire database table """