import frappe
from frappe import _

def before_save(doc, method):
    if doc.items:
        for item in doc.items:
            if item.bom_no:
                s_warehouse = frappe.db.get_value("BOM", item.bom_no, "custom_source_warehouse")
                if doc.custom_source_warehouse != s_warehouse:
                    frappe.throw("Source Warehouse should be the same as that of BOM No. in Items table")



def validate(doc, method):
    # Skip if updating existing BOM
    # if frappe.db.exists("BOM", doc.name):
    #     return

    # Step 1: Get item group
    item_grp = frappe.db.get_value("Item", doc.item, "item_group")
    if item_grp != "Semi-Finished Goods":
        return

    # Step 2: Get BOMs with same item and qty
    bom_list = frappe.get_all(
        "BOM",
        filters={"item": doc.item, "quantity": doc.quantity, "is_active": 1},
        fields=["name"]
    )

    # Remove itself from the list if updating
    bom_list = [b for b in bom_list if b.name != doc.name]

    # Step 3: Prepare new BOM items for comparison
    new_items = sorted(
        [{"item_code": d.item_code, "qty": d.qty} for d in doc.items],
        key=lambda x: x["item_code"]
    )

    for bom in bom_list:
        existing_doc = frappe.get_doc("BOM", bom.name)
        existing_items = sorted(
            [{"item_code": d.item_code, "qty": d.qty} for d in existing_doc.items],
            key=lambda x: x["item_code"]
        )

        if new_items == existing_items:
            frappe.throw(
                f"BOM {bom.name} already exists with the same item, quantity, and components."
            )

