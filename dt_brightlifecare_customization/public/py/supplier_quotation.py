import frappe


def fetch_connected_users(doc, method):
    if doc.supplier:
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




        # doc.save()