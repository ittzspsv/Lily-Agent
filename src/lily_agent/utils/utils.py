from typing import Any, Optional, Tuple
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

import json
import re

def stringify(content: Any) -> Any:
        if isinstance(content, (dict, list)):
            return json.dumps(content)
        return content



_duration = re.compile(r"(\d+(?:\.\d+)?)(ms|h|m|s)")
_unit = {"ms": 0.001, "s": 1.0, "m": 60.0, "h": 3600.0}

def parse_duration(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    parts = _duration.findall(value)
    return sum(float(n) * _unit[u] for n, u in parts) if parts else None

def parse_retry_after(value: Optional[str]) -> Optional[float]:
    """Retry-After is either delta-seconds or an HTTP date."""
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    try:
        when = parsedate_to_datetime(value)
        return max(0.0, (when - datetime.now(timezone.utc)).total_seconds())
    except (TypeError, ValueError):
        return None

def split_intent(arguments: dict) -> Tuple[Optional[str], dict]:
    args = dict(arguments)
    intent = args.pop("intent", None)
    if isinstance(intent, str) and intent.strip():
        return intent.strip(), args
    return None, args