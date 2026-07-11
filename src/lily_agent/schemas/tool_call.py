from pydantic import BaseModel

class ToolCall(BaseModel):
    id: str
    name: str
    input: dict