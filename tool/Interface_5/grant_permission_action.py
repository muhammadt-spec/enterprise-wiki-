import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class GrantPermissionAction(Tool):
    """Grant a permission to a user or group (permission_grants table)."""
    @staticmethod
    def invoke(data: Dict[str, Any], permission_set_id: str, subject_type: str,
               subject_id: str, action: str) -> str:
        permission_sets = data.get("permission_sets", {})
        permission_grants = data.get("permission_grants", {})
        users = data.get("users", {})
        groups = data.get("groups", {})
        if permission_set_id not in permission_sets:
            return json.dumps({"error":"Permission set not found"})
        if subject_type not in {"user","group"}:
            return json.dumps({"error":"Invalid subject_type; allowed (user | group)"})
        if subject_type=="user" and subject_id not in users:
            return json.dumps({"error":"User not found"})
        if subject_type=="group" and subject_id not in groups:
            return json.dumps({"error":"Group not found"})
        if action not in {"view","edit","delete","admin","comment","attach"}:
            return json.dumps({"error":"Invalid action"})
        key=f"{permission_set_id}:{subject_type}:{subject_id}:{action}"
        if key in permission_grants:
            return json.dumps({"error":"Grant already exists"})
        rec={"permission_set_id":permission_set_id,"subject_type":subject_type,"subject_id":subject_id,"action":action}
        permission_grants[key]=rec
        return json.dumps(rec)

    @staticmethod
    def get_info():
        return {
            "type":"function",
            "function":{
                "name":"grant_permission_action",
                "description":"Grant a permission action to a user or group within a permission_set.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "permission_set_id":{"type":"string","description":"Permission set ID"},
                        "subject_type":{"type":"string","description":"Subject type (user | group)"},
                        "subject_id":{"type":"string","description":"User ID or Group ID"},
                        "action":{"type":"string","description":"Action to grant (view | edit | delete | admin | comment | attach)"}
                    },
                    "required":["permission_set_id","subject_type","subject_id","action"]
                }
            }
        }
