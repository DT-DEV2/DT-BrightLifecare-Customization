import frappe
import time




def on_submit(doc, method):
    make_se_for_code_to_code_transfer(doc, method)
    make_serial_and_barcode_for_fg_item(doc, method)
    
    submit_stock_entry_with_qi(doc, method=None)





import frappe
import time

def submit_stock_entry_with_qi(doc, method=None):
    """
    After Stock Entry submission, wait for Serial & Batch Bundle creation
    then create multiple QIs for finished items based on Item templates.
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

    # Wait to ensure Serial & Batch Bundle is created
    time.sleep(10)

    se = frappe.get_doc("Stock Entry", doc.name)
    inspected_by = frappe.session.user

    for item in se.items:

        # Only finished items
        if not item.is_finished_item:
            continue

        item_doc = frappe.get_doc("Item", item.item_code)

        # Skip if no templates on Item
        if not item_doc.custom_quality_inspection_template_list:
            continue

        frappe.log_error(
            f"Processing item {item.item_code} with templates",
            "QI Debug"
        )

        sample_size = frappe.db.get_value("Item", item.item_code, "sample_quantity") or 0

        # Fetch Batch No from Bundle
        batch_no = None
        if item.serial_and_batch_bundle:
            try:
                bundle = frappe.get_doc(
                    "Serial and Batch Bundle",
                    item.serial_and_batch_bundle
                )
                if bundle.entries:
                    batch_no = bundle.entries[0].batch_no
            except Exception as e:
                frappe.log_error(
                    f"Error fetching batch for {item.item_code}: {e}",
                    "QI Debug"
                )

        # 🔁 CREATE QI FOR EACH TEMPLATE
        for tpl in item_doc.custom_quality_inspection_template_list:

            if getattr(tpl, "is_disabled", 0):
                continue

            # Avoid duplicate QI PER TEMPLATE
            if frappe.db.exists({
                "doctype": "Quality Inspection",
                "reference_type": "Stock Entry",
                "reference_name": se.name,
                "item_code": item.item_code,
                "quality_inspection_template": tpl.quality_inspection_template
            }):
                continue

            qi = frappe.get_doc({
                "doctype": "Quality Inspection",
                "inspection_type": "Incoming",
                "reference_type": "Stock Entry",
                "reference_name": se.name,
                "item_code": item.item_code,
                "company": se.company,
                "status": "Accepted",   # keep in draft
                "sample_size": sample_size,
                "inspected_by": inspected_by,
                "inspection_date": se.posting_date,
                "batch_no": batch_no,
                "serial_and_batch_bundle": item.serial_and_batch_bundle,
                "quality_inspection_template": tpl.quality_inspection_template
            })

            qi.insert()

            frappe.log_error(
                f"QI created for {item.item_code} | Template: {tpl.quality_inspection_template}",
                "QI Debug"
            )







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
