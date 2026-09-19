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