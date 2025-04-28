import frappe
from frappe import _

@frappe.whitelist()
def update_ownership(doctype, docname, new_owner):
    """
    Update the owner of a specified document.

    :param doctype: The type of the document (e.g., "ToDo")
    :param docname: The name of the document (e.g., "TASK0001")
    :param new_owner: The new owner to be set (e.g., "new_owner@example.com")
    """
    try:
        # Check if the current user has the System Manager role
        if "System Manager" not in frappe.get_roles(frappe.session.user):
            return {"status": "error", "message": _("You do not have permission to update the owner.")}

        # Fetch the document
        doc = frappe.get_doc(doctype, docname)

        # Update the owner field
        doc.db_set("owner", new_owner)

        return {"status": "success", "message": _("Owner updated successfully. New owner: {0}").format(new_owner)}
    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Failed to update owner"))
        return {"status": "error", "message": str(e)}