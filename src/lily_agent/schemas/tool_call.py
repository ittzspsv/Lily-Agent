from pydantic import BaseModel, PrivateAttr
from ..tools.base.tool_base import Tool
from ..schemas.message import Message


class ToolCall(BaseModel):
    id: str
    name: str
    input: dict

class ToolCallResult(BaseModel):
    id: str
    name: str
    input: dict
    result: Message
    _tool: Tool | None = PrivateAttr(default=None)