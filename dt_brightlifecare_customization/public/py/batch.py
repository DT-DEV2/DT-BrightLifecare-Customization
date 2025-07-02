# import frappe

# def set_expiry_date(doc, method):
#     if doc.reference_doctype != "Purchase Receipt" or not doc.reference_name:
#         return

#     pr = frappe.get_doc("Purchase Receipt", doc.reference_name)

#     for item in pr.items:
#         if item.item_code == doc.item:
#             # print("\n\n\n", item.item_code, doc.item ,"\n\n\n")
#             if item.item_group:
#                 is_expiry_needed = frappe.db.get_value("Item Group", item.item_group, "custom_batch_expiry_date")
#                 if is_expiry_needed and item.custom_expiry_date:
#                     doc.expiry_date = item.custom_expiry_date
#                     doc.save()
#                 else:
#                     continue
#             # break







import frappe
from frappe.utils import add_days


def set_expiry_date(doc, method):
    if doc.reference_doctype != "Purchase Receipt" or not doc.reference_name:
        return

    pr = frappe.get_doc("Purchase Receipt", doc.reference_name)

    doc.supplier = pr.supplier



    for item in pr.items:
        if item.item_code != doc.item:
            continue

        if not item.item_group:
            continue

        is_expiry_needed = frappe.db.get_value(
            "Item Group",
            item.item_group,
            "custom_batch_expiry_date"
        )

        # Only set if needed and item has custom date
        if is_expiry_needed and item.custom_expiry_date:
            doc.expiry_date = item.custom_expiry_date
            doc.save()

        retest = frappe.db.get_value("Item", doc.item, "custom_retest")

        schedule_date = add_days(pr.posting_date, retest)

        doc.append("custom_quality_check_schedule",{
            "schedule_date" : schedule_date,
            "actual_date" : pr.posting_date,
            "expiry_date" : item.custom_expiry_date,
            "ar_number" : item.quality_inspection
        })


           

    doc.save()
        
        # If expiry is needed but no custom_expiry_date, do nothing
        # The default value already set on the Batch will stay.
        # break
