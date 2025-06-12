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
    },
});