import frappe
import time

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
            qi.insert(ignore_permissions=True)
            frappe.log_error(f"QI created for item {item.item_code} with batch {batch_no}", "QI Debug")
