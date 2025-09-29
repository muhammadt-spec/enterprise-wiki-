import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class page_discover(Tool):
    @staticmethod
    def _space_id_by_key(spaces: Dict[str, Any], space_key: str) -> Optional[str]:
        for sid, s in spaces.items():
            if str(s.get("space_key")) == str(space_key):
                return sid
        return None

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        requester_id: str,
        page_id: Optional[str] = None,
        title: Optional[str] = None,
        space_key: Optional[str] = None,
        parent_page_id: Optional[str] = None,
        label: Optional[str] = None,
        creator_id: Optional[str] = None,
        last_modified_range: Optional[Dict[str, str]] = None
    ) -> str:
        users = data.get("users", {})
        pages = data.get("pages", {})
        spaces = data.get("spaces", {})
        labels = data.get("labels", {})
        page_labels = data.get("page_labels", {})

        if str(requester_id) not in users:
            return json.dumps({"error": f"requester_id {requester_id} not found"})

        space_id_filter = None
        if space_key:
            space_id_filter = page_discover._space_id_by_key(spaces, space_key)
            if not space_id_filter:
                return json.dumps([])

        label_id_filter = None
        if label:
            for lid, l in labels.items():
                if str(l.get("label_text","")).lower() == label.lower():
                    label_id_filter = lid
                    break
            if label and not label_id_filter:
                return json.dumps([])

        labeled_pages = None
        if label_id_filter:
            labeled_pages = set()
            for _, pl in page_labels.items():
                if str(pl.get("label_id")) == str(label_id_filter):
                    labeled_pages.add(str(pl.get("page_id")))

        def in_date_range(ts: Optional[str], rng: Dict[str,str]) -> bool:
            if not ts:
                return False
            start = rng.get("start")
            end = rng.get("end")
            day = ts[:10]
            if start and day < start:
                return False
            if end and day > end:
                return False
            return True

        results: List[Dict[str, Any]] = []
        for p in pages.values():
            if page_id and str(p.get("page_id")) != str(page_id):
                continue
            if title and title.lower() not in str(p.get("title","")).lower():
                continue
            if space_id_filter and str(p.get("space_id")) != str(space_id_filter):
                continue
            if parent_page_id and str(p.get("parent_page_id")) != str(parent_page_id):
                continue
            if creator_id and str(p.get("creator_id")) != str(creator_id):
                continue
            if label_id_filter and str(p.get("page_id")) not in (labeled_pages or set()):
                continue
            if last_modified_range:
                if not in_date_range(str(p.get("updated_at")), last_modified_range):
                    continue
            results.append(p)
        return json.dumps(results)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"page_discover",
                "description":"Find pages by filters.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "requester_id":{"type":"string","description":"ID of the requester"},
                        "page_id":{"type":"string","description":"Filter by page_id"},
                        "title":{"type":"string","description":"Partial match on page title"},
                        "space_key":{"type":"string","description":"Filter by space_key"},
                        "parent_page_id":{"type":"string","description":"Filter by parent_page_id"},
                        "label":{"type":"string","description":"Filter by label text"},
                        "creator_id":{"type":"string","description":"Filter by creator_id"},
                        "last_modified_range":{"type":"object","description":"Filter by last modified date range (YYYY-MM-DD) keys: start, end"}
                    },
                    "required":["requester_id"]
                }
            }
        }
