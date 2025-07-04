frappe.ui.form.on('Item', {
    // visibility of listing id based on itme grp
    item_group: function(frm) {
        if (frm.doc.item_group) {
            frappe.db.get_value("Item Group", frm.doc.item_group, "custom_listing_id_visibility")
                .then(r => {
                    let visibility = r.message.custom_listing_id_visibility;
                    frm.toggle_display("custom_listing_id", visibility);
                })
        }else {
            frm.toggle_display("custom_listing_id", false);
        }
    },


    onload: function(frm) {
        frm.get_field('supplier_items').grid.cannot_add_rows = true;

        if (frm.doc.item_group) {
            frappe.db.get_value('Item Group', frm.doc.item_group, 'custom_listing_id_visibility')
                .then(r => {
                    let visibility = r.message.custom_listing_id_visibility;
                    frm.toggle_display('custom_listing_id', visibility);
                });
        } else {
            frm.toggle_display('custom_listing_id', false);
        }
    },

    custom_listing_id: function(frm) {
        if (frm.doc.custom_listing_id) {
            frappe.call({
                method: 'dt_brightlifecare_customization.public.py.item.get_next_item_code_for_listing',
                args: {
                    listing_id: frm.doc.custom_listing_id
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('item_code', r.message);
                    }
                }
            });
        }
    }
})