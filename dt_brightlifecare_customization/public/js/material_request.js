// frappe.ui.form.on('Material Request', {
//     refresh: function(frm) {
//         if (!frm.doc.__islocal && frm.doc.docstatus === 1) {
//             frm.add_custom_button("Create RFQs from Suppliers", () => {
//                 frappe.call({
//                     method: "dt_brightlifecare_customization.public.py.material_request.make_request_for_quotation",
//                     args: {
//                         source_name: frm.doc.name   // <-- must be source_name, not material_request_name
//                     },
//                     callback: function(r) {
//                         if (r.message && r.message.length) {
//                             r.message.forEach(link => {
//                                 frappe.msgprint(`RFQ <a href="/app/request-for-quotation/${link}" target="_blank">${link}</a> created.`);
//                             });
//                         } else {
//                             frappe.msgprint("No RFQs were created.");
//                         }
//                     }
//                 });
//             });
//         }
//     }
// });






frappe.ui.form.on('Material Request', {  // Replace with your doctype
    refresh(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.custom_suppliers?.length && frm.doc.material_request_type == "Purchase") {
            frm.add_custom_button("Create RFQs", () => {
                frappe.call({
                    method: "dt_brightlifecare_customization.public.py.material_request.create_rfq_from_suppliers",
                    args: { docname: frm.doc.name },
                    callback(r) {
                        if (r.message) {
                            frappe.msgprint("RFQs Created: " + r.message.join(", "));
                        }
                    }
                });
            });
        }
    }
});
