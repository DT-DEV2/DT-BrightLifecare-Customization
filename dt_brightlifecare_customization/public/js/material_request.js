frappe.ui.form.on('Material Request', {
    refresh: function (frm) {
        if (frm.doc.docstatus === 1) {
            if(frm.doc.material_request_type == "Manufacture"){
                frm.page.add_inner_button(__('Create MRP'), function () {
                    frappe.call({
                        method: 'dt_brightlifecare_customization.mrp.custom.material_request.material_request.create_mrp',
                        args: { material_request: frm.doc.name, use_defaults: 0 ,company: frm.doc.company},
                        callback: function (r) {
                            if (r.message) {
                                let mrp_doc = frappe.model.sync([r.message])[0];
                                frappe.set_route('Form', mrp_doc.doctype, mrp_doc.name);
                            }
                        },
                        error: function (err) {
                            frappe.throw({
                                title: __("Some fields are missing in items"),
                                indicator: "red",
                                message: err.message,
                            });
                        }
                    });
                });
            }
        }

        if (frm.doc.docstatus === 1 && frm.doc.custom_suppliers?.length && frm.doc.material_request_type == "Purchase") {
            frm.add_custom_button("Create RFQs", () => {
                frappe.call({
                    method: "dt_brightlifecare_customization.public.py.material_request.create_rfq_from_suppliers",
                    args: { docname: frm.doc.name },
                    callback(r) {
                        if (r.message) {
                            frappe.msgprint("RFQs Created: " + r.message.join(", "));
                        }
                    }
                });
            });
        }

        frm.remove_custom_button('Request for Quotation', 'Create');


        // setTimeout(() => {
        //     frm.page.actions.find('[data-label="Request for Quotation"]').parent().parent().remove();
        // }, 100);
    }
});






frappe.ui.form.on('Material Request Item', {
    item_code: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];

        if (!row.item_code) {
            frappe.model.set_value(cdt, cdn, 'custom_linked_supplier', '[]');
            return;
        }

        frappe.db.get_doc('Item', row.item_code)
            .then(doc => {
                if (doc && doc.supplier_items && doc.supplier_items.length > 0) {
                    let suppliers = doc.supplier_items
                        .filter(s => s.supplier)
                        .map(s => s.supplier);

                    let supplier_json = JSON.stringify(suppliers, null, 2);

                    frappe.model.set_value(cdt, cdn, 'custom_linked_supplier', supplier_json);
                } else {
                    frappe.model.set_value(cdt, cdn, 'custom_linked_supplier', '[]');
                }
            })
            .catch(() => {
                frappe.model.set_value(cdt, cdn, 'custom_linked_supplier', '[]');
            });
    }
});


