import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AddCalendarEventRecord(Tool):
    """Add a calendar event to an existing calendar."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table: return "1"
        try: return str(max(int(k) for k in table.keys()) + 1)
        except Exception: return str(len(table) + 1)
    @staticmethod
    def invoke(data: Dict[str, Any], calendar_id: str, title: str, start_at: str,
               end_at: str, event_type: str, created_by: Optional[str] = None) -> str:
        calendars = data.get("calendars", {}); events = data.get("calendar_events", {}); users = data.get("users", {})
        if calendar_id not in calendars: return json.dumps({"error":"Calendar not found"})
        if event_type not in {"Meeting","Milestone","Release","Holiday","Other"}:
            return json.dumps({"error":"Invalid event_type (Meeting | Milestone | Release | Holiday | Other)"})
        if created_by and created_by not in users: return json.dumps({"error":"created_by user not found"})
        new_id = AddCalendarEventRecord._generate_id(events)
        rec={"event_id":new_id,"calendar_id":calendar_id,"title":title,"start_at":start_at,"end_at":end_at,
             "event_type":event_type,"created_by":created_by,"created_at":"2025-10-01T00:00:00"}
        events[new_id]=rec
        return json.dumps(rec)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"add_calendar_event_record","description":"Create a new event on an existing calendar.","parameters":{"type":"object","properties":{"calendar_id":{"type":"string","description":"Target calendar_id"},"title":{"type":"string","description":"Event title"},"start_at":{"type":"string","description":"Start date (YYYY-MM-DD)"},"end_at":{"type":"string","description":"End date (YYYY-MM-DD)"},"event_type":{"type":"string","description":"Event type (Meeting | Milestone | Release | Holiday | Other)"},"created_by":{"type":"string","description":"User ID who creates the event"}},"required":["calendar_id","title","start_at","end_at","event_type"]}}}
