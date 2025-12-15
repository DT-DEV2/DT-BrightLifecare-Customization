import frappe
import time




def on_submit(doc, method):
    make_se_for_code_to_code_transfer(doc, method)
    make_serial_and_barcode_for_fg_item(doc, method)
    
    submit_stock_entry_with_qi(doc, method=None)
    issued_qty_calculation_in_wo(doc, method)
    returned_qty_calculation_in_wo(doc, method)
    consumed_qty_calculation_in_wo(doc, method)





def submit_stock_entry_with_qi(doc, method=None):
    """
    After Stock Entry submission, wait for Serial & Batch Bundle creation
    then create QI for finished items if BOM requires quality inspection.
    """
    # Only for Manufacture entries
    if doc.stock_entry_type != "Manufacture":
        return

    # Ensure BOM is linked
    if not doc.bom_no:
        return

    # Check custom checkbox on BOM
    bom_flag = frappe.db.get_value("BOM", doc.bom_no, "custom_quality_inspection")
    if not bom_flag:
        return

    # Wait 10 seconds (to ensure bundles created)
    time.sleep(10)

    se = frappe.get_doc("Stock Entry", doc.name)
    inspected_by = frappe.session.user

    for item in se.items:
        # Only finished items
        if not item.is_finished_item:
            continue

        frappe.log_error(f"Processing finished item {item.item_code}, bundle: {item.serial_and_batch_bundle}", "QI Debug")

        # Avoid duplicate QI
        if not frappe.db.exists({
            "doctype": "Quality Inspection",
            "reference_type": "Stock Entry",
            "reference_name": se.name,
            "item_code": item.item_code
        }):
            sample_size = frappe.db.get_value("Item", item.item_code, "sample_quantity") or 0

            batch_no = None
            if item.serial_and_batch_bundle:
                try:
                    bundle = frappe.get_doc("Serial and Batch Bundle", item.serial_and_batch_bundle)
                    if bundle.entries:
                        batch_no = bundle.entries[0].batch_no
                except Exception as e:
                    frappe.log_error(f"Error fetching batch for item {item.item_code}: {e}", "QI Debug")

            # Create QI in Draft
            qi = frappe.get_doc({
                "doctype": "Quality Inspection",
                "inspection_type": "Incoming",
                "reference_type": "Stock Entry",
                "reference_name": se.name,
                "item_code": item.item_code,
                "company": se.company,
                "status": "Accepted",   # keep in draft state
                "sample_size": sample_size,
                "inspected_by": inspected_by,
                "inspection_date": se.posting_date,
                "batch_no": batch_no,
                "serial_and_batch_bundle": item.serial_and_batch_bundle
            })
            qi.insert()
            frappe.log_error(f"QI created for item {item.item_code} with batch {batch_no}", "QI Debug")







def make_serial_and_barcode_for_fg_item(doc, method):
    """
    When a Manufacture Stock Entry is submitted:
    - Check if linked to Work Order
    - Identify finished good item (t_warehouse present)
    - If item requires serial numbers, create Serial Number and Barcode doc
    - Populate child table with all serial numbers generated
    """
    if doc.stock_entry_type != "Manufacture" or not doc.work_order:
        return

    for item in doc.items:
        if not item.t_warehouse:
            continue

        has_serial_no = frappe.get_value("Item", item.item_code, "has_serial_no")
        if not has_serial_no:
            continue

        # Fetch all serial numbers linked to this Stock Entry and item
        serial_nos = frappe.get_all(
            "Serial No",
            filters={"item_code": item.item_code, "work_order": doc.work_order},
            pluck="name"
        )

        if not serial_nos:
            continue

        # Create parent document
        snb = frappe.get_doc({
            "doctype": "Serial Number and Barcode",
            "item_code": item.item_code,
            "work_order": doc.work_order,
            "stock_entry": doc.name
        })

        # Add child rows for each serial number
        for sn in serial_nos:
            snb.append("serial_no_and_barcode_detail", {
                "serial_number": sn
            })

        snb.insert()
        # frappe.db.commit()







# import frappe

# def on_cancel(doc, method):
#     """
#     When a Stock Entry is cancelled, remove Serial Number and Barcode docs
#     linked to its Work Order and finished good items.
#     """
#     if doc.stock_entry_type != "Manufacture" or not doc.work_order:
#         return

#     for item in doc.items:
#         if not item.t_warehouse:
#             continue

#         has_serial_no = frappe.get_value("Item", item.item_code, "has_serial_no")
#         if not has_serial_no:
#             continue

#         # Find all Serial Number and Barcode docs created for this WO + Item
#         snb_list = frappe.get_all(
#             "Serial Number and Barcode",
#             filters={"item_code": item.item_code, "work_order": doc.work_order, "stock_entry": doc.name},
#             pluck="name"
#         )

#         for snb in snb_list:
#             frappe.delete_doc("Serial Number and Barcode", snb)

    # frappe.db.commit()














