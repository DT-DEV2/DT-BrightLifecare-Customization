frappe.ui.form.on('Sales Order', {
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
    },

    onload: function(frm) {
        frm.set_query("set_warehouse", function() {
            return {
                "filters": {
                    "custom_company_address": frm.doc.company_address,
                    "is_group": 0
                }
            };
        });
	}
});