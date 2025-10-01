from .onboard_user_identity import onboard_user_identity
from .compose_group_container import compose_group_container
from .append_user_into_group import append_user_into_group
from .seed_permission_set_bundle import seed_permission_set_bundle
from .permit_action_assignment import permit_action_assignment
from .craft_workflow_spec import craft_workflow_spec
from .capture_page_workflow_transition import capture_page_workflow_transition
from .push_attachment_to_page import push_attachment_to_page
from .publish_label_term import publish_label_term
from .affix_label_to_page import affix_label_to_page
from .persist_template_blueprint import persist_template_blueprint
from .spawn_restriction_set import spawn_restriction_set
from .map_subjects_to_restriction import map_subjects_to_restriction
from .raise_incident_ticket import raise_incident_ticket
from .persist_configuration_item import persist_configuration_item
from .provision_service_catalog_item import provision_service_catalog_item
from .raise_problem_record import raise_problem_record
from .establish_sla_policy import establish_sla_policy
from .activate_incident_sla import activate_incident_sla
from .schedule_calendar_event import schedule_calendar_event
from .find_user_by_email_exact import find_user_by_email_exact
from .enumerate_group_members import enumerate_group_members
from .resolve_space_by_key import resolve_space_by_key
from .enumerate_pages_in_space import enumerate_pages_in_space
from .enumerate_attachments_for_page import enumerate_attachments_for_page
from .enumerate_permissions_for_target import enumerate_permissions_for_target
from .enumerate_incidents import enumerate_incidents

ALL_TOOLS_INTERFACE_5 = [
    onboard_user_identity,
    compose_group_container,
    append_user_into_group,
    seed_permission_set_bundle,
    permit_action_assignment,
    craft_workflow_spec,
    capture_page_workflow_transition,
    push_attachment_to_page,
    publish_label_term,
    affix_label_to_page,
    persist_template_blueprint,
    spawn_restriction_set,
    map_subjects_to_restriction,
    raise_incident_ticket,
    persist_configuration_item,
    provision_service_catalog_item,
    raise_problem_record,
    establish_sla_policy,
    activate_incident_sla,
    schedule_calendar_event,
    find_user_by_email_exact,
    enumerate_group_members,
    resolve_space_by_key,
    enumerate_pages_in_space,
    enumerate_attachments_for_page,
    enumerate_permissions_for_target,
    enumerate_incidents
]
