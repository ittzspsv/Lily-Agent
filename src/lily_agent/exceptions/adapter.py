class AdapterError(Exception):
    def __init__(self, message: str):
        super().__init__(f"An adapter error occurred: '{message}'")


class RateLimitExceeded(Exception):
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        *,
        retry_after: float | None = None,
        limit: int | None = None,
        remaining: int | None = None,
        provider: str | None = None,
    ) -> None:
        super().__init__(message)

        self.retry_after = retry_after
        self.limit = limit
        self.remaining = remaining
        self.provider = provider