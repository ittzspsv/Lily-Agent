class AgentError(Exception):
    """Base exception for all Agent related errors."""
    pass

class MaxIterationsError(AgentError):
    def __init__(self, max_iter: int):
        self.max_iter = max_iter
        super().__init__(f"Agent exceeded maximum iterations of {max_iter}")

class ToolNotFoundError(AgentError):
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        super().__init__(f"Tool '{tool_name}' not found")