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




def before_save(doc, method):
    # Get currently shared users for this Address
    shared_users = frappe.share.get_users(doc.doctype, doc.name)

 
    if doc.party_type == "Supplier":
        supplier = doc.party_name

            
        # Only share with users who are not already shared
        if doc.party_user and doc.party_user not in shared_users:
            frappe.share.add(doc.doctype, doc.name, doc.party_user, read=1, write=0, share=1)
