frappe.ui.form.on("Quality Inspection", {
    refresh: function (frm) {

        // Only allow on Draft QI with valid reference
        if (
            frm.doc.docstatus !== 0 ||
            !["Purchase Receipt", "Delivery Note", "Stock Entry"].includes(frm.doc.reference_type)
        ) {
            return;
        }

        frappe.call({
            method: "dt_brightlifecare_customization.public.py.quality_inspection.has_sample_stock_entry",
            args: { qi_name: frm.doc.name },
            callback: function (r) {
                if (r.exc || !r.message) return;

                // -------------------------------
                // Always update status field
                // -------------------------------
                frm.set_value(
                    "custom_sample_status",
                    r.message.status || ""
                );

                // -------------------------------
                // ALWAYS show Collect Sample button
                // -------------------------------
                frm.add_custom_button(__("Collect Sample"), function () {

                    // Guard: already collected
                    // if (r.message.active) {
                    //     frappe.msgprint({
                    //         title: __("Already Collected"),
                    //         message: __("Sample or Reference has already been collected for this Quality Inspection."),
                    //         indicator: "orange"
                    //     });
                    //     return;
                    // }

                    // -------------------------------
                    // Prompt fields
                    // -------------------------------
                    let fields = [
                        {
                            label: __("Enter Sample Quantity"),
                            fieldname: "sample_qty",
                            fieldtype: "Float",
                            reqd: 1,
                            default: frm.doc.sample_size || 1
                        }
                    ];

                    // Type of Sample only for Stock Entry
                    if (frm.doc.reference_type === "Stock Entry") {
                        fields.push({
                            label: __("Type of Sample"),
                            fieldname: "type_of_sample",
                            fieldtype: "Select",
                            options: ["", "Quality Testing Sample", "Reference Sample", "Sample Transfer to HO"].join("\n"),
                            reqd: 1
                        });
                    }

                    frappe.prompt(
                        fields,
                        function (data) {
                            frappe.call({
                                method: "dt_brightlifecare_customization.public.py.quality_inspection.make_internal_transfer",
                                args: {
                                    qi_name: frm.doc.name,
                                    sample_qty: data.sample_qty,
                                    type_of_sample: data.type_of_sample || null
                                },
                                callback: function (res) {
                                    if (res.exc) return;

                                    frm.reload_doc();

                                    if (res.message?.stock_entry) {
                                        frappe.msgprint({
                                            message: __(
                                                'Stock Entry created: <a href="/app/stock-entry/{0}" target="_blank">{0}</a>',
                                                [res.message.stock_entry]
                                            ),
                                            indicator: "green"
                                        });

                                        // Trigger workflow safely
                                        frappe.call({
                                            method: "frappe.model.workflow.apply_workflow",
                                            args: {
                                                doc: frm.doc,
                                                action: "Collect Sample"
                                            },
                                            callback: function () {
                                                frm.reload_doc();
                                            }
                                        });
                                    }
                                }
                            });
                        },
                        __("Collect Sample"),
                        __("Create")
                    );
                });
            }
        });


        if (frm.doc.docstatus === 0 && frm.doc.custom_sample_status === "Sample Collected") {
            frm.add_custom_button(__("NRGP"), () => {

        // STEP 1 → Choose NRGP Type
                let step1 = new frappe.ui.Dialog({
                    title: __("Choose NRGP Type"),
                    fields: [
                        {
                            fieldtype: "Select",
                            label: "NRGP Type",
                            fieldname: "nrgp_type",
                            options: ["Internal", "External"],
                            reqd: 1
                        }
                    ],
                    primary_action_label: __("Next"),
                    primary_action(values) {
                        step1.hide();

                        // ================= EXTERNAL NRGP =================
                        if (values.nrgp_type === "External") {
                            let readings_data = [];

                            frappe.call({
                                method: "frappe.client.get",
                                args: {
                                    doctype: "Quality Inspection",
                                    name: frm.doc.name
                                },
                                callback(res) {
                                    if (res.message && res.message.readings) {
                                        readings_data = res.message.readings.map(r => ({
                                            parameter: r.specification || r.parameter || "",
                                            test_cost: 0
                                        }));
                                    }

                                    let address_dialog = new frappe.ui.Dialog({
                                        title: __("External QC NRGP Details"),
                                        fields: [
                                            {
                                                fieldtype: "Check",
                                                label: "FOSCOS",
                                                fieldname: "foscos"
                                            },
                                            {
                                                fieldtype: "Link",
                                                label: "Source Warehouse",
                                                fieldname: "source_warehouse",
                                                options: "Warehouse",
                                                reqd: 1,
                                                get_query: function() {
                                                    // Make sure frm.doc.name exists and is the current QI name
                                                    if (!cur_frm || !cur_frm.doc || !cur_frm.doc.name) {
                                                        console.error("No current form or document found");
                                                        return;
                                                    }
                                                    
                                                    return {
                                                        query: "dt_brightlifecare_customization.public.py.quality_inspection.get_sample_batch_warehouses",
                                                        filters: {
                                                            qi_name: cur_frm.doc.name
                                                        }
                                                    };
                                                }
                                            },
                                            {
                                                fieldtype: "Link",
                                                label: "Ship To Address",
                                                fieldname: "ship_to_address",
                                                options: "Address",
                                                reqd: 1,
                                                get_query: () => ({
                                                    filters: { custom_ship_to_external_nrgp: 1 }
                                                })
                                            },
                                            {
                                                fieldtype: "Float",
                                                label: "Quantity",
                                                fieldname: "custom_qty",
                                                reqd: 1
                                            },
                                            {
                                                fieldtype: "Table",
                                                fieldname: "parameters_table",
                                                label: "Parameters",
                                                cannot_add_rows: true,
                                                in_place_edit: true,
                                                fields: [
                                                    {
                                                        fieldtype: "Data",
                                                        fieldname: "parameter",
                                                        label: "Parameter",
                                                        in_list_view: 1,
                                                        read_only: 1
                                                    },
                                                    {
                                                        fieldtype: "Float",
                                                        fieldname: "test_cost",
                                                        label: "Test Cost",
                                                        in_list_view: 1
                                                    }
                                                ]
                                            }
                                        ],

                                        // ---- DRAFT ----
                                        primary_action_label: __("Add Transporter Details"),
                                        primary_action(values) {
                                            const selected_rows =
                                                address_dialog.fields_dict.parameters_table.grid.get_selected_children();

                                            const parameters = (selected_rows || []).map(r => ({
                                                parameter: r.parameter,
                                                total_cost: r.test_cost || 0
                                            }));

                                            frappe.call({
                                                method: "dt_brightlifecare_customization.public.py.quality_inspection.make_external_nrgp",
                                                args: {
                                                    qi_name: frm.doc.name,
                                                    source_warehouse: values.source_warehouse,
                                                    ship_to_address: values.ship_to_address,
                                                    custom_qty: values.custom_qty,
                                                    draft: true,
                                                    parameters: parameters
                                                },
                                                callback(r) {
                                                    frm.reload_doc();
                                                    if (r.message?.stock_entry) {
                                                        frappe.msgprint({
                                                            message: __(
                                                                'External QC NRGP created in Draft: <a href="/app/stock-entry/{0}" target="_blank">{0}</a>',
                                                                [r.message.stock_entry]
                                                            ),
                                                            indicator: "green"
                                                        });
                                                    }
                                                }
                                            });
                                            address_dialog.hide();
                                        },

                                        // ---- SUBMIT ----
                                        secondary_action_label: __("Submit"),
                                        secondary_action() {
                                            const vals = address_dialog.get_values();
                                            const selected_rows =
                                                address_dialog.fields_dict.parameters_table.grid.get_selected_children();

                                            const parameters = (selected_rows || []).map(r => ({
                                                parameter: r.parameter,
                                                total_cost: r.test_cost || 0
                                            }));

                                            frappe.call({
                                                method: "dt_brightlifecare_customization.public.py.quality_inspection.make_external_nrgp",
                                                args: {
                                                    qi_name: frm.doc.name,
                                                    source_warehouse: vals.source_warehouse,
                                                    ship_to_address: vals.ship_to_address,
                                                    custom_qty: vals.custom_qty,
                                                    draft: false,
                                                    parameters: parameters
                                                },
                                                callback(r) {
                                                    frm.reload_doc();
                                                    if (r.message?.stock_entry) {
                                                        frappe.msgprint({
                                                            message: __(
                                                                'External QC NRGP created & Submitted: <a href="/app/stock-entry/{0}" target="_blank">{0}</a>',
                                                                [r.message.stock_entry]
                                                            ),
                                                            indicator: "green"
                                                        });
                                                    }
                                                }
                                            });
                                            address_dialog.hide();
                                        }
                                    });

                                    // BACK BUTTON
                                    $(`<button class="btn btn-default">${__("Back")}</button>`)
                                        .prependTo(address_dialog.$wrapper.find(".modal-footer"))
                                        .on("click", () => {
                                            address_dialog.hide();
                                            step1.show();
                                        });

                                    // LOAD PARAMETERS
                                    address_dialog.fields_dict.parameters_table.df.data = readings_data;
                                    address_dialog.fields_dict.parameters_table.refresh();

                                    // LOCK ROW DELETE
                                    let grid = address_dialog.fields_dict.parameters_table.grid;
                                    grid.cannot_delete_rows = true;
                                    grid.wrapper.find(".grid-remove-rows").hide();

                                    address_dialog.show();
                                }
                            });

                        // ================= INTERNAL NRGP (UNCHANGED) =================
                        } else {
                             let readings_data = [];

                            // Fetch readings data first
                            frappe.call({
                                method: "frappe.client.get",
                                args: {
                                    doctype: "Quality Inspection",
                                    name: frm.doc.name
                                },
                                callback: function (res) {
                                    if (res.message && res.message.readings) {
                                        readings_data = res.message.readings.map(r => ({
                                            parameter: r.specification || r.parameter || ""
                                        }));
                                    }

                                    // Now open the dialog once data is ready
                                    let step2 = new frappe.ui.Dialog({
                                        title: __("Select Target Warehouse"),
                                        fields: [
                                            {
                                                fieldtype: "Link",
                                                label: "Target Warehouse",
                                                fieldname: "target_warehouse",
                                                options: "Warehouse",
                                                reqd: 1,
                                                get_query: () => ({
                                                    filters: { custom_internal_nrgp: 1 }
                                                })
                                            },
                                            {
                                                fieldtype: "Float",
                                                label: "Quantity",
                                                fieldname: "custom_qty",
                                                reqd: 1
                                            },
                                            {
                                                fieldtype: "Table",
                                                fieldname: "parameters_table",
                                                label: "Parameters",
                                                cannot_add_rows: true,
                                                in_place_edit: true,
                                                fields: [
                                                    {
                                                        fieldtype: "Data",
                                                        fieldname: "parameter",
                                                        label: "Parameter",
                                                        in_list_view: 1,
                                                        read_only: 1
                                                    }
                                                ]
                                            }
                                        ],
                                        primary_action_label: __("Add Transporter Details"),
                                        primary_action(values) {
                                            // ✅ Get selected rows using ERPNext’s built-in selection
                                            const selected_rows = step2.fields_dict.parameters_table.grid.get_selected_children();
                                            const parameters = (selected_rows || []).map(r => ({
                                                parameter: r.parameter,
                                            }));

                                            frappe.call({
                                                method: "dt_brightlifecare_customization.public.py.quality_inspection.make_internal_nrgp",
                                                args: {
                                                    qi_name: frm.doc.name,
                                                    target_warehouse: values.target_warehouse,
                                                    custom_qty: values.custom_qty,
                                                    draft: true,
                                                    parameters: parameters
                                                },
                                                callback(r) {
                                                    frm.reload_doc();
                                                    if (r.message && r.message.stock_entry) {
                                                        frappe.msgprint({
                                                            message: __('Internal NRGP created in Draft: <a href="/app/stock-entry/{0}" target="_blank">{0}</a>', [r.message.stock_entry]),
                                                            indicator: 'green'
                                                        });
                                                    }
                                                }
                                            });
                                            step2.hide();
                                        },
                                        secondary_action_label: __("Submit"),
                                        secondary_action() {
                                            const vals = step2.get_values();
                                            const selected_rows = step2.fields_dict.parameters_table.grid.get_selected_children();
                                            const parameters = (selected_rows || []).map(r => ({
                                                parameter: r.parameter,
                                            }));

                                            frappe.call({
                                                method: "dt_brightlifecare_customization.public.py.quality_inspection.make_internal_nrgp",
                                                args: {
                                                    qi_name: frm.doc.name,
                                                    target_warehouse: vals.target_warehouse,
                                                    custom_qty: vals.custom_qty,
                                                    draft: false,
                                                    parameters: parameters
                                                },
                                                callback(r) {
                                                    frm.reload_doc();
                                                    if (r.message && r.message.stock_entry) {
                                                        frappe.msgprint({
                                                            message: __('Internal NRGP created & Submitted: <a href="/app/stock-entry/{0}" target="_blank">{0}</a>', [r.message.stock_entry]),
                                                            indicator: 'green'
                                                        });
                                                    }
                                                }
                                            });
                                            step2.hide();
                                        }
                                    });

                                    // Add Back button
                                    $(`<button class="btn btn-default">${__("Back")}</button>`)
                                        .prependTo(step2.$wrapper.find(".modal-footer"))
                                        .on("click", () => {
                                            step2.hide();
                                            step1.show();
                                        });

                                    // Populate parameters
                                    step2.fields_dict.parameters_table.df.data = readings_data;
                                    step2.fields_dict.parameters_table.refresh();

                                    step2.show();

                                    // 🔒 Disable delete in the table
                                    step2.fields_dict.parameters_table.grid.wrapper.find('.grid-remove-rows').hide();
                                    step2.fields_dict.parameters_table.grid.cannot_delete_rows = true;
                                }
                            });
                        }


                    }
                });

                step1.show();
            });
        }
    }
});

