from pydantic import BaseModel

from typing import Optional

class AgentPolicy(BaseModel):
    """ Base Policies """
    use_tools: Optional[bool] = None
    use_conversational_history: Optional[bool] = None
    use_memory: Optional[bool] = None

    """ Advanced Policy"""
    store_memory: Optional[bool] = None