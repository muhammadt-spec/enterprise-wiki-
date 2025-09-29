import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class audit_entry_create(Tool):
    @staticmethod
    def _now_iso() -> str:
        return "2025-10-01T00:00:00"

    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table:
            return "1"
        return str(max(int(k) for k in table.keys()) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        requester_id: str,
        meta: Optional[Dict[str, Any]] = None
    ) -> str:
        audit_tbl = data.get("audit_trail", {})
        users = data.get("users", {})

        if str(requester_id) not in users:
            return json.dumps({"error": f"requester_id {requester_id} not found"})

        audit_id = audit_entry_create._generate_id(audit_tbl)
        rec = {
            "audit_id": audit_id,
            "action": action,
            "actor_id": requester_id,
            "entity_type": (meta or {}).get("entity_type"),
            "entity_id": (meta or {}).get("entity_id"),
            "meta_json": json.dumps(meta or {}),
            "timestamp": audit_entry_create._now_iso(),
            "result": "logged",
            "error_message": None
        }
        audit_tbl[audit_id] = rec
        return json.dumps({"audit_id": audit_id, "success": True, "record": rec})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "audit_entry_create",
                "description": "Writes an audit log entry for any action executed or attempted.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "description": "Short name of the action performed"},
                        "requester_id": {"type": "string", "description": "ID of the requester/actor"},
                        "meta": {"type": "object", "description": "Optional metadata map (entity_type, filters, space_key, change_set_summary, scope, date_range, etc.)"}
                    },
                    "required": ["action", "requester_id"]
                }
            }
        }
