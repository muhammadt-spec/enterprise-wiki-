from .create_user_directory_entry import create_user_directory_entry
from .form_group_catalog_entry import form_group_catalog_entry
from .add_member_to_group import add_member_to_group
from .creates_permission_set_record import creates_permission_set_record
from .grant_permission_action import grant_permission_action
from .create_workflow_definition import create_workflow_definition
from .log_page_workflow_transition import log_page_workflow_transition
from .upload_attachment_for_page import upload_attachment_for_page
from .create_label_entry import create_label_entry
from .applies_label_to_page import applies_label_to_page
from .create_template_entry import create_template_entry
from .adds_restriction_subjects import adds_restriction_subjects
from .creates_restriction_set import creates_restriction_set
from .adds_restriction_subjects import adds_restriction_subjects
from .create_incident_record import create_incident_record
from .creates_configuration_item import creates_configuration_item
from .create_service_entry import create_service_entry
from .create_problem_record import create_problem_record
from .create_sla_policy import create_sla_policy
from .starts_incident_sla import starts_incident_sla
from .create_calendar_event import create_calendar_event
from .gets_user_by_email import gets_user_by_email
from .gets_group_members import gets_group_members
from .gets_space_by_key import gets_space_by_key
from .gets_pages_in_space import gets_pages_in_space
from .gets_attachments_for_page import gets_attachments_for_page
from .gets_permissions_for_target import gets_permissions_for_target
from .gets_incidents import gets_incidents

ALL_TOOLS_INTERFACE_5 = [
    create_user_directory_entry,
    form_group_catalog_entry,
    add_member_to_group,
    grant_permission_action,
    create_workflow_definition,
    log_page_workflow_transition,
    upload_attachment_for_page,
    create_label_entry,
    applies_label_to_page,
    create_template_entry,
    creates_permission_set_record,
    creates_restriction_set,
    adds_restriction_subjects,
    create_incident_record,
    creates_configuration_item,
    create_service_entry,
    create_problem_record,
    create_sla_policy,
    starts_incident_sla,
    create_calendar_event,
    gets_user_by_email,
    gets_group_members,
    gets_space_by_key,
    gets_pages_in_space,
    gets_attachments_for_page,
    gets_permissions_for_target,
    gets_incidents
]
