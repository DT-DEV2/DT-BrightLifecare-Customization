// frappe.ui.form.on('Request for Quotation', {
//     refresh(frm) {
//         frm.fields_dict.items.grid.get_field('item_code').get_query = function(doc) {
//             let filters = { 'disabled': 0 , "is_purchase_item" : 1};
            
//             if (doc.suppliers && doc.suppliers.length > 0) {
//                 let supplier_names = doc.suppliers.map(row => row.supplier);
//                 filters['supplier'] = ['in', supplier_names];
//             }
            
//             return { filters: filters };
//         };
//     }
// });





