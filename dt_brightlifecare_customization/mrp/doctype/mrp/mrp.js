// Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("MRP", {

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

	get_raw_materials_for_transfer: function (frm) {
		// frm.dirty();

		frappe.call({
			method: "dt_brightlifecare_customization.mrp.doctype.mrp.mrp.get_raw_materials_for_transfer",
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
