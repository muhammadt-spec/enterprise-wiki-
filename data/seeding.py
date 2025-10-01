import json
import random
from datetime import datetime, timedelta, timezone
from faker import Faker
from collections import defaultdict

fake = Faker()

# ------------------------------
# Helpers & Global Configuration
# ------------------------------

# IMPORTANT: if your checker looks in "<folder>/data", point OUTPUT_DIR there.
OUTPUT_DIR = "."  # e.g. r"c:\Users\Admin\Documents\proposal\Enterprise Wiki\data"

class IDGen:
    """Per-table incremental string ID generator starting from '1'."""
    def __init__(self):
        self.counters = defaultdict(int)
    def next(self, table):
        self.counters[table] += 1
        return str(self.counters[table])

idgen = IDGen()

def parse_iso(dt_str: str) -> datetime:
    # robust parse and normalize to naive for Faker
    dt = datetime.fromisoformat(dt_str)
    return dt.replace(tzinfo=None) if dt.tzinfo else dt

def parent_created_at(cls: str, ref_id: str) -> datetime:
    # map class -> table dict
    table_map = {
        "space": spaces,
        "page": pages,
        "template": templates,
        "workflow": workflows,
        "integration": integrations,
    }
    row = table_map[cls].get(ref_id)
    if not row:
        return datetime.now()
    return parse_iso(row["created_at"])

def ts_pair(days_back_max=365, jitter_hours=240):
    """Return created_at, updated_at with created_at <= updated_at, as ISO strings."""
    created = fake.date_time_between(start_date=f"-{days_back_max}d", end_date="-1d")
    updated = created + timedelta(hours=random.randint(0, jitter_hours))
    return created.isoformat(), updated.isoformat()

def pick_email(first, last, domains=None):
    domains = domains or ["example.com","acme.io","contoso.com","mail.com","workspace.org","product.dev"]
    base = f"{first}.{last}".lower().replace(" ", "")
    suffix = str(random.randint(1, 9999)) if random.random() < 0.35 else ""
    return f"{base}{suffix}@{random.choice(domains)}"

def phone_e164():
    # US-like E.164; adjust as needed for your locale
    area = random.choice(["202","213","305","312","415","503","617","646","650","702","720","781"])
    rest = f"{random.randint(200,999)}{random.randint(1000,9999)}"
    return f"+1{area}{rest}"

def chance(p):
    return random.random() < p

