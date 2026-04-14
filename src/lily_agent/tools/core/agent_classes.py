from pydantic import BaseModel, Field

class AgentToolInput(BaseModel):
    input: str = Field(description="The task or query to send to this agent")