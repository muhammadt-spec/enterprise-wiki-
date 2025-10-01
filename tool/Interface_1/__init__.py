from .create_user import create_user
from .create_group import create_group
from .add_group_member import add_group_member
from .grant_permission import grant_permission
from .create_permission_set import create_permission_set
from .create_workflow import create_workflow
from .transition_page_workflow import transition_page_workflow
from .upload_attachment import upload_attachment
from .create_label import create_label
from .apply_label_to_page import apply_label_to_page
from .create_template_simple import create_template_simple
from .create_restriction_set import create_restriction_set
from .add_restriction_subjects import add_restriction_subjects
from .create_incident import create_incident
from .create_configuration_item import create_configuration_item
from .create_service import create_service
from .create_problem import create_problem
from .create_sla import create_sla
from .start_incident_sla import start_incident_sla
from .add_calendar_event import add_calendar_event
from .get_user_by_email import get_user_by_email
from .get_group_members import get_group_members
from .get_space_by_key import get_space_by_key
from .get_pages_in_space import get_pages_in_space
from .get_attachments_for_page import get_attachments_for_page
from .get_permissions_for_target import get_permissions_for_target
from .get_incidents import get_incidents

ALL_TOOLS_INTERFACE_5 = [
    create_user,
    create_group,
    add_group_member,
    grant_permission,
    create_permission_set,
    create_workflow,
    transition_page_workflow,
    upload_attachment,
    create_label,
    apply_label_to_page,
    create_template_simple,
    create_restriction_set,
    add_restriction_subjects,
    create_incident,
    create_configuration_item,
    create_service,
    create_problem,
    create_sla,
    start_incident_sla,
    add_calendar_event,
    get_user_by_email,
    get_group_members,
    get_space_by_key,
    get_pages_in_space,
    get_attachments_for_page,
    get_permissions_for_target,
    get_incidents
]
