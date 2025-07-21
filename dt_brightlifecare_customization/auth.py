

import frappe

def restrict_google_users(login_manager):
    user = frappe.get_doc("User", login_manager.user)

    # You can identify SSO users by checking if they came via OAuth
    auth_provider = frappe.local.request and frappe.local.request.cookies.get("auth_provider")

    if auth_provider == "google":
        # Restrict login to specific domain
        if not user.email.endswith("@brightlifecare.com"):
            frappe.local.login_manager.logout()
            frappe.throw("Only brightlifecare.com emails are allowed for Google SSO.")
