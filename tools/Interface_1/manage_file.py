import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class manage_file(Tool):
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
        page_id: str,
        action: str,
        file: Optional[Dict[str, Any]] = None,
        new_file: Optional[Dict[str, Any]] = None,
        target_page_id: Optional[str] = None,
        attachment_id: Optional[str] = None
    )->str:
        pages = data.get("pages", {})
        attachments = data.setdefault("attachments", {})
        users = data.get("users", {})

        if str(page_id) not in pages:
            return json.dumps({"error": f"page_id {page_id} not found"})

        if action not in ["upload","replace","move","delete"]:
            return json.dumps({"error":"action must be one of (upload|replace|move|delete)"})

        if action == "upload":
            if not file or not isinstance(file, dict):
                return json.dumps({"error":"file (dict) is required for upload"})
            for req in ["filename","mime_type","filesize_bytes","uploader_id"]:
                if req not in file:
                    return json.dumps({"error": f"file.{req} is required"})
            if str(file["uploader_id"]) not in users:
                return json.dumps({"error": f"uploader_id {file['uploader_id']} not found"})
            aid = manage_file._gen_id(attachments)
            rec = {
                "attachment_id": aid,
                "page_id": page_id,
                "filename": file["filename"],
                "mime_type": file["mime_type"],
                "filesize_bytes": int(file["filesize_bytes"]),
                "uploader_id": file["uploader_id"],
                "uploaded_at": manage_file._now(),
                "version_number": 1,
                "created_at": manage_file._now(),
                "updated_at": manage_file._now()
            }
            attachments[aid] = rec
            return json.dumps(rec)

        if action in ["replace","move","delete"]:
            if not attachment_id or str(attachment_id) not in attachments:
                return json.dumps({"error":"valid attachment_id is required"})
            att = attachments[str(attachment_id)]

            if action == "replace":
                if not new_file or not isinstance(new_file, dict):
                    return json.dumps({"error":"new_file (dict) required for replace"})
                for req in ["filename","mime_type","filesize_bytes","uploader_id"]:
                    if req not in new_file:
                        return json.dumps({"error": f"new_file.{req} is required"})
                if str(new_file["uploader_id"]) not in users:
                    return json.dumps({"error": f"uploader_id {new_file['uploader_id']} not found"})
                att.update({
                    "filename": new_file["filename"],
                    "mime_type": new_file["mime_type"],
                    "filesize_bytes": int(new_file["filesize_bytes"]),
                    "uploader_id": new_file["uploader_id"],
                    "uploaded_at": manage_file._now(),
                    "version_number": int(att.get("version_number",1)) + 1,
                    "updated_at": manage_file._now()
                })
                return json.dumps(att)

            if action == "move":
                if not target_page_id or str(target_page_id) not in pages:
                    return json.dumps({"error":"valid target_page_id required"})
                att["page_id"] = target_page_id
                att["updated_at"] = manage_file._now()
                return json.dumps(att)

            if action == "delete":
                removed = attachments.pop(str(attachment_id))
                return json.dumps(removed)

        return json.dumps({"error":"unhandled branch"})

    @staticmethod
    def get_info()->Dict[str, Any]:
        return {
            "type":"function",
            "function":{
                "name":"manage_file",
                "description":"Perform file/attachment operations.",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "page_id":{"type":"string","description":"Owning page id"},
                        "action":{"type":"string","description":"upload | replace | move | delete"},
                        "file":{"type":"object","description":"For upload: {filename, mime_type, filesize_bytes, uploader_id}"},
                        "new_file":{"type":"object","description":"For replace: {filename, mime_type, filesize_bytes, uploader_id}"},
                        "target_page_id":{"type":"string","description":"For move: destination page_id"},
                        "attachment_id":{"type":"string","description":"For replace/move/delete: existing attachment_id"}
                    },
                    "required":["page_id","action"]
                }
            }
        }
