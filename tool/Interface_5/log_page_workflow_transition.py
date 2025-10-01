import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class LogPageWorkflowTransition(Tool):
    """Record a workflow transition for a page (workflow_transitions table)."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        try:
            return str(max(int(k) for k in table.keys()) + 1)
        except Exception:
            return str(len(table) + 1)

    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, from_state: str, to_state: str,
               action: str, actor_id: str, comment: Optional[str] = None) -> str:
        pages = data.get("pages", {})
        users = data.get("users", {})
        transitions = data.get("workflow_transitions", {})
        if page_id not in pages:
            return json.dumps({"error":"Page not found"})
        if actor_id not in users:
            return json.dumps({"error":"Actor user not found"})
        if action not in {"submit","approve","reject","request_changes","publish","retire"}:
            return json.dumps({"error":"Invalid action"})
        new_id = LogPageWorkflowTransition._generate_id(transitions)
        rec={"transition_id":new_id,"page_id":page_id,"from_state":from_state,"to_state":to_state,
             "action":action,"actor_id":actor_id,"comment":comment,"timestamp":"2025-10-01T00:00:00"}
        transitions[new_id]=rec
        p=pages[page_id]
        p["workflow_state"]=to_state
        p["last_modified_by"]=actor_id
        p["last_modified_at"]="2025-10-01T00:00:00"
        p["updated_at"]="2025-10-01T00:00:00"
        return json.dumps(rec)

    @staticmethod
    def get_info():
        return {
            "type":"function",
            "function":{
                "name":"log_page_workflow_transition",
                "description":"Create a workflow transition entry for a page and update its workflow_state.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "page_id":{"type":"string","description":"Target page_id"},
                        "from_state":{"type":"string","description":"Previous state"},
                        "to_state":{"type":"string","description":"New state"},
                        "action":{"type":"string","description":"Transition action (submit | approve | reject | request_changes | publish | retire)"},
                        "actor_id":{"type":"string","description":"User ID of actor"},
                        "comment":{"type":"string","description":"Optional comment"}
                    },
                    "required":["page_id","from_state","to_state","action","actor_id"]
                }
            }
        }
