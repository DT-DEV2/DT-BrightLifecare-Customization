frappe.ui.form.on('Purchase Order', {
    refresh: function(frm) {
        frm.fields_dict.items.grid.get_field('uom').get_query = function(doc, cdt, cdn) {
            const item_code = frappe.get_doc(cdt, cdn).item_code;
            return {
                query: 'dt_brightlifecare_customization.public.py.uom_filter.uom_filter_condition',
                filters: {
                    item_code: item_code
                }
            };
        };
    }
});
