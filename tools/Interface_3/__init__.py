from .audit_log_create import audit_log_create
from .auth_approval_verify import auth_approval_verify
from .calendar_lookup import calendar_lookup
from .calendar_manage import calendar_manage
from .escalate_to_agent import escalate_to_agent
from .file_lookup import file_lookup
from .file_manage import file_manage
from .group_lookup import group_lookup
from .label_lookup import label_lookup
from .label_update import label_update
from .notification_send import notification_send
from .page_lookup import page_lookup
from .page_manage import page_manage
from .restriction_update import restriction_update
from .space_lookup import space_lookup
from .space_new import space_new
from .template_lookup import template_lookup
from .user_lookup import user_lookup


ALL_TOOLS_INTERFACE_3 = [
    audit_log_create,
    auth_approval_verify,
    calendar_lookup,
    calendar_manage,
    escalate_to_agent,
    file_lookup,
    file_manage,
    group_lookup,
    label_lookup,
    label_update,
    notification_send,
    page_lookup,
    page_manage,
    restriction_update,
    space_lookup,
    space_new,
    template_lookup,
    user_lookup
]
