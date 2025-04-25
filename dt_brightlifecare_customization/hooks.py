app_name = "dt_brightlifecare_customization"
app_title = "DT-BrightLifecare-Customization"
app_publisher = "Digitalis Technologies Pvt Ltd"
app_description = "Customization for DT BrightLifecare Customization"
app_email = "contact@digitalistech.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "dt_brightlifecare_customization",
# 		"logo": "/assets/dt_brightlifecare_customization/logo.png",
# 		"title": "DT-BrightLifecare-Customization",
# 		"route": "/dt_brightlifecare_customization",
# 		"has_permission": "dt_brightlifecare_customization.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/dt_brightlifecare_customization/css/dt_brightlifecare_customization.css"
# app_include_js = "/assets/dt_brightlifecare_customization/js/dt_brightlifecare_customization.js"

# include js, css files in header of web template
# web_include_css = "/assets/dt_brightlifecare_customization/css/dt_brightlifecare_customization.css"
# web_include_js = "/assets/dt_brightlifecare_customization/js/dt_brightlifecare_customization.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "dt_brightlifecare_customization/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "dt_brightlifecare_customization/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "dt_brightlifecare_customization.utils.jinja_methods",
# 	"filters": "dt_brightlifecare_customization.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "dt_brightlifecare_customization.install.before_install"
# after_install = "dt_brightlifecare_customization.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "dt_brightlifecare_customization.uninstall.before_uninstall"
# after_uninstall = "dt_brightlifecare_customization.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "dt_brightlifecare_customization.utils.before_app_install"
# after_app_install = "dt_brightlifecare_customization.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "dt_brightlifecare_customization.utils.before_app_uninstall"
# after_app_uninstall = "dt_brightlifecare_customization.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "dt_brightlifecare_customization.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"dt_brightlifecare_customization.tasks.all"
# 	],
# 	"daily": [
# 		"dt_brightlifecare_customization.tasks.daily"
# 	],
# 	"hourly": [
# 		"dt_brightlifecare_customization.tasks.hourly"
# 	],
# 	"weekly": [
# 		"dt_brightlifecare_customization.tasks.weekly"
# 	],
# 	"monthly": [
# 		"dt_brightlifecare_customization.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "dt_brightlifecare_customization.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "dt_brightlifecare_customization.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "dt_brightlifecare_customization.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["dt_brightlifecare_customization.utils.before_request"]
# after_request = ["dt_brightlifecare_customization.utils.after_request"]

# Job Events
# ----------
# before_job = ["dt_brightlifecare_customization.utils.before_job"]
# after_job = ["dt_brightlifecare_customization.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"dt_brightlifecare_customization.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

doctype_js = {
    "Sales Order" : "public/js/sales_order.js",
    "Purchase Order" : "public/js/purchase_order.js",
    "Warehouse" : "public/js/warehouse.js",
    "Stock Entry": "public/js/stock_entry.js",
    "Supplier" : "public/js/supplier.js",
}


fixtures = [
    {
        "dt": "Custom Field", 
        "filters": [["module", "in", ["DT-BrightLifecare-Customization"]]]
    },
    {
        "dt": "Client Script", 
        "filters": [["module", "in", ["DT-BrightLifecare-Customization"]]]
    }
]


doc_events = {
    "Contact": {
        "before_save": "dt_brightlifecare_customization.public.py.contact.create_user_if_not_exists"
    },
    "Purchase Receipt": {
        "validate": "dt_brightlifecare_customization.public.py.purchase_receipt.validate_supplier_delivery_note"
    },
    "Purchase Order": {
        "before_save": "dt_brightlifecare_customization.public.py.purchase_order.before_save"
    },
    "Supplier": {
        "before_save": "dt_brightlifecare_customization.public.py.supplier.before_save"
    }

}
