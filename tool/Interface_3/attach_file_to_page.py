import json
from typing import Any, Dict, Optional
from tau_bench.envs.tool import Tool

class AttachFileToPage(Tool):
    """Upload a new attachment (attachments table)."""
    @staticmethod
    def _generate_id(table: Dict[str, Any]) -> str:
        if not table: return "1"
        try: return str(max(int(k) for k in table.keys()) + 1)
        except Exception: return str(len(table) + 1)
    @staticmethod
    def invoke(data: Dict[str, Any], page_id: str, filename: str, mime_type: str,
               filesize_bytes: int, uploader_id: str, version_number: int = 1) -> str:
        pages = data.get("pages", {})
        users = data.get("users", {})
        attachments = data.get("attachments", {})
        if page_id not in pages: return json.dumps({"error":"Page not found"})
        if uploader_id not in users: return json.dumps({"error":"Uploader user not found"})
        new_id = AttachFileToPage._generate_id(attachments)
        rec={"attachment_id":new_id,"page_id":page_id,"filename":filename,"mime_type":mime_type,
             "filesize_bytes":int(filesize_bytes),"uploader_id":uploader_id,"uploaded_at":"2025-10-01T00:00:00",
             "version_number":int(version_number),"created_at":"2025-10-01T00:00:00","updated_at":"2025-10-01T00:00:00"}
        attachments[new_id]=rec
        return json.dumps(rec)
    @staticmethod
    def get_info():
        return {"type":"function","function":{"name":"attach_file_to_page","description":"Upload a new attachment to a page.","parameters":{"type":"object","properties":{"page_id":{"type":"string","description":"Target page_id"},"filename":{"type":"string","description":"File name"},"mime_type":{"type":"string","description":"MIME type string"},"filesize_bytes":{"type":"integer","description":"File size in bytes"},"uploader_id":{"type":"string","description":"User ID of uploader"},"version_number":{"type":"integer","description":"Attachment version number (integer)"}},"required":["page_id","filename","mime_type","filesize_bytes","uploader_id"]}}}
