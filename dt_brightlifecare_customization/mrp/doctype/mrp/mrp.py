# Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
from frappe import _



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
