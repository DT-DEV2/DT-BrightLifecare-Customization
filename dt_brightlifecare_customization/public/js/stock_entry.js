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


        if (frm.doc.docstatus === 1 && frm.doc.stock_entry_type == "Transfer to Manufacturing Machine Setup") {

            frm.add_custom_button('Create Reversal SE', function () {
                let new_se = frappe.model.get_new_doc('Stock Entry');

                new_se.stock_entry_type = "Machine Setup Return";
                new_se.work_order = frm.doc.work_order;
                new_se.from_bom = 0;
                new_se.against_stock_entry = frm.doc.name;

                // Map items from current SE
                let reversed_items = frm.doc.items.map(item => {
                    return {
                        item_code: item.item_code,
                        item_name: item.item_name,
                        qty: 0,
                        uom: item.uom,
                        conversion_factor: item.conversion_factor,
                        basic_rate: item.basic_rate,
                        s_warehouse: item.t_warehouse,
                        t_warehouse: item.s_warehouse,
                        against_stock_entry: frm.doc.name,
                        ste_detail: item.name,
                        batch_no: item.batch_no,
                    };
                });

                frappe.set_route('Form', 'Stock Entry', new_se.name).then(() => {
                    let target_frm = cur_frm;

                    if (target_frm && target_frm.doctype === 'Stock Entry') {

                        // Clear items table first
                        target_frm.clear_table('items');

                        reversed_items.forEach(d => {
                            let row = target_frm.add_child('items');

                            // Suppress batch/serial popup by setting __run_batch_popup = false
                            row.__run_batch_popup = false;

                            // Set values programmatically
                            Object.keys(d).forEach(field => {
                                row[field] = d[field];
                            });
                        });

                        target_frm.refresh_field('items');
                        target_frm.set_value('from_bom', 0);
                    }
                });
            });

        }

    }
});


