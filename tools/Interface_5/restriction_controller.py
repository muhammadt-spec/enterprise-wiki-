import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class restriction_controller(Tool):
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
        page_id: str,
        restriction_type: str,
        subjects: Dict[str, List[str]]
    )->str:
        pages = data.get("pages", {})
        rs_tbl = data.setdefault("restriction_sets", {})
        rsu_tbl = data.setdefault("restriction_subject_users", {})
        rsg_tbl = data.setdefault("restriction_subject_groups", {})
        users = data.get("users", {})
        groups = data.get("groups", {})

        if str(page_id) not in pages:
            return json.dumps({"error": f"page_id {page_id} not found"})

        if restriction_type not in ["none","edit_only","view_and_edit"]:
            return json.dumps({"error":"restriction_type must be one of (none|edit_only|view_and_edit)"})

        rs_id = restriction_controller._gen_id(rs_tbl)
        rs_tbl[rs_id] = {"restrictions_id": rs_id, "type": restriction_type, "created_at": restriction_controller._now(), "updated_at": restriction_controller._now()}
        pages[str(page_id)]["restrictions_id"] = rs_id
        pages[str(page_id)]["updated_at"] = restriction_controller._now()

        added_users = []
        for uid in (subjects.get("users") or []):
            if str(uid) not in users:
                return json.dumps({"error": f"user {uid} not found"})
            rid = restriction_controller._gen_id(rsu_tbl)
            rsu_tbl[rid] = {"restriction_subject_users_id": rid, "restrictions_id": rs_id, "user_id": uid, "perm": restriction_type}
            added_users.append(uid)

        added_groups = []
        for gid in (subjects.get("groups") or []):
            if str(gid) not in groups:
                return json.dumps({"error": f"group {gid} not found"})
            rid = restriction_controller._gen_id(rsg_tbl)
            rsg_tbl[rid] = {"restrictions_id": rs_id, "group_id": gid, "perm": restriction_type}
            added_groups.append(gid)

        return json.dumps({
            "restrictions_set": rs_tbl[rs_id],
            "attached_users": added_users,
            "attached_groups": added_groups,
            "page": pages[str(page_id)]
        })

    @staticmethod
    def get_info()->Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"restriction_controller",
                "description":"Set page-level restrictions and subjects.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "page_id":{"type":"string","description":"Target page_id"},
                        "restriction_type":{"type":"string","description":"none | edit_only | view_and_edit"},
                        "subjects":{"type":"object","description":"Map with keys 'users' and/or 'groups' each containing arrays of ids"}
                    },
                    "required":["page_id","restriction_type","subjects"]
                }
            }
        }
