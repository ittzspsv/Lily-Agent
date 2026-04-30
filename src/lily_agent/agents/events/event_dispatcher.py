from typing import Set
import inspect
from collections import defaultdict

import asyncio

class EventDispatcher:
    """
    ### Definition
    - Internal event management system for registering, managing and invoking event handlers.
    - Provides a structured mechanism for extending the agent behavior based on events.
    
    """
    def __init__(self) -> None:
        self._events: Set[str] = set()

        self._handlers = defaultdict(list)

    def register(self, event_name, handler):
        if event_name not in self._events:
            raise ValueError(f"Invalid event: {event_name}")
        self._handlers[event_name].append(handler)


    def preload_events(self, events: Set[str]):
        self._events.update(events)


    async def _event_executor(self, func, *args, **kwargs):
        if inspect.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        return func(*args, **kwargs)


    async def invoke(self, name: str, *args, **kwargs):
        if name not in self._events:
            raise ValueError(f"Unknown event: {name}")
        
        handlers = self._handlers.get(name, [])

        tasks = [
            self._event_executor(handler, *args, **kwargs)
            for handler in handlers
        ]

        await asyncio.gather(*tasks, return_exceptions=True)
