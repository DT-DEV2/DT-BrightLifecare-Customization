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
