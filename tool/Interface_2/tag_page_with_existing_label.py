import json
from typing import Any, Dict
from tau_bench.envs.tool import Tool

class TagPageWithExistingLabel(Tool):
    """Apply an existing label to a page (page_labels table)."""
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, label_id: str) -> str:
        pages = data.get("pages", {}); labels = data.get("labels", {}); page_labels = data.get("page_labels", {})
        if page_id not in pages: return json.dumps({"error":"Page not found"})
        if label_id not in labels: return json.dumps({"error":"Label not found"})
        key=f"{page_id}:{label_id}"
        if key in page_labels: return json.dumps({"error":"Label already applied to page"})
        rec={"page_id":page_id,"label_id":label_id,"applied_at":"2025-10-01T00:00:00"}
        page_labels[key]=rec
        return json.dumps(rec)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"tag_page_with_existing_label","description":"Apply an existing label to a page.","parameters":{"type":"object","properties":{"page_id":{"type":"string","description":"Target page_id"},"label_id":{"type":"string","description":"Existing label_id"}},"required":["page_id","label_id"]}}}
