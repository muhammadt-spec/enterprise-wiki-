import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class PersistConfigurationItem(Tool):
    """Create a configuration item (CI) with enum-validated fields."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table: return "1"
        try: return str(max(int(k) for k in table.keys()) + 1)
        except Exception: return str(len(table) + 1)
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, ci_type: str, environment: str, status: str,
               service_id: Optional[str] = None, owner_group_id: Optional[str] = None) -> str:
        cis = data.get("configuration_items", {}); services = data.get("services", {}); groups = data.get("groups", {})
        if ci_type not in {"App","Service","Server","DB","Network","Storage","Endpoint","Other"}: return json.dumps({"error":"Invalid ci_type (App | Service | Server | DB | Network | Storage | Endpoint | Other)"})
        if environment not in {"Prod","Staging","Dev","Test"}: return json.dumps({"error":"Invalid environment (Prod | Staging | Dev | Test)"})
        if status not in {"Active","Maintenance","Retired"}: return json.dumps({"error":"Invalid status (Active | Maintenance | Retired)"})
        if service_id and service_id not in services: return json.dumps({"error":"Service not found"})
        if owner_group_id and owner_group_id not in groups: return json.dumps({"error":"Owner group not found"})
        for v in cis.values():
            if (v.get("name") or "").lower()==name.lower(): return json.dumps({"error":"CI name must be unique"})
        new_id = PersistConfigurationItem._generate_id(cis)
        rec={"ci_id":new_id,"name":name,"ci_type":ci_type,"environment":environment,"status":status,"service_id":service_id,
             "owner_group_id":owner_group_id,"created_at":"2025-10-01T00:00:00","updated_at":"2025-10-01T00:00:00"}
        cis[new_id]=rec
        return json.dumps(rec)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"persist_configuration_item","description":"Create a new configuration item (CI).","parameters":{"type":"object","properties":{"name":{"type":"string","description":"Unique CI name"},"ci_type":{"type":"string","description":"CI type (App | Service | Server | DB | Network | Storage | Endpoint | Other)"},"environment":{"type":"string","description":"Environment (Prod | Staging | Dev | Test)"},"status":{"type":"string","description":"CI status (Active | Maintenance | Retired)"},"service_id":{"type":"string","description":"Linked service_id"},"owner_group_id":{"type":"string","description":"Owner group_id"}},"required":["name","ci_type","environment","status"]}}}
