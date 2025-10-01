import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class AddsRestrictionSubjects(Tool):
    """Add subjects (users/groups) with perm (view | edit) to a restriction set."""
    @staticmethod
    def invoke(data: Dict[str, Any], restrictions_id: str, users_view: List[str] = None,
               users_edit: List[str] = None, groups_view: List[str] = None, groups_edit: List[str] = None) -> str:
        restriction_sets = data.get("restriction_sets", {})
        rsu = data.get("restriction_subject_users", {})
        rsg = data.get("restriction_subject_groups", {})
        users = data.get("users", {})
        groups = data.get("groups", {})
        if restrictions_id not in restriction_sets:
            return json.dumps({"error":"Restriction set not found"})
        users_view = users_view or []
        users_edit = users_edit or []
        groups_view = groups_view or []
        groups_edit = groups_edit or []
        added={"users":[],"groups":[]}
        for uid in users_view:
            if uid not in users:
                return json.dumps({"error":f"User not found: {uid}"})
            key=f"{restrictions_id}:{uid}:view"
            if key not in rsu:
                rsu[key]={"restrictions_id":restrictions_id,"user_id":uid,"perm":"view"}
                added["users"].append(rsu[key])
        for uid in users_edit:
            if uid not in users:
                return json.dumps({"error":f"User not found: {uid}"})
            key=f"{restrictions_id}:{uid}:edit"
            if key not in rsu:
                rsu[key]={"restrictions_id":restrictions_id,"user_id":uid,"perm":"edit"}
                added["users"].append(rsu[key])
        for gid in groups_view:
            if gid not in groups:
                return json.dumps({"error":f"Group not found: {gid}"})
            key=f"{restrictions_id}:{gid}:view"
            if key not in rsg:
                rsg[key]={"restrictions_id":restrictions_id,"group_id":gid,"perm":"view"}
                added["groups"].append(rsg[key])
        for gid in groups_edit:
            if gid not in groups:
                return json.dumps({"error":f"Group not found: {gid}"})
            key=f"{restrictions_id}:{gid}:edit"
            if key not in rsg:
                rsg[key]={"restrictions_id":restrictions_id,"group_id":gid,"perm":"edit"}
                added["groups"].append(rsg[key])
        return json.dumps({"added":added,"restrictions_id":restrictions_id})

    @staticmethod
    def get_info():
        return {
            "type":"function",
            "function":{
                "name":"adds_restriction_subjects",
                "description":"Add user/group subjects to a restriction set with specific perms.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "restrictions_id":{"type":"string","description":"Restriction set ID"},
                        "users_view":{"type":"array","items":{"type":"string"},"description":"User IDs with view perm"},
                        "users_edit":{"type":"array","items":{"type":"string"},"description":"User IDs with edit perm"},
                        "groups_view":{"type":"array","items":{"type":"string"},"description":"Group IDs with view perm"},
                        "groups_edit":{"type":"array","items":{"type":"string"},"description":"Group IDs with edit perm"}
                    },
                    "required":["restrictions_id"]
                }
            }
        }
