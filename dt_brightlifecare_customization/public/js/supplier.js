frappe.ui.form.on('Supplier', {

    custom_coip_approval: function(frm) {
        if (frm.doc.custom_coip_approval === "Approve") {
            frm.set_value('custom_coip_remarks', 'Approved');
            // frm.set_df_property('custom_coip_remarks', 'read_only', 1);
        } else {
            frm.set_value('custom_coip_remarks', '');
            // frm.set_df_property('custom_coip_remarks', 'read_only', 0);
        }
    },

    custom_br_approval: function(frm) {
        if (frm.doc.custom_br_approval === "Approve") {
            frm.set_value('custom_br_remarks', 'Approved');
            // frm.set_df_property('custom_br_remarks', 'read_only', 1);
        } else {
            frm.set_value('custom_br_remarks', '');
            // frm.set_df_property('custom_br_remarks', 'read_only', 0);
        }
    },

    custom_moa__aoa_approval: function(frm) {
        if (frm.doc.custom_moa__aoa_approval === "Approve") {
            frm.set_value('custom_moa__aoa_remarks', 'Approved');
        } else {
            frm.set_value('custom_moa__aoa_remarks', '');
        }
    },

    custom_authorised_signatory_aadhar_card_approval: function(frm) {
        if (frm.doc.custom_authorised_signatory_aadhar_card_approval === "Approve") {
            frm.set_value('custom_authorised_signatory_aadhar_card_remarks', 'Approved');
        } else {
            frm.set_value('custom_authorised_signatory_aadhar_card_remarks', '');
        }
    },

    custom_authorised_signatory_pan_approval: function(frm) {
        if (frm.doc.custom_authorised_signatory_pan_approval === "Approve") {
            frm.set_value('custom_authorised_signatory_pan_remarks', 'Approved');
        } else {
            frm.set_value('custom_authorised_signatory_pan_remarks', '');
        }
    },

    custom_authorised_dealer_approval: function(frm) {
        if (frm.doc.custom_authorised_dealer_approval === "Approve") {
            frm.set_value('custom_authorised_dealer_remarks', 'Approved');
        } else {
            frm.set_value('custom_authorised_dealer_remarks', '');
        }
    },

    custom_fssai_approval: function(frm) {
        if (frm.doc.custom_fssai_approval === "Approve") {
            frm.set_value('custom_fssai_remarks', 'Approved');
        } else {
            frm.set_value('custom_fssai_remarks', '');
        }
    },

    custom_ayush_approval: function(frm) {
        if (frm.doc.custom_ayush_approval === "Approve") {
            frm.set_value('custom_ayush_remarks', 'Approved');
        } else {
            frm.set_value('custom_ayush_remarks', '');
        }
    },

    custom_gmp_approval: function(frm) {
        if (frm.doc.custom_gmp_approval === "Approve") {
            frm.set_value('custom_gmp_remarks', 'Approved');
        } else {
            frm.set_value('custom_gmp_remarks', '');
        }
    },

    custom_dcl_approval: function(frm) {
        if (frm.doc.custom_dcl_approval === "Approve") {
            frm.set_value('custom_dcl_remarks', 'Approved');
        } else {
            frm.set_value('custom_dcl_remarks', '');
        }
    },




    // onload_post_render: function(frm) {
    //     toggle_fssai_license_field(frm);

    //     // Safe to use .grid.on now
    //     if (frm.fields_dict.custom_type_of_product.grid) {
    //         frm.fields_dict.custom_type_of_product.grid.on('after_add', function () {
    //             toggle_fssai_license_field(frm);
    //         });

    //         frm.fields_dict.custom_type_of_product.grid.on('after_delete', function () {
    //             setTimeout(() => {
    //                 toggle_fssai_license_field(frm);
    //             }, 100); // Let deletion reflect first
    //         });
    //     }
    // },

    // refresh: function(frm) {
    //     toggle_fssai_license_field(frm);
    // },
    
    

    onload: function(frm) {
        toggle_fssai_license_field(frm);
        toggle_ayush_license_field(frm);
        toggle_dc_license_field(frm);
    },

    refresh: function(frm) {
        toggle_fssai_license_field(frm);
        toggle_ayush_license_field(frm);
        toggle_dc_license_field(frm);
    },

    
    

    // this works for a field for now
    // before_workflow_action: function(frm) {
    //     const workflow_action = frm.selected_workflow_action;

    //     if (workflow_action === 'Send for Approval' && frm.doc.supplier_type === 'Company') {
    //         const certificate = frm.doc.custom_certificate_of_incorporationpartnership;
    //         const attachment = frm.doc.custom_certificate_of_incorporationpartnership_attachment;

    //         // Check if certificate is missing
    //         if (!certificate && !attachment) {
    //             // If both are missing
    //             frappe.dom.unfreeze();
    //             frm.scroll_to_field('custom_certificate_of_incorporationpartnership');
    //             frm.focus_on_first_input('custom_certificate_of_incorporationpartnership');
    //             frappe.throw(__('Please fill in both Certificate of Incorporation/Partnership and its Attachment before sending for approval.'));
    //         } else if (!certificate) {
    //             // If only certificate is missing
    //             frappe.dom.unfreeze();
    //             frm.scroll_to_field('custom_certificate_of_incorporationpartnership');
    //             frm.focus_on_first_input('custom_certificate_of_incorporationpartnership');
    //             frappe.throw(__('Please fill in Certificate of Incorporation/Partnership before sending for approval.'));
    //         } else if (!attachment) {
    //             // If only attachment is missing
    //             frappe.dom.unfreeze();
    //             frm.scroll_to_field('custom_certificate_of_incorporationpartnership_attachment');
    //             frm.focus_on_first_input('custom_certificate_of_incorporationpartnership_attachment');
    //             frappe.throw(__('Please fill in the Attachment for the Certificate of Incorporation/Partnership before sending for approval.'));
    //         }
    //     }
    // }




    before_workflow_action: function(frm) {
        const workflow_action = frm.selected_workflow_action;

        if (workflow_action === 'Send for Approval' && frm.doc.supplier_type === 'Company') {
            // Define an array of fields to check
            const fieldsToCheck = [
                { field: 'custom_certificate_of_incorporationpartnership', message: __('<b>Mandatory field:</b><br>Certificate of Incorporation/Partnership Number') },
                { field: 'custom_certificate_of_incorporationpartnership_attachment', message: __('<b>Mandatory field:</b><br>COI/P Attachment') },
                { field: 'custom_board_resolution', message: __('<b>Mandatory field:</b><br>Board Resolution Number') },
                { field: 'custom_board_resolution_attachment', message: __('<b>Mandatory field:</b><br>Board Resolution Attachment') },
                { field: 'custom_memorandum_of_association_moa_attachment', message: __('<b>Mandatory field:</b><br>MOA & AOA Attachment') },
                { field: 'custom_authorised_signatory_name', message: __('<b>Mandatory field:</b><br>Authorised Signatory Name') },
                { field: 'custom_authorised_signatory_aadhar_card', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card') },
                { field: 'custom_authorised_signatory_aadhar_card_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card Attachment') },
                { field: 'custom_authorised_signatory_pan', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN') },
                { field: 'custom_authorised_signatory_pan_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN Attachment') },
                { field: 'custom_in_case_of_authorised_dealer', message: __('<b>Mandatory field:</b><br>Authorised Dealer') },
                { field: 'custom_authorised_dealer_attachment', message: __('<b>Mandatory field:</b><br>Authorised Dealer Attachment') },

            ];

            // Loop through the fields and check if they are filled
            for (let i = 0; i < fieldsToCheck.length; i++) {
                const field = fieldsToCheck[i];
                const value = frm.doc[field.field];

                if (!value) {
                    // Unfreeze and scroll to the missing field
                    frappe.dom.unfreeze();
                    frm.scroll_to_field(field.field);
                    frm.focus_on_first_input(field.field);
                    frappe.throw(field.message);  // Show error specific to the missing field
                }
            }


            // Check child table (assume child table is "custom_document_checklist" — adjust if different)
            if (frm.doc.custom_type_of_product && frm.doc.custom_type_of_product.length > 0) {
                frm.doc.custom_type_of_product.forEach((row, index) => {
                    if (row.fssai_license && !frm.doc.custom_fssai_licence_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_fssai_licence_number');
                        frm.focus_on_first_input('custom_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>FSSAI Licence Number'));
                    }
                    
                    if (row.ayush_license && !frm.doc.custom_ayush_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_ayush_license_number');
                        frm.focus_on_first_input('custom_ayush_license_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>AYUSH License Number'));
                    }

                    if (row.drugs_and_cosmetic_license && !frm.doc.custom_drugs__cosmetic_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_drugs__cosmetic_license_number');
                        frm.focus_on_first_input('custom_drugs__cosmetic_license_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Drugs & Cosmetic License Number'));
                    }
                });
            }
        }


        else if (workflow_action === 'Send for Approval' && frm.doc.supplier_type === 'Individual') {
            // Define an array of fields to check
            const fieldsToCheck = [
                { field: 'custom_board_resolution', message: __('<b>Mandatory field:</b><br>Board Resolution Number') },
                { field: 'custom_board_resolution_attachment', message: __('<b>Mandatory field:</b><br>Board Resolution Attachment') },
                { field: 'custom_authorised_signatory_name', message: __('<b>Mandatory field:</b><br>Authorised Signatory Name') },
                { field: 'custom_authorised_signatory_aadhar_card', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card') },
                { field: 'custom_authorised_signatory_aadhar_card_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card Attachment') },
                { field: 'custom_authorised_signatory_pan', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN') },
                { field: 'custom_authorised_signatory_pan_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN Attachment') },
                { field: 'custom_in_case_of_authorised_dealer', message: __('<b>Mandatory field:</b><br>Authorised Dealer') },
                { field: 'custom_authorised_dealer_attachment', message: __('<b>Mandatory field:</b><br>Authorised Dealer Attachment') },

            ];

            // Loop through the fields and check if they are filled
            for (let i = 0; i < fieldsToCheck.length; i++) {
                const field = fieldsToCheck[i];
                const value = frm.doc[field.field];

                if (!value) {
                    // Unfreeze and scroll to the missing field
                    frappe.dom.unfreeze();
                    frm.scroll_to_field(field.field);
                    frm.focus_on_first_input(field.field);
                    frappe.throw(field.message);  // Show error specific to the missing field
                }
            }


            // Check child table (assume child table is "custom_document_checklist" — adjust if different)
            if (frm.doc.custom_type_of_product && frm.doc.custom_type_of_product.length > 0) {
                frm.doc.custom_type_of_product.forEach((row, index) => {
                    if (row.fssai_license && !frm.doc.custom_fssai_licence_number) {
                        frappe.dom.unfreeze();

                        frm.scroll_to_field('custom_fssai_licence_number');
                        frm.focus_on_first_input('custom_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>FSSAI Licence Number'));
                    }
                    
                    if (row.ayush_license && !frm.doc.custom_ayush_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_ayush_license_number');
                        frm.focus_on_first_input('custom_ayush_license_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>AYUSH License Number'));
                    }

                    if (row.drugs_and_cosmetic_license && !frm.doc.custom_drugs__cosmetic_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_drugs__cosmetic_license_number');
                        frm.focus_on_first_input('custom_drugs__cosmetic_license_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Drugs & Cosmetic License Number'));
                    }
                });
            }
        }


        else if (workflow_action === 'Send for Approval' && frm.doc.supplier_type === 'LLP') {
            // Define an array of fields to check
            const fieldsToCheck = [
                { field: 'custom_certificate_of_incorporationpartnership', message: __('<b>Mandatory field:</b><br>Certificate of Incorporation/Partnership Number') },
                { field: 'custom_certificate_of_incorporationpartnership_attachment', message: __('<b>Mandatory field:</b><br>COI/P Attachment') },
                { field: 'custom_board_resolution', message: __('<b>Mandatory field:</b><br>Board Resolution Number') },
                { field: 'custom_board_resolution_attachment', message: __('<b>Mandatory field:</b><br>Board Resolution Attachment') },
                { field: 'custom_authorised_signatory_name', message: __('<b>Mandatory field:</b><br>Authorised Signatory Name') },
                { field: 'custom_authorised_signatory_aadhar_card', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card') },
                { field: 'custom_authorised_signatory_aadhar_card_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card Attachment') },
                { field: 'custom_authorised_signatory_pan', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN') },
                { field: 'custom_authorised_signatory_pan_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN Attachment') },
                { field: 'custom_in_case_of_authorised_dealer', message: __('<b>Mandatory field:</b><br>Authorised Dealer') },
                { field: 'custom_authorised_dealer_attachment', message: __('<b>Mandatory field:</b><br>Authorised Dealer Attachment') },
            ];

            // Loop through the fields and check if they are filled
            for (let i = 0; i < fieldsToCheck.length; i++) {
                const field = fieldsToCheck[i];
                const value = frm.doc[field.field];

                if (!value) {
                    // Unfreeze and scroll to the missing field
                    frappe.dom.unfreeze();
                    frm.scroll_to_field(field.field);
                    frm.focus_on_first_input(field.field);
                    frappe.throw(field.message);  // Show error specific to the missing field
                }
            }


            // Check child table (assume child table is "custom_document_checklist" — adjust if different)
            if (frm.doc.custom_type_of_product && frm.doc.custom_type_of_product.length > 0) {
                frm.doc.custom_type_of_product.forEach((row, index) => {
                    if (row.fssai_license && !frm.doc.custom_fssai_licence_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_fssai_licence_number');
                        frm.focus_on_first_input('custom_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>FSSAI Licence Number'));
                    }
                    
                    if (row.ayush_license && !frm.doc.custom_ayush_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_ayush_license_number');
                        frm.focus_on_first_input('custom_ayush_license_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>AYUSH License Number'));
                    }

                    if (row.drugs_and_cosmetic_license && !frm.doc.custom_drugs__cosmetic_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_drugs__cosmetic_license_number');
                        frm.focus_on_first_input('custom_drugs__cosmetic_license_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Drugs & Cosmetic License Number'));
                    }
                });
            }
        }


        else if (workflow_action === 'Send for Approval' && frm.doc.supplier_type === 'Partnership') {
            // Define an array of fields to check
            const fieldsToCheck = [
                { field: 'custom_certificate_of_incorporationpartnership', message: __('<b>Mandatory field:</b><br>Certificate of Incorporation/Partnership Number') },
                { field: 'custom_certificate_of_incorporationpartnership_attachment', message: __('<b>Mandatory field:</b><br>COI/P Attachment') },
                { field: 'custom_board_resolution', message: __('<b>Mandatory field:</b><br>Board Resolution Number') },
                { field: 'custom_board_resolution_attachment', message: __('<b>Mandatory field:</b><br>Board Resolution Attachment') },
                { field: 'custom_authorised_signatory_name', message: __('<b>Mandatory field:</b><br>Authorised Signatory Name') },
                { field: 'custom_authorised_signatory_aadhar_card', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card') },
                { field: 'custom_authorised_signatory_aadhar_card_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card Attachment') },
                { field: 'custom_authorised_signatory_pan', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN') },
                { field: 'custom_authorised_signatory_pan_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN Attachment') },
                { field: 'custom_in_case_of_authorised_dealer', message: __('<b>Mandatory field:</b><br>Authorised Dealer') },
                { field: 'custom_authorised_dealer_attachment', message: __('<b>Mandatory field:</b><br>Authorised Dealer Attachment') },

            ];

            // Loop through the fields and check if they are filled
            for (let i = 0; i < fieldsToCheck.length; i++) {
                const field = fieldsToCheck[i];
                const value = frm.doc[field.field];

                if (!value) {
                    // Unfreeze and scroll to the missing field
                    frappe.dom.unfreeze();
                    frm.scroll_to_field(field.field);
                    frm.focus_on_first_input(field.field);
                    frappe.throw(field.message);  // Show error specific to the missing field
                }
            }

            // Check child table (assume child table is "custom_document_checklist" — adjust if different)
            if (frm.doc.custom_type_of_product && frm.doc.custom_type_of_product.length > 0) {
                frm.doc.custom_type_of_product.forEach((row, index) => {
                    if (row.fssai_license && !frm.doc.custom_fssai_licence_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_fssai_licence_number');
                        frm.focus_on_first_input('custom_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>FSSAI Licence Number'));
                    }
                    
                    if (row.ayush_license && !frm.doc.custom_ayush_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_ayush_license_number');
                        frm.focus_on_first_input('custom_ayush_license_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>AYUSH License Number'));
                    }

                    if (row.drugs_and_cosmetic_license && !frm.doc.custom_drugs__cosmetic_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_drugs__cosmetic_license_number');
                        frm.focus_on_first_input('custom_drugs__cosmetic_license_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Drugs & Cosmetic License Number'));
                    }
                });
            }
        }

    }
    
    
});







