import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class GetGroupMembers(Tool):
    """
    List members of a group (returns user records).
    """

    @staticmethod
    def invoke(data: Dict[str, Any], group_id: str) -> str:
        users = data.get("users", {})
        group_members = data.get("group_members", {})
        results: List[Dict[str, Any]] = []
        for k, gm in group_members.items():
            if gm.get("group_id") == group_id:
                uid = gm.get("user_id")
                if uid in users:
                    results.append(users[uid])
        return json.dumps(results)

    @staticmethod
    def get_info():
        return {
          "type": "function",
          "function": {
            "name": "get_group_members",
            "description": "Return the list of user records that are members of a group.",
            "parameters": {
              "type": "object",
              "properties": {
                "group_id": {"type": "string", "description": "Group ID to inspect"}
              },
              "required": ["group_id"]
            }
          }
        }
