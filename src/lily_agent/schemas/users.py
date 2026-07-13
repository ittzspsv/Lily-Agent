from pydantic import BaseModel
from uuid import UUID

from typing import Optional

class User(BaseModel):
    id: UUID | int
    name: Optional[str]