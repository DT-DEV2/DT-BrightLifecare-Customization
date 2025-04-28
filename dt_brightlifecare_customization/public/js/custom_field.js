frappe.ui.form.on('Custom Field', {
    refresh: function(frm) {
        if (frm.doc.is_system_generated == 0) {
            frm.add_custom_button(__('Update Ownership'), function() {
                frappe.call({
                    method: "dt_brightlifecare_customization.public.py.custom_field.update_ownership",
                    args: {
                        doctype: frm.doc.doctype,
                        docname: frm.doc.name,
                        new_owner: frappe.session.user
                    },
                    freeze: true,
                    async: true,
                    callback: function(r) {
                        if(r.message) {
                            frappe.msgprint(__(r.message));
                        }
                    }
                });
            });
        }
    }
});
