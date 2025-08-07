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

    custom_relabeller_fssai_approval: function(frm) {
        if (frm.doc.custom_relabeller_fssai_approval === "Approve") {
            frm.set_value('custom_relabeller_fssai_remarks', 'Approved');
        } else {
            frm.set_value('custom_relabeller_fssai_remarks', '');
        }
    },

    custom_oem_fssai_approval: function(frm) {
        if (frm.doc.custom_oem_fssai_approval === "Approve") {
            frm.set_value('custom_oem_fssai_remarks', 'Approved');
        } else {
            frm.set_value('custom_oem_fssai_remarks', '');
        }
    },

    custom_distributer_fssai_approval: function(frm) {
        if (frm.doc.custom_distributer_fssai_approval === "Approve") {
            frm.set_value('custom_distributer_fssai_remarks', 'Approved');
        } else {
            frm.set_value('custom_distributer_fssai_remarks', '');
        }
    },

    custom_importer_fssai_approval: function(frm) {
        if (frm.doc.custom_importer_fssai_approval === "Approve") {
            frm.set_value('custom_importer_fssai_remarks', 'Approved');
        } else {
            frm.set_value('custom_importer_fssai_remarks', '');
        }
    },

    custom_trader_fssai_approval: function(frm) {
        if (frm.doc.custom_trader_fssai_approval === "Approve") {
            frm.set_value('custom_trader_fssai_remarks', 'Approved');
        } else {
            frm.set_value('custom_trader_fssai_remarks', '');
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

    
    

    onload: function(frm) {
        toggle_fssai_license_field(frm);
        toggle_ayush_license_field(frm);
        toggle_dc_license_field(frm);
        toggle_relabeller_license_field(frm);
        toggle_distributer_license_field(frm);
        toggle_importer_license_field(frm);
        toggle_trader_license_field(frm);
        toggle_oem_license_field(frm);
    },

    refresh: function(frm) {
        const fields_to_color = [
            'custom_coip_approval',
            'custom_br_approval',
            'custom_moa__aoa_approval',
            'custom_authorised_signatory_aadhar_card_approval',
            'custom_authorised_signatory_pan_approval',
            'custom_authorised_dealer_approval',
            'custom_gmp_approval',
            'custom_fssai_approval',
            'custom_relabeller_fssai_approval',
            'custom_oem_fssai_approval',
            'custom_distributer_fssai_approval',
            'custom_importer_fssai_approval',
            'custom_trader_fssai_approval',
            'custom_ayush_approval',
            'custom_dcl_approval'
        ];

        setTimeout(() => {
            fields_to_color.forEach(fieldname => {
                if (frm.fields_dict[fieldname]) {
                    frm.fields_dict[fieldname].$wrapper
                        .closest('.frappe-control')
                        .find('label')
                        .css({
                            'color': 'orange',
                            'font-weight': 'bold'
                        });
                }
            });
        }, 100);

        // $("label[for='custom_coip_approval']").css("color", "orange");
        frm.remove_custom_button('Get Supplier Group Details', 'Actions');
        frm.remove_custom_button('Link with Customer', 'Actions');

        
        toggle_fssai_license_field(frm);
        toggle_ayush_license_field(frm);
        toggle_dc_license_field(frm);
        toggle_relabeller_license_field(frm);
        toggle_distributer_license_field(frm);
        toggle_importer_license_field(frm);
        toggle_trader_license_field(frm);
        toggle_oem_license_field(frm);


        toggle_custom_type_of_product(frm);




        frappe.call({
            method: 'dt_brightlifecare_customization.public.py.supplier.has_supplier_visibility_role',
            callback: function(r) {
                if (r.message) {
                    // Hide Accounting Ledger button if user has restricted role
                    frm.remove_custom_button('Accounting Ledger', 'View');
                    frm.remove_custom_button('Accounts Payable', 'View');
                    // frm.remove_custom_button('Help', 'Actions');
                    setTimeout(() => {
                        frm.page.actions.find('[data-label="Help"]').parent().parent().remove();
                    }, 100);
                }
            }
        });





        // frappe.call({
        //     method: 'dt_brightlifecare_customization.public.py.supplier.has_supplier_visibility_role',
        //     callback: function(response) {
        //         if (!response.message) {
        //             // User does NOT have the role with supplier_visibility = 1
        //             frm.add_custom_button(__('Contract'), function() {
        //                 frappe.model.with_doctype('Contract', function() {
        //                     var contract = frappe.model.get_new_doc('Contract');
                            
        //                     // Set basic fields
        //                     contract.party_type = 'Supplier';
        //                     contract.party_name = frm.doc.name;
                            
        //                     // Add terms if they exist
        //                     if(frm.doc.custom_fssai_contract_term) {
        //                         var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
        //                         frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_fssai_contract_term);
        //                         // Set other child fields
        //                     }
                            
        //                     if(frm.doc.custom_relabeller_fssai_contract_term) {
        //                         var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
        //                         frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_relabeller_fssai_contract_term);
        //                         // Set other child fields
        //                     }

        //                     if(frm.doc.custom_oem_fssai_contract_term) {
        //                         var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
        //                         frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_oem_fssai_contract_term);
        //                         // Set other child fields
        //                     }


        //                     if(frm.doc.custom_distributer_fssai_contract_term) {
        //                         var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
        //                         frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_distributer_fssai_contract_term);
        //                         // Set other child fields
        //                     }

        //                     if(frm.doc.custom_importer_fssai_contract_term) {
        //                         var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
        //                         frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_importer_fssai_contract_term);
        //                         // Set other child fields
        //                     }

        //                     if(frm.doc.custom_trader_fssai_contract_term) {
        //                         var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
        //                         frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_trader_fssai_contract_term);
        //                         // Set other child fields
        //                     }

        //                     if(frm.doc.custom_ayush_contract_term) {
        //                         var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
        //                         frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_ayush_contract_term);
        //                         // Set other child fields
        //                     }

        //                     if(frm.doc.custom_dcl_contract_term) {
        //                         var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
        //                         frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_dcl_contract_term);
        //                         // Set other child fields
        //                     }
                            
        //                     // Open in edit mode
        //                     frappe.set_route('Form', 'Contract', contract.name);
        //                 });
        //             }, __('Create'));
        //         }
        //     }
        // });



        frappe.call({
            method: 'dt_brightlifecare_customization.public.py.supplier.has_supplier_visibility_role',
            callback: function(response) {
                if (!response.message) {

                    let is_contract_applicable = false;
                    if (frm.doc.custom_supplier_category && frm.doc.custom_supplier_category.length){
                        frm.doc.custom_supplier_category.forEach (row => {
                            if (row.contract_applicable){
                                is_contract_applicable = true
                            }
                        });
                    }
                    if (is_contract_applicable){
                        // User does NOT have the role with supplier_visibility = 1
                        frm.add_custom_button(__('Contract'), function() {
                            frappe.model.with_doctype('Contract', function() {
                                var contract = frappe.model.get_new_doc('Contract');
                                
                                // Set basic fields
                                contract.party_type = 'Supplier';
                                contract.party_name = frm.doc.name;
                                
                                // Add terms if they exist
                                if(frm.doc.custom_fssai_contract_term) {
                                    var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
                                    frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_fssai_contract_term);
                                    // Set other child fields
                                }
                                
                                if(frm.doc.custom_relabeller_fssai_contract_term) {
                                    var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
                                    frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_relabeller_fssai_contract_term);
                                    // Set other child fields
                                }

                                if(frm.doc.custom_oem_fssai_contract_term) {
                                    var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
                                    frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_oem_fssai_contract_term);
                                    // Set other child fields
                                }


                                if(frm.doc.custom_distributer_fssai_contract_term) {
                                    var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
                                    frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_distributer_fssai_contract_term);
                                    // Set other child fields
                                }

                                if(frm.doc.custom_importer_fssai_contract_term) {
                                    var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
                                    frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_importer_fssai_contract_term);
                                    // Set other child fields
                                }

                                if(frm.doc.custom_trader_fssai_contract_term) {
                                    var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
                                    frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_trader_fssai_contract_term);
                                    // Set other child fields
                                }

                                if(frm.doc.custom_ayush_contract_term) {
                                    var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
                                    frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_ayush_contract_term);
                                    // Set other child fields
                                }

                                if(frm.doc.custom_dcl_contract_term) {
                                    var child = frappe.model.add_child(contract, 'custom_contract_terms_and_template');
                                    frappe.model.set_value(child.doctype, child.name, 'contract_term', frm.doc.custom_dcl_contract_term);
                                    // Set other child fields
                                }
                                
                                // Open in edit mode
                                frappe.set_route('Form', 'Contract', contract.name);
                            });
                        }, __('Create'));
                    }
                }
            }
        });




        frappe.call({
            method: 'dt_brightlifecare_customization.public.py.supplier.has_supplier_visibility_role',
            callback: function(response) {
                if (!response.message) {

                    is_supp_item_linking = false;

                    if (frm.doc.custom_supplier_category && frm.doc.custom_supplier_category.length){
                        frm.doc.custom_supplier_category.forEach(row =>{
                            if (row.supplier_item_link_visibility){
                                is_supp_item_linking = true;
                            }
                        })
                    }
                    if (is_supp_item_linking){
                        // User does NOT have the role with supplier_visibility = 1
                        frm.add_custom_button(__('Supplier-Item Linking'), function() {
                            frappe.model.with_doctype('Supplier Item Link', function() {
                                var linking = frappe.model.get_new_doc('Supplier Item Link');
                                
                                // Set basic fields
                                linking.supplier = frm.doc.name;
                                
                                // Open in edit mode
                                frappe.set_route('Form', 'Supplier Item Link', linking.name);
                            });
                        }, __('Create'));
                    }
                }
            }
        });
        

        
        

    },

    custom_msme_declaration: function(frm) {
        // Get the single FSSAI Declaration document
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Download MSME Declaration',
                fieldname: 'declaration'
            },
            callback: function(response) {
                if (response.message && response.message.declaration) {
                    // Open the file URL in new tab to trigger download
                    window.open(response.message.declaration, '_blank');
                } else {
                    frappe.msgprint(__('No MSME Declaration file found'));
                }
            }
        });
    },

    custom_download_fssai_declaration: function(frm) {
        // Get the single FSSAI Declaration document
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Download FSSAI Declaration',
                fieldname: 'declaration'
            },
            callback: function(response) {
                if (response.message && response.message.declaration) {
                    // Open the file URL in new tab to trigger download
                    window.open(response.message.declaration, '_blank');
                } else {
                    frappe.msgprint(__('No FSSAI Declaration file found'));
                }
            }
        });
    },

    custom_download_ayush_declaration: function(frm) {
        // Get the single FSSAI Declaration document
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Download AYUSH Declaration',
                fieldname: 'declaration'
            },
            callback: function(response) {
                if (response.message && response.message.declaration) {
                    // Open the file URL in new tab to trigger download
                    window.open(response.message.declaration, '_blank');
                } else {
                    frappe.msgprint(__('No AYUSH Declaration file found'));
                }
            }
        });
    },

    custom_download_dcl_declaration: function(frm) {
        // Get the single FSSAI Declaration document
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Download DCL Declaration',
                fieldname: 'declaration'
            },
            callback: function(response) {
                if (response.message && response.message.declaration) {
                    // Open the file URL in new tab to trigger download
                    window.open(response.message.declaration, '_blank');
                } else {
                    frappe.msgprint(__('No DCL Declaration file found'));
                }
            }
        });
    },

    custom_download_relabeller_fssai_declaration: function(frm) {
        // Get the single FSSAI Declaration document
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Download Relabeller FSSAI Declaration',
                fieldname: 'declaration'
            },
            callback: function(response) {
                if (response.message && response.message.declaration) {
                    // Open the file URL in new tab to trigger download
                    window.open(response.message.declaration, '_blank');
                } else {
                    frappe.msgprint(__('No Relabeller FSSAI Declaration file found'));
                }
            }
        });
    },

    custom_download_distributer_fssai_declaration: function(frm) {
        // Get the single FSSAI Declaration document
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Download Distributer FSSAI Declaration',
                fieldname: 'declaration'
            },
            callback: function(response) {
                if (response.message && response.message.declaration) {
                    // Open the file URL in new tab to trigger download
                    window.open(response.message.declaration, '_blank');
                } else {
                    frappe.msgprint(__('No Distributer FSSAI Declaration file found'));
                }
            }
        });
    },

    custom_download_importer_fssai_declaration: function(frm) {
        // Get the single FSSAI Declaration document
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Download Importer FSSAI Declaration',
                fieldname: 'declaration'
            },
            callback: function(response) {
                if (response.message && response.message.declaration) {
                    // Open the file URL in new tab to trigger download
                    window.open(response.message.declaration, '_blank');
                } else {
                    frappe.msgprint(__('No Importer FSSAI Declaration file found'));
                }
            }
        });
    },

    custom_download_trader_fssai_declaration: function(frm) {
        // Get the single FSSAI Declaration document
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Download Trader FSSAI Declaration',
                fieldname: 'declaration'
            },
            callback: function(response) {
                if (response.message && response.message.declaration) {
                    // Open the file URL in new tab to trigger download
                    window.open(response.message.declaration, '_blank');
                } else {
                    frappe.msgprint(__('No Trader FSSAI Declaration file found'));
                }
            }
        });
    },


    custom_download_oem_fssai_declaration: function(frm) {
        // Get the single FSSAI Declaration document
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Download OEM FSSAI Declaration',
                fieldname: 'declaration'
            },
            callback: function(response) {
                if (response.message && response.message.declaration) {
                    // Open the file URL in new tab to trigger download
                    window.open(response.message.declaration, '_blank');
                } else {
                    frappe.msgprint(__('No OEM FSSAI Declaration file found'));
                }
            }
        });
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
            const isMarketplace = frm.doc.custom_is_marketplace_workflow;
            // Define an array of fields to check
            const fieldsToCheck = [
                { field: 'custom_certificate_of_incorporationpartnership', message: __('<b>Mandatory field:</b><br>Certificate of Incorporation/Partnership Number') },
                { field: 'custom_certificate_of_incorporationpartnership_attachment', message: __('<b>Mandatory field:</b><br>COI/P Attachment') },
                { field: 'custom_authorised_signatory_name', message: __('<b>Mandatory field:</b><br>Authorised Signatory Name') },
                { field: 'custom_authorised_signatory_aadhar_card', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card') },
                { field: 'custom_authorised_signatory_aadhar_card_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card Attachment') },
                { field: 'custom_authorised_signatory_pan', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN') },
                { field: 'custom_authorised_signatory_pan_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN Attachment') },
                { field: 'custom_in_case_of_authorised_dealer', message: __('<b>Mandatory field:</b><br>Authorised Dealer') },
                // { field: 'custom_authorised_dealer_attachment', message: __('<b>Mandatory field:</b><br>Authorised Dealer Attachment') },

            ];


            // Add extra fields only if marketplace workflow is ticked
            if (isMarketplace) {
                fieldsToCheck.push(
                    { field: 'custom_board_resolution', message: __('<b>Mandatory field:</b><br>Board Resolution Number') },
                    { field: 'custom_board_resolution_attachment', message: __('<b>Mandatory field:</b><br>Board Resolution Attachment') },
                    { field: 'custom_memorandum_of_association_moa_attachment', message: __('<b>Mandatory field:</b><br>MOA & AOA Attachment') }
                );
            }

            setTimeout(() => {
                fieldsToCheck.forEach(field => {
                    add_fake_asterisk(frm, field.field);
                });
            }, 300); 
            

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

                    if (row.relabeller_fssai_license && !frm.doc.custom_relabeller_fssai_licence_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_relabeller_fssai_licence_number');
                        frm.focus_on_first_input('custom_relabeller_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Relabeller FSSAI License Number'));
                    }

                    if (row.distributer_fssai_license && !frm.doc.custom_distributer_fssai_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_distributer_fssai_license_number');
                        frm.focus_on_first_input('custom_distributer_fssai_license_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Distributer FSSAI License Number '));
                    }

                    if (row.importer_fssai_license && !frm.doc.custom_importer_fssai_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_importer_fssai_license_number');
                        frm.focus_on_first_input('custom_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Importer FSSAI License Number '));
                    }

                    if (row.trader_fssai_license && !frm.doc.custom_trader_fssai_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_trader_fssai_license_number');
                        frm.focus_on_first_input('custom_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Trader FSSAI License Number '));
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



            if (frm.doc.custom_ayush_product_approval && frm.doc.custom_ayush_product_approval.length > 0) {
                frm.doc.custom_ayush_product_approval.forEach((row, index) => {
                    if (row.product_name && !row.product_approval_copy) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_ayush_product_approval');
                        frm.focus_on_first_input('custom_ayush_product_approval');
                        frappe.throw(__('<b>Mandatory field:</b><br>Product Approval Copy'));
                    }
                });
            }

            if (frm.doc.custom_dcl_product_approval && frm.doc.custom_dcl_product_approval.length > 0) {
                frm.doc.custom_dcl_product_approval.forEach((row, index) => {
                    if (row.product_name && !row.product_approval_copy) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_dcl_product_approval');
                        frm.focus_on_first_input('custom_dcl_product_approval');
                        frappe.throw(__('<b>Mandatory field:</b><br>Product Approval Copy'));
                    }
                });
            }
        }


        else if (workflow_action === 'Send for Approval' && frm.doc.supplier_type === 'Individual') {
            const isMarketplace = frm.doc.custom_is_marketplace_workflow;
            // Define an array of fields to check
            const fieldsToCheck = [
                { field: 'custom_authorised_signatory_name', message: __('<b>Mandatory field:</b><br>Authorised Signatory Name') },
                { field: 'custom_authorised_signatory_aadhar_card', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card') },
                { field: 'custom_authorised_signatory_aadhar_card_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card Attachment') },
                { field: 'custom_authorised_signatory_pan', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN') },
                { field: 'custom_authorised_signatory_pan_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN Attachment') },
                { field: 'custom_in_case_of_authorised_dealer', message: __('<b>Mandatory field:</b><br>Authorised Dealer') },
                // { field: 'custom_authorised_dealer_attachment', message: __('<b>Mandatory field:</b><br>Authorised Dealer Attachment') },

            ];


            if (isMarketplace) {
                fieldsToCheck.push(
                    { field: 'custom_board_resolution', message: __('<b>Mandatory field:</b><br>Board Resolution Number') },
                    { field: 'custom_board_resolution_attachment', message: __('<b>Mandatory field:</b><br>Board Resolution Attachment') },
                );
            }

            setTimeout(() => {
                fieldsToCheck.forEach(field => {
                    add_fake_asterisk(frm, field.field);
                });
            }, 300); 

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

                    if (row.relabeller_fssai_license && !frm.doc.custom_relabeller_fssai_licence_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_relabeller_fssai_licence_number');
                        frm.focus_on_first_input('custom_relabeller_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Relabeller FSSAI License Number'));
                    }

                    if (row.distributer_fssai_license && !frm.doc.custom_distributer_fssai_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_distributer_fssai_license_number');
                        frm.focus_on_first_input('custom_distributer_fssai_license_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Distributer FSSAI License Number '));
                    }

                    if (row.importer_fssai_license && !frm.doc.custom_importer_fssai_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_importer_fssai_license_number');
                        frm.focus_on_first_input('custom_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Importer FSSAI License Number '));
                    }

                    if (row.trader_fssai_license && !frm.doc.custom_trader_fssai_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_trader_fssai_license_number');
                        frm.focus_on_first_input('custom_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Trader FSSAI License Number '));
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

            if (frm.doc.custom_ayush_product_approval && frm.doc.custom_ayush_product_approval.length > 0) {
                frm.doc.custom_ayush_product_approval.forEach((row, index) => {
                    if (row.product_name && !frm.doc.product_approval_copy) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_ayush_product_approval');
                        frm.focus_on_first_input('custom_ayush_product_approval');
                        frappe.throw(__('<b>Mandatory field:</b><br>Product Approval Copy'));
                    }
                });
            }

            if (frm.doc.custom_dcl_product_approval && frm.doc.custom_dcl_product_approval.length > 0) {
                frm.doc.custom_dcl_product_approval.forEach((row, index) => {
                    if (row.product_name && !frm.doc.product_approval_copy) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_dcl_product_approval');
                        frm.focus_on_first_input('custom_dcl_product_approval');
                        frappe.throw(__('<b>Mandatory field:</b><br>Product Approval Copy'));
                    }
                });
            }
        }


        else if (workflow_action === 'Send for Approval' && frm.doc.supplier_type === 'LLP') {
            const isMarketplace = frm.doc.custom_is_marketplace_workflow;
            // Define an array of fields to check
            const fieldsToCheck = [
                { field: 'custom_certificate_of_incorporationpartnership', message: __('<b>Mandatory field:</b><br>Certificate of Incorporation/Partnership Number') },
                { field: 'custom_certificate_of_incorporationpartnership_attachment', message: __('<b>Mandatory field:</b><br>COI/P Attachment') },
                { field: 'custom_authorised_signatory_name', message: __('<b>Mandatory field:</b><br>Authorised Signatory Name') },
                { field: 'custom_authorised_signatory_aadhar_card', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card') },
                { field: 'custom_authorised_signatory_aadhar_card_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card Attachment') },
                { field: 'custom_authorised_signatory_pan', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN') },
                { field: 'custom_authorised_signatory_pan_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN Attachment') },
                { field: 'custom_in_case_of_authorised_dealer', message: __('<b>Mandatory field:</b><br>Authorised Dealer') },
                // { field: 'custom_authorised_dealer_attachment', message: __('<b>Mandatory field:</b><br>Authorised Dealer Attachment') },
            ];


            if (isMarketplace) {
                fieldsToCheck.push(
                    { field: 'custom_board_resolution', message: __('<b>Mandatory field:</b><br>Board Resolution Number') },
                    { field: 'custom_board_resolution_attachment', message: __('<b>Mandatory field:</b><br>Board Resolution Attachment') },
                );
            }


            setTimeout(() => {
                fieldsToCheck.forEach(field => {
                    add_fake_asterisk(frm, field.field);
                });
            }, 300); 


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

                    if (row.relabeller_fssai_license && !frm.doc.custom_relabeller_fssai_licence_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_relabeller_fssai_licence_number');
                        frm.focus_on_first_input('custom_relabeller_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Relabeller FSSAI License Number'));
                    }

                    if (row.distributer_fssai_license && !frm.doc.custom_distributer_fssai_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_distributer_fssai_license_number');
                        frm.focus_on_first_input('custom_distributer_fssai_license_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Distributer FSSAI License Number '));
                    }

                    if (row.importer_fssai_license && !frm.doc.custom_importer_fssai_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_importer_fssai_license_number');
                        frm.focus_on_first_input('custom_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Importer FSSAI License Number '));
                    }

                    if (row.trader_fssai_license && !frm.doc.custom_trader_fssai_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_trader_fssai_license_number');
                        frm.focus_on_first_input('custom_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Trader FSSAI License Number '));
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

            if (frm.doc.custom_ayush_product_approval && frm.doc.custom_ayush_product_approval.length > 0) {
                frm.doc.custom_ayush_product_approval.forEach((row, index) => {
                    if (row.product_name && !frm.doc.product_approval_copy) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_ayush_product_approval');
                        frm.focus_on_first_input('custom_ayush_product_approval');
                        frappe.throw(__('<b>Mandatory field:</b><br>Product Approval Copy'));
                    }
                });
            }

            if (frm.doc.custom_dcl_product_approval && frm.doc.custom_dcl_product_approval.length > 0) {
                frm.doc.custom_dcl_product_approval.forEach((row, index) => {
                    if (row.product_name && !frm.doc.product_approval_copy) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_dcl_product_approval');
                        frm.focus_on_first_input('custom_dcl_product_approval');
                        frappe.throw(__('<b>Mandatory field:</b><br>Product Approval Copy'));
                    }
                });
            }
        }


        else if (workflow_action === 'Send for Approval' && frm.doc.supplier_type === 'Partnership') {
            const isMarketplace = frm.doc.custom_is_marketplace_workflow;
            // Define an array of fields to check
            const fieldsToCheck = [
                { field: 'custom_certificate_of_incorporationpartnership', message: __('<b>Mandatory field:</b><br>Certificate of Incorporation/Partnership Number') },
                { field: 'custom_certificate_of_incorporationpartnership_attachment', message: __('<b>Mandatory field:</b><br>COI/P Attachment') },
                { field: 'custom_authorised_signatory_name', message: __('<b>Mandatory field:</b><br>Authorised Signatory Name') },
                { field: 'custom_authorised_signatory_aadhar_card', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card') },
                { field: 'custom_authorised_signatory_aadhar_card_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory Aadhar Card Attachment') },
                { field: 'custom_authorised_signatory_pan', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN') },
                { field: 'custom_authorised_signatory_pan_attachment', message: __('<b>Mandatory field:</b><br>Authorised Signatory PAN Attachment') },
                { field: 'custom_in_case_of_authorised_dealer', message: __('<b>Mandatory field:</b><br>Authorised Dealer') },
                // { field: 'custom_authorised_dealer_attachment', message: __('<b>Mandatory field:</b><br>Authorised Dealer Attachment') },

            ];


            if (isMarketplace) {
                fieldsToCheck.push(
                    { field: 'custom_board_resolution', message: __('<b>Mandatory field:</b><br>Board Resolution Number') },
                    { field: 'custom_board_resolution_attachment', message: __('<b>Mandatory field:</b><br>Board Resolution Attachment') },
                );
            }


            setTimeout(() => {
                fieldsToCheck.forEach(field => {
                    add_fake_asterisk(frm, field.field);
                });
            }, 300); 

            

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

                    if (row.relabeller_fssai_license && !frm.doc.custom_relabeller_fssai_licence_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_relabeller_fssai_licence_number');
                        frm.focus_on_first_input('custom_relabeller_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Relabeller FSSAI License Number'));
                    }

                    if (row.distributer_fssai_license && !frm.doc.custom_distributer_fssai_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_distributer_fssai_license_number');
                        frm.focus_on_first_input('custom_distributer_fssai_license_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Distributer FSSAI License Number '));
                    }

                    if (row.importer_fssai_license && !frm.doc.custom_importer_fssai_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_importer_fssai_license_number');
                        frm.focus_on_first_input('custom_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Importer FSSAI License Number '));
                    }

                    if (row.trader_fssai_license && !frm.doc.custom_trader_fssai_license_number) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_trader_fssai_license_number');
                        frm.focus_on_first_input('custom_fssai_licence_number');
                        frappe.throw(__('<b>Mandatory field:</b><br>Trader FSSAI License Number '));
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

            if (frm.doc.custom_ayush_product_approval && frm.doc.custom_ayush_product_approval.length > 0) {
                frm.doc.custom_ayush_product_approval.forEach((row, index) => {
                    if (row.product_name && !frm.doc.product_approval_copy) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_ayush_product_approval');
                        frm.focus_on_first_input('custom_ayush_product_approval');
                        frappe.throw(__('<b>Mandatory field:</b><br>Product Approval Copy'));
                    }
                });
            }

            if (frm.doc.custom_dcl_product_approval && frm.doc.custom_dcl_product_approval.length > 0) {
                frm.doc.custom_dcl_product_approval.forEach((row, index) => {
                    if (row.product_name && !frm.doc.product_approval_copy) {
                        frappe.dom.unfreeze();
                        frm.scroll_to_field('custom_dcl_product_approval');
                        frm.focus_on_first_input('custom_dcl_product_approval');
                        frappe.throw(__('<b>Mandatory field:</b><br>Product Approval Copy'));
                    }
                });
            }
        }

    }
    
    
});




