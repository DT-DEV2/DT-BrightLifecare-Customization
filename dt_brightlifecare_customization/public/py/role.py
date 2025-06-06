import frappe

def create_role_config(doc, method):
    if not frappe.db.exists("Role Configuration", {"role": doc.name}):
        frappe.get_doc({
            "doctype": "Role Configuration",
            "role": doc.name,
            "supplier_visibility": 0
        }).insert(ignore_permissions=True)
