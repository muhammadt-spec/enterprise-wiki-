import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class FormGroupCatalogEntry(Tool):
    """Create a new group in groups table."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        try:
            return str(max(int(k) for k in table.keys()) + 1)
        except Exception:
            return str(len(table) + 1)

    @staticmethod
    def invoke(data: Dict[str, Any], group_name: str, description: Optional[str] = None) -> str:
        groups = data.get("groups", {})
        for g in groups.values():
            if (g.get("group_name") or "").lower() == group_name.lower():
                return json.dumps({"error": "Group name already exists"})
        new_id = FormGroupCatalogEntry._generate_id(groups)
        rec = {"group_id": new_id, "group_name": group_name, "description": description,
               "created_at":"2025-10-01T00:00:00","updated_at":"2025-10-01T00:00:00"}
        groups[new_id] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info():
        return {
            "type":"function",
            "function":{
                "name":"form_group_catalog_entry",
                "description":"Create a new group.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "group_name":{"type":"string","description":"Unique group name"},
                        "description":{"type":"string","description":"Group description"}
                    },
                    "required":["group_name"]
                }
            }
        }
