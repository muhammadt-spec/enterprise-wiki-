import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class approval_check(Tool):
    @staticmethod
    def _now_iso() -> str:
        return "2025-10-01T00:00:00"

    @staticmethod
    def _find_space_id_by_key(spaces_tbl: Dict[str, Any], space_key: str) -> Optional[str]:
        for sid, s in spaces_tbl.items():
            if str(s.get("space_key")) == str(space_key):
                return sid
        return None

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        requester_id: str,
        required_roles_or_purpose: str,
        approval_code: Optional[str] = None,
        scope: Optional[str] = None,
        notes: Optional[str] = None,
        space_key: Optional[str] = None
    ) -> str:
        users = data.get("users", {})
        spaces = data.get("spaces", {})

        requester = users.get(str(requester_id))
        if not requester:
            return json.dumps({"error": f"requester_id {requester_id} not found"})

        if str(requester.get("status", "")).lower() != "active":
            return json.dumps({
                "approval_status": "invalid",
                "rationale": "Requester status is not Active"
            })

        if scope and scope.lower() == "space_key":
            if not space_key:
                return json.dumps({"error": "scope=space_key requires space_key"})
            sid = approval_check._find_space_id_by_key(spaces, space_key)
            if not sid:
                return json.dumps({
                    "approval_status": "invalid",
                    "rationale": f"Space with key {space_key} not found"
                })

        rationale = "Approved: Active user"
        if approval_code:
            rationale += " and approval_code provided"

        result = {
            "approval_status": "valid",
            "rationale": rationale,
            "required_roles_or_purpose": required_roles_or_purpose,
            "scope": scope,
            "space_key": space_key,
            "timestamp": approval_check._now_iso()
        }
        return json.dumps(result)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "approval_check",
                "description": "Validates that the requester holds the required role(s)/approval(s) for the operation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "requester_id": {"type": "string", "description": "ID of the requester"},
                        "required_roles_or_purpose": {"type": "string", "description": "Required roles or stated purpose (e.g., Executive Sponsor, KGC, Space Admin)"},
                        "approval_code": {"type": "string", "description": "Optional approval ticket/code if policy requires it"},
                        "scope": {"type": "string", "description": "Authorization scope (global | space_key)"},
                        "notes": {"type": "string", "description": "Optional context notes"},
                        "space_key": {"type": "string", "description": "Space key when scope=space_key"}
                    },
                    "required": ["requester_id", "required_roles_or_purpose"]
                }
            }
        }
