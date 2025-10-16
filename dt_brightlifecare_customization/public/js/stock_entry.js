frappe.ui.form.on('Stock Entry', {
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


frappe.ui.form.on('Stock Entry', {
   refresh: function(frm) {
       if(frm.doc.stock_entry_type === "Material Transfer for Manufacture") {
           frm.add_custom_button(__('Print Dispensing Slips'), function() {
               frappe.call({
                   method: "dt_brightlifecare_customization.public.py.stock_entry.print_dispensing_slips_preview",
                   args: { docname: frm.doc.name },
                   callback: function(r) {
                       if(r.message){
                           let w = window.open('', '_blank');
                           w.document.write(`
                               <html>
                                   <head>
                                       <title>Dispensing Slips - ${frm.doc.name}</title>
                                       <style>
                                           @media print {
                                               .page-break { page-break-after: always; }
                                           }
                                       </style>
                                   </head>
                                   <body>
                                       ${r.message}
                                   </body>
                               </html>
                           `);
                           w.document.close();
                       }
                   }
               });
           });
       }
   }
});
