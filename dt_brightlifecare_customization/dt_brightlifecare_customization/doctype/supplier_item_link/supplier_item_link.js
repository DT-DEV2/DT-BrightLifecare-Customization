// Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("Supplier Item Link", {
	validate: function(frm) {
        if (frm.doc.share_owner_name_contact_details) {
            if (!frm.doc.share_owner_name_contact_details.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.rm_coas) {
            if (!frm.doc.rm_coas.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.for_botanical_ingredient) {
            if (!frm.doc.for_botanical_ingredient.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.for_vitaminminerals) {
            if (!frm.doc.for_vitaminminerals.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.for_compound_ingredients) {
            if (!frm.doc.for_compound_ingredients.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.fssai_license_copy) {
            if (!frm.doc.fssai_license_copy.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.storage_condition_declarationshelf_life) {
            if (!frm.doc.storage_condition_declarationshelf_life.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.method_of_analysis_moa) {
            if (!frm.doc.method_of_analysis_moa.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.wada_nada) {
            if (!frm.doc.wada_nada.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.rm_technical_sheet) {
            if (!frm.doc.rm_technical_sheet.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.food_grade_declaration) {
            if (!frm.doc.food_grade_declaration.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.naturalsynthetic_declaration) {
            if (!frm.doc.naturalsynthetic_declaration.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.source_of_ingredient) {
            if (!frm.doc.source_of_ingredient.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.msds) {
            if (!frm.doc.msds.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.allergen_and_cross_contamination_declaration) {
            if (!frm.doc.allergen_and_cross_contamination_declaration.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.halal_and_kosher_certificate) {
            if (!frm.doc.halal_and_kosher_certificate.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.non_gmovegannatural_declaration) {
            if (!frm.doc.non_gmovegannatural_declaration.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc._6th_month_foscos_test_report) {
            if (!frm.doc._6th_month_foscos_test_report.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.pds_and_tds) {
            if (!frm.doc.pds_and_tds.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.process_flow_chart) {
            if (!frm.doc.process_flow_chart.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }
        

        if (frm.doc.gluten_free) {
            if (!frm.doc.gluten_free.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.stability_data) {
            if (!frm.doc.stability_data.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.country_of_origin_declaration) {
            if (!frm.doc.country_of_origin_declaration.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }

        if (frm.doc.clinical_studies_and_publications) {
            if (!frm.doc.clinical_studies_and_publications.toLowerCase().endsWith('.pdf')) {
                frappe.throw(__('Only PDF files are allowed in the attachment.'));
            }
        }
    }
});
