from .approval_lookup import approval_lookup
from .create_new_audit_trail import create_new_audit_trail
from .create_notification import create_notification
from .discover_calendar_entities import discover_calendar_entities
from .discover_file_entities import discover_file_entities
from .discover_group_entities import discover_group_entities
from .discover_label_entities import discover_label_entities
from .discover_page_entities import discover_page_entities
from .discover_space_entities import discover_space_entities
from .discover_template_entities import discover_template_entities
from .discover_user_entities import discover_user_entities
from .manage_calendar import manage_calendar
from .manage_file import manage_file
from .manage_label import manage_label
from .manage_page import manage_page
from .manage_restrictions import manage_restrictions
from .manage_space import manage_space
from .transfer_to_human import transfer_to_human


ALL_TOOLS_INTERFACE_1 = [
    approval_lookup,
    create_new_audit_trail,
    create_notification,
    discover_calendar_entities,
    discover_file_entities,
    discover_group_entities,
    discover_label_entities,
    discover_page_entities,
    discover_space_entities,
    discover_template_entities,
    discover_user_entities,
    manage_calendar,
    manage_file,
    manage_label,
    manage_page,
    manage_restrictions,
    manage_space,
    transfer_to_human
]
