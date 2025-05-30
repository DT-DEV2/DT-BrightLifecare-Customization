import frappe

@frappe.whitelist()
def get_connected_users(doctype, txt, searchfield, start, page_len, filters):
    if not filters or filters.get("party_type") != "Supplier" or not filters.get("party_name"):
        return []

    supplier = frappe.get_doc("Supplier", filters.get("party_name"))
    connected_users = [
        row.user for row in supplier.get("custom_connected_users") if row.user
    ]

    filtered_users = [
        (user,) for user in connected_users if txt.lower() in user.lower()
    ] if txt else [(user,) for user in connected_users]

    return filtered_users
