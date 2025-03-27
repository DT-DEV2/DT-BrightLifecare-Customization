
import frappe

def create_user_if_not_exists(self, method):
    """Creates a User if the Contact is linked to a Supplier and the User doesn't already exist."""

    # Ensure the Contact has an email before proceeding
    if not self.email_id:
        return
    
    if not self.first_name:
        return

    # Find the Supplier linked to this Contact
    supplier_name = None
    for link in self.links:
        if link.link_doctype == "Supplier":
            supplier_name = link.link_name
            break  # Exit loop after finding the first Supplier

    if not supplier_name:
        return  # Exit if no Supplier link is found

    # Check if a User already exists with this email
    existing_user = frappe.db.exists("User", self.email_id)

    if not existing_user:
        # Create a new User
        user = frappe.get_doc({
            "doctype": "User",
            "email": self.email_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "send_welcome_email": 0,  # Avoid sending email automatically
            "roles": [{"role": "ZDT Merchant Onboarding"}],  # Assign the Supplier role
            "enabled": 1
        })
        user.insert(ignore_permissions=True)
        frappe.msgprint(f"User {self.email_id} created successfully.")


        existing_permission = frappe.db.exists(
            "User Permission", 
            {"user": user.name, "allow": "Supplier", "for_value": supplier_name}
        )

        if not existing_permission:
            # Create User Permission
            user_perm = frappe.get_doc({
                "doctype": "User Permission",
                "user": user.name,
                "allow": "Supplier",
                "for_value": supplier_name,  # Assign the Supplier from links
                "apply_to_all_doctypes": 1,  # Optional: restrict to specific doctypes
            })
            user_perm.insert(ignore_permissions=True)
            frappe.msgprint(f"User Permission for Supplier {supplier_name} created.")

