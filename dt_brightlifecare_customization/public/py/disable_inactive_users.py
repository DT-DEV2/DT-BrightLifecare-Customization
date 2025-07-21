import frappe
from frappe.utils import now_datetime, get_datetime

def disable_inactive_users():
    today = now_datetime()
    inactive_threshold = 90  # days

    # Users to exclude from disabling
    excluded_users = ["Administrator", "Guest"]

    # Get all enabled system users
    users = frappe.get_all(
        "User",
        filters={"enabled": 1, "user_type": "System User"},
        fields=["name", "creation", "last_login"]
    )

    for user in users:
        if user.name in excluded_users:
            continue

        # Determine last activity date
        last_activity = get_last_activity(user.name)

        if not last_activity:
            # Never logged in or did anything
            try:
                created_on = get_datetime(user.creation)
                days_since_creation = (today - created_on).days
                if days_since_creation >= inactive_threshold:
                    disable_user(user.name)
            except Exception as e:
                frappe.logger().error(f"[User Disable] Error processing creation for {user.name}: {e}")
        else:
            # Has login or document activity
            try:
                days_since_last_activity = (today - last_activity).days
                if days_since_last_activity >= inactive_threshold:
                    disable_user(user.name)
            except Exception as e:
                frappe.logger().error(f"[User Disable] Error calculating activity age for {user.name}: {e}")


def get_last_activity(username):
    try:
        last_login = frappe.db.get_value("User", username, "last_login")

        last_doc_activity = frappe.db.sql(
            """
            SELECT MAX(creation)
            FROM `tabActivity Log`
            WHERE user = %s AND operation NOT IN ('Login', 'Logout')
            """,
            (username,),
        )[0][0]

        last_login_dt = get_datetime(last_login) if last_login else None
        last_doc_dt = get_datetime(last_doc_activity) if last_doc_activity else None

        if last_login_dt and last_doc_dt:
            return max(last_login_dt, last_doc_dt)
        return last_login_dt or last_doc_dt or None

    except Exception as e:
        frappe.logger().error(f"[User Disable] Error fetching activity for {username}: {e}")
        return None


def disable_user(username):
    try:
        user_doc = frappe.get_doc("User", username)
        user_doc.enabled = 0
        user_doc.add_comment("Comment", text="User disabled due to 90+ days of inactivity.")
        user_doc.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.logger().info(f"[User Disable] User {username} disabled due to inactivity.")
    except Exception as e:
        frappe.logger().error(f"[User Disable] Failed to disable {username}: {e}")
