// Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("MRP", {

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

	allocate_to_bom: function (frm) {
		// frm.dirty();

		frappe.call({
			method: "dt_brightlifecare_customization.mrp.doctype.mrp.mrp.allocate_to_bom",
			args: {
				mrp_name: frm.doc.name
			},
			callback: function(r) {
				if (!r.exc) {
					frappe.msgprint("Allocation logs created");
				}
			}
		});
	}
});
