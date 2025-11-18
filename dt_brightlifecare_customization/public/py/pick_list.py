import frappe

def execute(doc, method):
    # Only run if Pick List created from Work Order
    if not doc.work_order:
        return

    # Fetch the Work Order document
    wo = frappe.get_doc("Work Order", doc.work_order)
    # print("\n\n\n",wo,"\n\n\n")

    # Create a lookup dictionary: item_code → source_warehouse from Work Order
    wo_items = {
        row.item_code: row.source_warehouse
        for row in wo.required_items
    }
    # print("\n\n\n",wo_items,"\n\n\n")

    # Update Pick List rows with warehouse from Work Order
    for row in doc.locations:
        if row.item_code in wo_items:
            # print("\n\n\n",wo_items[row.item_code],"\n\n\n")
            row.warehouse = wo_items[row.item_code] or row.from_warehouse

    
