import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class CreateProblem(Tool):
    """
    Create a problem record with enums.
    """

    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table: return "1"
        try: return str(max(int(k) for k in table.keys()) + 1)
        except Exception: return str(len(table) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        title: str,
        problem_type: str,
        status: str,
        owner_group_id: str,
        created_by: str
    ) -> str:
        problems = data.get("problems", {})
        groups = data.get("groups", {})
        users = data.get("users", {})

        if problem_type not in {"Known_Error", "RCA_Pending", "RCA_Confirmed"}:
            return json.dumps({"error": "Invalid problem_type (Known_Error | RCA_Pending | RCA_Confirmed)"})
        if status not in {"New", "Under_Investigation", "Resolved", "Closed"}:
            return json.dumps({"error": "Invalid status (New | Under_Investigation | Resolved | Closed)"})
        if owner_group_id not in groups:
            return json.dumps({"error": "Owner group not found"})
        if created_by not in users:
            return json.dumps({"error": "Created_by user not found"})

        new_id = create_problem._generate_id(problems)
        rec = {
            "problem_id": new_id,
            "title": title,
            "problem_type": problem_type,
            "status": status,
            "root_cause_code": None,
            "owner_group_id": owner_group_id,
            "created_by": created_by,
            "created_at": "2025-10-01T00:00:00",
            "resolved_at": None,
            "closed_at": None
        }
        problems[new_id] = rec
        return json.dumps(rec)

    @staticmethod
    def get_info():
        return {
          "type": "function",
          "function": {
            "name": "create_problem",
            "description": "Create a new problem record.",
            "parameters": {
              "type": "object",
              "properties": {
                "title": {"type": "string", "description": "Problem title"},
                "problem_type": {"type": "string", "description": "Type (Known_Error | RCA_Pending | RCA_Confirmed)"},
                "status": {"type": "string", "description": "Status (New | Under_Investigation | Resolved | Closed)"},
                "owner_group_id": {"type": "string", "description": "Owner group_id"},
                "created_by": {"type": "string", "description": "User ID who created the problem"}
              },
              "required": ["title", "problem_type", "status", "owner_group_id", "created_by"]
            }
          }
        }
