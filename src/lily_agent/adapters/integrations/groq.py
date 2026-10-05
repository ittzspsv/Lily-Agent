import json
from typing import Any, Dict, List, Optional

from ..adapter import AgentAdapter
from ...schemas import Message, LLMResponse, ToolCall, ResponseType
from ...exceptions.adapter import AdapterError
from ...utils import stringify

class GroqAdapter(AgentAdapter):
    def __init__(
        self,
        model: str,
        base_endpoint: Optional[str] = None,
        path: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 300.0,
        temperature: Optional[float] = None,
        reasoning_effort: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            model,
            base_endpoint or "https://api.groq.com/openai",
            path or "/v1/chat/completions",
            api_key,
            timeout,
            **kwargs,
        )
        self.temperature = temperature
        self.reasoning_effort = reasoning_effort

    def _build_request(self, messages: List[Message], tools: List[dict]) -> dict:
        mapped_messages: List[Dict[str, Any]] = []

        for message in messages:
            role = getattr(message.role, "value", message.role)
            content = message.content

            if role == "tool_result":
                mapped: Dict[str, Any] = {"role": "tool", "content": stringify(content)}
                if message.tool_call_id:
                    mapped["tool_call_id"] = message.tool_call_id
            elif role == "assistant" and isinstance(content, dict):
                mapped = {"role": "assistant", "content": content.get("content") or ""}
                if content.get("tool_calls"):
                    mapped["tool_calls"] = content["tool_calls"]
            else:
                mapped = {"role": role, "content": stringify(content)}

            mapped_messages.append(mapped)

        request: Dict[str, Any] = {
            "model": self.model,
            "messages": mapped_messages,
        }

        if self.reasoning_effort:
            request["reasoning_effort"] = self.reasoning_effort
        elif not self.think:
            request["reasoning_effort"] = "none"

        if self.temperature is not None:
            request["temperature"] = self.temperature

        if tools:
            request["tools"] = tools
            request["tool_choice"] = "auto"

        return request

    def _parse_response(self, response: Any) -> LLMResponse:
        if not isinstance(response, dict):
            raise AdapterError(f"Unexpected Groq response type: {type(response).__name__}")

        if response.get("error"):
            raise AdapterError(f"Groq returned an error: {response['error']}")

        choices = response.get("choices")
        if not choices:
            raise AdapterError("No choices returned from Groq response")

        message = choices[0].get("message")
        if not isinstance(message, dict):
            raise AdapterError("Groq response choice has no message")

        content = message.get("content")
        raw = {**response, "message": message}
        raw_tool_calls = message.get("tool_calls")

        if not raw_tool_calls:
            return LLMResponse(
                type=ResponseType.Text,
                content=content,
                tool_calls=None,
                raw=raw,
            )

        tool_calls: List[ToolCall] = []

        for tool_call in raw_tool_calls:
            function = tool_call.get("function")
            if not isinstance(function, dict):
                raise AdapterError("Tool call missing 'function'")

            name = function.get("name")
            if not name:
                raise AdapterError("Tool call missing 'name'")

            call_id = tool_call.get("id")
            if not call_id:
                raise AdapterError("Tool call missing 'id'")

            arguments = function.get("arguments") or "{}"
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError as error:
                    raise AdapterError(f"Tool call arguments are not valid JSON: {error}") from error

            if not isinstance(arguments, dict):
                raise AdapterError("Tool call arguments must be a JSON object")

            tool_calls.append(ToolCall(id=call_id, name=name, input=arguments))

        return LLMResponse(
            type=ResponseType.ToolCall,
            content=content,
            tool_calls=tool_calls,
            raw=raw,
        )