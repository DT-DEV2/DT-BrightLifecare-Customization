# import frappe


# def before_save(doc, method):
#     if not doc.custom_item_code:
#         return 
    
#     item = frappe.get_doc("Item", doc.custom_item_code)

#     exists = any(qit.quality_inspection_template == doc.name for qit in item.custom_quality_inspection_template_list)
        

#     if not exists:
#         item.append("custom_quality_inspection_template_list", {
#             "quality_inspection_template": doc.name
#         })
#         item.save()





import frappe

def before_save(doc, method):
    if not doc.custom_item_code:
        return

    # Fetch the Item
    item = frappe.get_doc("Item", doc.custom_item_code)
    found = False

    for row in item.custom_quality_inspection_template_list:
        if row.quality_inspection_template == doc.name:
            # Overwrite the link field again (forces UI to refresh is_default etc.)
            row.quality_inspection_template = doc.name
            found = True
            break

    if not found:
        # Not present: append new row
        item.append("custom_quality_inspection_template_list", {
            "quality_inspection_template": doc.name
        })

    item.save()
