from ..adapter import AgentAdapter
from typing import List, Any, Dict, Optional
from ...schemas import LLMResponse, Message, ToolCall, ResponseType, MessageRole
from ...exceptions.adapter import AdapterError
from ...utils import split_intent

import json


class OllamaAdapter(AgentAdapter):
    def __init__(
        self,
        model: str,
        base_endpoint: Optional[str] = "http://localhost:11434",
        path: Optional[str] = "/api/chat",
        api_key: Optional[str] = None,
        timeout: float = 300.0,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            model=model, 
            base_endpoint=base_endpoint, 
            path=path, 
            api_key=api_key, 
            timeout=timeout, 
            **kwargs
        )

    def _build_request(self, messages: List[Message], tools: List[dict]) -> dict:
        """
        ### Definition
        - Builds the request payload for the LLM.
        ### Parameters
        - **messages**: `List[Message]` => Message objects to convert into the compatible format
        - **tools**: `List[dict]` => Tools to include in the payload
        ### Returns
        - `dict` => the request body
        """
        messages_list: List[Dict[str, Any]] = []

        for message in messages:
            role = message.role
            content = message.content

            if role == MessageRole.Assistant and isinstance(content, dict):
                mapped = {
                    "role": MessageRole.Assistant.value,
                    "content": content.get("content") or "",
                }

                if content.get("tool_calls"):
                    mapped["tool_calls"] = content["tool_calls"]

            else:
                if content is None:
                    content = ""
                elif isinstance(content, (dict, list)):
                    content = json.dumps(content)
                elif not isinstance(content, str):
                    content = str(content)

                mapped = {"content": content}

                if role == MessageRole.ToolResult:
                    mapped["role"] = "tool"

                    if message.tool_call_id:
                        mapped["tool_call_id"] = message.tool_call_id
                else:
                    mapped["role"] = role

            messages_list.append(mapped)

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages_list,
            "stream": False,
            "think": self.think,
        }

        if tools:
            payload["tools"] = tools

        return payload

    def _parse_response(self, response: Any) -> LLMResponse:
        """
        ### Definition
        - Parses the raw API response into a structured LLMResponse
        ### Raises
        - `AdapterError` => if the response, message or any tool call is malformed
        """
        if not isinstance(response, dict):
            raise AdapterError(f"Unexpected Ollama response type: {type(response).__name__}")

        if response.get("error"):
            raise AdapterError(f"Ollama returned an error: {response['error']}")

        message = response.get("message")
        if not isinstance(message, dict):
            raise AdapterError("Ollama response has no message")

        content = message.get("content")
        raw_tool_calls = message.get("tool_calls")

        if not raw_tool_calls:
            return LLMResponse(
                type=ResponseType.Text,
                content=content,
                tool_calls=None,
                raw=response,
            )

        tool_calls: List[ToolCall] = []

        for index, tool_call in enumerate(raw_tool_calls):
            function = tool_call.get("function")
            if not isinstance(function, dict):
                raise AdapterError("Tool call missing 'function'")

            name = function.get("name")
            if not name:
                raise AdapterError("Tool call missing 'name'")

            call_id = tool_call.get("id") or f"call_{index}"

            arguments = function.get("arguments") or {}
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError as error:
                    raise AdapterError(f"Tool call arguments are not valid JSON: {error}") from error

            if not isinstance(arguments, dict):
                raise AdapterError("Tool call arguments must be a JSON object")

            intent, arguments = split_intent(arguments)

            tool_calls.append(
                ToolCall(id=call_id, name=name, input=arguments, description=intent)
            )

        return LLMResponse(
            type=ResponseType.ToolCall,
            content=content,
            tool_calls=tool_calls,
            raw=response,
        )