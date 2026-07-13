from abc import ABC, abstractmethod
from typing import Optional
from typing import List
from uuid import UUID

from ..schemas import AgentInfo

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
    ) -> AgentInfo:
        """Returns agent_id"""
        ...

    @abstractmethod
    def get(self, agent_key: str) -> Optional[AgentInfo]:
        ...

    @abstractmethod
    def resolve(self, agent_id: UUID) -> Optional[str]:
        """Returns agent_key"""
        ...

    @abstractmethod
    def list_agents(self) -> List[AgentInfo]:
        ...