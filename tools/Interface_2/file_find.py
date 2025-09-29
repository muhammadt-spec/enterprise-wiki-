import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class file_find(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        requester_id: str,
        attachment_id: Optional[str] = None,
        page_id: Optional[str] = None,
        filename: Optional[str] = None,
        uploader_id: Optional[str] = None,
        mime_type: Optional[str] = None,
        uploaded_date_range: Optional[Dict[str,str]] = None
    ) -> str:
        users = data.get("users", {})
        atts = data.get("attachments", {})
        if str(requester_id) not in users:
            return json.dumps({"error": f"requester_id {requester_id} not found"})

        def in_range(ts: Optional[str], rng: Dict[str,str]) -> bool:
            if not ts: return False
            d = ts[:10]
            s = rng.get("start"); e = rng.get("end")
            if s and d < s: return False
            if e and d > e: return False
            return True

        res: List[Dict[str, Any]] = []
        for a in atts.values():
            if attachment_id and str(a.get("attachment_id")) != str(attachment_id):
                continue
            if page_id and str(a.get("page_id")) != str(page_id):
                continue
            if filename and filename.lower() not in str(a.get("filename","")).lower():
                continue
            if uploader_id and str(a.get("uploader_id")) != str(uploader_id):
                continue
            if mime_type and str(a.get("mime_type","")).lower() != mime_type.lower():
                continue
            if uploaded_date_range and not in_range(str(a.get("uploaded_at")), uploaded_date_range):
                continue
            res.append(a)
        return json.dumps(res)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"file_find",
                "description":"Find files/attachments by filters.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "requester_id":{"type":"string","description":"ID of the requester"},
                        "attachment_id":{"type":"string","description":"Filter by attachment_id"},
                        "page_id":{"type":"string","description":"Filter by page_id"},
                        "filename":{"type":"string","description":"Partial match on filename"},
                        "uploader_id":{"type":"string","description":"Filter by uploader_id"},
                        "mime_type":{"type":"string","description":"Filter by exact MIME type"},
                        "uploaded_date_range":{"type":"object","description":"Date range (YYYY-MM-DD) with keys: start, end"}
                    },
                    "required":["requester_id"]
                }
            }
        }
