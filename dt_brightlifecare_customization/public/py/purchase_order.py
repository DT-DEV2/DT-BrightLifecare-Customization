import frappe

def before_save(doc, method):
    max_qty = 0
    max_item_group = None

    for item in doc.items:
        if item.qty > max_qty:
            max_qty = item.qty
            max_item_group = frappe.db.get_value("Item", item.item_code, "item_group")

    if not doc.custom_item_group:
        doc.custom_item_group = max_item_group
