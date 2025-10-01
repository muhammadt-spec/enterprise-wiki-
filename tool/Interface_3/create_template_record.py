import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateTemplateRecord(Tool):
    """Simple template creation (Active status)."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table: return "1"
        try: return str(max(int(k) for k in table.keys()) + 1)
        except Exception: return str(len(table) + 1)
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, scope: str, owner_id: str,
               sensitivity: str, sections: Dict[str, Any], space_id: Optional[str] = None) -> str:
        templates = data.get("templates", {}); users = data.get("users", {}); spaces = data.get("spaces", {})
        if owner_id not in users: return json.dumps({"error":"Owner user not found"})
        if scope not in {"Global","Space"}: return json.dumps({"error":"Invalid scope (Global | Space)"})
        if scope=="Space" and (not space_id or space_id not in spaces): return json.dumps({"error":"Space scope requires valid space_id"})
        if sensitivity not in {"Normal","Official"}: return json.dumps({"error":"Invalid sensitivity (Normal | Official)"})
        for t in templates.values():
            if t.get("scope")==scope and (t.get("space_id") or None)==(space_id or None) and (t.get("name") or "").lower()==name.lower():
                return json.dumps({"error":"Template with same name exists in scope"})
        new_id = CreateTemplateRecord._generate_id(templates)
        rec={"template_id":new_id,"name":name,"scope":scope,"space_id":space_id,"owner_id":owner_id,
             "sensitivity":sensitivity,"status":"Active","sections_json":json.dumps(sections),
             "review_due_at":None,"created_at":"2025-10-01T00:00:00","updated_at":"2025-10-01T00:00:00"}
        templates[new_id]=rec
        return json.dumps(rec)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"create_template_record","description":"Create a new template at Global or Space scope.","parameters":{"type":"object","properties":{"name":{"type":"string","description":"Template name"},"scope":{"type":"string","description":"Scope (Global | Space)"},"owner_id":{"type":"string","description":"Owner user_id"},"sensitivity":{"type":"string","description":"Sensitivity (Normal | Official)"},"sections":{"type":"object","description":"Sections JSON payload"},"space_id":{"type":"string","description":"Required if scope=Space: space_id"}},"required":["name","scope","owner_id","sensitivity","sections"]}}}
