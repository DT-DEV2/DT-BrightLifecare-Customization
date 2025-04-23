# File: your_custom_app/public/py/purchase_receipt.py

import frappe
from frappe import _

def validate_supplier_delivery_note(doc, method):
    if doc.supplier_delivery_note and doc.supplier:
        duplicate = frappe.db.exists(
            "Purchase Receipt",
            {
                "supplier_delivery_note": doc.supplier_delivery_note,
                "supplier": doc.supplier,
                "name": ["!=", doc.name]
            }
        )
        if duplicate:
            frappe.throw(_("A Purchase Receipt with Supplier Delivery Note <b>{0}</b> already exists for this supplier.".format(doc.supplier_delivery_note)))
