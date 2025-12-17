



frappe.ui.form.on("Work Order", {
    refresh(frm) {

        if (frm.doc.docstatus === 1 && frm.doc.production_item) {

            frappe.db.get_value("Item", frm.doc.production_item, "item_group", (r) => {

                if (r && r.item_group === "Finished Goods") {

                    frm.add_custom_button("Machine Setup SE", () => {

                        // Open new Stock Entry
                        frappe.new_doc('Stock Entry', {
                            stock_entry_type: "Transfer to Manufacturing Machine Setup",
                            work_order: frm.doc.name,
                        });

                        // Wait for form to load
                        setTimeout(() => {

                            frappe.model.set_value(
                                'Stock Entry',
                                cur_frm.docname,
                                'from_bom',
                                0
                            );
                            frappe.model.set_value(
                                'Stock Entry',
                                cur_frm.docname,
                                'bom_no',
                                ""
                            );


                            if (!cur_frm) return;

                            // Clear existing items table
                            cur_frm.clear_table("items");

                            // Loop Work Order required items
                            (frm.doc.required_items || []).forEach(row => {

                                frappe.db.get_value("Item", row.item_code, "item_group", (item) => {

                                    if (item && item.item_group === "Packing Material") {

                                        // Fetch active BOM for this item
                                        frappe.db.get_value("BOM", { item: row.item_code, is_active: 1 }, "name", (bom) => {

                                            if (bom && bom.name) {

                                                // Fetch BOM Items (child table)
                                                frappe.db.get_list("BOM Item", {
                                                    filters: { parent: bom.name, item_code: row.item_code },
                                                    fields: ["stock_uom", "conversion_factor"],
                                                    limit_page_length: 1
                                                }).then(bom_items => {

                                                    const child = frappe.model.add_child(cur_frm.doc, "items");
                                                    child.item_code = row.item_code;
                                                    child.s_warehouse = frm.doc.source_warehouse || "";
                                                    child.t_warehouse = frm.doc.wip_warehouse || "";
                                                    child.qty = null;

                                                    if (bom_items && bom_items.length > 0) {
                                                        child.uom = bom_items[0].stock_uom || "";
                                                        child.conversion_factor = bom_items[0].conversion_factor || 1;
                                                    }

                                                    cur_frm.refresh_field("items");

                                                });

                                            } else {
                                                // No BOM found, still add item with blank uom
                                                const child = frappe.model.add_child(cur_frm.doc, "items");
                                                child.item_code = row.item_code;
                                                child.s_warehouse = frm.doc.source_warehouse || "";
                                                child.t_warehouse = frm.doc.wip_warehouse || "";
                                                child.qty = null;
                                                child.uom = "";
                                                child.conversion_factor = 1;

                                                cur_frm.refresh_field("items");
                                            }

                                        });

                                    }

                                });

                            });

                        }, 1000); // wait 1 sec for Stock Entry form to load

                    }, "Create");
















                    // frm.add_custom_button("Create Machine Setup Consumption SE", () => {

                    //     // Open new Stock Entry
                    //     frappe.new_doc('Stock Entry', {
                    //         stock_entry_type: "Machine Setup Consumption Entry",
                    //         work_order: frm.doc.name,
                    //     });

                    //     // -------------------------------
                    //     // 1️⃣ Fetch Transfer + Return SE
                    //     // -------------------------------
                    //     let res = frappe.call({
                    //         method: "frappe.client.get_list",
                    //         args: {
                    //             doctype: "Stock Entry",
                    //             filters: {
                    //                 work_order: frm.doc.name,
                    //                 stock_entry_type: ["in", [
                    //                     "Transfer to Manufacturing Machine Setup",
                    //                     "Machine Setup Return"
                    //                 ]],
                    //                 docstatus: 1
                    //             },
                    //             fields: ["name", "stock_entry_type"]
                    //         }
                    //     });

                    //     let se_list = res.message || [];

                    //     // Track item totals
                    //     let totals = {};  // totals[item_code] = { transfer: 0, return: 0 }

                    //     // Get item rows from each SE
                    //     for (let se of se_list) {

                    //         let se_doc = frappe.call({
                    //             method: "frappe.client.get",
                    //             args: {
                    //                 doctype: "Stock Entry",
                    //                 name: se.name
                    //             }
                    //         });

                    //         let items = se_doc.message.items || [];

                    //         items.forEach(i => {
                    //             if (!totals[i.item_code]) {
                    //                 totals[i.item_code] = { transfer: 0, return: 0 };
                    //             }

                    //             if (se.stock_entry_type === "Transfer to Manufacturing Machine Setup") {
                    //                 totals[i.item_code].transfer += i.qty;
                    //             }

                    //             if (se.stock_entry_type === "Machine Setup Return") {
                    //                 totals[i.item_code].return += i.qty;
                    //             }
                    //         });
                    //     }

                    //     // -------------------------------
                    //     // 2️⃣ Calculate Final (Consuming) Qty
                    //     // -------------------------------
                    //     let final_qty = {};
                    //     Object.keys(totals).forEach(item_code => {
                    //         final_qty[item_code] = totals[item_code].transfer - totals[item_code].return;
                    //     });

                    //     console.log("Final Consumption Qty:", final_qty);


                    //     // Wait for form to load
                    //     setTimeout(() => {

                    //         frappe.model.set_value(
                    //             'Stock Entry',
                    //             cur_frm.docname,
                    //             'from_bom',
                    //             0
                    //         );
                    //         frappe.model.set_value(
                    //             'Stock Entry',
                    //             cur_frm.docname,
                    //             'bom_no',
                    //             ""
                    //         );


                    //         if (!cur_frm) return;

                    //         // Clear existing items table
                    //         cur_frm.clear_table("items");

                    //         // Loop Work Order required items
                    //         (frm.doc.required_items || []).forEach(row => {

                    //             frappe.db.get_value("Item", row.item_code, "item_group", (item) => {

                    //                 if (item && item.item_group === "Packing Material") {

                    //                     // Fetch active BOM for this item
                    //                     frappe.db.get_value("BOM", { item: row.item_code, is_active: 1 }, "name", (bom) => {

                    //                         if (bom && bom.name) {

                    //                             // Fetch BOM Items (child table)
                    //                             frappe.db.get_list("BOM Item", {
                    //                                 filters: { parent: bom.name, item_code: row.item_code },
                    //                                 fields: ["stock_uom", "conversion_factor"],
                    //                                 limit_page_length: 1
                    //                             }).then(bom_items => {

                    //                                 // -------------------------------
                    //                                 // 4️⃣ Insert items into new SE
                    //                                 // -------------------------------
                    //                                 for (let item_code of Object.keys(final_qty)) {

                    //                                     if (final_qty[item_code] <= 0) continue; // Skip non-positive qty

                    //                                     let child = frappe.model.add_child(cur_frm.doc, "items");

                    //                                     child.item_code = item_code;
                    //                                     child.qty = final_qty[item_code];

                    //                                     // Set your warehouses
                    //                                     child.s_warehouse = frm.doc.source_warehouse || "";
                    //                                 }

                    //                                 cur_frm.refresh_field("items");

                    //                             });

                    //                         } else {
                    //                             // No BOM found, still add item with blank uom
                    //                             const child = frappe.model.add_child(cur_frm.doc, "items");
                    //                             child.item_code = row.item_code;
                    //                             child.s_warehouse = frm.doc.source_warehouse || "";
                    //                             child.t_warehouse = frm.doc.wip_warehouse || "";
                    //                             child.qty = null;
                    //                             child.uom = "";
                    //                             child.conversion_factor = 1;

                    //                             cur_frm.refresh_field("items");
                    //                         }

                    //                     });

                    //                 }

                    //             });

                    //         });

                    //     }, 1000); // wait 1 sec for Stock Entry form to load

                    // }, "Create");








                    frm.add_custom_button("Machine Setup Consumption SE", async () => {

                        // 1️⃣ Create new Stock Entry draft
                        let new_se = await frappe.new_doc('Stock Entry', {
                            stock_entry_type: "Machine Setup Consumption Entry",
                            custom_machine_setup_consumption_work_order: frm.doc.name,
                        });

                        // Set from_bom and bom_no after form loads
                        setTimeout(function () {
                            frappe.model.set_value('Stock Entry', cur_frm.docname, 'from_bom', 0);
                            frappe.model.set_value('Stock Entry', cur_frm.docname, 'bom_no', "");
                        }, 1000);

                        // 2️⃣ Fetch SE list (submitted)
                        let res = await frappe.call({
                            method: "frappe.client.get_list",
                            args: {
                                doctype: "Stock Entry",
                                filters: {
                                    work_order: frm.doc.name,
                                    stock_entry_type: ["in", [
                                        "Transfer to Manufacturing Machine Setup",
                                        "Machine Setup Return"
                                    ]],
                                    docstatus: 1
                                },
                                fields: ["name", "stock_entry_type"]
                            }
                        });

                        let se_list = res.message || [];
                        console.log("Matched SE:", se_list);

                        if (!se_list.length) {
                            frappe.msgprint("No submitted Stock Entries found for this Work Order.");
                            return;
                        }

                        // 3️⃣ Find first SE of type "Transfer to Manufacturing Machine Setup"
                        let first_transfer_se = se_list.find(se => se.stock_entry_type === "Transfer to Manufacturing Machine Setup");
                        let first_se_items = [];
                        if (first_transfer_se) {
                            let se_doc_res = await frappe.call({
                                method: "frappe.client.get",
                                args: { doctype: "Stock Entry", name: first_transfer_se.name }
                            });
                            first_se_items = se_doc_res.message.items || [];
                        }

                        // 4️⃣ Loop through all SEs to calculate final_qty and transfer_qty
                        let totals = {};        // final_qty (consumption)
                        let transfer_totals = {}; // transfer_qty

                        for (let se of se_list) {
                            let se_doc_res = await frappe.call({
                                method: "frappe.client.get",
                                args: { doctype: "Stock Entry", name: se.name }
                            });
                            let items = se_doc_res.message.items || [];

                            items.forEach(i => {
                                if (!totals[i.item_code]) {
                                    totals[i.item_code] = { transfer: 0, return: 0 };
                                    transfer_totals[i.item_code] = { transfer: 0, return: 0 };
                                }

                                // For final_qty (consumption)
                                if (se.stock_entry_type === "Transfer to Manufacturing Machine Setup") totals[i.item_code].transfer += i.qty;
                                if (se.stock_entry_type === "Machine Setup Return") totals[i.item_code].return += i.qty;

                                // For transfer_qty
                                if (se.stock_entry_type === "Transfer to Manufacturing Machine Setup") transfer_totals[i.item_code].transfer += i.transfer_qty || 0;
                                if (se.stock_entry_type === "Machine Setup Return") transfer_totals[i.item_code].return += i.transfer_qty || 0;
                            });
                        }

                        // 5️⃣ Calculate final results
                        let final_qty = {};
                        let final_transfer_qty = {};

                        Object.keys(totals).forEach(item_code => {
                            final_qty[item_code] = totals[item_code].transfer - totals[item_code].return;
                            final_transfer_qty[item_code] = transfer_totals[item_code].transfer - transfer_totals[item_code].return;
                        });

                        console.log("Final Consumption Qty:", final_qty);
                        console.log("Final Transfer Qty:", final_transfer_qty);

                        // 6️⃣ Clear SE items and add new items with UOM, conversion_factor, rate, batch
                        cur_frm.clear_table("items");

                        Object.keys(final_qty).forEach(item_code => {
                            let qty = final_qty[item_code];
                            let transfer_qty = final_transfer_qty[item_code];
                            if (!qty || qty <= 0) return;

                            let child = frappe.model.add_child(cur_frm.doc, "items");
                            child.item_code = item_code;
                            child.qty = qty;
                            child.transfer_qty = transfer_qty; // Add transfer_qty field in SE items
                            child.s_warehouse = frm.doc.source_warehouse || "";

                            // Fetch details from first SE
                            if (first_se_items.length) {
                                let se_item = first_se_items.find(i => i.item_code === item_code);
                                if (se_item) {
                                    child.stock_uom = se_item.stock_uom || "";
                                    child.conversion_factor = se_item.conversion_factor || 1;
                                    child.basic_rate = se_item.basic_rate || 0;
                                    child.batch_no = se_item.batch_no || "";
                                }
                            }
                        });

                        cur_frm.refresh_field("items");

                    }, "Create");

















                    
                    // frm.add_custom_button("Create Machine Setup Consumption SE", async () => {

                    //     if (!frm.doc.name) return;

                    //     try {
                    //         // -------------------------------
                    //         // 1️⃣ Fetch Transfer + Return SE
                    //         // -------------------------------
                    //         let res = await frappe.call({
                    //             method: "frappe.client.get_list",
                    //             args: {
                    //                 doctype: "Stock Entry",
                    //                 filters: {
                    //                     work_order: frm.doc.name,
                    //                     stock_entry_type: ["in", [
                    //                         "Transfer to Manufacturing Machine Setup",
                    //                         "Machine Setup Return"
                    //                     ]],
                    //                     docstatus: 1
                    //                 },
                    //                 fields: ["name", "stock_entry_type"]
                    //             }
                    //         });

                    //         let se_list = res.message || [];

                    //         // Track item totals
                    //         let totals = {};  // totals[item_code] = { transfer: 0, return: 0 }

                    //         // Get item rows from each SE
                    //         for (let se of se_list) {

                    //             let se_doc = await frappe.call({
                    //                 method: "frappe.client.get",
                    //                 args: {
                    //                     doctype: "Stock Entry",
                    //                     name: se.name
                    //                 }
                    //             });

                    //             let items = se_doc.message.items || [];

                    //             items.forEach(i => {
                    //                 if (!totals[i.item_code]) {
                    //                     totals[i.item_code] = { transfer: 0, return: 0 };
                    //                 }

                    //                 if (se.stock_entry_type === "Transfer to Manufacturing Machine Setup") {
                    //                     totals[i.item_code].transfer += i.qty;
                    //                 }

                    //                 if (se.stock_entry_type === "Machine Setup Return") {
                    //                     totals[i.item_code].return += i.qty;
                    //                 }
                    //             });
                    //         }

                    //         // -------------------------------
                    //         // 2️⃣ Calculate Final (Consuming) Qty
                    //         // -------------------------------
                    //         let final_qty = {};
                    //         Object.keys(totals).forEach(item_code => {
                    //             final_qty[item_code] = totals[item_code].transfer - totals[item_code].return;
                    //         });

                    //         console.log("Final Consumption Qty:", final_qty);

                    //         // -------------------------------
                    //         // 3️⃣ Create Stock Entry (Consumption)
                    //         // -------------------------------
                    //         frappe.new_doc("Stock Entry", {
                    //             stock_entry_type: "Machine Setup Consumption Entry",
                    //             work_order: frm.doc.name,
                    //             from_bom: 0,
                    //             bom_no: ""
                    //         });

                    //         // Wait for form to load fully
                    //         await frappe.timeout(500);

                    //         if (!cur_frm) return;

                    //         // Clear items table
                    //         cur_frm.clear_table("items");

                    //         // -------------------------------
                    //         // 4️⃣ Insert items into new SE
                    //         // -------------------------------
                    //         for (let item_code of Object.keys(final_qty)) {

                    //             if (final_qty[item_code] <= 0) continue; // Skip non-positive qty

                    //             let child = frappe.model.add_child(cur_frm.doc, "items");

                    //             child.item_code = item_code;
                    //             child.qty = final_qty[item_code];

                    //             // Set your warehouses
                    //             child.s_warehouse = frm.doc.source_warehouse || "";
                    //             child.t_warehouse = frm.doc.wip_warehouse || "";
                    //         }

                    //         // Refresh table
                    //         cur_frm.refresh_field("items");

                    //     } catch (err) {
                    //         console.error("Error:", err);
                    //     }
                    // });



                }

            });

        }

    }
});

