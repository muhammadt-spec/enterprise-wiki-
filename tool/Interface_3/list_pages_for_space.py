import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class ListPagesForSpace(Tool):
    """List pages in a space by space_key, optional filter by status or workflow_state."""
    @staticmethod
    def invoke(data: Dict[str, Any], space_key: str, status: Optional[str] = None,
               workflow_state: Optional[str] = None) -> str:
        spaces = data.get("spaces", {}); pages = data.get("pages", {})
        sid=None
        for k,v in spaces.items():
            if (v.get("space_key") or "").lower()==space_key.lower():
                sid=k; break
        if not sid: return json.dumps({"error":"Space not found"})
        results: List[Dict[str, Any]] = []
        for p in pages.values():
            if p.get("space_id") != sid: continue
            if status and p.get("status") != status: continue
            if workflow_state and p.get("workflow_state") != workflow_state: continue
            results.append(p)
        return json.dumps(results)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"list_pages_for_space","description":"List pages within a space, with optional status/workflow filters.","parameters":{"type":"object","properties":{"space_key":{"type":"string","description":"Space key"},"status":{"type":"string","description":"Filter by status (Draft | Published | Archived)"},"workflow_state":{"type":"string","description":"Filter by workflow_state (Proposed | In_Review | Approved | Rejected | Retired)"}},"required":["space_key"]}}}
