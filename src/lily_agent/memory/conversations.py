from ..schemas import Message, User
from typing import Dict, List, Optional
from uuid import UUID


class Conversation:
    def __init__(self, system_prompt: str) -> None:
        self._system_prompt = system_prompt
        self._messages: Dict[UUID | int, List[Message]] = {}

    def _get_messages(self, user: User) -> List[Message]:
        if user.id not in self._messages:
            self._messages[user.id] = [Message(role="system", content=self._system_prompt)]
        return self._messages[user.id]

    def add_user(self, user: User, content: str) -> None:
        self._get_messages(user).append(Message(role="user", content=content))

    def add_assistant(self, user: User, content: str) -> None:
        self._get_messages(user).append(Message(role="assistant", content=content))

    def add_system(self, user: User, content: str) -> None:
        self._get_messages(user).append(Message(role="system", content=content))

    def add_tool_results(self, user: User, results: List[Message]) -> None:
        self._get_messages(user).extend(results)

    def get_messages(self, user: User, k: int = 5) -> List[Message]:
        thread = self._get_messages(user)
        system = thread[:1]
        recent = thread[1:][-k:]
        return system + recent

    def reset(self, user: User, system_prompt: Optional[str] = None) -> None:
        prompt = system_prompt or self._system_prompt
        self._messages[user.id] = [Message(role="system", content=prompt)]

    def drop_user(self, user: User) -> None:
        self._messages.pop(user.id, None)