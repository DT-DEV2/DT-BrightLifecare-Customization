import frappe
from frappe.core.doctype.user.user import User
from frappe.utils.data import sha256_hash
from frappe.utils import (
	cint,
	escape_html,
	flt,
	format_datetime,
	get_formatted_email,
	get_system_timezone,
	has_gravatar,
	now_datetime,
	today,
)

class CustomUser(User):
    def reset_password(self, send_email=False, password_expired=False):
        from frappe.utils import get_url

        key = frappe.generate_hash()
        hashed_key = sha256_hash(key)
        self.db_set("reset_password_key", hashed_key)
        self.db_set("last_reset_password_key_generated_on", now_datetime())

        url = "/update-password?key=" + key
        if password_expired:
            url = "/update-password?key=" + key + "&password_expired=true"

        # link = get_url(url, allow_header_override=False)                      Commented this line
        
        
        ###### Overidden part starts ######
        if frappe.request:
            base_url = f"{frappe.request.scheme}://{frappe.request.host}"
        else:
            # fallback when not inside a request (e.g. background job)
            base_url = frappe.local.conf.host_name

        link = url + base_url
        ###### Overidden part ends ######
        
        if send_email:
            self.password_reset_mail(link)

        return link