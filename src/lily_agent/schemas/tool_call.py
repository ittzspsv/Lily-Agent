from pydantic import BaseModel, PrivateAttr
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..tools import Tool
from ..schemas.message import Message
from typing import Optional


class ToolCall(BaseModel):
    id: str
    name: str
    input: dict
    description: Optional[str] = None

class ToolCallResult(BaseModel):
    id: str
    name: str
    input: dict
    result: Message
    _tool: "Tool | None" = PrivateAttr(default=None)