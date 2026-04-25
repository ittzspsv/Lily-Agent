from ..core.embedder import Embedder
from typing import Any, Dict, Optional, List

class OllamaEmbedder(Embedder):
    def __init__(
            self, 
            model: str, 
            dimensions: int,
            base_endpoint: Optional[str] = "", 
            route: Optional[str] = None, 
            api_key: Optional[str] = None, 
            timeout: float = 30, 
            **kwargs
    ) -> None:
        super().__init__(model, dimensions ,base_endpoint or "http://localhost:11434", route or "/api/embeddings", api_key, timeout, **kwargs)

    def _build_payload(self, text: str) -> Dict[str, Any]:
        return {
            "model": self.model,
            "prompt": text
        }
    
    def _parse_response(self, data: Dict[str, Any]) -> List[float]:
        if "embedding" not in data:
            raise ValueError(f"Invalid response {data}")

        embedding = data["embedding"]

        if not isinstance(embedding, list):
            raise TypeError("Embedding must be a list of floats")

        return embedding