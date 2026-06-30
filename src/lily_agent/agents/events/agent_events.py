from typing import Final

class AgentEvents:
    ON_TOOL_CALL_REQUESTED: Final = "on_tool_call_requested"
    ON_TOOL_EXECUTION_STARTED: Final = "on_tool_execution_started"
    ON_TOOL_EXECUTION_COMPLETED: Final = "on_tool_execution_completed"
    ON_TOOL_EXECUTION_FAILED: Final = "on_tool_execution_failed"

    ON_AGENT_TEXT_RESPONSE: Final = "on_agent_text_response"

    ON_MEMORY_RETRIEVED: Final = "on_memory_retrieved"
    ON_MEMORY_STORED: Final = "on_memory_stored"