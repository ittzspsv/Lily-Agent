from ..adapters.adapter_classes import Message
from typing import List

class Conversation:
    def __init__(self, system_prompt: str) -> None:

        self.messages: List[Message] = [
            Message(role="system", content=system_prompt)
        ]

    def add_user(self, content: str) -> None:
        self.messages.append(Message(role="user", content=content))

    def add_assistant(self, content: str) -> None:
        self.messages.append(Message(role="assistant", content=content))

    def add_system(self, content: str) -> None:
        self.messages.append(Message(role="system", content=content))

    def add_tool_results(self, results: List[Message]):
        self.messages.extend(results)

    def get_messages(self) -> List[Message]:
        return list(self.messages)
    
    def reset(self, system_prompt: str) -> None:
        self.messages = [Message(role="system", content=system_prompt)]