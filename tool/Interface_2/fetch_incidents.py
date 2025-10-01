import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class FetchIncidents(Tool):
    """Retrieve incidents with optional filters."""
    @staticmethod
    def invoke(data: Dict[str, Any], status: Optional[str] = None, priority: Optional[str] = None,
               service_id: Optional[str] = None, ci_id: Optional[str] = None) -> str:
        incidents = data.get("incidents", {})
        results: List[Dict[str, Any]] = []
        for inc in incidents.values():
            if status and inc.get("status") != status: continue
            if priority and inc.get("priority") != priority: continue
            if service_id and inc.get("service_id") != service_id: continue
            if ci_id and inc.get("ci_id") != ci_id: continue
            results.append(inc)
        return json.dumps(results)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"fetch_incidents","description":"Retrieve incidents with optional filters.","parameters":{"type":"object","properties":{"status":{"type":"string","description":"Filter by status (New | Assigned | In_Progress | Resolved | Closed)"},"priority":{"type":"string","description":"Filter by priority (P1 | P2 | P3 | P4 | P5)"},"service_id":{"type":"string","description":"Filter by related service_id"},"ci_id":{"type":"string","description":"Filter by related configuration item id"}},"required":[]}}}
