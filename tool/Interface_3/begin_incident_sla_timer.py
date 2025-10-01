import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class BeginIncidentSlaTimer(Tool):
    """Start tracking an SLA against an incident (incident_slas table)."""
    @staticmethod
    def invoke(data: Dict[str, Any], incident_id: str, sla_id: str, started_at: str,
               response_due_at: Optional[str] = None, resolution_due_at: Optional[str] = None) -> str:
        incidents = data.get("incidents", {}); slas = data.get("slas", {}); incident_slas = data.get("incident_slas", {})
        if incident_id not in incidents: return json.dumps({"error":"Incident not found"})
        if sla_id not in slas: return json.dumps({"error":"SLA not found"})
        key=f"{incident_id}:{sla_id}:{started_at}"
        if key in incident_slas: return json.dumps({"error":"Incident SLA instance already exists"})
        rec={"incident_id":incident_id,"sla_id":sla_id,"started_at":started_at,
             "response_due_at":response_due_at,"resolution_due_at":resolution_due_at,
             "first_response_at":None,"resolved_at":None,
             "response_breached":False,"resolution_breached":False}
        incident_slas[key]=rec
        return json.dumps(rec)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"begin_incident_sla_timer","description":"Create an incident SLA tracking instance.","parameters":{"type":"object","properties":{"incident_id":{"type":"string","description":"Incident ID"},"sla_id":{"type":"string","description":"SLA ID to apply"},"started_at":{"type":"string","description":"Start date (YYYY-MM-DD)"},"response_due_at":{"type":"string","description":"Response due date (YYYY-MM-DD)"},"resolution_due_at":{"type":"string","description":"Resolution due date (YYYY-MM-DD)"}},"required":["incident_id","sla_id","started_at"]}}}
