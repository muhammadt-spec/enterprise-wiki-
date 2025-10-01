import json
from typing import Any, Dict, List
from tau_bench.envs.tool import Tool

class EnumerateAttachmentsForPage(Tool):
    """List attachments for a given page_id."""
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str) -> str:
        attachments = data.get("attachments", {})
        results: List[Dict[str, Any]] = []
        for att in attachments.values():
            if att.get("page_id") == page_id:
                results.append(att)
        return json.dumps(results)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"enumerate_attachments_for_page","description":"List attachments for a page.","parameters":{"type":"object","properties":{"page_id":{"type":"string","description":"Target page_id"}},"required":["page_id"]}}}
