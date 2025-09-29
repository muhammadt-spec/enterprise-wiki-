import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class page_manage(Tool):
    @staticmethod
    def _now()->str:
        return "2025-10-01T00:00:00"

    @staticmethod
    def _gen_id(tbl: Dict[str, Any])->str:
        if not tbl: return "1"
        return str(max(int(k) for k in tbl.keys()) + 1)

    @staticmethod
    def _space_id_by_key(spaces: Dict[str, Any], key: str)->Optional[str]:
        for sid, s in spaces.items():
            if str(s.get("space_key")) == str(key):
                return sid
        return None

    @staticmethod
    def _ensure_labels(data: Dict[str, Any], labels_texts: List[str], space_id: str, creator_id: str)->List[str]:
        labels_tbl = data.setdefault("labels", {})
        created_ids = []
        for txt in labels_texts:
            lid_found = None
            for lid, lab in labels_tbl.items():
                if str(lab.get("space_id")) == str(space_id) and str(lab.get("label_text")).lower() == str(txt).lower():
                    lid_found = lid
                    break
            if not lid_found:
                new_id = page_manage._gen_id(labels_tbl)
                labels_tbl[new_id] = {
                    "label_id": new_id,
                    "label_text": txt,
                    "scope": "space",
                    "space_id": space_id,
                    "created_by": creator_id,
                    "created_at": page_manage._now()
                }
                lid_found = new_id
            created_ids.append(lid_found)
        return created_ids

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        space_key: Optional[str] = None,
        title: Optional[str] = None,
        content: Optional[str] = None,
        parent_page_id: Optional[str] = None,
        creator_id: Optional[str] = None,
        labels: Optional[List[str]] = None,
        page_id: Optional[str] = None,
        change_set: Optional[Dict[str, Any]] = None
    )->str:
        pages = data.get("pages", {})
        users = data.get("users", {})
        spaces = data.get("spaces", {})
        page_labels = data.setdefault("page_labels", {})

        if action == "create":
            if not all([space_key, title, content, creator_id]):
                return json.dumps({"error":"Missing required: space_key, title, content, creator_id"})
            if str(creator_id) not in users:
                return json.dumps({"error": f"creator_id {creator_id} not found"})
            sid = page_manage._space_id_by_key(spaces, space_key)
            if not sid:
                return json.dumps({"error": f"space_key {space_key} not found"})

            pid = page_manage._gen_id(pages)
            rec = {
                "page_id": pid,
                "space_id": sid,
                "title": title,
                "type": "page",
                "parent_page_id": parent_page_id,
                "content_body": content,
                "creator_id": creator_id,
                "last_modified_by": creator_id,
                "last_modified_at": page_manage._now(),
                "status": "current",
                "workflow_state": None,
                "restrictions_id": None,
                "version_number": 1,
                "created_at": page_manage._now(),
                "updated_at": page_manage._now()
            }
            pages[pid] = rec

            if labels:
                label_ids = page_manage._ensure_labels(data, labels, sid, creator_id)
                for lid in label_ids:
                    pl_id = page_manage._gen_id(page_labels)
                    page_labels[pl_id] = {
                        "page_label_id": pl_id,
                        "page_id": pid,
                        "label_id": lid,
                        "applied_at": page_manage._now()
                    }
            return json.dumps(rec)

        elif action == "update":
            if not page_id or not change_set:
                return json.dumps({"error":"action=update requires page_id and change_set"})
            rec = pages.get(str(page_id))
            if not rec:
                return json.dumps({"error": f"page_id {page_id} not found"})
            for k in ["title","content_body","parent_page_id","status","workflow_state","last_modified_by"]:
                if k in change_set:
                    rec[k] = change_set[k]
            rec["version_number"] = int(rec.get("version_number",1)) + 1
            rec["updated_at"] = page_manage._now()
            rec["last_modified_at"] = page_manage._now()
            return json.dumps(rec)

        else:
            return json.dumps({"error":"Unsupported action (use create|update)"})

    @staticmethod
    def get_info()->Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"page_manage",
                "description":"Create a page (optionally with labels) or update/move/rename content.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "action":{"type":"string","description":"create | update"},
                        "space_key":{"type":"string","description":"Required for create"},
                        "title":{"type":"string","description":"Page title (create)"},
                        "content":{"type":"string","description":"Page body/content (create)"},
                        "parent_page_id":{"type":"string","description":"Parent page id (optional)"},
                        "creator_id":{"type":"string","description":"User id of creator (create)"},
                        "labels":{"type":"array","items":{"type":"string"},"description":"List of label texts to attach (create)"},
                        "page_id":{"type":"string","description":"Target page for update"},
                        "change_set":{"type":"object","description":"Fields to update (title, content_body, parent_page_id, status, workflow_state, last_modified_by)"}
                    },
                    "required":["action"]
                }
            }
        }
