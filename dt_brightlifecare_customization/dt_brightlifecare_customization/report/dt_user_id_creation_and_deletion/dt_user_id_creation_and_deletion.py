import frappe

def execute(filters=None):
    columns = get_columns()
    data = []

    # 1. User Creation
    users = frappe.get_all(
        "User",
        fields=["name", "first_name", "last_name", "creation", "owner"]
    )

    for user in users:
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        data.append([
            user.name,
            full_name,
            "Created",
            user.creation,
            user.owner or ""
        ])

    # 2. User Deletion
    deleted_users = frappe.get_all(
        "Deleted Document",
        filters={"deleted_doctype": "User"},
        fields=["deleted_name", "creation", "owner"]
    )

    for deleted in deleted_users:
        full_name = ""
        if frappe.db.exists("User", deleted.deleted_name):
            user_doc = frappe.get_doc("User", deleted.deleted_name)
            full_name = f"{user_doc.first_name or ''} {user_doc.last_name or ''}".strip()

        data.append([
            deleted.deleted_name,
            full_name,
            "Deleted",
            deleted.creation,
            deleted.owner or ""
        ])

    return columns, data


def get_columns():
    return [
        {"label": "User ID", "fieldname": "user_id", "fieldtype": "Data", "width": 220},
        {"label": "User Name", "fieldname": "user_name", "fieldtype": "Data", "width": 220},
        {"label": "Action", "fieldname": "action", "fieldtype": "Data", "width": 100},
        {"label": "Timestamp", "fieldname": "timestamp", "fieldtype": "Datetime", "width": 200},
        {"label": "Performed By", "fieldname": "performed_by", "fieldtype": "Link", "options": "User", "width": 200}
    ]