def write_json(table_name, obj):
    with open(f"{OUTPUT_DIR}/{table_name}.json", "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

# ------------------------------
# Enumerations (schema "notes")
# ------------------------------
USER_STATUS = ["Active","Suspended","Deactivated"]
SPACE_TYPE = ["Team","Department","Project","Knowledge"]
SPACE_STATUS = ["Active","Suspended","Deactivated"]
PAGE_TYPE = ["Standard","Policy","SOP","Landing","Archive","Other"]
PAGE_STATUS = ["Draft","Published","Archived"]
WORKFLOW_STATE = ["Proposed","In_Review","Approved","Rejected","Retired"]
LABEL_SCOPE = ["Global","Space"]
TEMPLATE_SCOPE = ["Global","Space"]
TEMPLATE_SENS = ["Normal","Official"]
TEMPLATE_STATUS = ["Active","Deprecated"]
RESTRICTION_TYPE = ["none","edit_only","view_and_edit"]
RESTRICTION_PERM = ["view","edit"]
PERM_LEVEL = ["Global","Space","Page"]
PERM_ACTION = ["view","edit","delete","admin","comment","attach"]
WORKFLOW_SCOPE = ["Global","Space"]
EVENT_TYPE = ["Meeting","Milestone","Release","Holiday","Other"]
INTEGRATION_TYPE = ["jira","slack","teams","drive","sharepoint","analytics"]
INTEGRATION_SCOPE = ["Global","Space"]
INTEGRATION_STATUS = ["Active","Disabled","Error"]
REPORT_TYPE = ["top_pages","active_spaces","stale_content","trend"]
REPORT_SCOPE = ["Global","Space"]
NOTIF_TYPE = ["alert","report","reminder"]
NOTIF_CLASS = ["space","page","template","workflow","integration"]
NOTIF_STATUS = ["Queued","Sent","Failed"]
MIGRATION_STAGE = ["test","production"]
MIGRATION_MODE = ["all","related_only"]
MIGRATION_STATUS = ["draft","running","completed","failed"]
AUDIT_RESULT = ["success","failure"]
SERVICE_CRIT = ["Low","Medium","High","Critical"]
SERVICE_STATUS = ["Active","Retired"]
CI_TYPE = ["App","Service","Server","DB","Network","Storage","Endpoint","Other"]
CI_ENV = ["Prod","Staging","Dev","Test"]
CI_STATUS = ["Active","Maintenance","Retired"]
PROBLEM_TYPE = ["Known_Error","RCA_Pending","RCA_Confirmed"]
PROBLEM_STATUS = ["New","Under_Investigation","Resolved","Closed"]
ROOT_CAUSE = ["Config","Capacity","Code","Network","Vendor","Process","Unknown"]
INC_STATUS = ["New","Assigned","In_Progress","Resolved","Closed"]
INC_PRIORITY = ["P1","P2","P3","P4","P5"]
INC_IMPACT = ["Low","Medium","High","Critical"]
INC_URGENCY = ["Low","Medium","High","Critical"]

# Controlled "codes" (not free text)
INC_DESC_CODES = ["HW_DISK_FAILURE","SW_AUTH_ERROR","NET_LATENCY","ACCESS_LOCKED","SEC_EVENT"]
RESOLUTION_CODES = ["PATCH_APPLIED","REBOOTED","CRED_RESET","CFG_ROLLBACK","NO_FAULT_FOUND"]

# Category/Subcategory compatibility map (coherent connections)
CATEGORY_MAP = {
    "Hardware": ["Disk","CPU","Memory","Power"],
    "Software": ["Auth","UI","API","Deploy"],
    "Network": ["Latency","Routing","DNS","Firewall"],
    "Access": ["SSO","MFA","Provisioning","Roles"],
    "Security": ["Malware","Phishing","Vuln","Policy"]
}

# ------------------------------
# Containers (tables)
# ------------------------------
users = {}
groups = {}
# NOTE: all the following "join-ish" tables now have single IDs
group_members = {}                 # keyed by group_member_id
permission_sets = {}
permission_grants = {}             # keyed by permission_grant_id
spaces = {}
pages = {}
attachments = {}
labels = {}
page_labels = {}                   # keyed by page_label_id
attachment_labels = {}             # keyed by attachment_label_id
templates = {}
restriction_sets = {}
restriction_subject_users = {}     # keyed by restriction_subject_user_id
restriction_subject_groups = {}    # keyed by restriction_subject_group_id
workflows = {}
workflow_transitions = {}
calendars = {}
calendar_events = {}
integrations = {}
reports = {}
notifications = {}
migration_plans = {}
audit_trail = {}
services = {}
configuration_items = {}
problems = {}
incidents = {}
slas = {}
incident_slas = {}                 # keyed by incident_sla_id

# ------------------------------
# 1) Seed core Users & Groups
# ------------------------------
NUM_USERS = 20
NUM_GROUPS = 6

for _ in range(NUM_USERS):
    user_id = idgen.next("users")
    created_at, updated_at = ts_pair()
    first = fake.first_name()
    last = fake.last_name()
    users[user_id] = {
        "user_id": str(user_id),
        "full_name": f"{first} {last}",
        "email": pick_email(first, last),
        "status": random.choice(USER_STATUS),
        "timezone": random.choice(["UTC","America/New_York","Europe/Berlin","Asia/Karachi","Asia/Kolkata","America/Los_Angeles"]),
        "position": random.choice(["Engineer","Product Manager","Designer","Analyst","Support","DevOps","QA"]),
        "department": random.choice(["Engineering","Product","Design","IT","Support","Marketing"]),
        "location": f"{fake.city()}, {fake.country_code()}",
        "about_me": None,  # free text left empty
        "phone": phone_e164(),
        "created_at": created_at,
        "updated_at": updated_at
    }

for _ in range(NUM_GROUPS):
    gid = idgen.next("groups")
    created_at, updated_at = ts_pair()
    groups[gid] = {
        "group_id": str(gid),
        "group_name": f"{random.choice(['Platform','SRE','Mobile','Web','Ops','Data','Security','Growth'])}-{fake.unique.bothify(text='??')}".upper(),
        "description": None,  # free text left empty
        "created_at": created_at,
        "updated_at": updated_at
    }

# group_members: each group gets up to 3 random members (can be 0)
for gid in list(groups.keys()):
    member_count = random.randint(0, 3)
    if member_count:
        for user_id in random.sample(list(users.keys()), k=member_count):
            gm_id = idgen.next("group_members")
            group_members[gm_id] = {
                "group_member_id": str(gm_id),
                "group_id": str(gid),
                "user_id": str(user_id),
                "added_at": fake.date_time_between(start_date="-180d", end_date="now").isoformat()
            }

# ------------------------------
# 2) Seed Spaces & Permission Sets (resolve circular ref)
# ------------------------------
NUM_SPACES = 5

# Create spaces without baseline_permissions_id first
for _ in range(NUM_SPACES):
    sid = idgen.next("spaces")
    created_at, updated_at = ts_pair()
    spaces[sid] = {
        "space_id": str(sid),
        "space_key": fake.unique.bothify(text="????").upper(),
        "name": f"{random.choice(['Engineering','Design','Ops','Product','Support','Security'])} Space {fake.random_int(1, 99)}",
        "type": random.choice(SPACE_TYPE),
        "status": random.choice(SPACE_STATUS),
        "owner_group_id": random.choice(list(groups.keys())) if groups else "1",
        "baseline_permissions_id": None,  # to be assigned after permission_sets created
        "created_at": created_at,
        "updated_at": updated_at
    }

# Now create permission_sets targeting spaces
for sid in list(spaces.keys()):
    pset_id = idgen.next("permission_sets")
    created_at, updated_at = ts_pair()
    permission_sets[pset_id] = {
        "permission_set_id": str(pset_id),
        "level": "Space",
        "target_id": str(sid),  # references spaces.space_id
        "version": random.choice(["v1","v2"]),
        "created_at": created_at,
        "updated_at": updated_at
    }
    # Assign baseline_permissions_id back to space
    spaces[sid]["baseline_permissions_id"] = str(pset_id)

# permission_grants: each permission_set gets up to 3 grants
for pset_id, _ in permission_sets.items():
    grant_cnt = random.randint(1, 3)
    for _ in range(grant_cnt):
        subj_type = random.choice(["user","group"])
        subj_id = random.choice(list(users.keys())) if subj_type == "user" else random.choice(list(groups.keys()))
        action = random.choice(PERM_ACTION)
        pg_id = idgen.next("permission_grants")
        permission_grants[pg_id] = {
            "permission_grant_id": str(pg_id),
            "permission_set_id": str(pset_id),
            "subject_type": subj_type,
            "subject_id": str(subj_id),
            "action": action
        }

# ------------------------------
# 3) Pages (hierarchy), Attachments, Labels
# ------------------------------
# Create a small page tree per space (root + up to 3 children)
for sid in list(spaces.keys()):
    # root page
    root_id = idgen.next("pages")
    created_at, updated_at = ts_pair()
    creator = random.choice(list(users.keys()))
    last_by = random.choice(list(users.keys()))
    pages[root_id] = {
        "page_id": str(root_id),
        "space_id": str(sid),
        "title": f"{spaces[sid]['name']} Home",
        "type": random.choice(PAGE_TYPE),
        "parent_page_id": None,
        "content_body": None,  # free text left empty
        "creator_id": str(creator),
        "last_modified_by": str(last_by),
        "last_modified_at": updated_at,
        "status": random.choice(PAGE_STATUS),
        "workflow_state": random.choice(WORKFLOW_STATE),
        "restrictions_id": None,
        "version_number": random.randint(1, 12),
        "created_at": created_at,
        "updated_at": updated_at
    }

    # children (0-3)
    for _ in range(random.randint(0, 3)):
        page_id = idgen.next("pages")
        c_at, u_at = ts_pair()
        creator = random.choice(list(users.keys()))
        last_by = random.choice(list(users.keys()))
        pages[page_id] = {
            "page_id": str(page_id),
            "space_id": str(sid),
            "title": fake.sentence(nb_words=4).rstrip("."),
            "type": random.choice(PAGE_TYPE),
            "parent_page_id": str(root_id),
            "content_body": None,
            "creator_id": str(creator),
            "last_modified_by": str(last_by),
            "last_modified_at": u_at,
            "status": random.choice(PAGE_STATUS),
            "workflow_state": random.choice(WORKFLOW_STATE),
            "restrictions_id": None,
            "version_number": random.randint(1, 8),
            "created_at": c_at,
            "updated_at": u_at
        }

# Attachments per page (0-3)
for pgid in list(pages.keys()):
    for _ in range(random.randint(0, 3)):
        att_id = idgen.next("attachments")
        c_at, u_at = ts_pair()
        uploader = random.choice(list(users.keys()))
        ext = random.choice([".png",".jpg",".pdf",".docx",".xlsx",".pptx",".txt"])
        filename = fake.file_name(extension=ext.strip("."))
        attachments[att_id] = {
            "attachment_id": str(att_id),
            "page_id": str(pgid),
            "filename": filename,
            "mime_type": {
                ".png":"image/png", ".jpg":"image/jpeg", ".pdf":"application/pdf",
                ".docx":"application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ".xlsx":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ".pptx":"application/vnd.openxmlformats-officedocument.presentationml.presentation",
                ".txt":"text/plain"
            }[ext],
            "filesize_bytes": random.randint(3_000, 3_000_000),
            "uploader_id": str(uploader),
            "uploaded_at": fake.date_time_between(start_date="-180d", end_date="now").isoformat(),
            "version_number": random.randint(1, 5),
            "created_at": c_at,
            "updated_at": u_at
        }

# Labels (space-scoped or global) and applying to pages/attachments
for _ in range(12):
    lid = idgen.next("labels")
    scope = random.choice(LABEL_SCOPE)
    sp = random.choice(list(spaces.keys())) if scope == "Space" and spaces else None
    labels[lid] = {
        "label_id": str(lid),
        "label_text": fake.word().lower(),
        "scope": scope,
        "space_id": str(sp) if scope == "Space" else None,
        "created_by": random.choice(list(users.keys())),
        "created_at": fake.date_time_between(start_date="-180d", end_date="now").isoformat()
    }

# page_labels (0-3 labels per page)  -> now has single ID
label_ids = list(labels.keys())
for pgid in list(pages.keys()):
    for lid in random.sample(label_ids, k=random.randint(0, min(3, len(label_ids)))):
        pl_id = idgen.next("page_labels")
        page_labels[pl_id] = {
            "page_label_id": str(pl_id),
            "page_id": str(pgid),
            "label_id": str(lid),
            "applied_at": fake.date_time_between(start_date="-120d", end_date="now").isoformat()
        }

# attachment_labels (0-2 labels per attachment) -> now has single ID
for attid in list(attachments.keys()):
    for lid in random.sample(label_ids, k=random.randint(0, min(2, len(label_ids)))):
        al_id = idgen.next("attachment_labels")
        attachment_labels[al_id] = {
            "attachment_label_id": str(al_id),
            "attachment_id": str(attid),
            "label_id": str(lid),
            "applied_at": fake.date_time_between(start_date="-120d", end_date="now").isoformat()
        }

# ------------------------------
# 4) Templates & Restrictions
# ------------------------------
# A few restriction sets
for _ in range(5):
    rsid = idgen.next("restriction_sets")
    c_at, u_at = ts_pair()
    restriction_sets[rsid] = {
        "restrictions_id": str(rsid),
        "type": random.choice(RESTRICTION_TYPE),
        "created_at": c_at,
        "updated_at": u_at
    }

# Assign some pages a restriction set
rsids = list(restriction_sets.keys())
for pgid, row in pages.items():
    if rsids and chance(0.25):
        row["restrictions_id"] = random.choice(rsids)

# Subject users/groups for restrictions (0-3 each) -> now have single IDs
for rsid in rsids:
    for _ in range(random.randint(0, 3)):
        uid = random.choice(list(users.keys()))
        perm = random.choice(RESTRICTION_PERM)
        rsu_id = idgen.next("restriction_subject_users")
        restriction_subject_users[rsu_id] = {
            "restriction_subject_user_id": str(rsu_id),
            "restrictions_id": str(rsid),
            "user_id": str(uid),
            "perm": perm
        }
    for _ in range(random.randint(0, 3)):
        gid = random.choice(list(groups.keys()))
        perm = random.choice(RESTRICTION_PERM)
        rsg_id = idgen.next("restriction_subject_groups")
        restriction_subject_groups[rsg_id] = {
            "restriction_subject_group_id": str(rsg_id),
            "restrictions_id": str(rsid),
            "group_id": str(gid),
            "perm": perm
        }

# Templates (some global, some space)
for _ in range(8):
    tid = idgen.next("templates")
    c_at, u_at = ts_pair()
    scope = random.choice(TEMPLATE_SCOPE)
    sid = random.choice(list(spaces.keys())) if scope == "Space" else None
    templates[tid] = {
        "template_id": str(tid),
        "name": f"{random.choice(['SOP','RFC','Incident Report','Postmortem','Design Doc'])} Template {fake.bothify(text='##')}",
        "scope": scope,
        "space_id": str(sid) if scope == "Space" else None,
        "owner_id": random.choice(list(users.keys())),
        "sensitivity": random.choice(TEMPLATE_SENS),
        "status": random.choice(TEMPLATE_STATUS),
        "sections_json": None,  # free text left empty
        "review_due_at": fake.date_time_between(start_date="-60d", end_date="+60d").isoformat(),
        "created_at": c_at,
        "updated_at": u_at
    }

# ------------------------------
# 5) Workflows & Transitions
# ------------------------------
for _ in range(5):
    wf_id = idgen.next("workflows")
    c_at, u_at = ts_pair()
    scope = random.choice(WORKFLOW_SCOPE)
    sid = random.choice(list(spaces.keys())) if scope == "Space" else None
    workflows[wf_id] = {
        "workflow_id": str(wf_id),
        "name": f"WF-{fake.word().capitalize()}",
        "scope": scope,
        "space_id": str(sid) if scope == "Space" else None,
        "steps_json": None,  # free text left empty
        "enabled": chance(0.8),
        "created_at": c_at,
        "updated_at": u_at
    }

# A few transitions tied to existing pages
for _ in range(12):
    if not pages:
        break
    tr_id = idgen.next("workflow_transitions")
    pgid = random.choice(list(pages.keys()))
    from_state = random.choice(WORKFLOW_STATE)
    to_state = random.choice([s for s in WORKFLOW_STATE if s != from_state])
    actor = random.choice(list(users.keys()))
    ts = fake.date_time_between(start_date="-90d", end_date="now").isoformat()
    workflow_transitions[tr_id] = {
        "transition_id": str(tr_id),
        "page_id": str(pgid),
        "from_state": from_state,
        "to_state": to_state,
        "action": random.choice(["submit","approve","reject","request_changes","publish","retire"]),
        "actor_id": str(actor),
        "comment": None,  # free text left empty
        "timestamp": ts
    }

# ------------------------------
# 6) Calendars & Events
# ------------------------------
for sid in list(spaces.keys()):
    if chance(0.7):
        cal_id = idgen.next("calendars")
        c_at, u_at = ts_pair()
        creator = random.choice(list(users.keys()))
        calendars[cal_id] = {
            "calendar_id": str(cal_id),
            "space_id": str(sid),
            "name": f"{spaces[sid]['name']} Calendar",
            "created_by": str(creator),
            "created_at": c_at,
            "updated_at": u_at
        }
        # events (0-3)
        for _ in range(random.randint(0, 3)):
            evt_id = idgen.next("calendar_events")
            start = fake.date_time_between(start_date="-30d", end_date="+60d")
            end = start + timedelta(hours=random.choice([1,2,3]))
            calendar_events[evt_id] = {
                "event_id": str(evt_id),
                "calendar_id": str(cal_id),
                "title": fake.sentence(nb_words=3).rstrip("."),
                "start_at": start.isoformat(),
                "end_at": end.isoformat(),
                "event_type": random.choice(EVENT_TYPE),
                "created_by": str(creator),
                "created_at": fake.date_time_between(start_date="-60d", end_date="now").isoformat()
            }

# ------------------------------
# 7) Integrations, Reports, Notifications, Migration, Audit
# ------------------------------
for _ in range(6):
    iid = idgen.next("integrations")
    c_at, u_at = ts_pair()
    scope = random.choice(INTEGRATION_SCOPE)
    sid = random.choice(list(spaces.keys())) if scope == "Space" else None
    integrations[iid] = {
        "integration_id": str(iid),
        "type": random.choice(INTEGRATION_TYPE),
        "scope": scope,
        "space_id": str(sid) if scope == "Space" else None,
        "config_json": None,  # free text left empty
        "status": random.choice(INTEGRATION_STATUS),
        "approved_by_compliance": chance(0.8),
        "created_at": c_at,
        "updated_at": u_at
    }

for _ in range(8):
    rid = idgen.next("reports")
    start = fake.date_time_between(start_date="-120d", end_date="-30d")
    end = start + timedelta(days=random.randint(7, 45))
    reports[rid] = {
        "report_id": str(rid),
        "report_type": random.choice(REPORT_TYPE),
        "scope": random.choice(REPORT_SCOPE),
        "space_id": random.choice(list(spaces.keys())) if chance(0.6) else None,
        "date_range_start": start.isoformat(),
        "date_range_end": end.isoformat(),
        "generated_by": random.choice(list(users.keys())),
        "generated_at": (end + timedelta(hours=random.randint(1,24))).isoformat(),
        "export_ref": fake.file_name(extension="csv"),
        "created_at": fake.date_time_between(start_date="-120d", end_date="now").isoformat()
    }

# --- notifications: ensure class ↔ reference_entity_id consistency
CLASS_TO_TABLE = {
    "space": ("spaces", "space_id"),
    "page": ("pages", "page_id"),
    "template": ("templates", "template_id"),
    "workflow": ("workflows", "workflow_id"),
    "integration": ("integrations", "integration_id"),
}
_table_obj = {
    "spaces": spaces,
    "pages": pages,
    "templates": templates,
    "workflows": workflows,
    "integrations": integrations,
}
def pick_reference_for_class(cls_name):
    target = CLASS_TO_TABLE.get(cls_name)
    if target:
        tbl_name, _ = target
        pool = _table_obj[tbl_name]
        if pool:
            return random.choice(list(pool.keys())), cls_name
    # graceful fallbacks in priority order
    for fb in ["page", "space", "integration", "workflow", "template"]:
        t = CLASS_TO_TABLE.get(fb)
        pool = _table_obj[t[0]]
        if pool:
            return random.choice(list(pool.keys())), fb
    return None, None

for _ in range(10):
    nid = idgen.next("notifications")

    # pick a class and a valid reference id (your existing helper)
    cls = random.choice(NOTIF_CLASS)
    ref_id, cls = pick_reference_for_class(cls)
    if ref_id is None:
        continue

    # ensure notification.created_at >= parent.created_at
    p_created = parent_created_at(cls, ref_id)
    # Faker accepts datetimes for start/end; guarantee end >= start
    now_dt = datetime.now()
    start_dt = p_created if p_created < now_dt else now_dt - timedelta(seconds=1)
    created_dt = fake.date_time_between(start_date=start_dt, end_date=now_dt)
    sent_dt = (created_dt + timedelta(minutes=random.randint(1, 600))) if chance(0.7) else None

    notifications[nid] = {
        "notification_id": str(nid),
        "type": random.choice(NOTIF_TYPE),
        "class": cls,
        "recipient_email": pick_email(fake.first_name(), fake.last_name()),
        "recipient_group_id": random.choice(list(groups.keys())) if chance(0.5) else None,
        "reference_entity_type": cls,
        "reference_entity_id": str(ref_id),
        "status": random.choice(NOTIF_STATUS) if sent_dt else "Queued",
        "created_at": created_dt.isoformat(),
        "sent_at": sent_dt.isoformat() if sent_dt else None,
        "error_message": None
    }

for _ in range(3):
    mpid = idgen.next("migration_plans")
    created = fake.date_time_between(start_date="-200d", end_date="-1d")
    migration_plans[mpid] = {
        "plan_id": str(mpid),
        "name": f"Migration {fake.bothify(text='####')}",
        "stage": random.choice(MIGRATION_STAGE),
        "items_json": None,  # free text left empty
        "user_migration_mode": random.choice(MIGRATION_MODE),
        "created_by": random.choice(list(users.keys())),
        "created_at": created.isoformat(),
        "status": random.choice(MIGRATION_STATUS),
        "precheck_summary_json": None,
        "run_log_ref": fake.file_name(extension="log")
    }

for _ in range(15):
    aid = idgen.next("audit_trail")
    ts = fake.date_time_between(start_date="-200d", end_date="now").isoformat()
    entity_type = random.choice(["space","page","template","workflow","integration","user","group"])
    entity_id = random.choice(list(spaces.keys()) + list(pages.keys()) + list(users.keys()) + list(groups.keys()))
    audit_trail[aid] = {
        "audit_id": str(aid),
        "action": random.choice(["create","update","delete","grant","revoke","publish"]),
        "actor_id": random.choice(list(users.keys())),
        "entity_type": entity_type,
        "entity_id": str(entity_id),
        "meta_json": None,  # free text left empty
        "timestamp": ts,
        "result": random.choice(AUDIT_RESULT),
        "error_message": None  # free text left empty
    }

# ------------------------------
# 8) ITSM: Services, CIs, Problems (FIXED), Incidents, SLAs
# ------------------------------
# Services
for _ in range(5):
    sid = idgen.next("services")
    c_at, u_at = ts_pair()
    services[sid] = {
        "service_id": str(sid),
        "name": f"{random.choice(['Checkout','Auth','Search','Billing','Notifications','Analytics'])} Service",
        "business_criticality": random.choice(SERVICE_CRIT),
        "owner_group_id": random.choice(list(groups.keys())),
        "status": random.choice(SERVICE_STATUS),
        "created_at": c_at,
        "updated_at": u_at
    }

# Configuration Items linked to services and groups
for _ in range(10):
    ci = idgen.next("configuration_items")
    c_at, u_at = ts_pair()
    svc = random.choice(list(services.keys()))
    configuration_items[ci] = {
        "ci_id": str(ci),
        "name": f"{random.choice(['api','web','db','cache','queue','proxy'])}-{fake.bothify(text='??##')}".lower(),
        "ci_type": random.choice(CI_TYPE),
        "environment": random.choice(CI_ENV),
        "status": random.choice(CI_STATUS),
        "service_id": str(svc),
        "owner_group_id": random.choice(list(groups.keys())),
        "created_at": c_at,
        "updated_at": u_at
    }

# Problems  ✅ FIXED: keep datetimes as datetimes until final .isoformat()
for _ in range(6):
    pid = idgen.next("problems")
    created_dt = fake.date_time_between(start_date="-120d", end_date="-2d")
    resolved_dt = created_dt + timedelta(days=random.randint(1, 20)) if chance(0.5) else None
    closed_dt = (resolved_dt + timedelta(days=random.randint(1, 10))) if resolved_dt else None

    problems[pid] = {
        "problem_id": str(pid),
        "title": fake.sentence(nb_words=5).rstrip("."),
        "problem_type": random.choice(PROBLEM_TYPE),
        "status": random.choice(PROBLEM_STATUS if resolved_dt else ["New","Under_Investigation"]),
        "root_cause_code": random.choice(ROOT_CAUSE),
        "owner_group_id": random.choice(list(groups.keys())),
        "created_by": random.choice(list(users.keys())),
        "created_at": created_dt.isoformat(),
        "resolved_at": resolved_dt.isoformat() if resolved_dt else None,
        "closed_at": closed_dt.isoformat() if closed_dt else None
    }

# SLAs per service (P1-P3 active)
for svc in list(services.keys()):
    for prio in ["P1","P2","P3"]:
        sla_id = idgen.next("slas")
        c_at, u_at = ts_pair()
        slas[sla_id] = {
            "sla_id": str(sla_id),
            "service_id": str(svc),
            "priority": prio,
            "response_target_minutes": {"P1":15,"P2":30,"P3":60}[prio],
            "resolution_target_minutes": {"P1":240,"P2":480,"P3":1440}[prio],
            "active": True,
            "created_at": c_at,
            "updated_at": u_at
        }

# Incidents
for _ in range(14):
    iid = idgen.next("incidents")
    c_at, u_at = ts_pair()
    svc = random.choice(list(services.keys()))
    # Pick a CI of the same service if available; fallback to any CI
    service_cis = [ci for ci, row in configuration_items.items() if row["service_id"] == svc]
    ci = random.choice(service_cis if service_cis else list(configuration_items.keys()))

    cat = random.choice(list(CATEGORY_MAP.keys()))
    sub = random.choice(CATEGORY_MAP[cat])
    reporter = random.choice(list(users.keys()))
    assignee = random.choice(list(users.keys()))
    grp = random.choice(list(groups.keys()))
    status = random.choice(INC_STATUS)

    resolved_at = None
    closed_at = None
    if status in ["Resolved","Closed"]:
        resolved_at_dt = datetime.fromisoformat(u_at) - timedelta(hours=random.randint(0, 48))
        resolved_at = resolved_at_dt.isoformat()
        if status == "Closed":
            closed_at = (resolved_at_dt + timedelta(hours=random.randint(1, 24))).isoformat()

    incidents[iid] = {
        "incident_id": str(iid),
        "title": fake.sentence(nb_words=6).rstrip("."),
        "description_code": random.choice(INC_DESC_CODES),
        "status": status,
        "priority": random.choice(INC_PRIORITY),
        "impact": random.choice(INC_IMPACT),
        "urgency": random.choice(INC_URGENCY),
        "reporter_id": str(reporter),
        "assignee_id": str(assignee),
        "assignment_group_id": str(grp),
        "category": cat,
        "subcategory": sub,
        "ci_id": str(ci),
        "problem_id": random.choice(list(problems.keys())) if chance(0.3) else None,
        "service_id": str(svc),
        "resolution_notes_code": random.choice(RESOLUTION_CODES) if resolved_at else None,
        "resolved_at": resolved_at,
        "closed_at": closed_at,
        "created_at": c_at,
        "updated_at": u_at
    }

# Incident SLAs: apply one active SLA matching service & priority; track timing
for inc_id, inc in incidents.items():
    svc = inc["service_id"]
    prio = inc["priority"]
    matching_slas = [sid for sid, s in slas.items() if s["service_id"] == svc and s["priority"] == prio and s["active"]]
    if not matching_slas:
        continue
    sla_id = random.choice(matching_slas)
    started = fake.date_time_between(start_date="-10d", end_date="-1d")
    resp_due = started + timedelta(minutes=slas[sla_id]["response_target_minutes"])
    reso_due = started + timedelta(minutes=slas[sla_id]["resolution_target_minutes"])
    first_resp = started + timedelta(minutes=random.randint(1, slas[sla_id]["response_target_minutes"] + 30))
    resolved_at = datetime.fromisoformat(inc["resolved_at"]) if inc["resolved_at"] else None

    isl_id = idgen.next("incident_slas")
    incident_slas[isl_id] = {
        "incident_sla_id": str(isl_id),
        "incident_id": str(inc_id),
        "sla_id": str(sla_id),
        "started_at": started.isoformat(),
        "response_due_at": resp_due.isoformat(),
        "resolution_due_at": reso_due.isoformat(),
        "first_response_at": first_resp.isoformat(),
        "resolved_at": resolved_at.isoformat() if resolved_at else None,
        "response_breached": first_resp > resp_due,
        "resolution_breached": (resolved_at and resolved_at > reso_due) if resolved_at else False
    }

# ------------------------------
# Save all “tables” to JSON
# ------------------------------
write_json("users", users)
write_json("groups", groups)
write_json("group_members", group_members)
write_json("spaces", spaces)
write_json("permission_sets", permission_sets)
write_json("permission_grants", permission_grants)
write_json("pages", pages)
write_json("attachments", attachments)
write_json("labels", labels)
write_json("page_labels", page_labels)
write_json("attachment_labels", attachment_labels)
write_json("templates", templates)
write_json("restriction_sets", restriction_sets)
write_json("restriction_subject_users", restriction_subject_users)
write_json("restriction_subject_groups", restriction_subject_groups)
write_json("workflows", workflows)
write_json("workflow_transitions", workflow_transitions)
write_json("calendars", calendars)
write_json("calendar_events", calendar_events)
write_json("integrations", integrations)
write_json("reports", reports)
write_json("notifications", notifications)
write_json("migration_plans", migration_plans)
write_json("audit_trail", audit_trail)
write_json("services", services)
write_json("configuration_items", configuration_items)
write_json("problems", problems)
write_json("incidents", incidents)
write_json("slas", slas)
write_json("incident_slas", incident_slas)

print("✅ Seeding complete. JSON files written next to this script.")
