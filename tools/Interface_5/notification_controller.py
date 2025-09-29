import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class notification_controller(Tool):
    @staticmethod
    def _now()->str:
        return "2025-10-01T00:00:00"

    @staticmethod
    def _gen_id(tbl: Dict[str, Any])->str:
        if not tbl: return "1"
        return str(max(int(k) for k in tbl.keys()) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        email_or_group: str,
        type: str,
        _class: str,
        requester_id: str,
        reference_id: Optional[str] = None,
        approval_code: Optional[str] = None,
        comment: Optional[str] = None
    )->str:
        users = data.get("users", {})
        groups = data.get("groups", {})
        notifications = data.setdefault("notifications", {})

        if str(requester_id) not in users:
            return json.dumps({"error": f"requester_id {requester_id} not found"})

        if type not in ["alert","report","reminder"]:
            return json.dumps({"error":"type must be one of (alert|report|reminder)"})
        if _class not in ["space","page","template","workflow","integration"]:
            return json.dumps({"error":"class must be one of (space|page|template|workflow|integration)"})

        recipient_email = None
        recipient_group_id = None
        if email_or_group in groups:
            recipient_group_id = email_or_group
        else:
            recipient_email = email_or_group

        nid = notification_controller._gen_id(notifications)
        rec = {
            "notification_id": nid,
            "type": type,
            "class": _class,
            "recipient_email": recipient_email,
            "recipient_group_id": recipient_group_id,
            "reference_entity_type": _class,
            "reference_entity_id": reference_id,
            "status": "queued",
            "created_at": notification_controller._now(),
            "sent_at": None,
            "error_message": None
        }
        notifications[nid] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"notification_controller",
                "description":"Send alerts/reports/reminders for wiki events to users/groups.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "email_or_group":{"type":"string","description":"Recipient email or group_id"},
                        "type":{"type":"string","description":"Notification type (alert|report|reminder)"},
                        "class":{"type":"string","description":"Reference class (space|page|template|workflow|integration)"},
                        "requester_id":{"type":"string","description":"User id initiating the notification"},
                        "reference_id":{"type":"string","description":"Optional id of the referenced entity"},
                        "approval_code":{"type":"string","description":"Optional approval code"},
                        "comment":{"type":"string","description":"Optional comment"}
                    },
                    "required":["email_or_group","type","class","requester_id"]
                }
            }
        }
