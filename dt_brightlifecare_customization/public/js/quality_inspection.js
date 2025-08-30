frappe.ui.form.on("Quality Inspection", {
    refresh: function(frm) {
        if (
            frm.doc.docstatus === 0 &&
            (frm.doc.reference_type === "Purchase Receipt" || frm.doc.reference_type === "Delivery Note")
        ) {
            // Always show Collect Sample Approval button
            frm.add_custom_button("Collect Sample Approval", function() {
                frappe.call({
                    method: "dt_brightlifecare_customization.public.py.quality_inspection.make_internal_transfer",
                    args: { qi_name: frm.doc.name },
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(__("Created Stock Entry: {0}", [r.message.stock_entries.join(", ")]));
                            frm.reload_doc(); // reload to update custom_mt_target_warehouse
                        }
                    }
                });
            });

            // Show External NRGP button only if MT Target Warehouse already exists
            if (frm.doc.custom_mt_target_warehouse) {
                frm.add_custom_button("External NRGP", function() {
                    frappe.call({
                        method: "dt_brightlifecare_customization.public.py.quality_inspection.make_external_nrgp",
                        args: { qi_name: frm.doc.name },
                        callback: function(r2) {
                            if (r2.message) {
                                frappe.msgprint(__("Created Stock Entry: {0}", [r2.message.stock_entries.join(", ")]));
                                frm.reload_doc(); // keep data in sync
                            }
                        }
                    });
                });
            }
        }
    }
});
