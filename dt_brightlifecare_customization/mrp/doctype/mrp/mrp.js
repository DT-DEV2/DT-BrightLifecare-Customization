// Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on("MRP", {

	refresh: function(frm) {
		frm.set_query('bom_no', 'material_request_items', function(doc, cdt, cdn) {
            let child = locals[cdt][cdn];
            return {
                filters: {
                    item: child.item_code,
					is_active: 1,
					docstatus: 1,
					custom_source_warehouse: child.warehouse
                }
            };
		});

		// Add Create menu actions similar to Production Plan
		if (frm.doc.docstatus === 1) {
			frm.add_custom_button(__('Material Request'), () => {
				frappe.call({
					method: 'dt_brightlifecare_customization.mrp.doctype.mrp.mrp.make_material_request',
					args: { mrp_name: frm.doc.name },
					callback: function(r) {
						if (!r.exc) {
							frm.reload_doc();
							if (r.message && r.message.created && r.message.created.length) {
								let links = r.message.created.map(d => `<a href="#Form/${d.doctype}/${d.name}">${d.doctype} ${d.name}</a>`);
								frappe.msgprint(__('Created: {0}', [links.join(', ')]));
							}
						}
					}
				});
			}, __('Create'));

			frm.add_custom_button(__('Work Order'), () => {
				frappe.call({
					method: 'dt_brightlifecare_customization.mrp.doctype.mrp.mrp.make_work_orders',
					args: { mrp_name: frm.doc.name },
					callback: function(r) {
						if (!r.exc) {
							frm.reload_doc();
							if (r.message && r.message.created && r.message.created.length) {
								let links = r.message.created.map(d => `<a href="#Form/${d.doctype}/${d.name}">${d.doctype} ${d.name}</a>`);
								frappe.msgprint(__('Created: {0}', [links.join(', ')]));
							}
						}
					}
				});
			}, __('Create'));
		}
	},

	explode_bom: function (frm) {
		// frm.dirty();

		if (frm.doc.name) {

			frappe.call({
				method: "dt_brightlifecare_customization.mrp.doctype.mrp.mrp.explode_bom",
				args: {
					mrp_name: frm.doc.name
				},
				callback: function(r) {
					if (!r.exc) {
						frm.reload_doc();
					}
				}
			});
		}
	},

	// get_raw_materials_for_transfer: function (frm) {
	// 	// frm.dirty();

	// 	frappe.call({
	// 		method: "dt_brightlifecare_customization.mrp.doctype.mrp.mrp.get_raw_materials_for_transfer",
	// 		args: {
	// 			mrp_name: frm.doc.name
	// 		},
	// 		callback: function(r) {
	// 			if (!r.exc) {
	// 				frm.reload_doc();
	// 			}
	// 		}
	// 	});
	// },

	get_raw_materials_for_transfer: function (frm) {
		const title = __("Transfer Materials For Warehouse");

		let dialog = new frappe.ui.Dialog({
			title: title,
			fields: [
				{
					label: __("Transfer From Warehouses"),
					fieldtype: "Table MultiSelect",
					fieldname: "warehouses",
					options: "Feeding Warehouse", // <-- this must be a child table doctype with a Link field `warehouse`
					get_query: function () {
						return {
							filters: {
								company: frm.doc.company,
								is_group: 0,
							},
						};
					},
				},
			],
			primary_action_label: __("Get Items"),
			primary_action: function (values) {
				// values.warehouses will be an array of rows (dicts)
				let warehouses = (values.warehouses || []).map(row => row.warehouse);

				if (!warehouses.length) {
					frappe.msgprint(__("Please select at least one warehouse."));
					return;
				}

				frappe.call({
					method: "dt_brightlifecare_customization.mrp.doctype.mrp.mrp.get_raw_materials_for_transfer",
					args: {
						mrp_name: frm.doc.name,
						warehouses: warehouses
					},
					callback: function (r) {
						if (!r.exc) {
							frm.reload_doc();
							frappe.msgprint(__("Raw materials updated using selected warehouses."));
						}
					}
				});

				dialog.hide();
			}
		});

		dialog.show();
	},

	// Populate Sub Assembly Items based on selected BOMs on Material Request Items
	get_sub_assembly_items: function (frm) {
		if (!frm.doc.material_request_items || !frm.doc.material_request_items.length) {
			frappe.msgprint(__('Please add Material Request Items with BOMs first.'));
			return;
		}

		frappe.call({
			method: 'dt_brightlifecare_customization.mrp.doctype.mrp.mrp.get_sub_assembly_items',
			args: { mrp_name: frm.doc.name },
			// freeze: true,
			// freeze_message: __('Collecting sub-assembly items...'),
			callback: function(r) {
				if (!r.exc) {
					frm.reload_doc();
					frappe.show_alert({message: __('Sub-assembly items updated'), indicator: 'green'});
				}
			}
		});
	}


});
