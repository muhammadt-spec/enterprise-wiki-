import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class DefineSlaRule(Tool):
    """Create an SLA policy for a service+priority with response/resolution targets."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table: return "1"
        try: return str(max(int(k) for k in table.keys()) + 1)
        except Exception: return str(len(table) + 1)
    @staticmethod
    def invoke(data: Dict[str, Any], service_id: str, priority: str,
               response_target_minutes: int, resolution_target_minutes: int, active: bool = True) -> str:
        slas = data.get("slas", {}); services = data.get("services", {})
        if service_id not in services: return json.dumps({"error":"Service not found"})
        if priority not in {"P1","P2","P3","P4","P5"}: return json.dumps({"error":"Invalid priority (P1 | P2 | P3 | P4 | P5)"})
        for s in slas.values():
            if s.get("service_id")==service_id and s.get("priority")==priority:
                return json.dumps({"error":"SLA already exists for service+priority"})
        new_id = DefineSlaRule._generate_id(slas)
        rec={"sla_id":new_id,"service_id":service_id,"priority":priority,
             "response_target_minutes":int(response_target_minutes),
             "resolution_target_minutes":int(resolution_target_minutes),
             "active":bool(active),"created_at":"2025-10-01T00:00:00","updated_at":"2025-10-01T00:00:00"}
        slas[new_id]=rec
        return json.dumps(rec)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"define_sla_rule","description":"Create a new SLA policy for a service and priority.","parameters":{"type":"object","properties":{"service_id":{"type":"string","description":"Service ID"},"priority":{"type":"string","description":"Priority (P1 | P2 | P3 | P4 | P5)"},"response_target_minutes":{"type":"integer","description":"Response target in minutes"},"resolution_target_minutes":{"type":"integer","description":"Resolution target in minutes"},"active":{"type":"boolean","description":"Whether SLA is active (True/False)"}},"required":["service_id","priority","response_target_minutes","resolution_target_minutes"]}}}
