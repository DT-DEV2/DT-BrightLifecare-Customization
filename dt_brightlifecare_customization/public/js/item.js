frappe.ui.form.on('Item', {
    onload: function(frm) {
        
        frm.get_field('supplier_items').grid.cannot_add_rows = true;
}
})