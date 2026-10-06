from dataclasses import dataclass
from typing import Optional

import random

@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0                 
    jitter: bool = True
    max_retry_after: Optional[float] = 60.0

    def delay_for(self, attempt: int, retry_after: Optional[float]) -> Optional[float]:
        if retry_after is not None:
            if self.max_retry_after is not None and retry_after > self.max_retry_after:
                return None
            if not self.jitter:
                return retry_after
            return retry_after + random.uniform(0, max(0.5, retry_after * 0.1))

        backoff = min(self.max_delay, self.base_delay * 2 ** (attempt - 1))
        if self.jitter:
            return backoff / 2 + random.uniform(0, backoff / 2)
        return backoff