import frappe
from frappe.utils import nowdate



def submit(doc, method):
   on_submit(doc, method)
   bpr_on_wo_submittion(doc, method)



def on_submit(doc, method):
    """
    Automatically create a BMR in Draft when Work Order is submitted,
    only if the item has custom_enable_bmr checked, and fetch formula sheet from BOM items.
    """

    # Get item details
    item = frappe.get_doc("Item", doc.production_item)
    warehouse = frappe.get_doc("Warehouse", doc.fg_warehouse)

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
    bom_doc = frappe.get_doc("BOM", doc.bom_no)
    # ---- Work Order fields ----
    bmr.product_code = doc.production_item
    bmr.product_name = doc.item_name
    bmr.reference_name = doc.name

    # ---- Batch fields ----
    bmr.batch_no_letter_head = batch.name
    bmr.batch_uom = batch.stock_uom
    bmr.mfg_date = batch.manufacturing_date
    bmr.exp_date = batch.expiry_date

    # ---- BOM fields ----
    bmr.bom_quantity = bom_doc.quantity
    bmr.theoretical_yield = bom_doc.custom_theoretical_yield_
    bmr.theoretical_yield_batch = bom_doc.custom_theoretical_yield_

    # ---- Warehouse fields ----
    bmr.fssai_mfg_license_no = warehouse.custom_manufcaturing_fssai_license

    # ---- Item Master fields ----
    bmr.shelf_life_letter_head = item.shelf_life_in_days
    bmr.shelf_life = item.shelf_life_in_days
    bmr.product_code_no = doc.production_item
    bmr.storage_conditions = item.custom_storage_condition
    bmr.manufactured_for = doc.company

    # ---- System / User fields ----
    bmr.document_issued_by = frappe.session.user
    bmr.date = doc.modified
    

    # ---- Fetch BOM items and populate formula_sheet ----
    if doc.bom_no:
        bom_doc = frappe.get_doc("BOM", doc.bom_no)
        for bom_item in bom_doc.items:
            bmr.append("formula_sheet", {
                "material_code": bom_item.item_code,
                "ingredients": bom_item.item_name,
                "uom": bom_item.stock_uom,
                "act_req_qty_as_per_batch": bom_item.get("custom_formulation_quantity") or 0,
                "overage": bom_item.get("custom_overage_") or 0,
                "material_req_as_per_batch": bom_item.get("stock_qty") or 0
            })
    # ---- Fetch BOM items and populate sieve_integrity ----
    if doc.bom_no:
        bom_doc = frappe.get_doc("BOM", doc.bom_no)
        for bom_operations in bom_doc.operations:
            bmr.append("sieve_integrity", {
                "seive_size": bom_operations.operation,
            })
    # Save as Draft
    bmr.insert()
    frappe.msgprint(f"BMR created in Draft: <b>{bmr.name}</b>")







def bpr_on_wo_submittion(doc, method):
   bpr_checkbox = frappe.db.get_value("Item", doc.production_item, "custom_enable_bpr")

   if bpr_checkbox:
       
        batch = frappe.db.get_value(
            "Batch",
            {"item": doc.production_item, "reference_name": doc.name},
            ["name", "batch_qty", "stock_uom", "manufacturing_date", "expiry_date"],
            as_dict=True
        )

        item = frappe.db.get_value(
            "Item",
            {"name": doc.production_item},
            ["name", "shelf_life_in_days", "custom_storage_condition"],
            as_dict=True
        )

        bom = frappe.get_doc("BOM", doc.bom_no)
        
        bpr = frappe.new_doc("Batch Packaging Record - BPR")
        
        bpr.product_code = doc.production_item
        bpr.batch_no_1 = batch.name
        bpr.batch_size = doc.qty
        bpr.shelf_life_1 = item.shelf_life_in_days
        bpr.revision_no = doc.bom_no
        bpr.work_order = doc.name

        bpr.batch_packing_quantity = batch.batch_qty
        bpr.theoretical_yield = bom.custom_theoretical_yield_
        bpr.mfg_date = batch.manufacturing_date
        bpr.expiry_date = batch.expiry_date
        bpr.product_code_no = doc.production_item
        bpr.shelf_life = item.shelf_life_in_days
        bpr.storage_condition = item.custom_storage_condition
        bpr.manufactured_for = doc.company


        if doc.bom_no:
            bom_doc = frappe.get_doc("BOM", doc.bom_no)
            for bom_item in bom_doc.items:
                bpr.append("master_packing_sheet_detail", {
                    "material_code": bom_item.item_code,
                    "ingredients": bom_item.item_name,
                    "uom": bom_item.stock_uom,
                    "actual_required_qty_as_per_batch": bom_item.get("custom_formulation_quantity") or 0,
                    # "std_qty_per_batch": bom_item.get(),
                    "overage": bom_item.get("custom_overage_") or 0,
                    "actual_batch_size_qty": bom_item.get("stock_qty") or 0
                })


            bom_names = frappe.get_all(
                "BOM",
                filters={"item": doc.production_item},
                fields=["name", "creation"],
                order_by="creation desc"
            )

            for bm in bom_names:
                bpr.append("revision_history_detail", {
                    "revision_no": bm.name,
                    "date": bm.creation
                })



            
        

        bpr.insert()
        frappe.msgprint(f"BPR created in Draft: <b>{bpr.name}</b>")
