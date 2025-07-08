import frappe
from frappe import _

def execute(filters=None):
    if not filters:
        filters = {}
    validate_filters(filters)
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def validate_filters(filters):
    """Validate user input filters"""
    if filters.get("user"):
        if not frappe.db.exists("User", filters["user"]):
            frappe.throw(_("User {0} does not exist").format(filters["user"]))
    if filters.get("role"):
        if not frappe.db.exists("Role", filters["role"]):
            frappe.throw(_("Role {0} does not exist").format(filters["role"]))
    if filters.get("doctype"):
        if not frappe.db.exists("DocType", filters["doctype"]):
            frappe.throw(_("DocType {0} does not exist").format(filters["doctype"]))

def get_columns():
    return [
        {"label": _("User"), "fieldname": "user", "fieldtype": "Link", "options": "User", "width": 150},
        {"label": _("Full Name"), "fieldname": "full_name", "fieldtype": "Data", "width": 180},
        {"label": _("Role"), "fieldname": "role", "fieldtype": "Link", "options": "Role", "width": 150},
        {"label": _("DocType"), "fieldname": "doctype", "fieldtype": "Link", "options": "DocType", "width": 200},
        {"label": _("Perm Level"), "fieldname": "permlevel", "fieldtype": "Int", "width": 120},
        {"label": _("Read"), "fieldname": "read", "fieldtype": "Check", "width": 120},
        {"label": _("Write"), "fieldname": "write", "fieldtype": "Check", "width": 120},
        {"label": _("Create"), "fieldname": "create", "fieldtype": "Check", "width": 120},
        {"label": _("Delete"), "fieldname": "delete", "fieldtype": "Check", "width": 120},
        {"label": _("Submit"), "fieldname": "submit", "fieldtype": "Check", "width": 120},
        {"label": _("Cancel"), "fieldname": "cancel", "fieldtype": "Check", "width": 120},
        {"label": _("Amend"), "fieldname": "amend", "fieldtype": "Check", "width": 120},
        # {"label": _("Permission Type"), "fieldname": "permission_type", "fieldtype": "Data", "width": 120},
    ]

def get_data(filters):
    data = []
    user_filter = get_user_filters(filters)
    
    # frappe.error_log("User Filters = ", user_filter)
    users = frappe.get_all("User", 
                         filters=user_filter, 
                         fields=["name", "full_name", "enabled"],
                         order_by="name")

    for user in users:
        process_user_roles(user, filters, data)

    return data

def get_user_filters(filters):
    user_filter = {"user_type": "System User"}
    
    if filters.get("show_disable_users"):
        user_filter["enabled"] = 0
    else:
        user_filter["enabled"] = 1
    
    if filters.get("user"):
        user_filter["name"] = filters["user"]
    
    
    
    return user_filter

def process_user_roles(user, filters, data):
    user_roles = frappe.get_all("Has Role", 
                              filters={"parent": user.name}, 
                              fields=["role"],
                              order_by="role")

    if not user_roles and not filters.get("show_empty_roles"):
        return

    for role_entry in user_roles or [{"role": None}]:
        role = role_entry["role"]
        
        if filters.get("role") and role != filters.get("role"):
            continue
            
        process_role_doctypes(user, role, filters, data)

def process_role_doctypes(user, role, filters, data):
    doctype_list = get_doctypes_with_permissions(role)
    
    if not doctype_list and not filters.get("show_empty_perms"):
        return
        
    if not doctype_list:
        doctype_list = ["No Permissions"]

    for dt in doctype_list:
        if filters.get("doctype") and filters["doctype"] != dt:
            continue
            
        process_doctype_permissions(user, role, dt, data)

def get_doctypes_with_permissions(role):
    """Get all doctypes with permissions for the given role"""
    if not role:
        return []
        
    # Check custom permissions first
    doctypes = frappe.get_all("Custom DocPerm", 
                            filters={"role": role}, 
                            pluck="parent",
                            distinct=True)
    
    # Add standard permissions if no custom ones found
    if not doctypes:
        doctypes = frappe.get_all("DocPerm", 
                                filters={"role": role}, 
                                pluck="parent",
                                distinct=True)
    
    return doctypes

def process_doctype_permissions(user, role, doctype, data):
    """Process all permissions for a doctype-role combination"""
    # Try custom permissions first
    custom_perms = get_permissions("Custom DocPerm", role, doctype)
    if custom_perms:
        add_permissions_to_data(user, role, doctype, custom_perms, "Custom", data)
        return
        
    # Fall back to standard permissions
    standard_perms = get_permissions("DocPerm", role, doctype)
    if standard_perms:
        add_permissions_to_data(user, role, doctype, standard_perms, "Standard", data)
    elif doctype == "No Permissions":
        data.append(create_no_permissions_entry(user))

def get_permissions(doctype, role, parent):
    return frappe.get_all(
        doctype,
        filters={"role": role, "parent": parent},
        fields=["parent", "permlevel", "read", "write", "create", "delete", 
               "submit", "cancel", "amend"],
        order_by="permlevel"
    )

def add_permissions_to_data(user, role, doctype, permissions, perm_type, data):
    for perm in permissions:
        data.append({
            "user": user.name,
            "full_name": user.full_name,
            "role": role or "No Role Assigned",
            "doctype": perm["parent"],
            "permlevel": perm.get("permlevel", 0),
            "read": perm.get("read", 0),
            "write": perm.get("write", 0),
            "create": perm.get("create", 0),
            "delete": perm.get("delete", 0),
            "submit": perm.get("submit", 0),
            "cancel": perm.get("cancel", 0),
            "amend": perm.get("amend", 0),
            # "permission_type": perm_type,
        })

def create_no_permissions_entry(user):
    return {
        "user": user.name,
        "full_name": user.full_name,
        "role": "No Role Assigned",
        "doctype": "No Permissions",
        "permlevel": 0,
        "read": 0,
        "write": 0,
        "create": 0,
        "delete": 0,
        "submit": 0,
        "cancel": 0,
        "amend": 0,
        # "permission_type": "None",
    }