frappe.ui.form.on("Quality Inspection", {
    refresh: function(frm) {
        // Always visible & grey by default
        ["custom_internal_report", "custom_coa"].forEach(f => {
            frm.set_df_property(f, "hidden", 0);
            frm.fields_dict[f].df.read_only = 1;
            frm.refresh_field(f);
        });

        // Hide external billed received by default
        frm.set_df_property("custom_coa_externalbilledreceived", "hidden", 1);

        if (!frm.doc.name) return;

        frappe.call({
            method: "dt_brightlifecare_customization.public.py.quality_inspection.check_stock_entries",
            args: { qi_name: frm.doc.name },
            callback: function(r) {
                if (!r.message) return;
                const { internal_exists, external_exists } = r.message;

                // Internal COA → editable if ANY internal entry exists
                if (internal_exists) {
                    unlock_attach(frm, "custom_internal_report");
                }

                // Batch COA rules
                apply_batch_coa_rule(frm, internal_exists);

                // Show external billed received only if custom_coa is attached
                toggle_external_billed_received(frm);
            }
        });
    },

    custom_internal_report: function(frm) {
        recheck_batch_coa(frm);
    },

    custom_external_report: function(frm) {
        recheck_batch_coa(frm);
    },

    custom_coa: function(frm) {
        toggle_external_billed_received(frm);
    }
});

