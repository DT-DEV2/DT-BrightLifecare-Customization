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

	calculate_bom_allocation: function (frm) {
		frm.dirty();

		frappe.call({
			method: "dt_brightlifecare_customization.mrp.doctype.mrp.mrp.calculate_bom_allocation",
			args: {
				mrp_name: frm.doc.name
			},
			freeze: true,
			callback: function(r) {
				if (!r.exc) {
					frappe.msgprint("Allocation logs created");
				}
			}
		});
	},

	allocate_bom: function (frm) {
		frm.dirty();

		frappe.call({
			method: "dt_brightlifecare_customization.mrp.doctype.mrp.mrp.allocate_bom",
			args: {
				mrp_name: frm.doc.name
			},
			freeze: true,
			callback: function(r) {
				if (!r.exc) {
					frm.reload_doc();
				}
			}
		});
	},

	explode_bom: function (frm) {
		// frm.dirty();

		frappe.call({
			method: "dt_brightlifecare_customization.mrp.doctype.mrp.mrp.explode_bom",
			args: {
				mrp_name: frm.doc.name
			},
			callback: function(r) {
				if (!r.exc) {
					frm.reload_doc();
				}
			}
		});
	},	
});
