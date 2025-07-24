import frappe

def before_save(doc, method):
    max_amt = 0
    max_item_group = None

    sup = frappe.get_doc("Supplier", doc.supplier)

    if sup.custom_connected_users:
        # Extract existing user IDs from the current doc's child table
        existing_users = {row.user for row in doc.custom_connected_users}

        for user_entry in sup.custom_connected_users:
            if user_entry.user not in existing_users:
                doc.append("custom_connected_users", {
                    "user": user_entry.user
                    # add other fields if needed
                })

    for item in doc.items:
        if item.amount > max_amt:
            max_amt = item.amount
            max_item_group = frappe.db.get_value("Item", item.item_code, "item_group")

    if not doc.custom_item_group:
        doc.custom_item_group = max_item_group
