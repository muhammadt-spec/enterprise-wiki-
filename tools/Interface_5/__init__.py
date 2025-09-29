from .approval_role_check import approval_role_check
from .attachment_controller import attachment_controller
from .attachment_discover import attachment_discover
from .audit_record_create import audit_record_create
from .calendar_controller import calendar_controller
from .calendar_discover import calendar_discover
from .group_discover import group_discover
from .label_controller import label_controller
from .label_discover import label_discover
from .notification_controller import notification_controller
from .page_controller import page_controller
from .page_discover import page_discover
from .restriction_controller import restriction_controller
from .route_to_operator import route_to_operator
from .space_create_entry import space_create_entry
from .space_discover import space_discover
from .template_discover import template_discover
from .user_discover import user_discover


ALL_TOOLS_INTERFACE_5 = [
    approval_role_check,
    attachment_controller,
    attachment_discover,
    audit_record_create,
    calendar_controller,
    calendar_discover,
    group_discover,
    label_controller,
    label_discover,
    notification_controller,
    page_controller,
    page_discover,
    restriction_controller,
    route_to_operator,
    space_create_entry,
    space_discover,
    template_discover,
    user_discover
]
