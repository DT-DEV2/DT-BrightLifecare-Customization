// frappe.ui.form.on("Supplier Quotation", {
//     refresh: function(frm) {
//         if (frm.doc.docstatus === 1) {  // Ensure the document is submitted
//             frm.add_custom_button(__('Purchase Order'), function() {
//                 validate_supplier_quotation(frm);
//             }, __("Create"));
//         }
//     }
// });

// function validate_supplier_quotation(frm) {
//     frappe.call({
//         method: "frappe.client.get_list",
//         args: {
//             doctype: "Supplier Quotation",
//             filters: {
//                 request_for_quotation: frm.doc.request_for_quotation,
//                 docstatus: 1  // Only submitted quotations
//             },
//             fields: ["name", "total"]
//         },
//         callback: function(response) {
//             if (response.message) {
//                 let quotations = response.message;
//                 let current_total = frm.doc.total;
//                 let lower_exists = quotations.some(q => q.total < current_total);

//                 if (lower_exists) {
//                     frappe.prompt(
//                         [
//                             {
//                                 fieldname: "reason",
//                                 fieldtype: "Small Text",
//                                 label: "Reason for Choosing Higher Quotation",
//                                 reqd: 1
//                             }
//                         ],
//                         function(values) {
//                             proceed_with_po_creation(frm, values.reason);
//                         },
//                         __("Justification Required"),
//                         __("Submit")
//                     );
//                 } else {
//                     proceed_with_po_creation(frm);
//                 }
//             }
//         }
//     });
// }

// function proceed_with_po_creation(frm, reason = "") {
//     frappe.call({
//         method: "erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_purchase_order",
//         args: {
//             source_name: frm.doc.name
//         },
//         callback: function() {
//             if (reason) {
//                 frappe.msgprint(__("Purchase Order Created. Reason for higher quotation: " + reason));
//             } else {
//                 frappe.msgprint(__("Purchase Order Created."));
//             }
//         }
//     });
// }





// frappe.ui.form.on('Supplier Quotation', {
//     refresh: function(frm) {
//         frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
//             // Custom code for displaying a message when "Create" -> "Purchase Order" button is clicked
//             frm.page.add_action_icon('octicon octicon-info', function() {
//                 frappe.msgprint(__('This is your custom message!'));
//             });
//         }
//     }
// });

