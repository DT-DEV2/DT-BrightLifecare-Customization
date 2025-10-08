import frappe
from frappe.utils import nowdate

def on_submit(doc, method):
    """
    Automatically create a BMR in Draft when Work Order is submitted,
    only if the item has custom_enable_bmr checked, and fetch formula sheet from BOM items.
    """

    # Get item details
    item = frappe.get_doc("Item", doc.production_item)

    if not item.get("custom_enable_bmr"):
        return  # BMR creation not enabled for this item

    # Fetch the latest batch linked to this Work Order
    batch = frappe.db.get_value(
        "Batch",
        {"reference_name": doc.name},
        ["name", "batch_qty", "stock_uom", "manufacturing_date", "expiry_date"],
        order_by="creation desc",
        as_dict=True
    )

    if not batch:
        frappe.throw(f"No Batch found for Work Order: {doc.name}")

    # Create BMR document
    bmr = frappe.new_doc("BMR-Batch Manufacturing Report")

    # ---- Work Order fields ----
    bmr.product_code = doc.production_item
    bmr.product_name = doc.item_name
    bmr.reference_name = doc.name

    # ---- Batch fields ----
    bmr.batch_no_letter_head = batch.name
    bmr.batch_quantity = batch.batch_qty
    bmr.batch_uom = batch.stock_uom
    bmr.mfg_date = batch.manufacturing_date
    bmr.exp_date = batch.expiry_date

    # ---- Item Master fields ----
    bmr.shelf_life_letter_head = item.shelf_life_in_days
    bmr.shelf_life = item.shelf_life_in_days
    bmr.product_code_no = doc.production_item
    bmr.fssai_mfg_license_no = item.custom_fssai
    bmr.storage_conditions = item.custom_storage_condition

    # ---- System / User fields ----
    bmr.document_issued_by = frappe.session.user
    bmr.date = doc.modified
    bmr.document_received_by = frappe.session.user
    bmr.receiving_date = nowdate()

    # ---- Fetch BOM items and populate formula_sheet ----
    if doc.bom_no:
        bom_doc = frappe.get_doc("BOM", doc.bom_no)
        for bom_item in bom_doc.items:
            bmr.append("formula_sheet", {
                "material_code": bom_item.item_code,
                "uom": bom_item.stock_uom,
                "act_req_qty_as_per_batch": bom_item.get("custom_formulation_quantity") or 0,
                "overage": bom_item.get("custom_overage_") or 0,
                "material_req_as_per_batch": bom_item.get("stock_qty") or 0
            })

    # Save as Draft
    bmr.insert()
    frappe.msgprint(f"BMR created in Draft: <b>{bmr.name}</b>")
