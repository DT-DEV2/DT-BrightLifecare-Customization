# File: your_custom_app/public/py/purchase_receipt.py
from pydoc import doc
import frappe
from frappe import _

def validate_supplier_delivery_note(doc, method):
    if doc.supplier_delivery_note and doc.supplier:
        duplicate = frappe.db.exists(
            "Purchase Receipt",
            {
                "supplier_delivery_note": doc.supplier_delivery_note,
                "supplier": doc.supplier,
                "name": ["!=", doc.name]
            }
        )
        if duplicate:
            frappe.throw(_("A Purchase Receipt with Supplier Delivery Note <b>{0}</b> already exists for this supplier.".format(doc.supplier_delivery_note)))


# import frappe
# import time

# def submit_purchase_receipt_with_qi(doc, method=None):
#     """
#     Automatically create Quality Inspection for each item in a Purchase Receipt
#     if it doesn't already exist, fetching batch number from linked Serial and Batch Bundle.
#     """
#     inspected_by = frappe.session.user

#     for item in doc.items:
#         # Check if a QI already exists for this item in the Purchase Receipt
#         existing_qi = frappe.db.exists({
#             "doctype": "Quality Inspection",
#             "reference_type": "Purchase Receipt",
#             "reference_name": doc.name,
#             "item_code": item.item_code
#         })

#         if not existing_qi:
#             time.sleep(10)
#             # Fetch sample_quantity from Item master
#             sample_size = frappe.db.get_value("Item", item.item_code, "sample_quantity") or 0

#             # Initialize batch_no
#         batch_no = None
#         print("\n\n\n",item.serial_and_batch_bundle,"\n\n\n")

#         if item.serial_and_batch_bundle:
#             try:
#                 bundle_doc = frappe.get_doc("Serial and Batch Bundle", item.serial_and_batch_bundle)
#                 if bundle_doc.serial_and_batch_entry:
#                     # Take the batch_no of the first row only
#                     first_entry = bundle_doc.serial_and_batch_entry[0]
#                     batch_no = first_entry.batch_no
#             except Exception as e:
#                     frappe.log_error(f"Error fetching batch for item {item.item_code}: {e}")
#             # Create the Quality Inspection
#         qi = frappe.get_doc({
#                     "doctype": "Quality Inspection",
#                     "inspection_type": "Incoming",
#                     "reference_type": "Purchase Receipt",
#                     "reference_name": doc.name,
#                     "item_code": item.item_code,
#                     "company": doc.company,
#                     "status": "Accepted",
#                     "sample_size": sample_size,
#                     "inspected_by": inspected_by,
#                     "inspection_date": doc.posting_date,
#                     "batch_no": batch_no,
#                     "serial_and_batch_bundle": item.serial_and_batch_bundle
#                 })
#         qi.insert()



import frappe
import time


def on_submit(doc, method):
    submit_purchase_receipt_with_qi(doc, method)
    reserve_on_purchase_receipt(doc, method)
    


def submit_purchase_receipt_with_qi(doc, method=None):
   """
   Wait a few seconds to ensure Serial & Batch Bundle is generated,
   then create QI with batch_no from first entry.
   """
   # Wait 10 seconds
   time.sleep(10)
  

   pr = frappe.get_doc("Purchase Receipt", doc.name)
   inspected_by = frappe.session.user

   for item in pr.items:
       frappe.log_error(f"Processing item {item.item_code}, bundle: {item.serial_and_batch_bundle}", "QI Debug")

       # Check if QI already exists
       if not frappe.db.exists({
           "doctype": "Quality Inspection",
           "reference_type": "Purchase Receipt",
           "reference_name": pr.name,
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

           # Create QI
           qi = frappe.get_doc({
               "doctype": "Quality Inspection",
               "inspection_type": "Incoming",
               "reference_type": "Purchase Receipt",
               "reference_name": pr.name,
               "item_code": item.item_code,
               "company": pr.company,
               "status": "Accepted",
               "sample_size": sample_size,
               "inspected_by": inspected_by,
               "inspection_date": pr.posting_date,
               "batch_no": batch_no,
               "serial_and_batch_bundle": item.serial_and_batch_bundle
           })
           qi.insert()
           frappe.log_error(f"QI created for item {item.item_code} with batch {batch_no}", "QI Debug")




def reserve_on_purchase_receipt(doc, method):

    mrp_settings = frappe.get_single("MRP Settings")
    if mrp_settings.reserve_stock_against_purchase_receipt == 0:
        return

    for item in doc.items:

        if not item.material_request or not item.material_request_item:
            continue

        mr_item = frappe.db.get_value(
            "Material Request Item",
            item.material_request_item,
            [
                "custom_mrp",
                "custom_mrp_raw_material_item"
            ],
            as_dict=True
        )

        if not mr_item:
            continue

        if not mr_item.custom_mrp or not mr_item.custom_mrp_raw_material_item:
            continue

        reserve_qty = item.qty
        if reserve_qty <= 0:
            continue
        
        batch_no = None
        
        if item.batch_no:
            batch_no = item.batch_no
        elif item.serial_and_batch_bundle:
            bundle_doc = frappe.get_doc("Serial and Batch Bundle", item.serial_and_batch_bundle)
            if bundle_doc.entries:
                first_entry = bundle_doc.entries[0]
                batch_no = first_entry.batch_no


        reservation = frappe.new_doc("MRP Reservation Entry")
        reservation.item_code = item.item_code
        reservation.warehouse = item.warehouse
        reservation.voucher_type = "MRP"
        reservation.voucher_no = mr_item.custom_mrp
        reservation.voucher_detail_no = mr_item.custom_mrp_raw_material_item
        reservation.batch_no = batch_no
        
        reservation.from_voucher_type = doc.doctype
        reservation.from_voucher_no = doc.name
        reservation.from_voucher_detail_no = item.name

        reservation.stock_uom = item.stock_uom
        reservation.available_qty_to_reserve = reserve_qty
        reservation.voucher_qty = reserve_qty
        reservation.reserved_qty = reserve_qty
        reservation.issued_qty = 0
        reservation.transferred_qty = 0
        reservation.balance_reserved_qty = reserve_qty
        reservation.company = doc.company
        reservation.status = "Reserved"

        reservation.save()
        reservation.submit()


