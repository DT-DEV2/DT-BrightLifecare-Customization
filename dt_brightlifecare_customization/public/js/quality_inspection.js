// quality_inspection.js

frappe.ui.form.on("Quality Inspection", {
    refresh(frm) {
        // ✅ Button 1: Collect Sample (Draft + has reference)
        if (
            frm.doc.docstatus === 0 &&
            ["Purchase Receipt", "Delivery Note", "Stock Entry"].includes(frm.doc.reference_type)
        ) {
            frm.add_custom_button("Collect Sample", () => {
                frappe.call({
                    method: "dt_brightlifecare_customization.public.py.quality_inspection.make_internal_transfer",
                    args: { qi_name: frm.doc.name },
                    callback: function (r) {
                        if (r.message) {
                            frappe.msgprint(__("Created Stock Entry: {0}", [r.message.stock_entries.join(", ")]));
                            frm.reload_doc();
                        }
                    },
                });
            });
        }

        // ✅ Button 2: NRGP (Draft + Sample already collected)
        if (frm.doc.docstatus === 0 && frm.doc.custom_sample_status === "Sample Collected") {
            frm.add_custom_button(__("NRGP"), () => {
                // Step 1: choose type
                frappe.prompt(
                    [
                        {
                            fieldtype: "Select",
                            label: "NRGP Type",
                            fieldname: "nrgp_type",
                            options: ["Internal", "External"],
                            reqd: 1,
                        },
                    ],
                    (v) => {
                        if (v.nrgp_type === "External") {
                            // 🚫 Prevent duplicate External NRGP
                            if (frm.doc.custom_external_nrgp_created) {
                                frappe.msgprint(__("External NRGP has already been created for this Quality Inspection."));
                                return;
                            }
                            // External → direct call
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
                        } else {
                            // 🚫 Prevent duplicate Internal NRGP
                            if (frm.doc.custom_internal_nrgp_created) {
                                frappe.msgprint(__("Internal NRGP has already been created for this Quality Inspection."));
                                return;
                            }
                            // Internal → Step 2: ask for Target Warehouse
                            frappe.prompt(
                                [
                                    {
                                        fieldtype: "Link",
                                        label: "Target Warehouse",
                                        fieldname: "target_warehouse",
                                        options: "Warehouse",
                                        reqd: 1,
                                    },
                                ],
                                (data) => {
                                    frappe.call({
                                        method: "dt_brightlifecare_customization.public.py.quality_inspection.make_internal_nrgp",
                                        args: {
                                            qi_name: frm.doc.name,
                                            target_warehouse: data.target_warehouse,
                                        },
                                        callback: function (r) {
                                            if (!r.exc) {
                                                frappe.msgprint(
                                                    "Internal NRGP created: " + r.message.stock_entries.join(", ")
                                                );
                                                frm.reload_doc();
                                            }
                                        },
                                    });
                                },
                                __("Select Target Warehouse"),
                                __("Create")
                            );
                        }
                    },
                    __("Choose NRGP Type"),
                    __("Next")
                );
            });
        }
    },
});
