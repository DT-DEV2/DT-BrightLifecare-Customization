# import frappe

# def before_save(doc, method):
#     if doc.custom_coip_approval == "Approve":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for COI/P Approval",
#             "content": doc.custom_coip_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks
#     elif doc.custom_coip_approval == "Reject":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for COI/P Rejection",
#             "content": doc.custom_coip_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks

#     if doc.custom_br_approval == "Approve":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for BR Approval",
#             "content": doc.custom_br_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks
#     elif doc.custom_br_approval == "Reject":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for BR Rejection",
#             "content": doc.custom_br_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks






# import frappe

# def before_save(doc, method):
#     # Define a mapping of approval fields to their respective remarks and subject base
#     approvals = [
#         ("custom_coip_approval", "custom_coip_remarks", "COI/P"),
#         ("custom_br_approval", "custom_br_remarks", "BR"),
#         ("custom_moa__aoa_approval", "custom_moa__aoa_remarks", "MOA & AOA"),
#         ("custom_authorised_signatory_aadhar_card_approval", "custom_authorised_signatory_aadhar_card_remarks", "Authorised Signatory Aadhar Card"),
#         ("custom_authorised_signatory_pan_approval", "custom_authorised_signatory_pan_remarks", "Authorised Signatory PAN"),
#         ("custom_authorised_dealer_approval", "custom_authorised_dealer_remarks", "Authorised Dealer"),
#         ("custom_fssai_approval", "custom_fssai_remarks", "FSSAI"),
#         ("custom_ayush_approval", "custom_ayush_remarks", "AYUSH"),
#         ("custom_gmp_approval", "custom_gmp_remarks", "GMP"),
#         ("custom_dcl_approval", "custom_dcl_remarks", "Drugs & Cosmetic License"),
#     ]

#     # Get current user's full name
#     comment_by = frappe.db.get_value("User", frappe.session.user, "full_name")

#     # Fetch the old document to compare
#     if doc.get("name"):
#         old_doc = frappe.get_doc(doc.doctype, doc.name)
#     else:
#         old_doc = None

#     for approval_field, remarks_field, label in approvals:
#         approval_value = getattr(doc, approval_field, None)
#         remarks = getattr(doc, remarks_field, "")

#         # Check if the remarks field has changed
#         if old_doc and getattr(old_doc, remarks_field, "") == remarks:
#             continue  # Skip if remarks have not changed

#         if approval_value in ("Approve", "Reject") and remarks:
#             subject = f"Comment for {label} {approval_value}"
#             frappe.get_doc({
#                 "doctype": "Comment",
#                 "comment_type": "Comment",
#                 "reference_doctype": "Supplier",
#                 "reference_name": doc.name,
#                 "subject": subject,
#                 "content": remarks,
#                 "comment_by": comment_by
#             }).insert(ignore_permissions=True)




# import frappe

# def before_save(doc, method):
#     approvals = [
#         ("custom_coip_approval", "custom_coip_remarks", "COI/P"),
#         ("custom_br_approval", "custom_br_remarks", "BR"),
#         ("custom_moa__aoa_approval", "custom_moa__aoa_remarks", "MOA & AOA"),
#         ("custom_authorised_signatory_aadhar_card_approval", "custom_authorised_signatory_aadhar_card_remarks", "Authorised Signatory Aadhar Card"),
#         ("custom_authorised_signatory_pan_approval", "custom_authorised_signatory_pan_remarks", "Authorised Signatory PAN"),
#         ("custom_authorised_dealer_approval", "custom_authorised_dealer_remarks", "Authorised Dealer"),
#         ("custom_fssai_approval", "custom_fssai_remarks", "FSSAI"),
#         ("custom_ayush_approval", "custom_ayush_remarks", "AYUSH"),
#         ("custom_gmp_approval", "custom_gmp_remarks", "GMP"),
#         ("custom_dcl_approval", "custom_dcl_remarks", "Drugs & Cosmetic License"),
#     ]

#     comment_by = frappe.db.get_value("User", frappe.session.user, "full_name")
#     is_new = doc.is_new()

#     old_doc = None
#     if not is_new and frappe.db.exists(doc.doctype, doc.name):
#         old_doc = frappe.get_doc(doc.doctype, doc.name)

#     for approval_field, remarks_field, label in approvals:
#         approval_value = getattr(doc, approval_field, None)
#         remarks = getattr(doc, remarks_field, "")

#         # For updates: skip if remarks haven't changed
#         if old_doc and getattr(old_doc, remarks_field, "") == remarks:
#             continue

#         # For new docs: allow if remarks and approval exist
#         if approval_value in ("Approve", "Reject") and remarks:
#             subject = f"Comment for {label} {approval_value}"
#             content = f"{subject}: {remarks}"

#             frappe.get_doc({
#                 "doctype": "Comment",
#                 "comment_type": "Comment",
#                 "reference_doctype": "Supplier",
#                 "reference_name": doc.name,
#                 "subject": subject,
#                 "content": content,
#                 "comment_by": comment_by
#             }).insert(ignore_permissions=True)



import frappe