function add_fake_asterisk(frm, fieldname) {
    const field = frm.fields_dict[fieldname];
    if (!field || !field.$wrapper) return;

    const label_text = field.df.label;
    const label = field.$wrapper.find('.control-label');

    label.each(function () {
        const $label = $(this);
        const current = $label.html().trim();

        // Only add asterisk if not already present
        if (!current.includes('*')) {
            $label.html(`${label_text} <span style="color:red">*</span>`);
        }
    });
}






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

    relabeller_fssai_license: function(frm, cdt, cdn) {
        toggle_relabeller_license_field(frm);
        toggle_oem_license_field(frm);
    },

    distributer_fssai_license: function(frm, cdt, cdn) {
        toggle_distributer_license_field(frm)
    },

    importer_fssai_license: function(frm, cdt, cdn) {
        toggle_trader_license_field(frm);
    },

    trader_fssai_license: function(frm, cdt, cdn) {
        toggle_trader_license_field(frm);
    },

    custom_type_of_product_remove: function(frm) {
        toggle_fssai_license_field(frm);
        toggle_ayush_license_field(frm);
        toggle_dc_license_field(frm);
        toggle_relabeller_license_field(frm);
        toggle_distributer_license_field(frm);
        toggle_importer_license_field(frm);
        toggle_trader_license_field(frm);
    },

    // Optional: run after any row is added
    custom_type_of_product_add: function(frm) {
        toggle_fssai_license_field(frm);
        toggle_ayush_license_field(frm);
        toggle_dc_license_field(frm);
        toggle_relabeller_license_field(frm);
        toggle_distributer_license_field(frm);
        toggle_importer_license_field(frm);
        toggle_trader_license_field(frm);
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

function toggle_relabeller_license_field(frm) {
    const rows = frm.doc.custom_type_of_product || [];
    const any_checked = rows.some(row => row.relabeller_fssai_license === 1);
    frm.toggle_display('custom_relabeller_fssai_licence_number', any_checked);
}

function toggle_distributer_license_field(frm) {
    const rows = frm.doc.custom_type_of_product || [];
    const any_checked = rows.some(row => row.distributer_fssai_license === 1);
    frm.toggle_display('custom_distributer_fssai_license_number', any_checked);
}

function toggle_importer_license_field(frm) {
    const rows = frm.doc.custom_type_of_product || [];
    const any_checked = rows.some(row => row.importer_fssai_license === 1);
    frm.toggle_display('custom_importer_fssai_license_number', any_checked);
}

function toggle_trader_license_field(frm) {
    const rows = frm.doc.custom_type_of_product || [];
    const any_checked = rows.some(row => row.trader_fssai_license === 1);
    frm.toggle_display('custom_trader_fssai_license_number', any_checked);
}

function toggle_oem_license_field(frm) {
    const rows = frm.doc.custom_type_of_product || [];
    const any_checked = rows.some(row => row.relabeller_fssai_license === 1);
    frm.toggle_display('custom_oem_fssai_license_number', any_checked);
}










frappe.ui.form.on('Supplier Categories', {
    type_of_product_required(frm, cdt, cdn) {
        toggle_custom_type_of_product(frm);
    }
});

function toggle_custom_type_of_product(frm) {
    let show = false;
    let iso = false;
    cc = false;
    is_mktplace = false;
    is_raw_mat = false;
    is_packing_mat = false;
    is_indirect_sup = false;
    is_import_sup = false;
    if (frm.doc.custom_supplier_category && frm.doc.custom_supplier_category.length > 0) {
        frm.doc.custom_supplier_category.forEach(row => {
            if (row.type_of_product_required) {
                show = true;
            }
            if (row.iso_required) {
                iso = true;
            }
            if (row.cancelled_cheque_required) {
                cc = true;
            }
            if (row.is_marketplace_workflow) {
                is_mktplace = true;
            }
            if (row.is_raw_material) {
                is_raw_mat = true;
            }
            if (row.is_packing_material) {
                is_packing_mat = true;
            }
            if (row.is_indirect_supplier) {
                is_indirect_sup = true;
            }
            if (row.is_import_supplier) {
                is_import_sup = true;
            }
        });
    }

    frm.toggle_display('custom_type_of_product', show);
    frm.toggle_display('custom_iso_certificate', iso);
    frm.toggle_display('custom_cancelled_cheque', cc);
    frm.doc.custom_is_marketplace_workflow = is_mktplace;
    frm.refresh_field('custom_is_marketplace_workflow');
    frm.doc.custom_is_raw_material = is_raw_mat;
    frm.refresh_field('custom_is_raw_material');
    frm.doc.custom_is_packing_material = is_packing_mat;
    frm.refresh_field('custom_is_packing_material');
    frm.doc.custom_is_indirect_supplier = is_indirect_sup;
    frm.refresh_field('custom_is_indirect_supplier');
    frm.doc.custom_is_import_supplier = is_import_sup;
    frm.refresh_field('custom_is_import_supplier');


    if (!show && frm.doc.custom_type_of_product && frm.doc.custom_type_of_product.length > 0) {
        frm.clear_table('custom_type_of_product');
        frm.refresh_field('custom_type_of_product');
    }
}