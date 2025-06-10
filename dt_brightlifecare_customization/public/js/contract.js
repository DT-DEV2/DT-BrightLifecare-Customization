frappe.ui.form.on('Contract', {
    party_name(frm) {
        // Clear the party_user field when party_name changes
        frm.set_value('party_user', null);
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


    // to make the field readonly after saved so that none can change it again
    refresh(frm) {
        if (frm.doc.custom_supplier_approval == 1) {
            frm.set_df_property('custom_supplier_approval', 'read_only', 1);
        }
        if (frm.doc.custom_healthkart_approval == 1) {
            frm.set_df_property('custom_healthkart_approval', 'read_only', 1);
        }
    }


    
});
