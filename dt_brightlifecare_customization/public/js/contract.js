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
    }
});
