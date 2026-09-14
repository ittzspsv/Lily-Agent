from dataclasses import dataclass
from typing import Optional, List

@dataclass
class VectorRetrieval:
    id: str
    text: str
    embedding: Optional[List[float]]
    user_id: str
    agent_id: str
    metadata: Optional[dict]