def make_se_for_code_to_code_transfer(doc, method):
    if doc.stock_entry_type != "Manufacture":
        return

    for item in doc.items:
        # Check if code-to-code transfer is enabled for this item
        ctc = frappe.db.get_value("Item", item.item_code, "custom_code_to_code_transfer")
        ctc_item = frappe.db.get_value("Item", item.item_code, "custom_code_to_code_transfer_item")

        if ctc and ctc_item:
            try:
                CtC_SE = frappe.get_doc({
                    "doctype": "Stock Entry",
                    "stock_entry_type": "Code To Code Transfer",
                    "company": doc.company,
                    "posting_date": doc.posting_date,
                    "posting_time": doc.posting_time,
                    "set_posting_time": 1
                })

                # Outgoing (from t_warehouse of manufacture entry)
                CtC_SE.append("items", {
                    "s_warehouse": item.t_warehouse,
                    "item_code": item.item_code,
                    "qty": item.qty
                })

                # Incoming (into t_warehouse of manufacture entry)
                CtC_SE.append("items", {
                    "t_warehouse": item.t_warehouse,
                    "item_code": ctc_item,
                    "qty": item.qty
                })

                # Save and submit
                CtC_SE.insert()
                CtC_SE.submit()

                frappe.msgprint(f"Code to Code Transfer created: {CtC_SE.name}")

            except Exception as e:
                frappe.log_error(frappe.get_traceback(), "Error in make_se_for_code_to_code_transfer")
                frappe.msgprint(f"Error while creating Code to Code Transfer: {str(e)}")


import frappe

@frappe.whitelist()
def print_dispensing_slips_preview(docname):
   doc = frappe.get_doc("Stock Entry", docname)

   # Just get HTML of your custom print format
   html = frappe.get_print(
       doctype="Stock Entry",
       name=doc.name,
       print_format="DT Dispensing Slips for RM",
       doc=doc,
       as_pdf=False
   )

   return html








def before_save(doc, method):
    for item in doc.items:
        if item.ste_detail:
            se_doc = frappe.get_doc("Stock Entry Detail", item.ste_detail)

            if se_doc.qty and item.qty > se_doc.qty:
                frappe.throw("Quanity must be less than or equals to linked Stock Entry quanity")





# @frappe.whitelist()
# def remove_unwanted_rows(row_name):
#     source = frappe.get_doc("Stock Entry Detail", row_name)
#     source.delete()







import frappe

def issued_qty_calculation_in_wo(doc, method):
    if doc.stock_entry_type != "Transfer to Manufacturing Machine Setup":
        return

    if not doc.work_order:
        return

    # Fetch submitted Work Order
    wo = frappe.get_doc("Work Order", doc.work_order)

    if wo.docstatus != 1:
        return  # Safety check

    for se_item in doc.items:
        if not se_item.item_code or not se_item.qty:
            continue

        wo.append("custom_machine_setup_inventory_detail", {
            "item_code": se_item.item_code,
            "issued_qty": se_item.qty
        })

    # Save submitted document safely
    wo.save()







def returned_qty_calculation_in_wo(doc, method):
    if doc.stock_entry_type != "Machine Setup Return":
        return

    if not doc.work_order:
        return

    # Fetch submitted Work Order
    wo = frappe.get_doc("Work Order", doc.work_order)

    if wo.docstatus != 1:
        return

    # Build item_code → row map for quick lookup
    wo_items_map = {
        d.item_code: d
        for d in wo.custom_machine_setup_inventory_detail
        if d.item_code
    }

    for se_item in doc.items:
        if not se_item.item_code or not se_item.qty:
            continue

        if se_item.item_code in wo_items_map:
            # 🔁 Item exists → add qty
            row = wo_items_map[se_item.item_code]
            row.returned_qty = (row.returned_qty or 0) + se_item.qty
        else:
            # ➕ Item not present → add new row
            wo.append("custom_machine_setup_inventory_detail", {
                "item_code": se_item.item_code,
                "returned_qty": se_item.qty
            })

    # Save submitted document safely
    wo.save()








def consumed_qty_calculation_in_wo(doc, method):
    if doc.stock_entry_type != "Machine Setup Consumption Entry":
        return

    if not doc.work_order:
        return

    # Fetch submitted Work Order
    wo = frappe.get_doc("Work Order", doc.work_order)

    if wo.docstatus != 1:
        return

    # Build item_code → row map for quick lookup
    wo_items_map = {
        d.item_code: d
        for d in wo.custom_machine_setup_inventory_detail
        if d.item_code
    }

    print("\n\n\n",wo_items_map,"\n\n\n")

    for se_item in doc.items:
        if not se_item.item_code or not se_item.qty:
            continue

        if se_item.item_code in wo_items_map:
            # 🔁 Item exists → add qty
            row = wo_items_map[se_item.item_code]
            row.consumed_qty = (row.consumed_qty or 0) + se_item.qty
            print("\n\n\n",se_item.item_code, row.consumed_qty,"\n\n\n")
        else:
            # ➕ Item not present → add new row
            wo.append("custom_machine_setup_inventory_detail", {
                "item_code": se_item.item_code,
                "consumed_qty": se_item.qty
            })

    # Save submitted document safely
    wo.save()