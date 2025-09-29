import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class template_find(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        requester_id: str,
        template_id: Optional[str] = None,
        name: Optional[str] = None,
        scope: Optional[str] = None,
        space_key: Optional[str] = None,
        owner_id: Optional[str] = None,
        sensitivity: Optional[str] = None,
        status: Optional[str] = None
    ) -> str:
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        templates = data.get("templates", {})

        if str(requester_id) not in users:
            return json.dumps({"error": f"requester_id {requester_id} not found"})

        space_id = None
        if scope and scope.lower() == "space_key":
            if not space_key:
                return json.dumps({"error":"scope=space_key requires space_key"})
            for sid, s in spaces.items():
                if str(s.get("space_key")) == str(space_key):
                    space_id = sid
                    break
            if not space_id:
                return json.dumps([])

        res: List[Dict[str, Any]] = []
        for t in templates.values():
            if template_id and str(t.get("template_id")) != str(template_id):
                continue
            if name and name.lower() not in str(t.get("name","")).lower():
                continue
            if scope and scope.lower() == "global" and t.get("scope") != "global":
                continue
            if scope and scope.lower() == "space_key":
                if str(t.get("scope")) != str(space_key):
                    continue
                if space_id and str(t.get("space_id")) != str(space_id):
                    continue
            if owner_id and str(t.get("owner_id")) != str(owner_id):
                continue
            if sensitivity and str(t.get("sensitivity","")).lower() != sensitivity.lower():
                continue
            if status and str(t.get("status","")).lower() != status.lower():
                continue
            res.append(t)
        return json.dumps(res)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"template_find",
                "description":"Find templates by filters.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "requester_id":{"type":"string","description":"ID of the requester"},
                        "template_id":{"type":"string","description":"Filter by template_id"},
                        "name":{"type":"string","description":"Partial match on template name"},
                        "scope":{"type":"string","description":"Scope (global | space_key)"},
                        "space_key":{"type":"string","description":"Space key when scope=space_key"},
                        "owner_id":{"type":"string","description":"Filter by owner_id"},
                        "sensitivity":{"type":"string","description":"Sensitivity (normal | official)"},
                        "status":{"type":"string","description":"Status (Active | Suspended | Deactivated)"}
                    },
                    "required":["requester_id"]
                }
            }
        }
