frappe.ui.form.on("Quality Inspection", {
   refresh: function(frm) {
       if (frm.doc.docstatus === 0 &&
           (frm.doc.reference_type === "Purchase Receipt" || frm.doc.reference_type === "Delivery Note")) {

           // Internal Transfer button
           frm.add_custom_button("Internal Transfer", function() {
               frappe.call({
                   method: "dt_brightlifecare_customization.public.py.quality_inspection.make_internal_transfer",
                   args: { qi_name: frm.doc.name },
                   callback: function(r) {
                       if (r.message) {
                           frappe.msgprint(__("Created Stock Entry: {0}", [r.message.stock_entries.join(", ")]));
                       }
                   }
               });
           });

           // Internal + External Transfer button
           frm.add_custom_button("Internal + External Transfer", function() {
               frappe.call({
                   method: "dt_brightlifecare_customization.public.py.quality_inspection.make_internal_external_transfer",
                   args: { qi_name: frm.doc.name },
                   callback: function(r) {
                       if (r.message) {
                           frappe.msgprint(__("Created Stock Entries: {0}", [r.message.stock_entries.join(", ")]));
                       }
                   }
               });
           });
       }
   }
});

