import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class space_register(Tool):
    @staticmethod
    def _now() -> str:
        return "2025-10-01T00:00:00"

    @staticmethod
    def _gen_id(tbl: Dict[str, Any]) -> str:
        if not tbl: return "1"
        return str(max(int(k) for k in tbl.keys()) + 1)

    @staticmethod
    def _space_by_key(spaces: Dict[str, Any], key: str) -> Optional[Dict[str, Any]]:
        for s in spaces.values():
            if str(s.get("space_key")) == str(key):
                return s
        return None

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        name: Optional[str] = None,
        key: Optional[str] = None,
        type: Optional[str] = None,
        owner_group: Optional[str] = None
    ) -> str:
        spaces = data.get("spaces", {})
        groups = data.get("groups", {})
        if action != "create":
            return json.dumps({"error":"Only action=\"create\" supported in manage_space"})

        if not all([name, key, type, owner_group]):
            return json.dumps({"error":"Missing required params: name, key, type, owner_group"})

        if type not in ["Team","Department","Project","Knowledge"]:
            return json.dumps({"error":"type must be one of (Team|Department|Project|Knowledge)"})

        if space_register._space_by_key(spaces, key):
            return json.dumps({"error": f"space_key {key} already exists"})

        if str(owner_group) not in groups:
            return json.dumps({"error": f"owner_group {owner_group} not found"})

        sid = space_register._gen_id(spaces)
        rec = {
            "space_id": sid,
            "space_key": key,
            "name": name,
            "type": type,
            "status": "Active",
            "owner_group_id": owner_group,
            "baseline_permissions_id": None,
            "created_at": space_register._now(),
            "updated_at": space_register._now()
        }
        spaces[sid] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info()->Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"space_register",
                "description":"Create a new space.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "action":{"type":"string","description":"Must be \"create\""},
                        "name":{"type":"string","description":"Space display name"},
                        "key":{"type":"string","description":"Unique space key"},
                        "type":{"type":"string","description":"Space type (Team | Department | Project | Knowledge)"},
                        "owner_group":{"type":"string","description":"Group ID that will own the space"}
                    },
                    "required":["action","name","key","type","owner_group"]
                }
            }
        }
