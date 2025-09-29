import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class space_search(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        requester_id: str,
        space_key: Optional[str] = None,
        name: Optional[str] = None,
        type: Optional[str] = None,
        owner_group: Optional[str] = None,
        status: Optional[str] = None
    ) -> str:
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        if str(requester_id) not in users:
            return json.dumps({"error": f"requester_id {requester_id} not found"})

        results: List[Dict[str, Any]] = []
        for s in spaces.values():
            if space_key and str(s.get("space_key")) != str(space_key):
                continue
            if name and name.lower() not in str(s.get("name","")).lower():
                continue
            if type and str(s.get("type","")).lower() != type.lower():
                continue
            if owner_group and str(s.get("owner_group_id")) != str(owner_group):
                continue
            if status and str(s.get("status","")).lower() != status.lower():
                continue
            results.append(s)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"space_search",
                "description":"Find spaces by filters.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "requester_id":{"type":"string","description":"ID of the requester"},
                        "space_key":{"type":"string","description":"Filter by exact space_key"},
                        "name":{"type":"string","description":"Partial match on space name"},
                        "type":{"type":"string","description":"Space type (Team | Department | Project | Knowledge)"},
                        "owner_group":{"type":"string","description":"Filter by owner_group_id"},
                        "status":{"type":"string","description":"Space status (Active | Suspended | Deactivated)"}
                    },
                    "required":["requester_id"]
                }
            }
        }
