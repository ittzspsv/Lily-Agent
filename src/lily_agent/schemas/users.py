from dataclasses import dataclass
from uuid import UUID

from typing import Optional

@dataclass
class User:
    id: UUID | int
    name: Optional[str]