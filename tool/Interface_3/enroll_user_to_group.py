import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class EnrollUserToGroup(Tool):
    """Add a user to a group (group_members table)."""
    @staticmethod
    def invoke(data: Dict[str, Any], group_id: str, user_id: str) -> str:
        groups = data.get("groups", {})
        users = data.get("users", {})
        group_members = data.get("group_members", {})
        if group_id not in groups: return json.dumps({"error":"Group not found"})
        if user_id not in users: return json.dumps({"error":"User not found"})
        key = f"{group_id}:{user_id}"
        if key in group_members: return json.dumps({"error":"User already in group"})
        rec = {"group_id":group_id,"user_id":user_id,"added_at":"2025-10-01T00:00:00"}
        group_members[key]=rec
        return json.dumps(rec)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"enroll_user_to_group","description":"Add a user to an existing group.","parameters":{"type":"object","properties":{"group_id":{"type":"string","description":"Group ID"},"user_id":{"type":"string","description":"User ID to add"}},"required":["group_id","user_id"]}}}
