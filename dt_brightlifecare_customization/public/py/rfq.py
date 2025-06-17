# import frappe
# from frappe import _

# def validate_supplier_items(doc, method):
#     supplier_list = [row.supplier for row in doc.suppliers]

#     if not supplier_list:
#         frappe.throw(_("Please add at least one supplier."))

#     invalid_items = []

#     for row in doc.items:
#         # Check if the item has any of the selected suppliers in Item Supplier
#         exists = frappe.db.exists(
#             "Item Supplier",
#             {
#                 "parent": row.item_code,
#                 "supplier": ["in", supplier_list]
#             }
#         )
#         if not exists:
#             invalid_items.append(row.item_code)

#     if invalid_items:
#         frappe.throw(
#             _("The following items do not have any of the selected suppliers in the Item master: {0}")
#             .format(", ".join(invalid_items))
#         )


import frappe

def before_save(doc, method):
    # Get currently shared users for this Address
    shared_users = frappe.share.get_users(doc.doctype, doc.name)

    for sup in doc.suppliers:
        if sup.supplier:
            supplier = sup.supplier

            # Fetch connected users from the custom child table
            connected_users = frappe.get_all("Connected Users",  # Use actual Child Table name
                                             filters={"parent": supplier, "parenttype": "Supplier"},
                                             fields=["user"])

            for user_entry in connected_users:
                user = user_entry.get("user")
                
                # Only share with users who are not already shared
                if user and user not in shared_users:
                    frappe.share.add(doc.doctype, doc.name, user, read=1, write=0, share=1)
