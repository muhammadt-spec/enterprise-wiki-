import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class ListPermissionsForTarget(Tool):
    """Return permission_set and grants for a given target_id (by matching permission_sets.target_id)."""
    @staticmethod
    def invoke(data: Dict[str, Any], target_id: str) -> str:
        permission_sets = data.get("permission_sets", {}); permission_grants = data.get("permission_grants", {})
        results: List[Dict[str, Any]] = []
        for psid, ps in permission_sets.items():
            if ps.get("target_id") == target_id:
                grants = [g for g in permission_grants.values() if g.get("permission_set_id") == psid]
                results.append({"permission_set": ps, "grants": grants})
        return json.dumps(results)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"list_permissions_for_target","description":"List permission sets and grants for a target entity (space/page/global).","parameters":{"type":"object","properties":{"target_id":{"type":"string","description":"Target entity id (space_id or page_id or global target id)"}},"required":["target_id"]}}}
