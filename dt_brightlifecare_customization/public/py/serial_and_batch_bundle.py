import frappe

def set_expiry_date(doc, method):
    if doc.voucher_type == "Purchase Receipt":
        pr = frappe.get_doc("Purchase Receipt", doc.voucher_no)

        for item in pr.items:
            if item.item_code == doc.item_code:
                is_expiry_needed = frappe.db.get_value("Item Group", item.item_group, "custom_batch_expiry_date")
                if is_expiry_needed:
                    for entry in doc.entries:
                        entry.custom_batch_expiry_date = item.custom_expiry_date
                    # doc.save()
                    # break