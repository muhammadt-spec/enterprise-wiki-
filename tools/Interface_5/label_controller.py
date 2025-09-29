import json
from typing import Any, Dict, List, Optional
from tau_bench.envs.tool import Tool

class label_controller(Tool):
    @staticmethod
    def _now()->str:
        return "2025-10-01T00:00:00"

    @staticmethod
    def _gen_id(tbl: Dict[str, Any])->str:
        if not tbl: return "1"
        return str(max(int(k) for k in tbl.keys()) + 1)

    @staticmethod
    def invoke(
        data: Dict[str, Any],
        action: str,
        page_id: str,
        labels: Optional[List[str]] = None
    )->str:
        pages = data.get("pages", {})
        labels_tbl = data.get("labels", {})
        page_labels = data.setdefault("page_labels", {})

        if str(page_id) not in pages:
            return json.dumps({"error": f"page_id {page_id} not found"})

        if action not in ["apply","remove"]:
            return json.dumps({"error":"action must be one of (apply|remove)"})

        if not labels or not isinstance(labels, list):
            return json.dumps({"error":"labels must be a non-empty array of label_text"})

        text_to_id = {}
        for txt in labels:
            lid = None
            for k, l in labels_tbl.items():
                if str(l.get("label_text","")).lower() == str(txt).lower():
                    lid = k; break
            if not lid:
                return json.dumps({"error": f"label '{txt}' not found. Create via template/page flow first."})
            text_to_id[txt] = lid

        if action == "apply":
            applied = []
            for txt, lid in text_to_id.items():
                dup = False
                for r in page_labels.values():
                    if str(r.get("page_id")) == str(page_id) and str(r.get("label_id")) == str(lid):
                        dup = True; break
                if dup:
                    applied.append({"label_text": txt, "status": "already_applied"})
                    continue
                plid = label_controller._gen_id(page_labels)
                rec = {
                    "page_label_id": plid,
                    "page_id": page_id,
                    "label_id": lid,
                    "applied_at": label_controller._now()
                }
                page_labels[plid] = rec
                applied.append({"label_text": txt, "status": "applied", "record": rec})
            return json.dumps({"result":"apply","details": applied})

        else:
            removed = []
            to_delete = []
            for txt, lid in text_to_id.items():
                found_key = None
                for k, r in page_labels.items():
                    if str(r.get("page_id")) == str(page_id) and str(r.get("label_id")) == str(lid):
                        found_key = k; break
                if found_key:
                    to_delete.append(found_key)
                    removed.append({"label_text": txt, "status": "removed"})
                else:
                    removed.append({"label_text": txt, "status": "not_found"})
            for k in to_delete:
                page_labels.pop(k, None)
            return json.dumps({"result":"remove","details": removed})

    @staticmethod
    def get_info()->Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"label_controller",
                "description":"Apply or remove labels on a page.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "action":{"type":"string","description":"apply | remove"},
                        "page_id":{"type":"string","description":"Target page_id"},
                        "labels":{"type":"array","items":{"type":"string"},"description":"Array of label_text values"}
                    },
                    "required":["action","page_id","labels"]
                }
            }
        }
