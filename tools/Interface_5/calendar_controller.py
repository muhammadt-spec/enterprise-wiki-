import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class calendar_controller(Tool):
    @staticmethod
    def _now()->str:
        return "2025-10-01T00:00:00"

    @staticmethod
    def _gen_id(tbl: Dict[str, Any])->str:
        if not tbl: return "1"
        return str(max(int(k) for k in tbl.keys()) + 1)

    @staticmethod
    def _space_id_by_key(spaces: Dict[str, Any], key: str)->Optional[str]:
        for sid, s in spaces.items():
            if str(s.get("space_key")) == str(key):
                return sid
        return None

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        space_key: Optional[str] = None,
        calendar_name: Optional[str] = None,
        calendar_id: Optional[str] = None,
        event: Optional[Dict[str, Any]] = None,
        event_id: Optional[str] = None
    )->str:
        spaces = data.get("spaces", {})
        calendars = data.setdefault("calendars", {})
        events = data.setdefault("calendar_events", {})
        users = data.get("users", {})

        if action == "create":
            if not space_key or not calendar_name:
                return json.dumps({"error":"space_key and calendar_name required"})
            sid = calendar_controller._space_id_by_key(spaces, space_key)
            if not sid:
                return json.dumps({"error": f"space_key {space_key} not found"})
            cid = calendar_controller._gen_id(calendars)
            rec = {
                "calendar_id": cid,
                "space_id": sid,
                "name": calendar_name,
                "created_by": None,
                "created_at": calendar_controller._now(),
                "updated_at": calendar_controller._now()
            }
            calendars[cid] = rec
            return json.dumps(rec)

        if action == "add_event":
            if not calendar_id or str(calendar_id) not in calendars:
                return json.dumps({"error":"valid calendar_id required"})
            if not event or not isinstance(event, dict):
                return json.dumps({"error":"event dict required: {title, start, end, type, created_by}"})
            for req in ["title","start","end","type","created_by"]:
                if req not in event:
                    return json.dumps({"error": f"event.{req} is required"})
            if str(event["created_by"]) not in users:
                return json.dumps({"error": f"created_by {event['created_by']} not found"})

            eid = calendar_controller._gen_id(events)
            rec = {
                "event_id": eid,
                "calendar_id": calendar_id,
                "title": event["title"],
                "start_at": event["start"],
                "end_at": event["end"],
                "event_type": event["type"],
                "created_by": event["created_by"],
                "created_at": calendar_controller._now()
            }
            events[eid] = rec
            return json.dumps(rec)

        if action == "delete_event":
            if not calendar_id or str(calendar_id) not in calendars:
                return json.dumps({"error":"valid calendar_id required"})
            if not event_id or str(event_id) not in events:
                return json.dumps({"error":"valid event_id required"})
            if str(events[str(event_id)].get("calendar_id")) != str(calendar_id):
                return json.dumps({"error":"event does not belong to the given calendar_id"})
            removed = events.pop(str(event_id))
            return json.dumps(removed)

        return json.dumps({"error":"Unsupported action (create|add_event|delete_event)"})

    @staticmethod
    def get_info()->Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"calendar_controller",
                "description":"Create a calendar; add or delete events.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "action":{"type":"string","description":"create | add_event | delete_event"},
                        "space_key":{"type":"string","description":"Required for create"},
                        "calendar_name":{"type":"string","description":"Required for create"},
                        "calendar_id":{"type":"string","description":"Required for add_event/delete_event"},
                        "event":{"type":"object","description":"For add_event: {title, start (YYYY-MM-DD), end (YYYY-MM-DD), type, created_by}"},
                        "event_id":{"type":"string","description":"For delete_event: event_id"}
                    },
                    "required":["action"]
                }
            }
        }
