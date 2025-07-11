frappe.ui.form.on('Request for Quotation', {
    onload: function(frm) {
        frm.fields_dict.items.grid.get_field('custom_quality_inspection_template').get_query = function(doc, cdt, cdn) {
          let child = locals[cdt][cdn];
          return {
            filters: {
              custom_item_code: child.item_code
            }
          };
        };
    }
});





