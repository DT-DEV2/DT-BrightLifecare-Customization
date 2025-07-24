import frappe
from frappe.model.document import Document

def before_save(doc, method):
    supplier_set = set()
    doc.custom_suppliers = []

    for item in doc.items:
        if not item.item_code:
            continue

        item_doc = frappe.get_doc("Item", item.item_code)

        for supp in item_doc.supplier_items:
            if supp.supplier and supp.supplier not in supplier_set:
                supplier_set.add(supp.supplier)
                doc.append("custom_suppliers", {
                    "supplier": supp.supplier
                })







# Code to create RFQ for each supplier against their respective items
import frappe
from frappe.utils import nowdate


@frappe.whitelist()
def create_rfq_from_suppliers(docname):
    doc = frappe.get_doc("Material Request", docname)
    rfq_names = []

    # Find suppliers already used in RFQs for this Material Request
    existing_rfq_suppliers = frappe.get_all(
        "Request for Quotation Item",
        filters={"material_request": docname},
        fields=["parent"]
    )

    existing_suppliers = set()

    for rfq_item in existing_rfq_suppliers:
        suppliers = frappe.get_all(
            "Request for Quotation Supplier",
            filters={"parent": rfq_item.parent},
            fields=["supplier"]
        )
        for s in suppliers:
            existing_suppliers.add(s.supplier)

    supplier_items = {}

    for item in doc.items:
        item_doc = frappe.get_doc("Item", item.item_code)
        for supp in item_doc.supplier_items:
            if supp.supplier in [s.supplier for s in doc.custom_suppliers]:
                if supp.supplier in existing_suppliers:
                    continue  # Skip if already in RFQ for this material request
                supplier_items.setdefault(supp.supplier, []).append({
                    "item_code": item.item_code,
                    "qty": item.qty,
                    "schedule_date": item.schedule_date,
                    "warehouse": item.warehouse,
                    "conversion_factor": item.conversion_factor,
                    "uom": item.uom,
                    "material_request": doc.name,
                    "material_request_item": item.name
                })

    for supplier, items in supplier_items.items():
        rfq = frappe.new_doc("Request for Quotation")
        rfq.transaction_date = nowdate()  # Set today's date
        rfq.append("suppliers", {"supplier": supplier})
        for item in items:
            rfq.append("items", item)

        sup = frappe.get_doc("Supplier", supplier)
        if sup.custom_connected_users:
            for user_entry in sup.custom_connected_users:
                rfq.append("custom_connected_users", {
                    "user": user_entry.user
                    # add other fields if needed (e.g., role, email, etc.)
                })

                
        rfq.message_for_supplier = "Please provide your best quote."
        rfq.save()
        rfq_names.append(rfq.name)

    if not rfq_names:
        frappe.msgprint("RFQs already exist.")
    return rfq_names
