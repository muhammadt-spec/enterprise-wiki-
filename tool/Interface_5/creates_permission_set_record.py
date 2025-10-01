import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreatesPermissionSetRecord(Tool):
    """Create a permission_set for a target (Global | Space | Page)."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        try:
            return str(max(int(k) for k in table.keys()) + 1)
        except Exception:
            return str(len(table) + 1)

    @staticmethod
    def invoke(data: Dict[str, Any], level: str, target_id: str, version: str) -> str:
        permission_sets = data.get("permission_sets", {})
        if level not in {"Global","Space","Page"}:
            return json.dumps({"error":"Invalid level; allowed (Global | Space | Page)"})
        new_id = CreatesPermissionSetRecord._generate_id(permission_sets)
        rec = {"permission_set_id":new_id,"level":level,"target_id":target_id,"version":version,
               "created_at":"2025-10-01T00:00:00","updated_at":"2025-10-01T00:00:00"}
        permission_sets[new_id]=rec
        return json.dumps(rec)

    @staticmethod
    def get_info():
        return {
            "type":"function",
            "function":{
                "name":"creates_permission_set_record",
                "description":"Create a permission_set at Global, Space, or Page scope.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "level":{"type":"string","description":"Permission level (Global | Space | Page)"},
                        "target_id":{"type":"string","description":"ID of target entity (e.g., space_id or page_id)"},
                        "version":{"type":"string","description":"Version tag/label for the permission set"}
                    },
                    "required":["level","target_id","version"]
                }
            }
        }
