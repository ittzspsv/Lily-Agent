from typing import List, Optional
from ..agent_registry import AgentInfo, AgentRegistry

import json
import os
import uuid


class JSONRegistry(AgentRegistry):
    def __init__(self, path: Optional[str] = None) -> None:
        self.path: Optional[str] = path or ".configs/agent_registry.json"
        self.cache: dict = {}

        super().__init__(self.path)

        self._load()

    def _load(self) -> None:
        """Load JSON file into memory cache"""

        if self.path is not None:
            if not os.path.exists(self.path):
                os.makedirs(os.path.dirname(self.path), exist_ok=True)
                with open(self.path, "w") as f:
                    json.dump({}, f)

            with open(self.path, "r") as f:
                self.cache = json.load(f)

    def _save(self) -> None:
        """ Save JSON to the path """
        if self.path is not None:
            with open(self.path, "w") as f:
                json.dump(self.cache, f, indent=4)


    def register(self, agent_key: str, name: str, role: str, prompt: str) -> str:
        if agent_key in self.cache:
            agent_id = self.cache[agent_key]["agent_id"]

            self.cache[agent_key].update({
                "name": name,
                "role": role,
                "prompt": prompt
            })

        else:
            agent_id = f"agent_{uuid.uuid4().hex}"

            self.cache[agent_key] = {
                "agent_id": agent_id,
                "name": name,
                "role": role,
                "prompt": prompt
            }

        self._save()
        return agent_id


    def get(self, agent_key: str) -> Optional[AgentInfo]:
        if agent_key not in self.cache:
            return None

        data = self.cache[agent_key]

        return AgentInfo(
            key=agent_key,
            id=data["agent_id"],
            name=data["name"],
            role=data["role"],
            prompt=data["prompt"]
        )


    def resolve(self, agent_id: str) -> Optional[str]:
        for key, value in self.cache.items():
            if value["agent_id"] == agent_id:
                return key
        return None


    def list_agents(self) -> List[AgentInfo]:
        return [
            AgentInfo(
                key=k,
                id=v["agent_id"],
                name=v["name"],
                role=v["role"],
                prompt=v["prompt"]
            )
            for k, v in self.cache.items()
        ]