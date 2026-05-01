# Vector Stores
### Basic Introduction
- A vector store is basically storing, indexing and searching text, images and audio as embedding format.
- These embeddings are generated using a machine learning model that convert data into vectors.
- We use this information to sematically search for similar embeddings (retrieval) using distance matrics.

### Purpose Of Vector Store
#### Stateless Architechture of LLM.
- Most Large Language Models (LLMs) are stateless by default.
- They are not persistent across restarts
- Each prompt query is evaluated independently unless context is explicitly provided.
#### Why vector stores are used?
- Instead of relaying on the context window we
  - Extract important factual information from the conversations
  - convert it into embeddings using an embedding model
  - store it in a vector database for later use.

## 1. Integrating a Vector Store
- With Lily Framework you can integrate any vector databases with a high level abstractions provided
- The base abstraction allows developers to switch b/w different databases  without changing application core logic.

## 2. Prerequisites
- A Vector Database pipeline with python support.

## 3. Getting Started
- For this demonstration we will integrate chroma database.
- Start off by installing chroma on your virtual environment
```bash
pip install chromadb
```


### 4. Inheriting the abstraction class and methods
- Let us inherit all the methods that we need inorder to work with.

```python
from lily_agent.vectorstore import VectorStore, VectorRetrieval
from typing import Dict, Any, Optional, List

class ChromaDB(VectorStore):
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

```