frappe.ui.form.on('Stock Entry', {
    custom_validate_batch: function (frm) {
        // This runs when you click your existing button
        open_camera_dialog(frm);
    },

    refresh: function(frm) {

        frm.fields_dict.custom_parameters.grid.wrapper
            .find('.grid-add-row, .grid-remove-rows').hide();

        // Also disable the ability to add/delete via keyboard shortcuts or API
        frm.fields_dict.custom_parameters.grid.cannot_add_rows = true;
        frm.fields_dict.custom_parameters.grid.cannot_delete_rows = true;


        if(frm.doc.stock_entry_type === "Material Transfer for Manufacture") {
            frm.add_custom_button(__('Print Dispensing Tags'), function() {
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
        };
   }
});



// function open_camera_dialog(frm) {
//     // Load jsQR (lightweight QR decoder)
//     frappe.require("https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js", function () {

//         let d = new frappe.ui.Dialog({
//             title: "Scan QR Code",
//             fields: [
//                 { fieldtype: "HTML", fieldname: "camera_area" }
//             ],
//             primary_action_label: "Close",
//             primary_action: function () {
//                 stopCamera();
//                 d.hide();
//             }
//         });

//         d.show();

//         const wrapper = d.get_field("camera_area").$wrapper;
//         const vidId = "se-camera-" + frappe.utils.get_random(6);
//         const canvasId = "se-canvas-" + frappe.utils.get_random(6);

//         wrapper.html(`
//             <div style="text-align:center;">
//                 <video id="${vidId}" autoplay playsinline style="max-width:100%; height:auto; border:1px solid #ccc; border-radius:6px;"></video>
//                 <canvas id="${canvasId}" style="display:none;"></canvas>
//             </div>
//             <div style="text-align:center; margin-top:8px;">
//                 <small>Show a QR code in front of the camera to check.</small>
//             </div>
//         `);

//         const video = wrapper.find(`#${vidId}`)[0];
//         const canvas = wrapper.find(`#${canvasId}`)[0];
//         const ctx = canvas.getContext("2d");

//         let currentStream = null;
//         let scanning = true;

//         function stopCamera() {
//             scanning = false;
//             if (currentStream) {
//                 currentStream.getTracks().forEach(t => t.stop());
//                 currentStream = null;
//             }
//         }

//         const modal = d.$wrapper.find('.modal');
//         modal.on('hidden.bs.modal', () => {
//             stopCamera();
//         });

//         if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
//             frappe.msgprint("Camera API not supported in this browser.");
//             return;
//         }

//         navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
//             .then(stream => {
//                 currentStream = stream;
//                 video.srcObject = stream;
//                 video.play();

//                 const tick = () => {
//                     if (!scanning) return;
//                     if (video.readyState === video.HAVE_ENOUGH_DATA) {
//                         canvas.height = video.videoHeight;
//                         canvas.width = video.videoWidth;
//                         ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
//                         const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
//                         const code = jsQR(imageData.data, imageData.width, imageData.height);
//                         if (code) {
//                             stopCamera();
//                             d.hide();

//                             // Extract batch number (handles both plain and full URLs)
//                             let scanned_value = code.data.trim();
//                             let batch_no = scanned_value.split("/").pop();

//                             let matched = false;
//                             let changed = false;

//                             // Iterate through Stock Entry items table
//                             (frm.doc.items || []).forEach(row => {
//                                 if (row.batch_no && row.batch_no === batch_no) {
//                                     if (row.custom_batch_validation !== "Matched") {
//                                         frappe.model.set_value(row.doctype, row.name, "custom_batch_validation", "Matched");
//                                         changed = true;
//                                     }
//                                     matched = true;
//                                 }
//                             });

//                             frm.refresh_field("items");

//                             if (!matched) {
//                                 frappe.msgprint(`❌ No matching batch found for: ${batch_no}`);
//                             } else {
//                                 frappe.show_alert({ message: `✅ Batch ${batch_no} matched and updated!`, indicator: "green" });

//                                 // Auto-save only if something changed
//                                 if (changed) {
//                                     frm.save()
//                                         .then(() => {
//                                             frappe.show_alert({ message: "💾 Stock Entry saved successfully!", indicator: "blue" });
//                                         })
//                                         .catch(() => {
//                                             frappe.msgprint("⚠️ Failed to auto-save the Stock Entry.");
//                                         });
//                                 }
//                             }
//                             return;
//                         }
//                     }
//                     requestAnimationFrame(tick);
//                 };
//                 requestAnimationFrame(tick);
//             })
//             .catch(err => {
//                 frappe.msgprint("Unable to access camera: " + err.message);
//             });
//     });
// }





function open_camera_dialog(frm) {
    // Load jsQR (lightweight QR decoder)
    frappe.require("https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js", function () {

        let d = new frappe.ui.Dialog({
            title: "Scan QR Code",
            fields: [
                { fieldtype: "HTML", fieldname: "camera_area" }
            ],
            primary_action_label: "Close",
            primary_action: function () {
                stopCamera();
                d.hide();
            }
        });

        d.show();

        const wrapper = d.get_field("camera_area").$wrapper;
        const vidId = "se-camera-" + frappe.utils.get_random(6);
        const canvasId = "se-canvas-" + frappe.utils.get_random(6);

        wrapper.html(`
            <div style="text-align:center;">
                <video id="${vidId}" autoplay playsinline
                    style="max-width:100%; height:auto; border:1px solid #ccc; border-radius:6px;">
                </video>
                <canvas id="${canvasId}" style="display:none;"></canvas>
            </div>
            <div style="text-align:center; margin-top:8px;">
                <small>Show a QR code in front of the camera to check.</small>
            </div>
        `);

        const video = wrapper.find(`#${vidId}`)[0];
        const canvas = wrapper.find(`#${canvasId}`)[0];
        const ctx = canvas.getContext("2d");

        let currentStream = null;
        let scanning = true;

        function stopCamera() {
            scanning = false;
            if (currentStream) {
                currentStream.getTracks().forEach(t => t.stop());
                currentStream = null;
            }
        }

        const modal = d.$wrapper.find('.modal');
        modal.on('hidden.bs.modal', () => {
            stopCamera();
        });

        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            frappe.msgprint("Camera API not supported in this browser.");
            return;
        }

        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
            .then(stream => {
                currentStream = stream;
                video.srcObject = stream;
                video.play();

                const tick = () => {
                    if (!scanning) return;

                    if (video.readyState === video.HAVE_ENOUGH_DATA) {
                        canvas.height = video.videoHeight;
                        canvas.width = video.videoWidth;
                        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                        const code = jsQR(
                            imageData.data,
                            imageData.width,
                            imageData.height
                        );

                        if (code) {
                            stopCamera();
                            d.hide();

                            // ✅ Extract batch number from QR
                            let scanned_value = code.data.trim();
                            let batch_no = scanned_value.split("/").pop();

                            let matched = false;
                            let changed = false;
                            let pending = 0;

                            (frm.doc.items || []).forEach(row => {
                                if (!row.serial_and_batch_bundle) return;

                                pending++;

                                frappe.model.with_doc(
                                    "Serial and Batch Bundle",
                                    row.serial_and_batch_bundle,
                                    function () {
                                        let bundle = frappe.model.get_doc(
                                            "Serial and Batch Bundle",
                                            row.serial_and_batch_bundle
                                        );

                                        if (bundle && bundle.entries) {
                                            bundle.entries.forEach(entry => {
                                                if (entry.batch_no === batch_no) {
                                                    matched = true;

                                                    if (row.custom_batch_validation !== "Matched") {
                                                        frappe.model.set_value(
                                                            row.doctype,
                                                            row.name,
                                                            "custom_batch_validation",
                                                            "Matched"
                                                        );
                                                        changed = true;
                                                    }
                                                }
                                            });
                                        }

                                        pending--;

                                        // ✅ Decide result ONLY after all bundles checked
                                        if (pending === 0) {
                                            frm.refresh_field("items");

                                            if (!matched) {
                                                frappe.msgprint(
                                                    `❌ No matching batch found for: ${batch_no}`
                                                );
                                            } else {
                                                frappe.show_alert({
                                                    message: `✅ Batch ${batch_no} matched and updated!`,
                                                    indicator: "green"
                                                });

                                                if (changed) {
                                                    if (frm.doc.docstatus === 0) {
                                                        // Draft → normal save
                                                        frm.save();
                                                    } else if (frm.doc.docstatus === 1) {
                                                        // Submitted → Update After Submit
                                                        frm.save('Update');
                                                    }
                                                }


                                            }
                                        }
                                    }
                                );
                            });

                            return;
                        }
                    }

                    requestAnimationFrame(tick);
                };

                requestAnimationFrame(tick);
            })
            .catch(err => {
                frappe.msgprint("Unable to access camera: " + err.message);
            });
    });
}




// opens camera and diaply msg when QR code shown 
// function open_camera_dialog(frm) {
//     // Load jsQR (lightweight QR decoder)
//     frappe.require("https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js", function () {

//         let d = new frappe.ui.Dialog({
//             title: "Scan QR Code",
//             fields: [
//                 { fieldtype: "HTML", fieldname: "camera_area" }
//             ],
//             primary_action_label: "Close",
//             primary_action: function () {
//                 stopCamera();
//                 d.hide();
//             }
//         });

//         d.show();

//         const wrapper = d.get_field("camera_area").$wrapper;
//         const vidId = "se-camera-" + frappe.utils.get_random(6);
//         const canvasId = "se-canvas-" + frappe.utils.get_random(6);

//         wrapper.html(`
//             <div style="text-align:center;">
//                 <video id="${vidId}" autoplay playsinline style="max-width:100%; height:auto; border:1px solid #ccc; border-radius:6px;"></video>
//                 <canvas id="${canvasId}" style="display:none;"></canvas>
//             </div>
//             <div style="text-align:center; margin-top:8px;">
//                 <small>Show a QR code in front of the camera to test.</small>
//             </div>
//         `);

//         const video = wrapper.find(`#${vidId}`)[0];
//         const canvas = wrapper.find(`#${canvasId}`)[0];
//         const ctx = canvas.getContext("2d");

//         let currentStream = null;
//         let scanning = true;

//         // Stop camera helper
//         function stopCamera() {
//             scanning = false;
//             if (currentStream) {
//                 currentStream.getTracks().forEach(t => t.stop());
//                 currentStream = null;
//             }
//         }

//         // Stop camera when dialog closes
//         const modal = d.$wrapper.find('.modal');
//         modal.on('hidden.bs.modal', () => {
//             stopCamera();
//         });

//         // Request camera access
//         if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
//             frappe.msgprint("Camera API not supported in this browser.");
//             return;
//         }

//         navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
//             .then(stream => {
//                 currentStream = stream;
//                 video.srcObject = stream;
//                 video.play();

//                 // Start scanning loop
//                 const tick = () => {
//                     if (!scanning) return;
//                     if (video.readyState === video.HAVE_ENOUGH_DATA) {
//                         canvas.height = video.videoHeight;
//                         canvas.width = video.videoWidth;
//                         ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
//                         const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
//                         const code = jsQR(imageData.data, imageData.width, imageData.height);
//                         if (code) {
//                             frappe.msgprint("Hello");
//                             stopCamera();
//                             d.hide();
//                             return;
//                         }
//                     }
//                     requestAnimationFrame(tick);
//                 };
//                 requestAnimationFrame(tick);
//             })
//             .catch(err => {
//                 frappe.msgprint("Unable to access camera: " + err.message);
//             });
//     });
// }



// opens camera all fine
// function open_camera_dialog(frm) {
//     // Create dialog with an HTML field to hold the <video>
//     let d = new frappe.ui.Dialog({
//         title: "Camera",
//         fields: [
//             { fieldtype: "HTML", fieldname: "camera_area" }
//         ],
//         primary_action_label: "Close",
//         primary_action: function () {
//             // Will trigger bootstrap modal close which we handle below
//             d.hide();
//         }
//     });

//     d.show();

//     // Prepare video element
//     const wrapper = d.get_field("camera_area").$wrapper;
//     const vidId = "se-camera-" + frappe.utils.get_random(6);
//     wrapper.html(`<div style="text-align:center;">
//                     <video id="${vidId}" autoplay playsinline style="max-width:100%; height:auto; border:1px solid #ccc; border-radius:6px;"></video>
//                   </div>
//                   <div style="text-align:center; margin-top:8px;">
//                     <small>Allow camera permission if prompted. Close dialog to stop camera.</small>
//                   </div>`);

//     const video = wrapper.find(`#${vidId}`)[0];
//     let currentStream = null;

//     // Helper to stop camera
//     function stopCamera() {
//         if (currentStream) {
//             currentStream.getTracks().forEach(t => t.stop());
//             currentStream = null;
//         }
//     }

//     // Stop camera when dialog closes (handles both primary action and modal close)
//     const modal = d.$wrapper.find('.modal');
//     modal.on('hidden.bs.modal', () => {
//         stopCamera();
//     });

//     // Request camera
//     if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
//         frappe.msgprint("Camera API not supported in this browser.");
//         return;
//     }

//     navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
//         .then(stream => {
//             currentStream = stream;
//             try {
//                 video.srcObject = stream;
//             } catch (e) {
//                 // fallback
//                 video.src = window.URL.createObjectURL(stream);
//             }
//             video.play().catch(() => { /* play may be blocked until user interacts */ });
//         })
//         .catch(err => {
//             frappe.msgprint("Unable to access camera: " + err.message);
//             // close dialog if you want:
//             // d.hide();
//         });
// }
