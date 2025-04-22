frappe.ui.form.on('Purchase Order', {
    before_workflow_action: (frm) => {
        if (frm.selected_workflow_action === "Send Back") {

            // Create and display a dialog box
            const sendbackDialog = new frappe.ui.Dialog({
                title: 'Send Back Purchase Order',
                fields: [
                    {
                        label: 'Reason for Send Back',
                        fieldname: 'reason',
                        fieldtype: 'Text',
                        reqd: 1 // Make this field mandatory
                    }
                ],
                primary_action_label: 'Submit',
                primary_action(values) {
                    if (!values.reason) {
                        frappe.msgprint(__('Please provide a reason for send back.'));
                        return;
                    }


                    // Call server-side method to update the rejection reason and status
                    frappe.call({
                        method: 'dt_brightlifecare_customization.public.py.purchase_order.send_back_po',
                        args: {
                            docname: frm.doc.name,
                            reason: values.reason
                        },
                        callback: function(response) {
                            if (!response.exc) {
                                frappe.msgprint(__('Purchase Order has been sendback for the following reason: {0}', [values.reason]));
                                // frm.reload_doc(); // Reload the form to reflect the changes
                            } else {
                                frappe.msgprint(__('An error occurred while sendback the Purchase Order.'));
                            }
                        }
                    });
                    // Hide the dialog
                    sendbackDialog.hide();
                }
            });
            sendbackDialog.show();
        }
    },



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


        // Ensure filters are applied on refresh or form load
        frm.fields_dict['items'].grid.get_field('item_tax_template').get_query = function(doc, cdt, cdn) {
            const company = frm.doc.company;
            return {
                filters: {
                    company: company || ''
                }
            };
        };


        // this code put the value of reject dialog box data in the custom field
        frm.page.wrapper.find('a:contains("Reject")').on('click', function (e) {
            e.preventDefault(); // Prevent the default action
            
            // Create and display a dialog box
            const rejectDialog = new frappe.ui.Dialog({
                title: 'Reject Purchase Order',
                fields: [
                    {
                        label: 'Reason for Rejection',
                        fieldname: 'reason',
                        fieldtype: 'Text',
                        reqd: 1 // Make this field mandatory
                    }
                ],
                primary_action_label: 'Submit',
                primary_action(values) {
                    if (!values.reason) {
                        frappe.msgprint(__('Please provide a reason for rejection.'));
                        return;
                    }

                    // Call server-side method to update the rejection reason and status
                    frappe.call({
                        method: 'dt_brightlifecare_customization.public.py.purchase_order.reject_purchase_order',
                        args: {
                            docname: frm.doc.name,
                            reason: values.reason
                        },
                        callback: function(response) {
                            if (!response.exc) {
                                frappe.msgprint(__('Purchase Order has been rejected for the following reason: {0}', [values.reason]));
                                frm.reload_doc(); // Reload the form to reflect the changes
                            } else {
                                frappe.msgprint(__('An error occurred while rejecting the Purchase Order.'));
                            }
                        }
                    });

                    // Hide the dialog
                    rejectDialog.hide();
                }
            });

            rejectDialog.show();
        });


        frm.page.wrapper.find('a:contains("Approve")').on('click', function (e) {
            e.preventDefault(); // Prevent the default action
            
            // Create and display a dialog box
            const approveDialog = new frappe.ui.Dialog({
                title: 'Approve Purchase Order',
                fields: [
                    {
                        label: 'Comment for Approval',
                        fieldname: 'reason',
                        fieldtype: 'Text',
                        reqd: 1 // Make this field mandatory
                    }
                ],
                primary_action_label: 'Submit',
                primary_action(values) {
                    if (!values.reason) {
                        frappe.msgprint(__('Please provide a comment for Approval.'));
                        return;
                    }

                    // Call server-side method to update the rejection reason and status
                    frappe.call({
                        method: 'dt_brightlifecare_customization.public.py.purchase_order.approve_po',
                        args: {
                            docname: frm.doc.name,
                            reason: values.reason
                        },
                        callback: function(response) {
                            if (!response.exc) {
                                frappe.msgprint(__('Purchase Order has been approved for the following reason: {0}', [values.reason]));
                                // frm.reload_doc(); // Reload the form to reflect the changes
                            } else {
                                frappe.msgprint(__('An error occurred while approving the Purchase Order.'));
                            }
                        }
                    });
                    // Hide the dialog
                    approveDialog.hide();
                }
            });

            approveDialog.show();
        });


    },

    company: function(frm) {
        // Reapply filters when the company changes
        frm.fields_dict['items'].grid.get_field('item_tax_template').get_query = function(doc, cdt, cdn) {
            const company = frm.doc.company;
            return {
                filters: {
                    company: company || ''
                }
            };
        };
    },

    onload: function(frm) {
        frm.set_query("set_warehouse", function() {
            return {
                "filters": {
                    "custom_company_address": frm.doc.billing_address,
                    "is_group": 0
                }
            };
        });
	}
});