// Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
// For license information, please see license.txt

// frappe.ui.form.on("BMR-Batch Manufacturing Report", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("BMR-Batch Manufacturing Report", {
    production_dispense: function(frm) {
        // Copy Production Dispense to all child rows
        if (frm.doc.production_dispense) {
            (frm.doc.line_clearance || []).forEach(row => {
                frappe.model.set_value(row.doctype, row.name, "production", frm.doc.production_dispense);
            });
        } else {
            // Clear child values if parent is cleared
            (frm.doc.line_clearance || []).forEach(row => {
                frappe.model.set_value(row.doctype, row.name, "production", "");
            });
        }
        frm.refresh_field("line_clearance");
    },

    quality_dispense: function(frm) {
        // Copy Quality Dispense to all child rows
        if (frm.doc.quality_dispense) {
            (frm.doc.line_clearance || []).forEach(row => {
                frappe.model.set_value(row.doctype, row.name, "quality", frm.doc.quality_dispense);
            });
        } else {
            // Clear child values if parent is cleared
            (frm.doc.line_clearance || []).forEach(row => {
                frappe.model.set_value(row.doctype, row.name, "quality", "");
            });
        }
        frm.refresh_field("line_clearance");
    },

    before_save(frm) {
        // Ensure both values are synced before saving
        if (frm.doc.production_dispense) {
            (frm.doc.line_clearance || []).forEach(row => {
                frappe.model.set_value(row.doctype, row.name, "production", frm.doc.production_dispense);
            });
        }
        if (frm.doc.quality_dispense) {
            (frm.doc.line_clearance || []).forEach(row => {
                frappe.model.set_value(row.doctype, row.name, "quality", frm.doc.quality_dispense);
            });
        }
        frm.refresh_field("line_clearance");
    }
});
