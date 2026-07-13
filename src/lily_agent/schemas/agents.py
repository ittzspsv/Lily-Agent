from dataclasses import dataclass
from uuid import UUID
from pydantic import BaseModel
from typing import Optional


class AgentInfo(BaseModel):
    id: UUID
    key: str
    name: str
    role: str
    prompt: str

    @property
    def system_prompt(self) -> str:
        return f"{self.role}\n\n{self.prompt}"

class AgentPolicy(BaseModel):
    use_tools: Optional[bool] = None
    use_conversational_history: Optional[bool] = None
    use_memory: Optional[bool] = None
    store_memory: Optional[bool] = None