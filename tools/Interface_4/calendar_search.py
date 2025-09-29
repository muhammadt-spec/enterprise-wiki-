import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class calendar_search(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        requester_id: str,
        calendar_id: Optional[str] = None,
        space_key: Optional[str] = None,
        name: Optional[str] = None
    ) -> str:
        users = data.get("users", {})
        calendars = data.get("calendars", {})
        spaces = data.get("spaces", {})

        if str(requester_id) not in users:
            return json.dumps({"error": f"requester_id {requester_id} not found"})

        space_id = None
        if space_key:
            for sid, s in spaces.items():
                if str(s.get("space_key")) == str(space_key):
                    space_id = sid
                    break
            if not space_id:
                return json.dumps([])

        res: List[Dict[str, Any]] = []
        for c in calendars.values():
            if calendar_id and str(c.get("calendar_id")) != str(calendar_id):
                continue
            if space_id and str(c.get("space_id")) != str(space_id):
                continue
            if name and name.lower() not in str(c.get("name","")).lower():
                continue
            res.append(c)
        return json.dumps(res)

    @staticmethod
    def get_info()->Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"calendar_search",
                "description":"Find team calendars by id/filters.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "requester_id":{"type":"string","description":"ID of the requester"},
                        "calendar_id":{"type":"string","description":"Filter by calendar_id"},
                        "space_key":{"type":"string","description":"Filter by space_key"},
                        "name":{"type":"string","description":"Partial match on calendar name"}
                    },
                    "required":["requester_id"]
                }
            }
        }