def before_save(doc, method):
    if not doc.custom_gmp_certificate_number:
        doc.custom_gmp_certificate_attachment = ""
        doc.custom_gmp_certificate_valid_from = ""
        doc.custom_gmp_certificate_valid_till = ""

    if not doc.custom_fssai_licence_number:
        doc.custom_fssai_licence_attachment = ""
        doc.custom_fssai_licence_valid_from = ""
        doc.custom_fssai_licence_valid_till = ""
        doc.custom_fssai_signed_declaration_attachment = ""
        doc.custom_product_details = ""

    if not doc.custom_relabeller_fssai_licence_number:
        doc.custom_relabeller_fssai_licence_attachment = ""
        doc.custom_relabeller_fssai_license_valid_from = ""
        doc.custom_relabeller_fssai_license_valid_till = ""
        doc.custom_relabeller_fssai_signed_declaration_attachment = ""
        doc.custom_relabeller_product_details = ""

    if not doc.custom_oem_fssai_license_number:
        doc.custom_oem_fssai_license_attachment = ""
        doc.custom_oem_fssai_license_valid_from = ""
        doc.custom_oem_fssai_license_valid_till = ""
        doc.custom_oem_fssai_signed_declaration_attachment = ""
        doc.custom_oem_product_details = ""

    if not doc.custom_distributer_fssai_license_number:
        doc.custom_distributer_fssai_licence_attachment = ""
        doc.custom_distributer_fssai_license_valid_from = ""
        doc.custom_distributer_fssai_license_valid_till = ""
        doc.custom_distributer_fssai_signed_declaration_attachment = ""
        doc.custom_distributer_product_detail = ""

    if not doc.custom_importer_fssai_license_number:
        doc.custom_importer_fssai_license_attachment = ""
        doc.custom_importer_fssai_license_valid_from = ""
        doc.custom_importer_fssai_license_valid_till = ""
        doc.custom_importer_fssai_signed_declaration_attachment = ""
        doc.custom_importer_product_details = ""

    if not doc.custom_trader_fssai_license_number:
        doc.custom_trader_fssai_license_attachment = ""
        doc.custom_trader_fssai_license_valid_from = ""
        doc.custom_trader_fssai_license_valid_till = ""
        doc.custom_trader_fssai_signed_declaration_attachment = ""
        doc.custom_trader_product_details = ""

    if not doc.custom_ayush_license_number:
        doc.custom_ayush_license_attachment = ""
        doc.custom_ayush_license_valid_from = ""
        doc.custom_ayush_license_valid_till = ""
        doc.custom_ayush_signed_declaration_attachment = ""
        doc.custom_ayush_product_approval = ""

    if not doc.custom_drugs__cosmetic_license_number:
        doc.custom_drugs__cosmetic_license_attachment = ""
        doc.custom_drugs__cosmetic_license_valid_from = ""
        doc.custom_drugs__cosmetic_license_valid_till = ""
        doc.custom_dcl_signed_declaration_attachment = ""
        doc.custom_dcl_product_approval = ""


    approvals = [
        ("custom_coip_approval", "custom_coip_remarks", "COI/P"),
        ("custom_br_approval", "custom_br_remarks", "BR"),
        ("custom_moa__aoa_approval", "custom_moa__aoa_remarks", "MOA & AOA"),
        ("custom_authorised_signatory_aadhar_card_approval", "custom_authorised_signatory_aadhar_card_remarks", "Authorised Signatory Aadhar Card"),
        ("custom_authorised_signatory_pan_approval", "custom_authorised_signatory_pan_remarks", "Authorised Signatory PAN"),
        ("custom_authorised_dealer_approval", "custom_authorised_dealer_remarks", "Authorised Dealer"),
        ("custom_fssai_approval", "custom_fssai_remarks", "FSSAI"),
        ("custom_relabeller_fssai_approval", "custom_relabeller_fssai_remarks", "Relabeller"),
        ("custom_oem_fssai_approval", "custom_oem_fssai_remarks", "OEM"),
        ("custom_distributer_fssai_approval", "custom_distributer_fssai_remarks", "Distributer"),
        ("custom_importer_fssai_approval", "custom_importer_fssai_remarks", "Importer"),
        ("custom_trader_fssai_approval", "custom_trader_fssai_remarks", "Trader"),
        ("custom_ayush_approval", "custom_ayush_remarks", "AYUSH"),
        ("custom_gmp_approval", "custom_gmp_remarks", "GMP"),
        ("custom_dcl_approval", "custom_dcl_remarks", "Drugs & Cosmetic License"),
    ]

    # Skip if new document
    if doc.flags.in_insert:
        return

    comment_by = frappe.db.get_value("User", frappe.session.user, "full_name")
    old_doc = frappe.get_doc(doc.doctype, doc.name)

    for approval_field, remarks_field, label in approvals:
        approval_value = getattr(doc, approval_field, None)
        new_remarks = getattr(doc, remarks_field, "") or ""
        old_remarks = getattr(old_doc, remarks_field, "") or ""

        # Only if remarks changed
        if new_remarks != old_remarks:
            if approval_value in ("Approve", "Reject") and new_remarks:
                subject = f"Comment for {label} {approval_value}"
                content = f"{subject}: {new_remarks}"

                frappe.get_doc({
                    "doctype": "Comment",
                    "comment_type": "Comment",
                    "reference_doctype": "Supplier",
                    "reference_name": doc.name,
                    "subject": subject,
                    "content": content,
                    "comment_by": comment_by
                }).insert()
