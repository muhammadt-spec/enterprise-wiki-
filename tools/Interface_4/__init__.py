from .approval_gate_validate import approval_gate_validate
from .attachment_manager import attachment_manager
from .attachment_search import attachment_search
from .audit_entry_create import audit_entry_create
from .calendar_manager import calendar_manager
from .calendar_search import calendar_search
from .escalate_to_operator import escalate_to_operator
from .group_search import group_search
from .label_editor import label_editor
from .label_search import label_search
from .notification_dispatch import notification_dispatch
from .page_editor import page_editor
from .page_search import page_search
from .restriction_editor import restriction_editor
from .space_register import space_register
from .space_search import space_search
from .template_search import template_search
from .user_search import user_search


ALL_TOOLS_INTERFACE_4 = [
    approval_gate_validate,
    attachment_manager,
    attachment_search,
    audit_entry_create,
    calendar_manager,
    calendar_search,
    escalate_to_operator,
    group_search,
    label_editor,
    label_search,
    notification_dispatch,
    page_editor,
    page_search,
    restriction_editor,
    space_register,
    space_search,
    template_search,
    user_search
]
