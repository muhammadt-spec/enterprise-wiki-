import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class group_lookup(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        requester_id: str,
        group_name: Optional[str] = None,
        member_user_id: Optional[str] = None,
        description: Optional[str] = None
    ) -> str:
        users = data.get("users", {})
        groups = data.get("groups", {})
        gm = data.get("group_members", {})

        if str(requester_id) not in users:
            return json.dumps({"error": f"requester_id {requester_id} not found"})

        membership = {}
        for r in gm.values():
            gid = str(r.get("group_id"))
            uid = str(r.get("user_id"))
            membership.setdefault(gid, set()).add(uid)

        results: List[Dict[str, Any]] = []
        for g in groups.values():
            if group_name and group_name.lower() not in str(g.get("group_name","")).lower():
                continue
            if description and description.lower() not in str(g.get("description","")).lower():
                continue
            if member_user_id:
                gids = [gid for gid, us in membership.items() if str(member_user_id) in us]
                if str(g.get("group_id")) not in gids:
                    continue
            results.append(g)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"group_lookup",
                "description":"Find groups by filters.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "requester_id":{"type":"string","description":"ID of the requester"},
                        "group_name":{"type":"string","description":"Partial match on group_name"},
                        "member_user_id":{"type":"string","description":"Filter by a member's user_id"},
                        "description":{"type":"string","description":"Partial match on group description"}
                    },
                    "required":["requester_id"]
                }
            }
        }
