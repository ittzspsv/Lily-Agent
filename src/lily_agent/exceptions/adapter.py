from typing import Optional


class AdapterError(Exception):
    def __init__(self, message: str):
        super().__init__(f"An adapter error occurred: '{message}'")



class RetryableAdapterError(AdapterError):
    """Failures where retrying the same request may succeed."""
    def __init__(self, message: str, *, retry_after: Optional[float] = None,
                 provider: Optional[str] = None, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.retry_after = retry_after 
        self.provider = provider
        self.status_code = status_code


class RateLimitError(RetryableAdapterError):
    def __init__(self, message: str, *, limit_type: Optional[str] = None, **kwargs) -> None:
        super().__init__(message, **kwargs)
        self.limit_type = limit_type     

class TransientAdapterError(RetryableAdapterError):
    pass