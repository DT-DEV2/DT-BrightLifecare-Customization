// this code hides the standard button and displays the new po button
// frappe.ui.form.on('Supplier Quotation', {
//     refresh: function(frm) {
//         if (frm.doc.docstatus === 1) {
//             frm.add_custom_button(__('PO'), function() {
//                 frappe.model.open_mapped_doc({
//                     method: "erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_purchase_order",
//                     frm: frm
//                 });
//             }, __("Create"));

//             frm.page.set_inner_btn_group_as_primary(__("Create"));

//             setTimeout(function() {
//                 frm.remove_custom_button("Purchase Order", "Create");
//                 // Add your custom button here
//             }, 300);
//         }
//     }
// });





// this code displays a dialog box for making PO
// frappe.ui.form.on('Supplier Quotation', {
//     refresh: function(frm) {
//         if (frm.doc.docstatus === 1) {
//             // Remove the standard Purchase Order button
//             setTimeout(() => frm.remove_custom_button("Purchase Order", "Create"), 300);

//             // Add custom PO button with a reason input dialog
//             frm.add_custom_button(__('PO'), function() {
//                 // Create a dialog box
//                 const dialog = new frappe.ui.Dialog({
//                     title: __("Create Purchase Order"),
//                     fields: [
//                         {
//                             label: __("Reason for PO Creation"),
//                             fieldname: "reason",
//                             fieldtype: "Text",
//                             reqd: 1, // Mandatory field
//                             placeholder: __("E.g., Urgent requirement, Supplier agreement...")
//                         }
//                     ],
//                     primary_action_label: __("Proceed"),
//                     primary_action(values) {
//                         if (!values.reason) {
//                             frappe.throw(__("Reason is required to proceed."));
//                             return;
//                         }
                        
//                         // Close the dialog
//                         dialog.hide();
                        
//                         // Show a loading indicator
//                         frappe.dom.freeze(__("Creating Purchase Order..."));

//                         // Proceed with PO creation
//                         frappe.model.open_mapped_doc({
//                             method: "erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_purchase_order",
//                             frm: frm
//                         }).then(() => {
//                             frappe.dom.unfreeze();
//                             frappe.show_alert({
//                                 message: __("Purchase Order created successfully!"),
//                                 indicator: "green"
//                             });
                            
//                             // Optionally, log the reason in the server
//                             frappe.call({
//                                 method: "frappe.client.set_value",
//                                 args: {
//                                     doctype: "Supplier Quotation",
//                                     name: frm.doc.name,
//                                     fieldname: "custom_po_reason", // Ensure this custom field exists
//                                     value: values.reason
//                                 }
//                             });
//                         });
//                     }
//                 });

//                 dialog.show();
//             }, __("Create"));

//             frm.page.set_inner_btn_group_as_primary(__("Create"));
//         }
//     }
// });











frappe.ui.form.on('Supplier Quotation', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 1) {
            // Remove standard PO button
            setTimeout(() => frm.remove_custom_button("Purchase Order", "Create"), 300);

            // Add custom PO button
            frm.add_custom_button(__('Purchase order'), async function() {
                const shouldShowPopup = await checkIfCheaperSQExists(frm);
                if (shouldShowPopup) showReasonDialog(frm);
                else {
                    // Automatically set reason if this is the lowest quotation
                    await frappe.call({
                        method: "frappe.client.set_value",
                        args: {
                            doctype: "Supplier Quotation",
                            name: frm.doc.name,
                            fieldname: "custom_reason_for_selection",
                            value: "L1 Quotation Selected"
                        }
                    });
                    createPurchaseOrder(frm);
                }
            }, __("Create"));
        }
    }
});

// Check if cheaper SQ exists for the same RFQ
async function checkIfCheaperSQExists(frm) {
    // Get unique RFQs linked to this SQ
    const rfqList = [...new Set(
        frm.doc.items
            .filter(item => item.request_for_quotation)
            .map(item => item.request_for_quotation)
    )];

    if (rfqList.length === 0) return false;

    // Fetch all SQs linked to these RFQs
    const { message: sqList } = await frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Supplier Quotation",
            filters: [
                ["Supplier Quotation Item", "request_for_quotation", "in", rfqList],
                ["name", "!=", frm.doc.name],
                ["docstatus", "=", 1]
            ],
            fields: ["name", "grand_total"],
            distinct: true
        }
    });

    // Check if any SQ has a lower total
    return sqList.some(sq => sq.grand_total < frm.doc.grand_total);
}

// Show reason dialog (same as before)
function showReasonDialog(frm) {
    const dialog = new frappe.ui.Dialog({
        title: __("Justification Required"),
        fields: [{
            label: __("Reason for choosing this Supplier Quotation?"),
            fieldname: "reason",
            fieldtype: "Text",
            reqd: 1
        }],
        primary_action: values => {
            if (!values.reason) frappe.throw(__("Reason is required"));
            dialog.hide();
            createPurchaseOrder(frm, values.reason);
        }
    });
    dialog.show();
}

// Create PO (same as before)
function createPurchaseOrder(frm, reason = null) {
    frappe.dom.freeze(__("Creating PO..."));
    frappe.model.open_mapped_doc({
        method: "erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_purchase_order",
        frm: frm
    }).then(() => {
        frappe.dom.unfreeze();
        if (reason) {
            frappe.call({
                method: "frappe.client.set_value",
                args: {
                    doctype: "Supplier Quotation",
                    name: frm.doc.name,
                    fieldname: "custom_reason_for_selection",
                    value: reason
                }
            });
        }
    });
}