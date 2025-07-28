// Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("MRP", {

	calculate_bom_allocation: function (frm) {
		if (frm.doc.allocation_status === "In Progress") {
			frappe.msgprint("BOM Allocation is already in progress. Please wait...");
			return;
		}
		
		// Prevent multiple concurrent runs
		if (frm.__allocation_in_progress) {
			frappe.msgprint("BOM Allocation is already in progress. Please wait...");
			return;
		}

		frm.dirty();
		frm.__allocation_in_progress = true;

		// Optional: Generate a unique job ID (safer if multiple users)
		const job_id = frappe.utils.get_random(8);
		frm.__allocation_job_id = job_id;

		// Show initial progress
		frappe.show_progress("Calculating BOM Allocation", 0, 100, "Starting...");

		// Clear any previous listener
		if (frm.__unsubscribe_allocation) {
			frm.__unsubscribe_allocation(); // cleanup
		}

		// Listen to progress updates only for this session
		const unsubscribe = frappe.realtime.on("mrp_bom_allocation_progress", function (data) {
			// Optional: if using job_id, filter messages
			// if (data.job_id !== job_id) return;

			frappe.show_progress("Calculating BOM Allocation", data.progress, 100, data.message);

			if (data.progress === 100 || data.failed) {
				frm.__allocation_in_progress = false;
				frappe.hide_progress();

				if (!data.failed) {
					setTimeout(() => {
						// frm.set_value("allocation_status", "Completed");
						frm.reload_doc();
					}, 500); // 500ms delay to ensure UI is ready
				}

				// Unsubscribe to avoid duplicate listeners
				if (frm.__unsubscribe_allocation) {
					frm.__unsubscribe_allocation();
					frm.__unsubscribe_allocation = null;
				}

				frm.reload_doc();
			}
		});

		frm.__unsubscribe_allocation = unsubscribe;

		// Trigger backend
		frappe.call({
			method: "dt_brightlifecare_customization.mrp.doctype.mrp.mrp.calculate_bom_allocation",
			args: {
				mrp_name: frm.doc.name,
				job_id: job_id  // optional if you want to match messages
			},
			freeze: true,
			error: function () {
				frm.__allocation_in_progress = false;
				frappe.hide_progress();
				if (frm.__unsubscribe_allocation) {
					frm.__unsubscribe_allocation();
					frm.__unsubscribe_allocation = null;
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
