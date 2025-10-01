import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class FindUserByEmailExact(Tool):
    """Retrieve a single user by exact email."""
    @staticmethod
    def invoke(data: Dict[str, Any], email: str) -> str:
        users = data.get("users", {})
        for u in users.values():
            if (u.get("email") or "").lower() == email.lower():
                return json.dumps(u)
        return json.dumps([])
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"find_user_by_email_exact","description":"Retrieve a user by exact email.","parameters":{"type":"object","properties":{"email":{"type":"string","description":"Exact email to match"}},"required":["email"]}}}
