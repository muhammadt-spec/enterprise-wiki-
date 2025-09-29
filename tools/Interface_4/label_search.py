import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class label_search(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        requester_id: str,
        label_text: Optional[str] = None,
        space_key: Optional[str] = None,
        applied_to_type: Optional[str] = None,
        applied_to_id: Optional[str] = None
    ) -> str:
        users = data.get("users", {})
        labels = data.get("labels", {})
        spaces = data.get("spaces", {})
        page_labels = data.get("page_labels", {})
        attachment_labels = data.get("attachment_labels", {})

        if str(requester_id) not in users:
            return json.dumps({"error": f"requester_id {requester_id} not found"})

        space_id = None
        if space_key:
            for sid, s in spaces.items():
                if str(s.get("space_key")) == str(space_key):
                    space_id = sid
                    break
            if not space_id:
                return json.dumps([])

        results: List[Dict[str, Any]] = []
        for lid, l in labels.items():
            if label_text and label_text.lower() != str(l.get("label_text","")).lower():
                continue
            if space_id and str(l.get("space_id")) != str(space_id):
                continue

            mapping = {"label": l, "applied": []}
            if applied_to_type in (None, "page"):
                for _, pl in page_labels.items():
                    if str(pl.get("label_id")) == str(lid):
                        if not applied_to_id or str(pl.get("page_id")) == str(applied_to_id):
                            mapping["applied"].append({"type":"page","id":pl.get("page_id"),"applied_at":pl.get("applied_at")})
            if applied_to_type in (None, "attachment"):
                for _, al in attachment_labels.items():
                    if str(al.get("label_id")) == str(lid):
                        if not applied_to_id or str(al.get("attachment_id")) == str(applied_to_id):
                            mapping["applied"].append({"type":"attachment","id":al.get("attachment_id"),"applied_at":al.get("applied_at")})
            results.append(mapping)
        return json.dumps(results)

    @staticmethod
    def get_info()->Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"label_search",
                "description":"Find labels and where they are applied.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "requester_id":{"type":"string","description":"ID of the requester"},
                        "label_text":{"type":"string","description":"Exact label text to match"},
                        "space_key":{"type":"string","description":"Restrict to a space by space_key"},
                        "applied_to_type":{"type":"string","description":"Filter applied items by type (page | attachment)"},
                        "applied_to_id":{"type":"string","description":"Filter by specific target id"}
                    },
                    "required":["requester_id"]
                }
            }
        }
