# Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SupplierItemLink(Document):
	pass


import frappe

def on_submit(doc, method):
    if not doc.item or not doc.supplier:
        return

    item_doc = frappe.get_doc("Item", doc.item)

    # Check if supplier already exists in the supplier_items child table
    existing_suppliers = [d.supplier for d in item_doc.supplier_items]

    if doc.supplier not in existing_suppliers:
        item_doc.append("supplier_items", {
            "supplier": doc.supplier,
            "supplier_part_no" : doc.supplier_part_number
        })
        item_doc.save()
        frappe.msgprint(f"Supplier '{doc.supplier}' added to Item '{doc.item}'.")
