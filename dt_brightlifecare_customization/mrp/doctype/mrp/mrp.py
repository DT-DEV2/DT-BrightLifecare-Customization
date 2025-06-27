# Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
from frappe import _
from frappe.utils import now_datetime, flt, ceil


class MRP(Document):
	def validate(doc):
		pass


	@frappe.whitelist()
	def get_raw_materials(self):
		self.set("raw_materials", [])  # clear existing

		material_map = {}

		# From assembly_items
		for row in self.assembly_items:
			if row.bom_no and frappe.db.exists("BOM", row.bom_no):
				raw_materials = get_raw_materials_from_bom(row.bom_no, row.planned_qty, row.item_code)
				for item in raw_materials:
					key = (item["item_code"], item["warehouse"])
					if key in material_map:
						material_map[key]["required_bom_qty"] += item["required_bom_qty"]
					else:
						material_map[key] = item

		# From sub_assembly_items
		for row in self.sub_assembly_items:
			if row.bom_no and frappe.db.exists("BOM", row.bom_no):
				raw_materials = get_raw_materials_from_bom(row.bom_no, row.qty, row.parent_item_code)
				for item in raw_materials:
					key = (item["item_code"], item["warehouse"])
					if key in material_map:
						material_map[key]["required_bom_qty"] += item["required_bom_qty"]
					else:
						material_map[key] = item

		# Debug print (optional)
		# print(material_map.values())

		for val in material_map.values():
			self.append("raw_materials", val)




def get_raw_materials_from_bom(bom_name, qty=1, parent_item=None):
    raw_items = []
    bom_doc = frappe.get_doc("BOM", bom_name)

    for row in bom_doc.items:
        # Only consider items that DO NOT have their own BOM
        has_bom = frappe.db.exists("BOM", {
            "item": row.item_code,
            "is_active": 1,
            "is_default": 1
        })
        if not has_bom:
            raw_items.append({
                "item_code": row.item_code,
                "item_name": row.item_name,
                "required_bom_qty": flt(row.qty) * flt(qty),
                "uom": row.uom,
                "warehouse": row.source_warehouse or "",
                "parent_item_code": parent_item
            })

    return raw_items




import frappe
from frappe.utils import now_datetime, flt, ceil

@frappe.whitelist()
def allocate_to_bom(mrp_name):
	mrp_doc = frappe.get_doc("MRP", mrp_name)

	for row in mrp_doc.material_request_items:
		# 🔁 Fetch all active BOMs for the item
		bom_list = frappe.get_all(
			"BOM",
			filters={"item": row.item_code, "is_active": 1},
			fields=["name", "custom_priority", "custom_fg_batch_size", 
			        "custom_total_operation_time_for_batch_size", "custom_target_warehouse"]
		)

		# 🔁 Create a log per BOM
		for bom in bom_list:
			log = frappe.new_doc("MRP BOM Allocation Log")
			log.mrp = mrp_doc.name
			log.mrp_date = mrp_doc.posting_date
			log.material_requested = row.item_code
			log.material_requested_detail = row.name
			log.required_by = row.required_by
			log.uom = row.uom
			log.required_qty = row.material_requested_qty
			log.uom_conversion_factor = row.uom_conversion_factor
			log.qty_in_stock_uom = row.qty_in_stock_uom
			log.stock_uom = row.stock_uom
			log.bom_allocation_log_datetime = now_datetime()

			# 🔁 BOM details
			log.bom = bom.name
			log.bom_priority = bom.custom_priority
			log.bom_fg_batch_size = bom.custom_fg_batch_size
			log.operation_time_per_batch_size = bom.custom_total_operation_time_for_batch_size
			log.bom_warehouse = bom.custom_target_warehouse

			log.save()

	frappe.msgprint("MRP BOM Allocation Logs created for all active BOMs.")
