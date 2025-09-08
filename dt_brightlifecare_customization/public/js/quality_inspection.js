frappe.ui.form.on("Quality Inspection", {
    refresh: function (frm) {
        if (
            frm.doc.docstatus === 0 &&
            ["Purchase Receipt", "Delivery Note", "Stock Entry"].includes(frm.doc.reference_type)
        ) {
            frappe.call({
                method: "dt_brightlifecare_customization.public.py.quality_inspection.has_sample_stock_entry",
                args: { qi_name: frm.doc.name },
                callback: function (r) {
                    if (!r.exc) {
                        // Update field based on backend result
                        frappe.model.set_value(frm.doctype, frm.docname, "custom_sample_status", r.message.status);

                        if (!r.message.active) {
                            frm.add_custom_button("Collect Sample", function () {
                                frappe.call({
                                    method: "dt_brightlifecare_customization.public.py.quality_inspection.make_internal_transfer",
                                    args: { qi_name: frm.doc.name },
                                    callback: function (r) {
                                        frm.reload_doc();
                                    }
                                });
                            });
                        }
                    }
                }
            });
        }

        // 🔹 NRGP Button (only if Sample Collected)
        if (frm.doc.docstatus === 0 && frm.doc.custom_sample_status === "Sample Collected") {
            frm.add_custom_button(__("NRGP"), () => {
                // ------------------------
                // STEP 1: Choose NRGP Type
                // ------------------------
                let step1 = new frappe.ui.Dialog({
                    title: __("Choose NRGP Type"),
                    fields: [
                        {
                            fieldtype: "Select",
                            label: "NRGP Type",
                            fieldname: "nrgp_type",
                            options: ["Internal", "External"],
                            reqd: 1,
                        },
                    ],
                    primary_action_label: __("Next"),
                    primary_action(values) {
                        if (values.nrgp_type === "External") {
                            if (frm.doc.custom_external_nrgp_created) {
                                frappe.msgprint(__("External NRGP has already been created for this Quality Inspection."));
                                return;
                            }
                            frappe.call({
                                method: "dt_brightlifecare_customization.public.py.quality_inspection.make_external_nrgp",
                                args: { qi_name: frm.doc.name },
                                callback: function (r) {
                                    if (!r.exc) {
                                        frappe.msgprint("External NRGP created: " + r.message.stock_entries.join(", "));
                                        frm.reload_doc();
                                    }
                                },
                            });
                            step1.hide();
                        } else {
                            if (frm.doc.custom_internal_nrgp_created) {
                                frappe.msgprint(__("Internal NRGP has already been created for this Quality Inspection."));
                                return;
                            }
                            step1.hide();
                            open_step2();
                        }
                    },
                });

                // ------------------------
                // STEP 2: Target Warehouse
                // ------------------------
                function open_step2() {
                    let step2 = new frappe.ui.Dialog({
                        title: __("Select Target Warehouse"),
                        fields: [
                            {
                                fieldtype: "Link",
                                label: "Target Warehouse",
                                fieldname: "target_warehouse",
                                options: "Warehouse",
                                reqd: 1,
                            },
                        ],
                        primary_action_label: __("Create"),
                        primary_action(values) {
                            frappe.call({
                                method: "dt_brightlifecare_customization.public.py.quality_inspection.make_internal_nrgp",
                                args: {
                                    qi_name: frm.doc.name,
                                    target_warehouse: values.target_warehouse,
                                },
                                callback: function (r) {
                                    if (!r.exc) {
                                        frappe.msgprint("Internal NRGP created: " + r.message.stock_entries.join(", "));
                                        frm.reload_doc();
                                    }
                                },
                            });
                            step2.hide();
                        },
                    });

                    // ✅ Back button
                    step2.set_secondary_action_label(__("Back"));
                    step2.set_secondary_action(() => {
                        step2.hide();
                        step1.show();
                    });

                    step2.show();
                }

                step1.show();
            });
        }
    },
});
