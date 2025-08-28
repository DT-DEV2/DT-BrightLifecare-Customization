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




