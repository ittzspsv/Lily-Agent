from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass
from typing import List

@dataclass
class AgentInfo:
    id: str
    key: str
    name: str
    role: str
    prompt: str

class AgentRegistry(ABC):
    def __init__(self, path: Optional[str] = None) -> None:

        self.path: Optional[str] = path

    @abstractmethod
    def register(
        self,
        agent_key: str,
        name: str,
        role: str,
        prompt: str,
    ) -> str:
        """Returns agent_id"""
        ...

    @abstractmethod
    def get(self, agent_key: str) -> Optional[AgentInfo]:
        ...

    @abstractmethod
    def resolve(self, agent_id: str) -> Optional[str]:
        """Returns agent_key"""
        ...

    @abstractmethod
    def list_agents(self) -> List[AgentInfo]:
        ...
    