// Helpers
function lock_attach(frm, fieldname) {
    frm.fields_dict[fieldname].df.read_only = 1;
    frm.refresh_field(fieldname);
}
function unlock_attach(frm, fieldname) {
    frm.fields_dict[fieldname].df.read_only = 0;
    frm.refresh_field(fieldname);
}
function apply_batch_coa_rule(frm, internal_exists, external_exists) {
    lock_attach(frm, "custom_coa"); // default lock

    if (internal_exists && !external_exists) {
        // Only internal
        if (frm.doc.custom_internal_report) unlock_attach(frm, "custom_coa");
    } else if (!internal_exists && external_exists) {
        // Only external
        if (frm.doc.custom_external_report) unlock_attach(frm, "custom_coa");
        
    }
}
function recheck_batch_coa(frm) {
    frappe.call({
        method: "dt_brightlifecare_customization.public.py.quality_inspection.check_stock_entries",
        args: { qi_name: frm.doc.name },
        callback: function(r) {
            if (!r.message) return;
            apply_batch_coa_rule(frm, r.message.internal_exists, r.message.external_exists);
            toggle_external_billed_received(frm);
        }
    });
}
function toggle_external_billed_received(frm) {
    if (frm.doc.custom_coa) {
        frm.set_df_property("custom_coa_externalbilledreceived", "hidden", 0);
    } else {
        frm.set_df_property("custom_coa_externalbilledreceived", "hidden", 1);
    }
}
frappe.ui.form.on("Quality Inspection", {
    onload: function(frm) {
        // Disable Add Row button for the child table
        frm.fields_dict["custom_external_nrgp_test_results"].grid.cannot_add_rows = true;
    },
    refresh: function(frm) {
        // Only fetch once per form open
        if (!frm.__stock_entries_fetched && !frm.doc.__islocal) {
            frm.__stock_entries_fetched = true;

            frappe.call({
                method: "dt_brightlifecare_customization.public.py.quality_inspection.get_external_qc_stock_entries",
                args: { qi_name: frm.doc.name },
                callback: function(r) {
                    if (r.message && r.message.length) {
                        frm.clear_table("custom_external_nrgp_test_results");

                        r.message.forEach(function(se) {
                            let row = frm.add_child("custom_external_nrgp_test_results");
                            row.stock_entry = se.name;
                            row.stock_entry_type = se.stock_entry_type;
                        });

                        frm.refresh_field("custom_external_nrgp_test_results");

                    }
                }
            });
        }
    }
});



