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









def before_save(doc, method):
    if getattr(doc, "_disable_hook", False):
        return

    if doc.custom_listing_id:
        filters = {"custom_listing_id": doc.custom_listing_id}
        item_codes = frappe.db.get_all("Item", filters=filters, pluck="name")

        for item_code in item_codes:
            item_doc = frappe.get_doc("Item", item_code)
            
            # Prevent recursion in inner saves
            item_doc._disable_hook = True
            item_doc.disabled = 1
            item_doc.save()
