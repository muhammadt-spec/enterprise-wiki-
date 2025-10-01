import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class CreateRestrictionPolicy(Tool):
    """Create a restriction set (restrictions_id + type)."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table: return "1"
        try: return str(max(int(k) for k in table.keys()) + 1)
        except Exception: return str(len(table) + 1)
    @staticmethod
    def invoke(data: Dict[str, Any], restriction_type: str) -> str:
        restriction_sets = data.get("restriction_sets", {})
        if restriction_type not in {"none","edit_only","view_and_edit"}:
            return json.dumps({"error":"Invalid restriction_type (none | edit_only | view_and_edit)"})
        new_id = CreateRestrictionPolicy._generate_id(restriction_sets)
        rec={"restrictions_id":new_id,"type":restriction_type,"created_at":"2025-10-01T00:00:00","updated_at":"2025-10-01T00:00:00"}
        restriction_sets[new_id]=rec
        return json.dumps(rec)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"create_restriction_policy","description":"Create a restriction set to be applied on pages.","parameters":{"type":"object","properties":{"restriction_type":{"type":"string","description":"Restriction type (none | edit_only | view_and_edit)"}},"required":["restriction_type"]}}}
