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

frappe.ui.form.on("BMR-Batch Manufacturing Report", {
    actual_yield_after_manufacturing(frm) {
        frm.trigger("check_deviation_condition");
    },
    theoretical_yield_reconcile(frm) {
        frm.trigger("check_deviation_condition");
    },
    refresh(frm) {
        frm.trigger("check_deviation_condition");
    },
    check_deviation_condition(frm) {
        const actual = frm.doc.actual_yield_after_manufacturing || 0;
        const theoretical = frm.doc.theoretical_yield_reconcile || 0;

        const fields = [
            'any_procedural_deviation',
            'deviation_held_in_production_qa__me',
            'action_done__planned',
            'done_by',
            'approval',
            'reference_report_no',
            'deviation_remarks'
        ];

        if (actual < theoretical) {
            frm.set_value('deviation_remarks', 'No Deviation');

            // Make all target fields read-only
            fields.forEach(f => {
                if (frm.fields_dict[f]) {
                    frm.fields_dict[f].df.read_only = 1;
                    frm.refresh_field(f);
                } else {
                    console.warn(`Field not found: ${f}`);
                }
            });
        } else {
            // Make them editable again
            fields.forEach(f => {
                if (frm.fields_dict[f]) {
                    frm.fields_dict[f].df.read_only = 0;
                    frm.refresh_field(f);
                }
            });
            frm.set_value('deviation_remarks', '');
        }
    }
});

frappe.ui.form.on('BMR-Batch Manufacturing Report', {
    check_rinse_test_of_equipment_is_done_qc_report_available(frm) {
        const value = frm.doc.check_rinse_test_of_equipment_is_done_qc_report_available;

        if (!value) return;

        const fields_to_update = [
            'check_general_cleanliness_and_housekeeping_of_the_area',
            'check_any_person_exposed_to_the_product',
            'check_cleaning_of_duct_filter_equipment',
            'check_testing_equipment_such_as_wet_and_dry',
            'check_weighing_balance_verified_recorded',
            'check_all_tools_are_properly_clean_in_good_condition',
            'check_no_leakage_in_sifter',
            'check_adequate_light_in_area',
            'check_the_waste_bins_are_empty_and_labeled_properly'
        ];

        fields_to_update.forEach(fieldname => {
            frm.set_value(fieldname, value);
        });
    }
});

