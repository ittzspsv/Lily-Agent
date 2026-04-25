from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from .embedder_exceptions import EmbedderError

import httpx

class Embedder(ABC):
    def __init__(
            self, 
            model: str,
            dimensions: int,
            base_endpoint: Optional[str]=None, 
            route: Optional[str]=None,
            api_key: Optional[str]=None,
            timeout: float = 30.0,
            **kwargs
    ) -> None:

        self.model = model
        self.dimensions = dimensions
        self.base_endpoint = base_endpoint or ""
        self.route = route or ""
        self.api_key = api_key
        self.config = kwargs
        self.timeout = timeout

        self._network_client = httpx.AsyncClient(timeout=timeout)


    async def embed(self, text: str) -> List[float]:
        payload = self._build_payload(text)

        try:
            response = await self._network_client.post(self.endpoint, json=payload)

            response.raise_for_status()

            data = response.json()

            embedding = self._parse_response(data)
            if len(embedding) != self.dimensions:
                raise ValueError(f"Expected {self.dimensions} got {len(embedding)}")
            
            return embedding
        
        except httpx.ConnectError as e:
            raise EmbedderError(f"Could not connect to {self.base_endpoint}.") from e
        
        except httpx.TimeoutException as e:
          raise EmbedderError("Request timed out") from e
        
        except httpx.HTTPStatusError as e:
            response_status: int = e.response.status_code

            if response_status == 404:
                raise EmbedderError(f"The response returned {e.response.status_code}") from e
            elif response_status == 401:
                raise EmbedderError("Unauthorized (401)") from e
            elif response_status == 403:
                raise EmbedderError("Forbidden (403)") from e
            else:
                raise EmbedderError(f"HTTP error {response_status}: {e.response.text}") from e
    
    @abstractmethod
    def _build_payload(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def _parse_response(self, data: Dict[str, Any]) -> List[float]:
        raise NotImplementedError

    @property
    def endpoint(self):
        return f"{self.base_endpoint.rstrip('/')}/{self.route.lstrip('/')}"