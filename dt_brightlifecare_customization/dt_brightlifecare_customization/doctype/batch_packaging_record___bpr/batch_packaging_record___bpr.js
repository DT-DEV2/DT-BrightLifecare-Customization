// Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("Batch Packaging Record - BPR", {
    
    onload: function (frm) {
        // Disable add/delete for first table
        frm.fields_dict["line_clearance_for_primary_packing_area_detail"].grid.cannot_add_rows = false;
        frm.fields_dict["line_clearance_for_primary_packing_area_detail"].grid.cannot_delete_rows = false;
        
        // Disable add/delete for second table
        frm.fields_dict["primary_packing_defects_monitoring_detail"].grid.cannot_add_rows = true;
        frm.fields_dict["primary_packing_defects_monitoring_detail"].grid.cannot_delete_rows = true;

        frm.fields_dict["line_clearance_for_secondary_packing_area_detail"].grid.cannot_add_rows = true;
        frm.fields_dict["line_clearance_for_secondary_packing_area_detail"].grid.cannot_delete_rows = true;

        frm.fields_dict["online_inspection_details"].grid.cannot_add_rows = true;
        frm.fields_dict["online_inspection_details"].grid.cannot_delete_rows = true;

        frm.fields_dict["reconcilation_of_packing_material_detail"].grid.cannot_add_rows = true;
        frm.fields_dict["reconcilation_of_packing_material_detail"].grid.cannot_delete_rows = true;

        frm.refresh_field("line_clearance_for_primary_packing_area_detail");
        frm.refresh_field("primary_packing_defects_monitoring_detail");
        frm.refresh_field("line_clearance_for_secondary_packing_area_detail");
        frm.refresh_field("online_inspection_details");
        frm.refresh_field("reconcilation_of_packing_material_detail");
        
        
        if (frm.is_new()) {
            // First table
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Line Clearance for Primary Packing Area Template",
                    filters: { is_default: 1 },
                    fields: ["name"],
                    limit_page_length: 1
                },
                callback: function (r) {
                    if (r.message && r.message.length > 0) {
                        const default_template = r.message[0].name;
                        frappe.call({
                            method: "frappe.client.get",
                            args: { doctype: "Line Clearance for Primary Packing Area Template", name: default_template },
                            callback: function (res) {
                                if (res.message) {
                                    frm.clear_table("line_clearance_for_primary_packing_area_detail");
                                    (res.message.detail || []).forEach(detail => {
                                        let row = frm.add_child("line_clearance_for_primary_packing_area_detail");
                                        row.check_point = detail.check_point;
                                    });
                                    frm.refresh_field("line_clearance_for_primary_packing_area_detail");
                                }
                            }
                        });
                    }
                }
            });

            // Second table
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Primary Packing Defects Monitoring Template",
                    filters: { is_default: 1 },
                    fields: ["name"],
                    limit_page_length: 1
                },
                callback: function (r) {
                    if (r.message && r.message.length > 0) {
                        const default_template = r.message[0].name;
                        frappe.call({
                            method: "frappe.client.get",
                            args: { doctype: "Primary Packing Defects Monitoring Template", name: default_template },
                            callback: function (res) {
                                if (res.message) {
                                    frm.clear_table("primary_packing_defects_monitoring_detail");
                                    (res.message.detail || []).forEach(detail => {
                                        let row = frm.add_child("primary_packing_defects_monitoring_detail");
                                        row.types_of_defects = detail.types_of_defects;
                                    });
                                    frm.refresh_field("primary_packing_defects_monitoring_detail");
                                }
                            }
                        });
                    }
                }
            });



            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Line Clearance for Secondary Packing Area Template",
                    filters: { is_default: 1 },
                    fields: ["name"],
                    limit_page_length: 1
                },
                callback: function (r) {
                    if (r.message && r.message.length > 0) {
                        const default_template = r.message[0].name;
                        frappe.call({
                            method: "frappe.client.get",
                            args: { doctype: "Line Clearance for Secondary Packing Area Template", name: default_template },
                            callback: function (res) {
                                if (res.message) {
                                    frm.clear_table("line_clearance_for_secondary_packing_area_detail");
                                    (res.message.detail || []).forEach(detail => {
                                        let row = frm.add_child("line_clearance_for_secondary_packing_area_detail");
                                        row.check_point = detail.check_point;
                                    });
                                    frm.refresh_field("line_clearance_for_secondary_packing_area_detail");
                                }
                            }
                        });
                    }
                }
            });


            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Online Inspection Template",
                    filters: { is_default: 1 },
                    fields: ["name"],
                    limit_page_length: 1
                },
                callback: function (r) {
                    if (r.message && r.message.length > 0) {
                        const default_template = r.message[0].name;
                        frappe.call({
                            method: "frappe.client.get",
                            args: { doctype: "Online Inspection Template", name: default_template },
                            callback: function (res) {
                                if (res.message) {
                                    frm.clear_table("online_inspection_details");
                                    (res.message.detail || []).forEach(detail => {
                                        let row = frm.add_child("online_inspection_details");
                                        row.types_of_defectstime = detail.types_of_defectstime;
                                    });
                                    frm.refresh_field("online_inspection_details");
                                }
                            }
                        });
                    }
                }
            });


            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Reconcilation of Packing Material Template",
                    filters: { is_default: 1 },
                    fields: ["name"],
                    limit_page_length: 1
                },
                callback: function (r) {
                    if (r.message && r.message.length > 0) {
                        const default_template = r.message[0].name;
                        frappe.call({
                            method: "frappe.client.get",
                            args: { doctype: "Reconcilation of Packing Material Template", name: default_template },
                            callback: function (res) {
                                if (res.message) {
                                    frm.clear_table("reconcilation_of_packing_material_detail");
                                    (res.message.reconcilation_of_packing_material_particular_detail || []).forEach(detail => {
                                        let row = frm.add_child("reconcilation_of_packing_material_detail");
                                        row.particular = detail.particular;
                                    });
                                    frm.refresh_field("reconcilation_of_packing_material_detail");
                                }
                            }
                        });
                    }
                }
            });


            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Line Clearance for Coding Machine Template",
                    filters: { is_default: 1 },
                    fields: ["name"],
                    limit_page_length: 1
                },
                callback: function (r) {
                    if (r.message && r.message.length > 0) {
                        const default_template = r.message[0].name;
                        frappe.call({
                            method: "frappe.client.get",
                            args: { doctype: "Line Clearance for Coding Machine Template", name: default_template },
                            callback: function (res) {
                                if (res.message) {
                                    frm.clear_table("machine_setting_check_packing_in_charge");
                                    (res.message.detail || []).forEach(detail => {
                                        let row = frm.add_child("machine_setting_check_packing_in_charge");
                                        row.time = detail.time;
                                    });
                                    frm.refresh_field("machine_setting_check_packing_in_charge");
                                }
                            }
                        });
                    }
                }
            });

            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Auger Machine Line Critical Accessories Verification Template",
                    filters: { is_default: 1 },
                    fields: ["name"],
                    limit_page_length: 1
                },
                callback: function (r) {
                    if (r.message && r.message.length > 0) {
                        const default_template = r.message[0].name;
                        frappe.call({
                            method: "frappe.client.get",
                            args: { doctype: "Auger Machine Line Critical Accessories Verification Template", name: default_template },
                            callback: function (res) {
                                if (res.message) {
                                    frm.clear_table("auger_machine_line_critical_accessories_verification_details");
                                    (res.message.detail || []).forEach(detail => {
                                        let row = frm.add_child("auger_machine_line_critical_accessories_verification_details");
                                        row.auger_machine_line_parts = detail.auger_machine_line_parts;
                                        row.no_of_nutsbolts = detail.no_of_nutsbolts;
                                    });
                                    frm.refresh_field("auger_machine_line_critical_accessories_verification_details");
                                }
                            }
                        });
                    }
                }
            });

        }
    },
});
frappe.ui.form.on('Batch Packaging Record - BPR', {
    signature(frm) {
        if (frm.doc.signature) {
            frm.set_value('date_and_time', frappe.datetime.now_datetime());
        }
    }
});
