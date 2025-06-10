import frappe

def before_save(doc, method):
    # Get currently shared users for this Address
    shared_users = frappe.share.get_users(doc.doctype, doc.name)

    for link in doc.links:
        if link.link_doctype == "Supplier":
            supplier = link.link_name

            # Fetch connected users from the custom child table
            connected_users = frappe.get_all("Connected Users",  # Use actual Child Table name
                                             filters={"parent": supplier, "parenttype": "Supplier"},
                                             fields=["user"])

            for user_entry in connected_users:
                user = user_entry.get("user")
                
                # Only share with users who are not already shared
                if user and user not in shared_users:
                    frappe.share.add(doc.doctype, doc.name, user, read=1, write=0, share=1)
