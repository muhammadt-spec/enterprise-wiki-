import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class transfer_to_human(Tool):
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
        reason: str,
        context: Dict[str, Any]
    ) -> str:
        notif_tbl = data.get("notifications", {})
        nid = transfer_to_human._generate_id(notif_tbl)
        rec = {
            "notification_id": nid,
            "type": "escalation",
            "class": "sop",
            "recipient_email": None,
            "recipient_group_id": None,
            "reference_entity_type": context.get("entity_type"),
            "reference_entity_id": context.get("entity_id"),
            "status": "queued",
            "created_at": transfer_to_human._now_iso(),
            "sent_at": None,
            "error_message": None
        }
        notif_tbl[nid] = rec
        return json.dumps({"escalation_ref": nid, "reason": reason, "record": rec})

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "transfer_to_human",
                "description": "Halts the SOP and routes to a human operator when policy requires escalation.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reason": {"type": "string", "description": "Why escalation is needed"},
                        "context": {"type": "object", "description": "Context dict for the escalation (entity_type, entity_id, etc.)"}
                    },
                    "required": ["reason", "context"]
                }
            }
        }
