import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class OpenIncidentTicket(Tool):
    """Create an incident record respecting enum fields."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table: return "1"
        try: return str(max(int(k) for k in table.keys()) + 1)
        except Exception: return str(len(table) + 1)
    @staticmethod
    def invoke(data: Dict[str, Any], title: str, description_code: str, status: str, priority: str,
               impact: str, urgency: str, reporter_id: str, assignee_id: Optional[str] = None,
               assignment_group_id: Optional[str] = None, category: Optional[str] = None,
               subcategory: Optional[str] = None, ci_id: Optional[str] = None,
               problem_id: Optional[str] = None, service_id: Optional[str] = None,
               resolution_notes_code: Optional[str] = None) -> str:
        incidents = data.get("incidents", {}); users = data.get("users", {}); groups = data.get("groups", {})
        cis = data.get("configuration_items", {}); problems = data.get("problems", {}); services = data.get("services", {})
        if status not in {"New","Assigned","In_Progress","Resolved","Closed"}: return json.dumps({"error":"Invalid status (New | Assigned | In_Progress | Resolved | Closed)"})
        if priority not in {"P1","P2","P3","P4","P5"}: return json.dumps({"error":"Invalid priority (P1 | P2 | P3 | P4 | P5)"})
        if impact not in {"Low","Medium","High","Critical"}: return json.dumps({"error":"Invalid impact (Low | Medium | High | Critical)"})
        if urgency not in {"Low","Medium","High","Critical"}: return json.dumps({"error":"Invalid urgency (Low | Medium | High | Critical)"})
        if reporter_id not in users: return json.dumps({"error":"Reporter user not found"})
        if assignee_id and assignee_id not in users: return json.dumps({"error":"Assignee user not found"})
        if assignment_group_id and assignment_group_id not in groups: return json.dumps({"error":"Assignment group not found"})
        if ci_id and ci_id not in cis: return json.dumps({"error":"Configuration item not found"})
        if problem_id and problem_id not in problems: return json.dumps({"error":"Problem not found"})
        if service_id and service_id not in services: return json.dumps({"error":"Service not found"})
        new_id = OpenIncidentTicket._generate_id(incidents)
        rec={"incident_id":new_id,"title":title,"description_code":description_code,"status":status,"priority":priority,
             "impact":impact,"urgency":urgency,"reporter_id":reporter_id,"assignee_id":assignee_id,
             "assignment_group_id":assignment_group_id,"category":category,"subcategory":subcategory,"ci_id":ci_id,
             "problem_id":problem_id,"service_id":service_id,"resolution_notes_code":resolution_notes_code,
             "resolved_at":None,"closed_at":None,"created_at":"2025-10-01T00:00:00","updated_at":"2025-10-01T00:00:00"}
        incidents[new_id]=rec
        return json.dumps(rec)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"open_incident_ticket","description":"Create a new incident with enum-validated fields.","parameters":{"type":"object","properties":{"title":{"type":"string","description":"Incident title"},"description_code":{"type":"string","description":"Controlled description code"},"status":{"type":"string","description":"Incident status (New | Assigned | In_Progress | Resolved | Closed)"},"priority":{"type":"string","description":"Priority (P1 | P2 | P3 | P4 | P5)"},"impact":{"type":"string","description":"Impact (Low | Medium | High | Critical)"},"urgency":{"type":"string","description":"Urgency (Low | Medium | High | Critical)"},"reporter_id":{"type":"string","description":"Reporter user_id"},"assignee_id":{"type":"string","description":"Assignee user_id"},"assignment_group_id":{"type":"string","description":"Assignment group_id"},"category":{"type":"string","description":"Category (e.g., Hardware | Software | Network | Access | Security)"},"subcategory":{"type":"string","description":"Subcategory code"},"ci_id":{"type":"string","description":"Configuration item id"},"problem_id":{"type":"string","description":"Related problem id"},"service_id":{"type":"string","description":"Related service id"},"resolution_notes_code":{"type":"string","description":"Controlled resolution code"}},"required":["title","description_code","status","priority","impact","urgency","reporter_id"]}}}
