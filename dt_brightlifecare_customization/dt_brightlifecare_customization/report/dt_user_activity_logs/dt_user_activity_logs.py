import frappe
from frappe import _
from frappe.utils import add_days, now_datetime
from frappe.utils.data import get_datetime_str


user_map = {}

def get_username(user_name):
    """ Check if user exists in user_map if exists then return user full name else create new entry in user_map with user.name as key and user.full_name as value """
    if user_name in user_map:
        return user_map[user_name]
    else:
        # fetch user full name from database
        user_full_name = frappe.db.get_value("User", user_name, "full_name")
        user_map[user_name] = user_full_name
        return user_full_name
    
    

def execute(filters=None):
    """Main function to generate the report"""
    
    validate_filters(filters)
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def validate_filters(filters):
    if not filters:
        filters = {}

    if not filters.get("from_date"):
        filters["from_date"] = add_days(now_datetime(), -7)
    if not filters.get("to_date"):
        filters["to_date"] = now_datetime()
        


def get_columns():
    """Return report columns structure"""
    return [
        {"label": _("Timestamp"), "fieldname": "creation", "fieldtype": "Datetime", "width": 200},
        {"label": _("User"), "fieldname": "user", "fieldtype": "Link", "options": "User", "width": 200},
        {"label": _("Operation"), "fieldname": "operation", "fieldtype": "Data", "width": 100,"align":"center"},
        # {"label": _("Full Name"), "fieldname": "full_name", "fieldtype": "Hidden", "width": 200},
        # {"label": _("Activity Type"), "fieldname": "activity_type", "fieldtype": "Data", "width": 180},
        {"label": _("Document Type"), "fieldname": "ref_doctype", "fieldtype": "Link", "options": "DocType", "width": 150},
        {"label": _("Document"), "fieldname": "ref_name", "fieldtype": "Dynamic Link", "options": "ref_doctype", "width": 180},
    ]


def get_data(filters):
    """Fetch and combine all activity data"""
    activity_data = []

    # Document creation detection (based on 'creation' field)
    activity_data.extend(get_created_documents(filters))

    # Get login/logout activity
    activity_data.extend(get_activity_logs(filters))

    # Get document transaction activity (submit, cancel, update)
    activity_data.extend(get_version_logs(filters))
    
    # Get deleted documents
    activity_data.extend(get_deleted_documents(filters))

    # Sort all activities by timestamp (newest first)
    activity_data.sort(key=lambda x: get_datetime_str(x["creation"]), reverse=True)

    return activity_data


def get_track_doctypes():
    """Return list of document types that have a 'track_changes' field tick"""
    return frappe.db.sql_list("""
                              SELECT name
                              FROM `tabDocType`
                              WHERE track_changes = 1
                              AND istable = 0
                              AND issingle = 0
                              AND name NOT IN ('Comment', 'File', 'Deleted Document','Email Queue','DocShare','Version','Notification Settings')
                              """, as_dict=False)
    
    

def get_created_documents(filters):
    """Use document 'creation' field to detect document creation"""
    tracked_doctypes = get_track_doctypes()

    creation_data = []
    
    filters_dict = {
        "creation": ["between", [filters["from_date"], filters["to_date"]]],
    }

    if filters.get("user"):
        filters_dict["owner"] = ["=", filters["user"]]

    
    
    
    for doctype in tracked_doctypes:
        docs = frappe.get_all(
            doctype,
            fields=["name", "creation", "owner"],
            filters = filters_dict
        )
        for doc in docs:
            creation_data.append({
                "creation": doc.creation,
                "user": doc.owner,
                "full_name":get_username(doc.owner),
                "activity_type": "Document Create",
                "ref_doctype": doctype,
                "ref_name": doc.name,
                "operation": "Create"
            })
    return creation_data


def get_activity_logs(filters):
    """Get user login/logout activities"""
    filters_dict = {
        "creation": ["between", [filters["from_date"], filters["to_date"]]],
    }

    if filters.get("user"):
        filters_dict["user"] = ["=", filters["user"]]

    logs = frappe.get_all(
        "Activity Log",
        fields=["creation", "user", "operation"],
        filters=filters_dict,
        order_by="creation DESC",
        limit_page_length=1000
    )

    return [{
        "creation": log.creation,
        "user": log.user,
        "full_name": get_username(log.user),
        "activity_type": log.operation,
        "ref_doctype": None,
        "ref_name": None,
        "operation": log.operation
    } for log in logs]


def get_version_logs(filters):
    """Get document version changes (submit, cancel, update)"""
    filters_dict = {
        "creation": ["between", [filters["from_date"], filters["to_date"]]],
    }

    if filters.get("user"):
        filters_dict["owner"] = ["=", filters["user"]]

    versions = frappe.get_all(
        "Version",
        fields=["creation", "owner as user", "ref_doctype", "docname as ref_name", "data"],
        filters=filters_dict,
        order_by="creation DESC",
        limit_page_length=1000
    )

    version_activities = []
    for version in versions:
        operation = get_version_operation(version)
        if operation:
            version_activities.append({
                "creation": version.creation,
                "user": version.user,
                "full_name": get_username(version.user),
                "activity_type": f"Document {operation}",
                "ref_doctype": version.ref_doctype,
                "ref_name": version.ref_name,
                "operation": operation
            })

    return version_activities


def get_deleted_documents(filters):
    """Get deleted documents from the Deleted Document doctype"""
    filters_dict = {
        "creation": ["between", [filters["from_date"], filters["to_date"]]],
    }

    if filters.get("user"):
        filters_dict["owner"] = ["=", filters["user"]]

    deleted_docs = frappe.get_all(
        "Deleted Document",
        fields=["name", "creation", "owner as user", "deleted_doctype as ref_doctype", "deleted_name as ref_name"],
        filters=filters_dict,
        order_by="creation DESC",
        limit_page_length=1000
    )

    return [{
        "creation": doc.creation,
        "user": doc.user,
        "full_name": get_username(doc.user),
        "activity_type": "Document Delete",
        "ref_doctype": doc.ref_doctype,
        "ref_name": doc.ref_name,
        "operation": "Delete"
    } for doc in deleted_docs]


def get_version_operation(version):
    """Determine the operation type from version data"""
    try:
        data = frappe.parse_json(version.data)
        if not data:
            return None

        # Detect Submit or Cancel
        if data.get("changed"):
            for field in data.get("changed"):
                if field[0] == "docstatus" and field[1] == 0 and field[2] == 1:
                    return "Submit"
                if field[0] == "docstatus" and field[1] == 1 and field[2] == 2:
                    return "Cancel"

        # Detect Create: only one version exists for this document and 'added' fields present
        

        # Detect Update
        if data.get("changed") or data.get("row_changed") or data.get("removed"):
            return "Update"

        return None
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Failed to parse version data")
        return None