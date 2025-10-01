import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateServiceRecord(Tool):
    """Create a service with business criticality enum."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table: return "1"
        try: return str(max(int(k) for k in table.keys()) + 1)
        except Exception: return str(len(table) + 1)
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, business_criticality: str, owner_group_id: str, status: str = "Active") -> str:
        services = data.get("services", {}); groups = data.get("groups", {})
        if owner_group_id not in groups: return json.dumps({"error":"Owner group not found"})
        if business_criticality not in {"Low","Medium","High","Critical"}: return json.dumps({"error":"Invalid business_criticality (Low | Medium | High | Critical)"})
        if status not in {"Active","Retired"}: return json.dumps({"error":"Invalid status (Active | Retired)"})
        for s in services.values():
            if (s.get("name") or "").lower()==name.lower(): return json.dumps({"error":"Service name must be unique"})
        new_id = CreateServiceRecord._generate_id(services)
        rec={"service_id":new_id,"name":name,"business_criticality":business_criticality,"owner_group_id":owner_group_id,
             "status":status,"created_at":"2025-10-01T00:00:00","updated_at":"2025-10-01T00:00:00"}
        services[new_id]=rec
        return json.dumps(rec)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"create_service_record","description":"Create a new service with business criticality.","parameters":{"type":"object","properties":{"name":{"type":"string","description":"Unique service name"},"business_criticality":{"type":"string","description":"Criticality (Low | Medium | High | Critical)"},"owner_group_id":{"type":"string","description":"Owner group_id"},"status":{"type":"string","description":"Service status (Active | Retired)"}},"required":["name","business_criticality","owner_group_id"]}}}
