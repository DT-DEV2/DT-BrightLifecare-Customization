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
    "Custom Field" : "public/js/custom_field.js",
    "Request for Quotation" : "public/js/rfq.js",
    "Supplier Quotation" : "public/js/supplier_quotation.js",
    "Material Request": "public/js/material_request.js",
    "Contract": "public/js/contract.js",
    "Material Request": "public/js/material_request.js",
    "Item": "public/js/item.js",
}


custom_field = [
    "Supplier Quotation-custom_process_status",
    "Warehouse-custom_shift_type",
    "Material Request Item-custom_linked_supplier",
    "Supplier-custom_supplier_category",
    "Contract-custom_section_break_ujptl",
    "Contract-custom_nda_sign_by_supplier",
    "Contract-custom_nda_sign_by_supplier_approver",
    "Contract-custom_nda_sign_by_supplier_approver_name",
    "Contract-custom_section_break_pxugv",
    "Contract-custom_nda_sign_by_healthkart",
    "Contract-custom_nda_sign_by_healthkart_approver",
    "Contract-custom_nda_sign_by_healthkart_approver_name",
    "BOM-custom_fg_batch_size",
    "BOM-custom_operation_time_for_this_bom_qty",
    "BOM-custom_operation_time_for_subassembly_bom_quantities",
    "BOM-custom_total_of_operation_time_for_bom",
    "BOM Item-custom_total_of_operation_time_for_bom",
    "Supplier Quotation Item-custom_moq",
    "Supplier Quotation Item-custom_freight_type",
    "Supplier-custom_section_break_oqq59",
    "Supplier-custom_iso_certificate",
    "Supplier-custom_column_break_agezn",
    "Supplier-custom_cancelled_cheque",
    "BOM-custom_priority",
    # "BOM-custom_total_operation_time_for_bom_qty",
    "BOM-custom_section_break_jsdpr",
    "BOM-custom_column_break_eqa1j",
    "BOM-custom_total_operation_time_for_batch_size",
    # "BOM-custom_operation_time_for_bom_qty",
    # "BOM-custom_operation_time_for_subbom_quantities",
    # "BOM Item-custom_total_operation_time_for_subbom_quantity",
    "Serial and Batch Entry-custom_batch_expiry_date",
    "Item Group-custom_rm_for_supplier_item_link",
    "Item Group-custom_pm_for_supplier_item_link",
    "BOM-custom_target_warehouse",
    "Supplier-custom_relabeller_fssai_contract_term",
    "Supplier-custom_oem_fssai_contract_term",
    "Supplier-custom_distributer_fssai_contract_term",
    "Supplier-custom_importer_fssai_contract_term",
    "Supplier-custom_trader_fssai_contract_term",
    "Supplier-custom_ayush_contract_term",
    "Supplier-custom_dcl_contract_term",
    "Supplier-custom_fssai_contract_term",
    "Contract-custom_section_break_nvfee",
    "Contract-custom_section_break_fqzbn",
    "Contract-custom_approvals",
    "Contract-custom_column_break_bt7ac",
    "Contract-custom_supplier_approval",
    "Contract-custom_healthkart_approval",
    "Contract-custom_supplier_approver",
    "Contract-custom_supplier_approver_name",
    "Contract-custom_healthkart_approver",
    "Contract-custom_healthkart_approver_name",
    "Material Request-custom_suppliers",
    "Contract-custom_contract_terms_and_template",
    "Supplier-custom_terms_and_conditions",
    "Supplier-custom_detail",
    "Supplier-custom_connected_users",
    "Supplier-custom_trader_fssai_license_valid_till",
    "Supplier-custom_oem_manufacturer_fssai_license",
    "Supplier-custom_oem_fssai_license_number",
    "Supplier-custom_column_break_tlk8e",
    "Supplier-custom_oem_fssai_license_attachment",
    "Supplier-custom_oem_fssai_license_valid_from",
    "Supplier-custom_oem_fssai_license_valid_till",
    "Supplier-custom_download_oem_fssai_declaration",
    "Supplier-custom_oem_fssai_signed_declaration_attachment",
    "Supplier-custom_oem_fssai_approval",
    "Supplier-custom_oem_fssai_remarks",
    "Supplier-custom_oem_product_details",
    "Supplier-custom_section_break_r2oer",
    "Supplier-custom_importer_fssai_license",
    "Supplier-custom_importer_fssai_license_number",
    "Supplier-custom_column_break_iztsk",
    "Supplier-custom_importer_fssai_license_attachment",
    "Supplier-custom_importer_fssai_license_valid_from",
    "Supplier-custom_importer_fssai_license_valid_till",
    "Supplier-custom_download_importer_fssai_declaration",
    "Supplier-custom_importer_fssai_signed_declaration_attachment",
    "Supplier-custom_importer_fssai_approval",
    "Supplier-custom_importer_fssai_remarks",
    "Supplier-custom_importer_product_details",
    "Supplier-custom_trader_fssai_license",
    "Supplier-custom_trader_fssai_license_number",
    "Supplier-custom_column_break_mlthg",
    "Supplier-custom_trader_fssai_license_attachment",
    "Supplier-custom_trader_fssai_license_valid_from",
    "Supplier-custom_download_trader_fssai_declaration",
    "Supplier-custom_trader_fssai_signed_declaration_attachment",
    "Supplier-custom_trader_fssai_approval",
    "Supplier-custom_trader_product_details",
    "Supplier-custom_trader_fssai_remarks",
    "Supplier-custom_distributer_download_fssai_declaration",
    "Supplier-custom_distributer_fssai_approval",
    "Supplier-custom_relabeller_download_fssai_declaration",
    "Supplier-custom_relabeller_fssai_approval",
    "Supplier Quotation-custom_section_break_5h8kq",
    "Supplier Quotation-custom_reason_for_selection",
    "Supplier-custom_product_details",
    "Supplier-custom_relabeller_product_details",
    "Supplier-custom_distributer_product_detail",
    "Supplier-custom_distributer_fssai_signed_declaration_attachment",
    "Supplier-custom_distributer_fssai_licence_attachment",
    "Request for Quotation Item-custom_hsnsac",
    "Supplier-custom_relabeller_fssai_license",
    "Supplier-custom_column_break_yb8zh",
    "Supplier-custom_distributer_fssai_license",
    "Supplier-custom_distributer_fssai_license_number",
    "Supplier-custom_column_break_29vxp",
    "Supplier-custom_distributer_fssai_license_valid_from",
    "Supplier-custom_distributer_fssai_remarks",
    "Supplier-custom_relabeller_fssai_remarks",
    "Supplier-custom_relabeller_fssai_signed_declaration_attachment",
    "Supplier-custom_fssai_remarks",
    "Supplier-custom_relabeller_fssai_licence_attachment",
    "Supplier-custom_relabeller_fssai_licence_valid_till",
    "Supplier-custom_relabeller_fssai_licence_number",
    "Supplier-custom_relabeller_fssai_licence_valid_from",
    "Supplier-custom_distributer_fssai_license_valid_till",
    "Supplier-custom_fssai_licence_attachment",
    "Supplier-custom_fssai_licence_valid_till",
    "Supplier-custom_fssai_licence",
    "Supplier-custom_fssai_licence_number",
    "Supplier-custom_fssai_licence_valid_from",
    "Supplier-custom_download_fssai_declaration",
    "Supplier-custom_ayush_product_approval",
    "Supplier-custom_dcl_product_approval",
    "Supplier-custom_download_dcl_declaration",
    "Supplier-custom_download_ayush_declaration",
    "Supplier-custom_section_break_rjafn",
    "Supplier-custom_column_break_k9dya",
    "Item-custom_item_sub_category",
    "Purchase Order-custom_item_group",
    "Purchase Receipt-custom_item_group",
    "Purchase Invoice-custom_item_group",
    "Supplier-custom_type_of_product",
    "Supplier-custom_section_break_itpwj",
    "Supplier-custom_section_break_dnjba",
    "Supplier-custom_type_of_product_compliance",
    "Supplier-custom_column_break_ig7x0",
    "Supplier-custom_section_break_p3fns",
    "Supplier-custom_column_break_8s46j",
    "Supplier-custom_section_break_1j9pl",
    "Supplier-custom_section_break_olxyc",
    "Supplier-custom_column_break_czofx",
    "Supplier-custom_section_break_obhua",
    "Supplier-custom_section_break_tgh2g",
    "Supplier-custom_column_break_tvtka",
    "Supplier-custom_column_break_eowxj",
    "Supplier-custom_dcl_signed_declaration_attachment",
    "Supplier-custom_ayush_signed_declaration_attachment",
    "Supplier-custom_fssai_signed_declaration_attachment",
    "Supplier-custom_authorised_dealer_remarks",
    "Supplier-custom_authorised_dealer_approval",
    "Supplier-custom_authorised_signatory_pan_remarks",
    "Supplier-custom_authorised_signatory_pan_approval",
    "Supplier-custom_authorised_signatory_aadhar_card_remarks",
    "Supplier-custom_authorised_signatory_aadhar_card_approval",
    "Supplier-custom_moa__aoa_remarks",
    "Supplier-custom_moa__aoa_approval",
    "Supplier-custom_br_remarks",
    "Supplier-custom_br_approval",
    "Supplier-custom_dcl_remarks",
    "Supplier-custom_gmp_remarks",
    "Supplier-custom_ayush_remarks",
    "Supplier-custom_coip_remarks",
    "Supplier-custom_coip_approval",
    "Supplier-custom_dcl_approval",
    "Supplier-custom_gmp_approval",
    "Supplier-custom_ayush_approval",
    "Supplier-custom_fssai_approval",
    "Sales Order-custom_terms_and_conditions_group",
    "Sales Order-custom_description",
    "Warehouse-custom_company_address",
    "Purchase Receipt-custom_supplier_delivery_note_date",
    "Company-custom_tan",
    "Company-custom_cin",
    "Company-custom_iec",
    "Sales Order-custom_sales_order_type",
    "Sales Order-custom_sales_order_channel",
    "Purchase Order-custom_purchase_order_type",
    "Delivery Note-custom_sales_order_type",
    "Delivery Note-custom_sales_order_channel",
    "Sales Invoice-custom_sales_order_type",
    "Sales Invoice-custom_sales_order_channel",
    "Purchase Receipt-custom_purchase_order_type",
    "Purchase Invoice-custom_purchase_order_type",
    "Supplier-custom_msme",
    "Supplier-custom_msme_number",
    "Supplier-custom_msme_type",
    "Warehouse-custom_branch",
    "Warehouse-custom_location",
    "Supplier-custom_certificate_of_incorporationpartnership",
    "Supplier-custom_terms",
    "Supplier-custom_gst_certificate_attachment",
    "Supplier-custom_pan_certificate_attachment",
    "Item-custom_type_of_product",
    "Supplier-custom_board_resolution_attachment",
    "Supplier-custom_board_resolution",
    "Supplier-custom_other_info",
    "Supplier-custom_column_break_xxpfy",
    "Supplier-custom_certificate_of_incorporationpartnership_attachment",
    "Supplier-custom_memorandum_of_association_moa_attachment",
    "Supplier-custom_authorised_signatory_name",
    "Supplier-custom_authorised_signatory_aadhar_card",
    "Supplier-custom_authorised_signatory_aadhar_card_attachment",
    "Supplier-custom_authorised_signatory_pan",
    "Supplier-custom_authorised_signatory_pan_attachment",
    "Supplier-custom_in_case_of_authorised_dealer",
    "Supplier-custom_column_break_jtrzh",
    "Supplier-custom_authorised_dealer_attachment",
    "Supplier-custom_ayush_license",
    "Supplier-custom_ayush_license_number",
    "Supplier-custom_ayush_license_attachment",
    "Supplier-custom_column_break_i7hju",
    "Supplier-custom_ayush_license_valid_from",
    "Supplier-custom_ayush_license_valid_till",
    "Supplier-custom_gmp_certificate",
    "Supplier-custom_gmp_certificate_number",
    "Supplier-custom_gmp_certificate_attachment",
    "Supplier-custom_column_break_toik2",
    "Supplier-custom_gmp_certificate_valid_from",
    "Supplier-custom_gmp_certificate_valid_till",
    "Supplier-custom_drugs__cosmetic_license",
    "Supplier-custom_drugs__cosmetic_license_number",
    "Supplier-custom_drugs__cosmetic_license_attachment",
    "Supplier-custom_column_break_obfy2",
    "Supplier-custom_drugs__cosmetic_license_valid_from",
    "Supplier-custom_drugs__cosmetic_license_valid_till",
    "Batch-custom_quality_check_schedule",
    "Item-custom_listing_id",
    "Item Group-custom_listing_id_visibility",
    "Material Request Item-custom_purpose_of_purchase",
    "Purchase Receipt Item-custom_expiry_date",
    "Item Group-custom_batch_expiry_date",
    "Item-custom_retest",
    "Batch-custom_supplier_name",
    "Purchase Order Item-custom_quality_inspection_template",
    "Request for Quotation Item-custom_quality_inspection_template",
    "Batch-custom_batch_grade",
    "Sales Invoice Item-custom_listing_id",
    "Delivery Note Item-custom_listing_id",
    "Sales Order Item-custom_listing_id",
    "Purchase Invoice Item-custom_listing_id",
    "Purchase Receipt Item-custom_listing_id",
    "Purchase Order Item-custom_listing_id",
    "Material Request Item-custom_listing_id",
    "Stock Entry Detail-custom_expiry_date",
    "Bank Account-custom_swift_code",
    "Quality Inspection Template-custom_item_code",
    "Quality Inspection Template-custom_is_default",
    "Quality Inspection Template-custom_is_disabled",
    "Item-custom_quality_inspection_template_list",
    "BOM-custom_workstation",
    "Supplier-custom_sourcing",
    "Stock Entry Detail-custom_batch_status",
    "Batch-custom_status",
    "Supplier-custom_is_marketplace_workflow",
    "Supplier-custom_section_break_2d9ub",
    "Supplier-custom_contract_id",
    "Supplier-custom_contract_supplier_approver",
    "Supplier-custom_contract_hk_approver",
    "Supplier-custom_nda_supplier_approver",
    "Supplier-custom_nda_hk_approver",
    "Blanket Order-custom_vendor_remarks",
    "Purchase Order-custom_vendor_remarks",
    "Quality Inspection Reading-custom_parameter_status",
    "Quality Inspection Reading-custom_specifications",
    "Quality Inspection Reading-custom_reference_number"
    "Item Quality Inspection Parameter-custom_status",
    "Item Quality Inspection Parameter-custom_specifications",
    "Item Quality Inspection Parameter-custom_reference_number",
    "Item Quality Inspection Parameter-custom_description",
    "Quality Inspection Parameter-custom_status",
    "Quality Inspection Parameter-custom_specifications",
    "Quality Inspection Parameter-custom_reference_number",
    "Quality Inspection Reading-custom_method_of_analysis",
    "Quality Inspection Reading-custom_test_uom",
    "Item Quality Inspection Parameter-custom_method_of_analysis",
    "Item Quality Inspection Parameter-custom_test_uom",
    "Quality Inspection Parameter-custom_method_of_analysis",
    "Quality Inspection Parameter-custom_test_uom",
    "Supplier Quotation-custom_connected_users",
    "Request for Quotation-custom_connected_users",
    "Purchase Order-custom_connected_users",
    "Purchase Order-custom_section_break_nclcq"
]


