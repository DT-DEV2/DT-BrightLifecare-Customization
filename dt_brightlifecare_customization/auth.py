
import base64
import json
from collections.abc import Callable
import frappe
import frappe.utils
from frappe.utils.oauth import get_info_via_oauth, update_oauth_user, SignupDisabledError, redirect_post_login
from frappe import _


@frappe.whitelist(allow_guest=True)
def custom_login_via_google(code: str, state: str):
	login_via_oauth2("google", code, state, decoder=decoder_compat)



def login_via_oauth2(provider: str, code: str, state: str, decoder: Callable | None = None):
	info = get_info_via_oauth(provider, code, decoder)
	login_oauth_user(info, provider=provider, state=state)



def login_oauth_user(
	data: dict | str,
	*,
	provider: str | None = None,
	state: dict | str,
	generate_login_token: bool = False,
):
	# json.loads data and state
	if isinstance(data, str):
		data = json.loads(data)

	if isinstance(state, str):
		state = base64.b64decode(state)
		state = json.loads(state.decode("utf-8"))

	if not (state and state["token"]):
		frappe.respond_as_web_page(_("Invalid Request"), _("Token is missing"), http_status_code=417)
		return

	user = get_email(data)

	if not user:
		frappe.respond_as_web_page(
			_("Invalid Request"), _("Please ensure that your profile has an email address")
		)
		return

    # 🚫 Restrict Google SSO domain
	allowed_domain = frappe.db.get_single_value("DT Settings", "allowed_sso_domain")
	if provider == "google" and allowed_domain:
		if not user.lower().endswith(f"@{allowed_domain.lower()}"):
			frappe.respond_as_web_page(
				_("Access Denied"),
				_(f"Only accounts from {allowed_domain} are allowed for Google SSO."),
				http_status_code=403,
			)
			return
    
        # 🔒 Apply IP restriction (same logic as normal login)
		_apply_ip_restriction(user)

	try:
		if update_oauth_user(user, data, provider) is False:
			return

	except SignupDisabledError:
		return frappe.respond_as_web_page(
			"Signup is Disabled",
			"Sorry. Signup from Website is disabled.",
			success=False,
			http_status_code=403,
		)

	frappe.local.login_manager.login_as(user)

	# because of a GET request!
	frappe.db.commit()

	if frappe.utils.cint(generate_login_token):
		login_token = frappe.generate_hash(length=32)
		frappe.cache.set_value(f"login_token:{login_token}", frappe.local.session.sid, expires_in_sec=120)

		frappe.response["login_token"] = login_token

	else:
		redirect_to = state.get("redirect_to")
		redirect_post_login(
			desk_user=frappe.local.response.get("message") == "Logged In",
			redirect_to=redirect_to,
			provider=provider,
		)


def get_email(data: dict) -> str:
	return data.get("email") or data.get("upn") or data.get("unique_name")

def decoder_compat(b):
	# https://github.com/litl/rauth/issues/145#issuecomment-31199471
	return json.loads(bytes(b).decode("utf-8"))



import frappe
from ipaddress import ip_address, ip_network
from frappe import _
from frappe.sessions import delete_session


def _apply_ip_restriction(user):
	if user == "Administrator":
		return

	email = frappe.db.get_value("User", user, "email") or ""
	domain = email.split("@")[-1].lower() if "@" in email else ""

	settings = frappe.get_single("DT Settings")
	rows = [r for r in (settings.domain_based_user_restriction or []) if (r.domain or "").lower() == domain]

	if not rows:
		return  # No restriction defined for this domain

	client_ip = _get_client_ip()
	if not client_ip or not _ip_in_rows(client_ip, rows):
		frappe.respond_as_web_page(
			_("Access Denied"),
			_(f"Your IP ({client_ip or 'Unknown'}) is not allowed for domain {domain}."),
			http_status_code=403,
		)
		raise frappe.AuthenticationError(_("IP Restriction Failed"))



def restrict_normal_login(login_manager):
    user = login_manager.user
    if user == "Administrator":
        return

    email = frappe.db.get_value("User", user, "email") or ""
    domain = email.split("@")[-1].lower() if "@" in email else ""

    settings = frappe.get_single("DT Settings")
    rows = [r for r in (settings.domain_based_user_restriction or []) if (r.domain or "").lower() == domain]

    if not rows:
        return

    client_ip = _get_client_ip()

    if not client_ip or not _ip_in_rows(client_ip, rows):
        # don't call login_manager.logout(); do this instead:
        sid = getattr(frappe.session, "sid", None)
        if sid:
            try:
                delete_session(sid, user=user, reason="IP not allowed")
            except Exception:
                pass
        # now block
        frappe.throw(
            _("Login denied: Your IP ({0}) is not allowed for domain {1}.").format(client_ip or "Unknown", domain)
        )

def _get_client_ip():
    xff = frappe.get_request_header("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()
    return getattr(frappe.local, "request_ip", None) or getattr(frappe.request, "remote_addr", None)

def _ip_in_rows(client_ip_str, rows):
    try:
        ip_obj = ip_address(client_ip_str)
    except Exception:
        return False

    for r in rows:
        raw = (r.ip_address or "").strip()
        if not raw:
            continue
        try:
            if "/" in raw:
                if ip_obj in ip_network(raw, strict=False):
                    return True
            else:
                if ip_obj == ip_address(raw):
                    return True
        except Exception:
            continue
    return False
