import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class ResolveSpaceByKey(Tool):
    """Retrieve space by exact space_key."""
    @staticmethod
    def invoke(data: Dict[str, Any], space_key: str) -> str:
        spaces = data.get("spaces", {})
        for s in spaces.values():
            if (s.get("space_key") or "").lower() == space_key.lower():
                return json.dumps(s)
        return json.dumps([])
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"resolve_space_by_key","description":"Get a space record by its space_key.","parameters":{"type":"object","properties":{"space_key":{"type":"string","description":"Exact space key"}},"required":["space_key"]}}}