// frappe.ui.form.on('Type Of Product Detail', {
//     fssai_license: function(frm, cdt, cdn) {
//         // Run check every time fssai_license is changed in any row
//         toggle_fssai_license_field(frm);
//     }
// });


// function toggle_fssai_license_field(frm) {
//     const rows = frm.doc.custom_type_of_product || [];
//     const any_checked = rows.some(row => row.fssai_license === 1);

//     frm.toggle_display('custom_fssai_licence_number', any_checked);
// }




// Hook into child table row events
frappe.ui.form.on('Type Of Product Detail', {
    fssai_license: function(frm, cdt, cdn) {
        toggle_fssai_license_field(frm);
    },

    ayush_license: function(frm, cdt, cdn) {
        toggle_ayush_license_field(frm)
    },

    drugs_and_cosmetic_license: function(frm, cdt, cdn) {
        toggle_dc_license_field(frm)
    },

    custom_type_of_product_remove: function(frm) {
        toggle_fssai_license_field(frm);
        toggle_ayush_license_field(frm);
        toggle_dc_license_field(frm);
    },

    // Optional: run after any row is added
    custom_type_of_product_add: function(frm) {
        toggle_fssai_license_field(frm);
        toggle_ayush_license_field(frm);
        toggle_dc_license_field(frm);
    }
});

function toggle_fssai_license_field(frm) {
    const rows = frm.doc.custom_type_of_product || [];
    const any_checked = rows.some(row => row.fssai_license === 1);
    frm.toggle_display('custom_fssai_licence_number', any_checked);
}

function toggle_ayush_license_field(frm) {
    const rows = frm.doc.custom_type_of_product || [];
    const any_checked = rows.some(row => row.ayush_license === 1);
    frm.toggle_display('custom_ayush_license_number', any_checked);
}

function toggle_dc_license_field(frm) {
    const rows = frm.doc.custom_type_of_product || [];
    const any_checked = rows.some(row => row.drugs_and_cosmetic_license === 1);
    frm.toggle_display('custom_drugs__cosmetic_license_number', any_checked);
}