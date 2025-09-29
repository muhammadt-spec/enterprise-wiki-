from .approval_check import approval_check
from .audit_trail_write import audit_trail_write
from .calendar_find import calendar_find
from .calendar_ops import calendar_ops
from .escalate_to_human import escalate_to_human
from .file_find import file_find
from .file_ops import file_ops
from .group_find import group_find
from .label_apply_or_remove import label_apply_or_remove
from .label_find import label_find
from .notification_create import notification_create
from .page_find import page_find
from .page_write import page_write
from .restriction_set_update import restriction_set_update
from .space_create import space_create
from .template_find import template_find
from .user_find import user_find
from .space_find import space_find


ALL_TOOLS_INTERFACE_2 = [
    approval_check,
    audit_trail_write,
    calendar_find,
    calendar_ops,
    escalate_to_human,
    file_find,
    file_ops,
    group_find,
    label_apply_or_remove,
    label_find,
    notification_create,
    page_find,
    page_write,
    restriction_set_update,
    space_create,
    template_find,
    user_find,
    space_find
]
