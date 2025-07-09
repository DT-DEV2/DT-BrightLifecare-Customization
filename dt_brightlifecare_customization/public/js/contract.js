frappe.ui.form.on('Contract', {
    party_name(frm) {
        // Clear the party_user field when party_name changes
        frm.set_value('party_user', null);

        if (frm.doc.party_type === "Supplier" && frm.doc.party_name) {
            console.log("test1")
            frappe.db.get_doc('Supplier', frm.doc.party_name)
                .then(supplier => {
                    let nda_required = false;
                    console.log("test2")
                    if (supplier.custom_supplier_category && supplier.custom_supplier_category.length) {
                        supplier.custom_supplier_category.forEach(row => {
                            if (row.nda_sign_required) {
                                nda_required = true;
                            }
                        });
                    }
                    console.log("test3")
                    frm.set_df_property(
                        "custom_nda_sign_by_supplier",
                        "hidden",
                        !nda_required
                    );
                    frm.set_df_property(
                        "custom_nda_sign_by_healthkart",
                        "hidden",
                        !nda_required
                    );
                });
        } else {
            // If party_type is not Supplier, always hide the field
            frm.set_df_property("custom_nda_sign_by_supplier", "hidden", 1);
            frm.set_df_property("custom_nda_sign_by_healthkart", "hidden", 1);
        }
    },

    onload(frm) {
        frm.set_query('party_user', () => {
            if (frm.doc.party_type !== "Supplier" || !frm.doc.party_name) {
                return {};  // Disable query if not Supplier
            }

            return {
                query: 'dt_brightlifecare_customization.public.py.contract.get_connected_users',
                filters: {
                    party_name: frm.doc.party_name,
                    party_type: frm.doc.party_type
                }
            };
        });
    },



    custom_supplier_approval: function(frm) {
        if (frm.doc.custom_supplier_approval) {
            // Set the current user's name in the custom_user field
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'User',
                    name: frappe.session.user
                },
                callback: function(response) {
                    if (response.message) {
                        frm.set_value('custom_supplier_approver', response.message.name);
                    }
                }
            });
        } else {
            // Optionally clear the field if unchecked
            frm.set_value('custom_supplier_approver', '');
        }
    },

    custom_healthkart_approval: function(frm){
        if (frm.doc.custom_healthkart_approval) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: "User",
                    name: frappe.session.user
                },
                callback: function(response) {
                    if (response.message) {
                        frm.set_value('custom_healthkart_approver', response.message.name);
                    }
                }
            });
        }else{
            frm.set_value('custom_healthkart_approver', "")
        }
    },


    custom_nda_sign_by_supplier: function(frm) {
        if (frm.doc.custom_nda_sign_by_supplier) {
            // Set the current user's name in the custom_user field
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'User',
                    name: frappe.session.user
                },
                callback: function(response) {
                    if (response.message) {
                        frm.set_value('custom_nda_sign_by_supplier_approver', response.message.name);
                    }
                }
            });
        } else {
            // Optionally clear the field if unchecked
            frm.set_value('custom_nda_sign_by_supplier_approver', '');
        }
    },


    custom_nda_sign_by_healthkart: function(frm){
        if (frm.doc.custom_nda_sign_by_healthkart) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: "User",
                    name: frappe.session.user
                },
                callback: function(response) {
                    if (response.message) {
                        frm.set_value('custom_nda_sign_by_healthkart_approver', response.message.name);
                    }
                }
            });
        }else{
            frm.set_value('custom_nda_sign_by_healthkart_approver', "")
        }
    },



    // to make the field readonly after saved so that none can change it again
    refresh(frm) {
        if (frm.is_new() || frm.doc.custom_supplier_approval == 1 || (frm.doc.party_user && frm.doc.party_user !== frappe.session.user)) {
            frm.set_df_property('custom_supplier_approval', 'read_only', 1);
        }
        if (frm.doc.custom_healthkart_approval == 1) {
            frm.set_df_property('custom_healthkart_approval', 'read_only', 1);
        }

        if (frm.doc.docstatus == 0) {
            if (frm.doc.party_type === "Supplier" && frm.doc.party_name) {
                frappe.db.get_doc('Supplier', frm.doc.party_name)
                    .then(supplier => {
                        let nda_required = false;

                        if (supplier.custom_supplier_category && supplier.custom_supplier_category.length) {
                            supplier.custom_supplier_category.forEach(row => {
                                if (row.nda_sign_required) {
                                    nda_required = true;
                                }
                            });
                        }

                        frm.set_df_property("custom_nda_sign_by_supplier", "hidden", !nda_required);
                        frm.set_df_property("custom_nda_sign_by_healthkart", "hidden", !nda_required);
                    });
            } else {
                frm.set_df_property("custom_nda_sign_by_supplier", "hidden", 1);
                frm.set_df_property("custom_nda_sign_by_healthkart", "hidden", 1);
            }
        }
    }


    
});
