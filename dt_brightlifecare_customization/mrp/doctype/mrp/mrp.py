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
from frappe.utils import now_datetime, flt, get_time, getdate
from datetime import datetime, timedelta

def get_shift_config(warehouse):
	shift_type = frappe.db.get_value("Warehouse", warehouse, "custom_shift_type")
	if not shift_type:
		return {
			"start_time": get_time("00:00:00"),
			"end_time": get_time("23:59:00"),
			"working_minutes": 1440,
			"holidays": set()
		}

	shift = frappe.get_doc("Shift Type", shift_type)
	start_time = get_time(shift.start_time) if shift.start_time else get_time("00:00:00")
	end_time = get_time(shift.end_time) if shift.end_time else get_time("23:59:00")

	working_minutes = int(
		(datetime.combine(datetime.today(), end_time) - datetime.combine(datetime.today(), start_time)).total_seconds() / 60
	)

	holidays = set()
	if shift.holiday_list:
		holidays = {
			h.holiday_date for h in frappe.get_all(
				"Holiday",
				filters={"parent": shift.holiday_list},
				fields=["holiday_date"]
			)
		}

	return {
		"start_time": start_time,
		"end_time": end_time,
		"working_minutes": working_minutes,
		"holidays": holidays
	}

@frappe.whitelist()
def calculate_bom_allocation(mrp_name):
	mrp_doc = frappe.get_doc("MRP", mrp_name)

	for row in mrp_doc.material_request_items:
		bom_list = frappe.get_all(
			"BOM",
			filters={"item": row.item_code, "is_active": 1},
			fields=["name", "custom_priority", "custom_fg_batch_size", 
			        "custom_total_operation_time_for_batch_size", "custom_target_warehouse"]
		)

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
   
			bom_doc = frappe.get_doc("BOM", bom.name)
			log.bom = bom.name
			log.bom_qty = bom_doc.quantity
			log.bom_priority = bom.custom_priority
			log.bom_fg_batch_size = bom.custom_fg_batch_size
			log.operation_time_per_batch_size = bom.custom_total_operation_time_for_batch_size
			log.bom_warehouse = bom.custom_target_warehouse

			if log.operation_time_per_batch_size and log.qty_in_stock_uom:
				log.total_number_of_batches = flt(log.qty_in_stock_uom) / flt(log.operation_time_per_batch_size)

			if log.total_number_of_batches and log.operation_time_per_batch_size:
				log.total_operation_time = flt(log.total_number_of_batches) * flt(log.operation_time_per_batch_size)

			total_operation_minutes = flt(log.total_operation_time or 0)

			if total_operation_minutes > 0 and row.required_by:
				if isinstance(row.required_by, str):
					required_by = datetime.strptime(row.required_by, "%Y-%m-%d")
				elif isinstance(row.required_by, datetime):
					required_by = row.required_by
				else:
					required_by = row.required_by

				shift_info = get_shift_config(log.bom_warehouse)
				start_time = shift_info["start_time"]
				end_time = shift_info["end_time"]
				working_minutes_per_day = shift_info["working_minutes"]
				holidays = shift_info["holidays"]

				# Calculate ideal production end datetime (day before required_by)
				ideal_end_date = getdate(required_by) - timedelta(days=1)
				ideal_production_end_datetime = datetime.combine(ideal_end_date, end_time)

				remaining_minutes = total_operation_minutes
				current_date = ideal_end_date
				ideal_start_datetime = None

				while True:
					if current_date in holidays or current_date.weekday() >= 5:
						current_date -= timedelta(days=1)
						continue

					if remaining_minutes <= working_minutes_per_day:
						# Partial or full-day usage
						start_time_actual = (datetime.combine(current_date, end_time) - timedelta(minutes=remaining_minutes)).time()
						ideal_start_datetime = datetime.combine(current_date, start_time_actual)
						break

					# If not break, consume full day
					remaining_minutes -= working_minutes_per_day
					current_date -= timedelta(days=1)


				log.ideal_production_start_datetime = ideal_start_datetime
				log.ideal_production_end_datetime = ideal_production_end_datetime
   

     
		


			log.save()

	frappe.msgprint("MRP BOM Allocation Logs created with ideal production windows.")
