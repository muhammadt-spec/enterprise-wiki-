import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateLabelEntry(Tool):
    """Create a label (labels table) respecting uniqueness (scope, space_id, label_text)."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        try:
            return str(max(int(k) for k in table.keys()) + 1)
        except Exception:
            return str(len(table) + 1)

    @staticmethod
    def invoke(data: Dict[str, Any], label_text: str, scope: str = "Global",
               space_id: Optional[str] = None, created_by: Optional[str] = None) -> str:
        labels = data.get("labels", {})
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        if scope not in {"Global","Space"}:
            return json.dumps({"error":"Invalid scope; allowed (Global | Space)"})
        if scope=="Space" and (not space_id or space_id not in spaces):
            return json.dumps({"error":"Space scope requires valid space_id"})
        if created_by and created_by not in users:
            return json.dumps({"error":"created_by user not found"})
        for lv in labels.values():
            if lv.get("scope")==scope and (lv.get("space_id") or None)==(space_id or None) and (lv.get("label_text") or "").lower()==label_text.lower():
                return json.dumps({"error":"Label already exists in scope"})
        new_id = CreateLabelEntry._generate_id(labels)
        rec={"label_id":new_id,"label_text":label_text,"scope":scope,"space_id":space_id,
             "created_by":created_by,"created_at":"2025-10-01T00:00:00"}
        labels[new_id]=rec
        return json.dumps(rec)

    @staticmethod
    def get_info():
        return {
            "type":"function",
            "function":{
                "name":"create_label_entry",
                "description":"Create a new label in Global or Space scope.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "label_text":{"type":"string","description":"Label text"},
                        "scope":{"type":"string","description":"Label scope (Global | Space)"},
                        "space_id":{"type":"string","description":"Required if scope=Space: target space_id"},
                        "created_by":{"type":"string","description":"User ID creating this label"}
                    },
                    "required":["label_text"]
                }
            }
        }
