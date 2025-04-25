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


#     if doc.custom_moa__aoa_approval == "Approve":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for MOA & AOA Approval",
#             "content": doc.custom_moa__aoa_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks
#     elif doc.custom_moa__aoa_approval == "Reject":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for MOA & AOA Rejection",
#             "content": doc.custom_moa__aoa_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks
    


#     if doc.custom_authorised_signatory_aadhar_card_approval == "Approve":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for Authorised Signatory Aadhar Card Approval",
#             "content": doc.custom_authorised_signatory_aadhar_card_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks
#     elif doc.custom_authorised_signatory_aadhar_card_approval == "Reject":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for Authorised Signatory Aadhar Card Rejection",
#             "content": doc.custom_authorised_signatory_aadhar_card_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks


#     if doc.custom_authorised_signatory_pan_approval == "Approve":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for Authorised Signatory PAN Approval",
#             "content": doc.custom_authorised_signatory_pan_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks
#     elif doc.custom_authorised_signatory_pan_approval == "Reject":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for Authorised Signatory PAN Rejection",
#             "content": doc.custom_authorised_signatory_pan_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks



#     if doc.custom_authorised_dealer_approval == "Approve":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for Authorised Dealer Approval",
#             "content": doc.custom_authorised_dealer_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks
#     elif doc.custom_authorised_dealer_approval == "Reject":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for Authorised Dealer Rejection",
#             "content": doc.custom_authorised_dealer_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks



#     if doc.custom_fssai_approval == "Approve":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for FSSAI Approval",
#             "content": doc.custom_fssai_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks
#     elif doc.custom_fssai_approval == "Reject":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for FSSAI Rejection",
#             "content": doc.custom_fssai_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks



#     if doc.custom_ayush_approval == "Approve":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for AYUSH Approval",
#             "content": doc.custom_ayush_remarks,  # Set the comment content
#             "comment_by": frappe.db.get_value("User", frappe.session.user, "full_name")  # Set the author of the comment
#         }).insert(ignore_permissions=True)  # Allow insertion without permission checks
#     elif doc.custom_ayush_approval == "Reject":
#         frappe.get_doc({
#             "doctype": "Comment",
#             "comment_type": "Comment",  # Mark as a user comment
#             "reference_doctype": "Supplier",  # Link comment to supplier
#             "reference_name": doc.name,  # Link to the specified supplier
#             "subject": "Comment for AYUSH Rejection",
#             "content": doc.custom_ayush_remarks,  # Set the comment content
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




import frappe

def before_save(doc, method):
    approvals = [
        ("custom_coip_approval", "custom_coip_remarks", "COI/P"),
        ("custom_br_approval", "custom_br_remarks", "BR"),
        ("custom_moa__aoa_approval", "custom_moa__aoa_remarks", "MOA & AOA"),
        ("custom_authorised_signatory_aadhar_card_approval", "custom_authorised_signatory_aadhar_card_remarks", "Authorised Signatory Aadhar Card"),
        ("custom_authorised_signatory_pan_approval", "custom_authorised_signatory_pan_remarks", "Authorised Signatory PAN"),
        ("custom_authorised_dealer_approval", "custom_authorised_dealer_remarks", "Authorised Dealer"),
        ("custom_fssai_approval", "custom_fssai_remarks", "FSSAI"),
        ("custom_ayush_approval", "custom_ayush_remarks", "AYUSH"),
        ("custom_gmp_approval", "custom_gmp_remarks", "GMP"),
        ("custom_dcl_approval", "custom_dcl_remarks", "Drugs & Cosmetic License"),
    ]

    comment_by = frappe.db.get_value("User", frappe.session.user, "full_name")
    is_new = doc.is_new()

    old_doc = None
    if not is_new and frappe.db.exists(doc.doctype, doc.name):
        old_doc = frappe.get_doc(doc.doctype, doc.name)

    for approval_field, remarks_field, label in approvals:
        approval_value = getattr(doc, approval_field, None)
        remarks = getattr(doc, remarks_field, "")

        # For updates: skip if remarks haven't changed
        if old_doc and getattr(old_doc, remarks_field, "") == remarks:
            continue

        # For new docs: allow if remarks and approval exist
        if approval_value in ("Approve", "Reject") and remarks:
            subject = f"Comment for {label} {approval_value}"
            content = f"{subject}: {remarks}"

            frappe.get_doc({
                "doctype": "Comment",
                "comment_type": "Comment",
                "reference_doctype": "Supplier",
                "reference_name": doc.name,
                "subject": subject,
                "content": content,
                "comment_by": comment_by
            }).insert(ignore_permissions=True)
