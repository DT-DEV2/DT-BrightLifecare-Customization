import frappe

@frappe.whitelist()
def get_connected_users(doctype, txt, searchfield, start, page_len, filters):
    if not filters or filters.get("party_type") != "Supplier" or not filters.get("party_name"):
        return []

    supplier = frappe.get_doc("Supplier", filters.get("party_name"))
    connected_users = [
        row.user for row in supplier.get("custom_connected_users") if row.user
    ]

    filtered_users = [
        (user,) for user in connected_users if txt.lower() in user.lower()
    ] if txt else [(user,) for user in connected_users]

    return filtered_users




def before_save(doc, method):
    # Get currently shared users for this Address
    shared_users = frappe.share.get_users(doc.doctype, doc.name)

 
    if doc.party_type == "Supplier":
        supplier = doc.party_name

            
        # Only share with users who are not already shared
        if doc.party_user and doc.party_user not in shared_users:
            frappe.share.add(doc.doctype, doc.name, doc.party_user, read=1, write=0, share=1)



def on_submit(doc, method):
    if doc.party_type == "Supplier":
        supplier = frappe.get_doc("Supplier", doc.party_name)

        supplier.custom_contract_id = doc.name
        supplier.custom_contract_supplier_approver = doc.custom_supplier_approver
        supplier.custom_contract_hk_approver = doc.custom_healthkart_approver
        supplier.custom_nda_supplier_approver = doc.custom_nda_sign_by_supplier_approver
        supplier.custom_nda_hk_approver = doc.custom_nda_sign_by_healthkart_approver
        supplier.save()


def on_cancel(doc, method):
    if doc.party_type == "Supplier":
        # Find suppliers with matching contract id
        suppliers = frappe.get_all(
            "Supplier",
            filters={"custom_contract_id": doc.name},
            pluck="name"
        )
        for supplier_name in suppliers:
            supplier = frappe.get_doc("Supplier", supplier_name)
            supplier.custom_contract_id = ""
            supplier.custom_contract_supplier_approver = ""
            supplier.custom_contract_hk_approver = ""
            supplier.custom_nda_supplier_approver = ""
            supplier.custom_nda_hk_approver = ""
            supplier.save()



