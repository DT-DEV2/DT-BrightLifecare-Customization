// Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("MRP", {
	get_sub_assembly_items: function (frm) {
		frm.dirty();

		frappe.call({
			method: "get_sub_assembly_items",
			freeze: true,
			doc: frm.doc,
			callback: function () {
				refresh_field("sub_assembly_items");
			},
		});
	},

	get_raw_materials: function (frm) {
		frm.dirty();

		frappe.call({
			method: "get_raw_materials",
			freeze: true,
			doc: frm.doc,
			callback: function () {
				refresh_field("raw_materials");
			},
		});
	},
});
