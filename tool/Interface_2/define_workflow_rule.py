import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class DefineWorkflowRule(Tool):
    """Create a workflow (enabled flag, steps_json payload)."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table: return "1"
        try: return str(max(int(k) for k in table.keys()) + 1)
        except Exception: return str(len(table) + 1)
    @staticmethod
    def _find_space_id_by_key(spaces: Dict[str, Any], space_key: Optional[str]) -> Optional[str]:
        if not space_key: return None
        for sid, s in spaces.items():
            if (s.get("space_key") or "").lower() == (space_key or "").lower():
                return sid
        return None
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, scope: str, steps: Dict[str, Any],
               enabled: bool = True, space_key: Optional[str] = None) -> str:
        workflows = data.get("workflows", {})
        spaces = data.get("spaces", {})
        if scope not in {"Global","Space"}: return json.dumps({"error":"Invalid scope; allowed (Global | Space)"})
        space_id=None
        if scope=="Space":
            space_id=DefineWorkflowRule._find_space_id_by_key(spaces, space_key)
            if not space_id: return json.dumps({"error":"Space not found for workflow scope"})
        for w in workflows.values():
            if (w.get("space_id") or None)==(space_id or None) and (w.get("name") or "").lower()==name.lower():
                return json.dumps({"error":"Workflow with same name already exists in scope"})
        new_id = DefineWorkflowRule._generate_id(workflows)
        rec={"workflow_id":new_id,"name":name,"scope":scope,"space_id":space_id,
             "steps_json":json.dumps(steps),"enabled":bool(enabled),
             "created_at":"2025-10-01T00:00:00","updated_at":"2025-10-01T00:00:00"}
        workflows[new_id]=rec
        return json.dumps(rec)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"define_workflow_rule","description":"Create a workflow with steps (JSON) at Global or Space scope.","parameters":{"type":"object","properties":{"name":{"type":"string","description":"Workflow name"},"scope":{"type":"string","description":"Workflow scope (Global | Space)"},"steps":{"type":"object","description":"Steps JSON payload for the workflow"},"enabled":{"type":"boolean","description":"Enable workflow (True/False)"},"space_key":{"type":"string","description":"Required if scope is Space: space key"}},"required":["name","scope","steps"]}}}
