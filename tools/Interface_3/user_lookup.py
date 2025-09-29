import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class user_lookup(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        requester_id: str,
        user_id: Optional[str] = None,
        email: Optional[str] = None,
        role: Optional[str] = None,
        status: Optional[str] = None,
        name: Optional[str] = None
    ) -> str:
        users = data.get("users", {})
        if str(requester_id) not in users:
            return json.dumps({"error": f"requester_id {requester_id} not found"})

        results: List[Dict[str, Any]] = []
        for u in users.values():
            if user_id and str(u.get("user_id")) != str(user_id):
                continue
            if email and str(u.get("email", "")).lower() != str(email).lower():
                continue
            if status and str(u.get("status", "")).lower() != str(status).lower():
                continue
            if name and (name.lower() not in str(u.get("full_name", "")).lower()):
                continue
            results.append(u)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"user_lookup",
                "description":"Find users by filters.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "requester_id":{"type":"string","description":"ID of the requester"},
                        "user_id":{"type":"string","description":"Filter by user_id"},
                        "email":{"type":"string","description":"Filter by email"},
                        "role":{"type":"string","description":"Filter by role (not present in this schema; ignored)"},
                        "status":{"type":"string","description":"Filter by status (Active | Suspended | Deactivated)"},
                        "name":{"type":"string","description":"Partial match on full_name"}
                    },
                    "required":["requester_id"]
                }
            }
        }
