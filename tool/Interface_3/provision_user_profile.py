import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class ProvisionUserProfile(Tool):
    """Create a new user in users table."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table: return "1"
        try: return str(max(int(k) for k in table.keys()) + 1)
        except Exception: return str(len(table) + 1)
    @staticmethod
    def invoke(data: Dict[str, Any], full_name: str, email: str, status: str = "Active",
               timezone: Optional[str] = None, position: Optional[str] = None,
               department: Optional[str] = None, location: Optional[str] = None,
               about_me: Optional[str] = None, phone: Optional[str] = None) -> str:
        users = data.get("users", {})
        for u in users.values():
            if (u.get("email") or "").lower() == email.lower():
                return json.dumps({"error": "Email already exists"})
        new_id = ProvisionUserProfile._generate_id(users)
        rec = {
            "user_id": new_id, "full_name": full_name, "email": email, "status": status,
            "timezone": timezone, "position": position, "department": department,
            "location": location, "about_me": about_me, "phone": phone,
            "created_at": "2025-10-01T00:00:00", "updated_at": "2025-10-01T00:00:00"
        }
        users[new_id] = rec
        return json.dumps(rec)
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {"type":"function","function":{"name":"provision_user_profile","description":"Create a new user record.","parameters":{"type":"object","properties":{"full_name":{"type":"string","description":"Full name of the user"},"email":{"type":"string","description":"Unique email address"},"status":{"type":"string","description":"User status (Active | Suspended | Deactivated)"},"timezone":{"type":"string","description":"IANA timezone string"},"position":{"type":"string","description":"Job position/role"},"department":{"type":"string","description":"Department name"},"location":{"type":"string","description":"User location"},"about_me":{"type":"string","description":"Short bio"},"phone":{"type":"string","description":"Phone number"}},"required":["full_name","email"]}}}
