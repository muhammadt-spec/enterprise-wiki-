from .provision_user_profile import provision_user_profile
from .create_team_grouping import create_team_grouping
from .enroll_user_to_group import enroll_user_to_group
from .bootstrap_permission_set import bootstrap_permission_set
from .authorize_permission_action import authorize_permission_action
from .configure_workflow_blueprint import configure_workflow_blueprint
from .record_page_workflow_transition import record_page_workflow_transition
from .attach_file_to_page import attach_file_to_page
from .create_taxonomy_label import create_taxonomy_label
from .label_page_with_tag import label_page_with_tag
from .create_template_record import create_template_record
from .create_restriction_policy import create_restriction_policy
from .add_subjects_to_restriction import add_subjects_to_restriction
from .create_incident_ticket import create_incident_ticket
from .create_ci_record import create_ci_record
from .create_service_record import create_service_record
from .create_problem_ticket import create_problem_ticket
from .create_sla_rule import create_sla_rule
from .begin_incident_sla_timer import begin_incident_sla_timer
from .add_calendar_event_record import add_calendar_event_record
from .query_user_by_email import query_user_by_email
from .list_group_members_users import list_group_members_users
from .lookup_space_by_key import lookup_space_by_key
from .list_pages_for_space import list_pages_for_space
from .list_attachments_for_page import list_attachments_for_page
from .list_permissions_for_target import list_permissions_for_target
from .list_incidents import list_incidents

ALL_TOOLS_INTERFACE_5 = [
    provision_user_profile,
    create_team_grouping,
    enroll_user_to_group,
    bootstrap_permission_set,
    authorize_permission_action,
    configure_workflow_blueprint,
    record_page_workflow_transition,
    attach_file_to_page,
    create_taxonomy_label,
    label_page_with_tag,
    create_template_record,
    create_restriction_policy,
    add_subjects_to_restriction,
    create_incident_ticket,
    create_ci_record,
    create_service_record,
    create_problem_ticket,
    create_sla_rule,
    begin_incident_sla_timer,
    add_calendar_event_record,
    query_user_by_email,
    list_group_members_users,
    lookup_space_by_key,
    list_pages_for_space,
    list_attachments_for_page,
    list_permissions_for_target,
    list_incidents
    
]
