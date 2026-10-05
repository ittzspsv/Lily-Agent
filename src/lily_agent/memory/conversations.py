from ..schemas import Message, User, MessageRole
from typing import Dict, List, Optional
from uuid import UUID


class Conversation:
    def __init__(self, system_prompt: str) -> None:
        self._system_prompt = system_prompt
        self._messages: Dict[UUID | int, List[Message]] = {}

    def _get_messages(self, user: User) -> List[Message]:
        if user.id not in self._messages:
            self._messages[user.id] = [Message(role=MessageRole.System, content=self._system_prompt)]
        return self._messages[user.id]

    def add_message(self, user: User, content: str, role: MessageRole):
        self._get_messages(user).append(Message(
            role = role,
            content=content
        ))

    def add_tool_results(self, user: User, results: List[Message]) -> None:
        self._get_messages(user).extend(results)

    def get_messages(
        self,
        user: User,
        k: int = 5,
        context: Optional[str] = None,
    ) -> List[Message]:
        thread = self._get_messages(user)
        system, history = thread[0], thread[1:]

        user_idx = [i for i, m in enumerate(history) if m.role == MessageRole.User]
        k = max(k, 1)
        start = user_idx[-k] if len(user_idx) > k else 0

        if context:
            system = Message(
                role=MessageRole.System,
                content=f"{system.content}\n\n{context}",
            )

        return [system] + history[start:]

    def reset(self, user: User, system_prompt: Optional[str] = None) -> None:
        prompt = system_prompt or self._system_prompt
        self._messages[user.id] = [Message(role=MessageRole.System, content=prompt)]

    def drop_user(self, user: User) -> None:
        self._messages.pop(user.id, None)