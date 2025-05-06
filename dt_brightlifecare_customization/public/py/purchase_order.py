import frappe

def before_save(doc, method):
    max_amt = 0
    max_item_group = None

    for item in doc.items:
        if item.amount > max_amt:
            max_amt = item.amount
            max_item_group = frappe.db.get_value("Item", item.item_code, "item_group")

    if not doc.custom_item_group:
        doc.custom_item_group = max_item_group
