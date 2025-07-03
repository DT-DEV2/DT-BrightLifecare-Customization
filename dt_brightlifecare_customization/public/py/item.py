# import frappe

# @frappe.whitelist()
# def generate_item_code(listing_id):
#     # Find all items starting with this listing_id
#     items = frappe.get_all('Item',
#         filters={'item_code': ['like', f'{listing_id}%']},
#         fields=['item_code'],
#         order_by='item_code'
#     )
    
#     if not items:
#         return listing_id  # first item gets plain listing_id
    
#     # Find the highest existing number
#     max_num = 0
#     for item in items:
#         if item.item_code == listing_id:
#             max_num = max(max_num, 1)
#         elif item.item_code.startswith(listing_id + '-'):
#             try:
#                 num = int(item.item_code.split('-')[-1])
#                 max_num = max(max_num, num)
#             except ValueError:
#                 pass
    
#     # Generate next number with 3-digit padding
#     next_num = max_num + 1
#     return f"{listing_id}-{str(next_num).zfill(3)}"





# import frappe

# def item_autoname(doc, method):
#     if doc.custom_listing_id:
#         base = doc.custom_listing_id

#         # Get count of existing items with similar base
#         existing_items = frappe.db.get_all(
#             "Item",
#             filters={"name": ["like", f"{base}-%"]},
#             fields=["name"]
#         )
#         count = len(existing_items) + 1

#         doc.item_code = f"{base}-{count:03d}"

#         doc.name = f"{base}-{count:03d}"



import frappe

@frappe.whitelist()
def get_next_item_code_for_listing(listing_id):
    if not listing_id:
        return ""

    base = listing_id.strip()

    # Get all existing Item codes starting with base
    existing_codes = frappe.db.get_all(
        "Item",
        filters={"item_code": ["like", f"{base}%"]},
        pluck="item_code"
    )

    max_suffix = -1
    for code in existing_codes:
        if code == base:
            max_suffix = max(max_suffix, 0)
        elif code.startswith(base + "-"):
            try:
                suffix = int(code.split("-")[-1])
                max_suffix = max(max_suffix, suffix)
            except ValueError:
                continue

    # Decide new item_code
    if max_suffix == -1:
        return base
    else:
        return f"{base}-{(max_suffix + 1):03d}"
