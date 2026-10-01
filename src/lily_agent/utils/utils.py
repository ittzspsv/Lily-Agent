from typing import Any

import json

def stringify(content: Any) -> Any:
        if isinstance(content, (dict, list)):
            return json.dumps(content)
        return content