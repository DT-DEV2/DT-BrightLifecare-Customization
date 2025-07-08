frappe.query_reports["DT User Access Review Report"] = {
    filters: [
        {
            fieldname: "user",
            label: __("User"),
            fieldtype: "Link",
            options: "User",
            get_query: function () {
                const show_disabled = frappe.query_report.get_filter_value("show_disable_users");
                return {
                    filters: {
                        enabled: show_disabled ? 0 : 1
                    }
                };
            }
        },
        {
            fieldname: "role",
            label: __("Role"),
            fieldtype: "Link",
            options: "Role"
        },
        {
            fieldname: "doctype",
            label: __("Document Type"),
            fieldtype: "Link",
            options: "DocType"
        },
        {
            fieldname: "show_empty_roles",
            label: __("Show Users with No Roles"),
            fieldtype: "Check",
            default: 1
        },
        {
            fieldname: "show_empty_perms",
            label: __("Show Roles with No Permissions"),
            fieldtype: "Check",
            default: 1
        },
        {
            fieldname: "show_disable_users",
            label: __("Show Disable Users"),
            fieldtype: "Check",
            default: 0,
            onchange: function () {
				// Clear value
				frappe.query_report.set_filter_value("user", "");
			
				// Refresh all filters to re-evaluate get_query
				frappe.query_report.refresh_filters();
			
				// Refresh report results
				frappe.query_report.refresh();
				
			}
        },
    ],

   
    formatter: function (value, row, column, data, default_formatter) {
        let formatted_value = default_formatter(value, row, column, data);

        if (column.id === "role" && value === "No Role Assigned") {
            return `<span style="color: red; font-weight: bold;">${value}</span>`;
        }

        if (column.id === "doctype" && value === "No Permissions") {
            return `<span style="color: orange; font-weight: bold;">${value}</span>`;
        }

        if (column.fieldtype === "Check") {
            formatted_value = value ? "✔" : "✖";
        }

        

        return formatted_value;
    }
};
