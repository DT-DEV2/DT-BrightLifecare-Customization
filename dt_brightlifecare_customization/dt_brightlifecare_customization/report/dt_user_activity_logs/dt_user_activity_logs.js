frappe.query_reports["DT User Activity Logs"] = {
	filters: [
		{
			fieldname: "user",
			label: __("User"),
			fieldtype: "Link",
			options: "User",
			reqd: 0
		},
		{
			fieldname: "from_date",
			label: __("From Datetime"),
			fieldtype: "Datetime",
			default: frappe.datetime.add_days(frappe.datetime.now_datetime(), -7),
			reqd: 1
		},
		{
			fieldname: "to_date",
			label: __("To Datetime"),
			fieldtype: "Datetime",
			default: frappe.datetime.now_datetime(),
			reqd: 1
		}
	]
};