fixtures = [
    {
        "dt": "Custom Field", 
        "filters": [["name", "in", custom_field]]
    },
    {
        "dt": "Client Script", 
        "filters": [["module", "in", ["DT-BrightLifecare-Customization"]]]
    },
    {
        "dt": "Server Script", 
        "filters": [["module", "in", ["DT-BrightLifecare-Customization"]]]
    }
]


doc_events = {
    "Contact": {
        "before_save": "dt_brightlifecare_customization.public.py.contact.create_user_if_not_exists",
        "after_insert": "dt_brightlifecare_customization.public.py.contact.share_contact_with_email",
    },
    "Purchase Receipt": {
        "validate": "dt_brightlifecare_customization.public.py.purchase_receipt.validate_supplier_delivery_note"
    },
    "Purchase Order": {
        "before_save": "dt_brightlifecare_customization.public.py.purchase_order.before_save"
    },
    "Supplier": {
        "before_save": "dt_brightlifecare_customization.public.py.supplier.before_save"
    },
    "Request for Quotation": {
        "on_update": "dt_brightlifecare_customization.public.py.rfq.before_save"
    },
    "Material Request": {
        "before_save": "dt_brightlifecare_customization.public.py.material_request.before_save"
    },
    "Address":{
        "on_update": "dt_brightlifecare_customization.public.py.address.before_save",
    },
    "Bank Account":{
        "on_update": "dt_brightlifecare_customization.public.py.bank_account.before_save",
    },
    "Contract":{
        "on_update": "dt_brightlifecare_customization.public.py.contract.before_save",
        "on_submit": "dt_brightlifecare_customization.public.py.contract.on_submit",
        "on_cancel": "dt_brightlifecare_customization.public.py.contract.on_cancel",
    },
    "Role": {
        "on_update": "dt_brightlifecare_customization.public.py.role.create_role_config"
    },
    "Supplier Item Link": {
        "on_submit": "dt_brightlifecare_customization.dt_brightlifecare_customization.doctype.supplier_item_link.supplier_item_link.on_submit"
    },
    "Batch": {
        "after_insert": "dt_brightlifecare_customization.public.py.batch.set_expiry_date"
    },
    "Serial and Batch Bundle": {
        "before_submit": "dt_brightlifecare_customization.public.py.serial_and_batch_bundle.set_expiry_date"
    },
    "Item": {
        "before_save": "dt_brightlifecare_customization.public.py.item.before_save"
    },
    "Quality Inspection Template": {
        "on_update": "dt_brightlifecare_customization.public.py.quality_inspection_template.before_save"
    },
    "Supplier Quotation": {
        "before_save": "dt_brightlifecare_customization.public.py.supplier_quotation.fetch_connected_users"
    },

}

scheduler_events = {
    "daily": [
        "dt_brightlifecare_customization.public.py.disable_inactive_users.disable_inactive_users"
    ]
}



override_whitelisted_methods = {
    "frappe.integrations.oauth2_logins.login_via_google": "dt_brightlifecare_customization.auth.custom_login_via_google"
}

on_login = "dt_brightlifecare_customization.auth.restrict_normal_login"
