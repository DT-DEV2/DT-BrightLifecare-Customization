# Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
from frappe import _
from frappe.utils import now_datetime, flt, get_time, getdate
from datetime import datetime, timedelta
import time

class MRP(Document):
	pass



@frappe.whitelist()
def calculate_bom_allocation(mrp_name):
	mrp = frappe.get_doc("MRP", mrp_name)

	if mrp.allocation_status == "In Progress":
		frappe.throw("BOM Allocation is already in progress. Please wait...")

	mrp.db_set("allocation_status", "In Progress")
	frappe.enqueue("dt_brightlifecare_customization.mrp.doctype.mrp.mrp.run_calculate_bom_allocation", 
					queue="long", job_name=f"bom_allocation_{mrp_name}",
					mrp_name=mrp_name)



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
def run_calculate_bom_allocation(mrp_name, user=None):
	try:
		mrp_doc = frappe.get_doc("MRP", mrp_name)

		existing_logs = frappe.get_all(
			"MRP BOM Allocation Log",
			filters={"mrp": mrp_doc.name},
			fields=["name"]
		)
		boms_total = 0
		boms_processed = 0
		
		if existing_logs:
			for log in existing_logs:
				bom_log = frappe.get_doc("MRP BOM Allocation Log", log.name)
				bom_log.db_set('disabled', 1)


		for row in mrp_doc.material_request_items:
			bom_list = frappe.get_all("BOM", filters={"item": row.item_code, "is_active": 1, "docstatus": 1})
			if bom_list:
				boms_total += len(bom_list)

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
					log.bom = bom_doc.name
					log.bom_qty = bom_doc.quantity
					log.bom_priority = bom_doc.custom_priority
					log.bom_fg_batch_size = bom_doc.custom_fg_batch_size
					log.operation_time_per_batch_size = bom_doc.custom_total_operation_time_for_batch_size
					log.bom_warehouse = bom_doc.custom_source_warehouse
					log.workstation = bom_doc.custom_workstation
					print(f"Processing BOM: {bom_doc.name} for MRP: {mrp_doc.name}")

					if log.operation_time_per_batch_size and log.qty_in_stock_uom:
						log.total_number_of_batches = flt(row.qty_in_stock_uom) / flt(bom_doc.custom_fg_batch_size)

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

						if log.ideal_production_start_datetime and log.ideal_production_end_datetime:

							# Ensure these are already set
							ideal_start = log.ideal_production_start_datetime
							ideal_end = log.ideal_production_end_datetime
							operation_hours_required = flt(log.total_operation_time) / 60
							operation_duration = timedelta(hours=operation_hours_required)

							# Step 1: Try ideal window
							conflict = frappe.db.sql("""
								SELECT name FROM `tabJob Card`
								WHERE workstation = %s
								AND status = 'Open'
								AND (%s < expected_end_date AND %s > expected_start_date)
							""", (
								bom_doc.custom_workstation,
								ideal_start, ideal_end
							))

							if not conflict:
								log.expected_production_start_datetime = ideal_start
								log.expected_production_end_datetime = ideal_end
								log.workstation_availability = "Available"
								
							else:
								# Step 2: Step back in 1-hour intervals from ideal_end
								cursor = ideal_end - timedelta(hours=1)
								now = frappe.utils.now_datetime()

								# Extract shift details
								shift_start = shift_info["start_time"]
								shift_end = shift_info["end_time"]
								holidays = shift_info["holidays"]

								while cursor > now:
									slot_end = cursor
									slot_start = slot_end - operation_duration

									# Skip if it's a holiday
									if slot_start.date() in holidays:
										cursor -= timedelta(hours=1)
										continue

									# Skip if slot start/end is outside shift hours
									if not (shift_start <= slot_start.time() <= shift_end and shift_start <= slot_end.time() <= shift_end):
										cursor -= timedelta(hours=1)
										continue

									# Optional: skip weekends
									if slot_start.weekday() >= 5:
										cursor -= timedelta(hours=1)
										continue

									# Check for overlapping Job Cards
									conflict = frappe.db.sql("""
										SELECT name FROM `tabJob Card`
										WHERE workstation = %s
										AND status = 'Open'
										AND (%s < expected_end_date AND %s > expected_start_date)
									""", (
										bom_doc.custom_workstation,
										slot_start, slot_end
									))

									if not conflict:
										log.expected_production_start_datetime = slot_start
										log.expected_production_end_datetime = slot_end
										log.workstation_availability = "Available"
										break

									cursor -= timedelta(hours=1)

								# If no slot found
								if not log.expected_production_start_datetime:
									log.workstation_availability = "Unavailable"
					log.save()
		
					# Simulate time-consuming work (remove in production)
					time.sleep(0.2)

					# Update progress
					boms_processed += 1
					frappe.publish_realtime(
						"mrp_bom_allocation_progress",
						{
							"progress": int((boms_processed / boms_total) * 100),
							"message": f"Processing BOM {bom.name} ({boms_processed}/{boms_total})"
						},
						user=user
					)
			else:
				frappe.publish_realtime(
					"mrp_bom_allocation_progress",
					{
						"progress": 100,
						"message": "No active BOMs found for any items."
					},
					user=user
				)
				mrp_doc.db_set("allocation_status", "Completed")
				return
		frappe.publish_realtime(
			"mrp_bom_allocation_progress",
			{
				"progress": 100,
				"message": "Allocation complete."
			},
			user=user
		)
		mrp_doc.save()
		mrp_doc.db_set("allocation_status", "Completed")

	except Exception as e:
		frappe.publish_realtime("mrp_bom_allocation_progress", {
			"progress": 100,
			"failed": True,
			"message": f"Error: {str(e)}",
		}, user=frappe.session.user)
		frappe.db.set_value("MRP", mrp_name, "allocation_status", "Failed")
		frappe.log_error("BOM Allocation Failed", frappe.get_traceback())





@frappe.whitelist()
def allocate_bom(mrp_name):
	mrp_doc = frappe.get_doc("MRP", mrp_name)
	mrp_doc.set("mrp_bom_allocation_detail", [])

	for mr_item in mrp_doc.material_request_items:

		# Get all available allocation logs for this item, ordered by priority
		allocation_log = frappe.db.sql("""
			SELECT
				name, bom, bom_fg_batch_size, bom_warehouse, bom_priority, workstation, expected_production_start_datetime, expected_production_end_datetime
			FROM
				`tabMRP BOM Allocation Log`
			WHERE
				mrp = %(mrp)s AND
				material_requested = %(item_code)s AND
				material_requested_detail = %(detail_name)s AND
				disabled = 0 AND
				workstation_availability = 'Available'
			ORDER BY
				bom_fg_batch_size DESC,
				bom_priority ASC
			LIMIT 1
		""", {
			"mrp": mrp_doc.name,
			"item_code": mr_item.item_code,
			"detail_name": mr_item.name
		}, as_dict=True)

		row = {
			"fg_item_code": mr_item.item_code,
			"fg_quantity": mr_item.material_requested_qty,
		}

		if allocation_log:
			row.update({
				"allocated_bom_no": allocation_log[0].bom,
				"fg_batch_size": allocation_log[0].bom_fg_batch_size,
				"warehouse": allocation_log[0].bom_warehouse,
				"priority": allocation_log[0].bom_priority,
				"workstation": allocation_log[0].workstation,
				"expected_production_start_datetime": allocation_log[0].expected_production_start_datetime,
				"expected_production_end_datetime": allocation_log[0].expected_production_end_datetime,
				"qty_in_stock_uom": mr_item.qty_in_stock_uom,
				"uom_conversion_factor": mr_item.uom_conversion_factor,
				"stock_uom": mr_item.stock_uom,
				"uom": mr_item.uom,
				"material_request": mr_item.material_request,
				"material_request_item_detail": mr_item.material_request_item_detail,
			})

		mrp_doc.append("mrp_bom_allocation_detail", row)

	mrp_doc.save()
	frappe.msgprint("MRP BOM Allocation Detail rows created.")








@frappe.whitelist()
def explode_bom(mrp_name):
	mrp_doc = frappe.get_doc("MRP", mrp_name)

	# Step 1: Clear old exploded items
	mrp_doc.set("mrp_bom_exploded_items", [])

	# Step 2: Temp dict to accumulate RM qtys
	rm_aggregate = {}

	for allocation in mrp_doc.mrp_bom_allocation_detail:
		if not allocation.allocated_bom_no:
			continue

		bom_doc = frappe.get_doc("BOM", allocation.allocated_bom_no)

		for item in bom_doc.exploded_items:
			key = (item.item_code, item.source_warehouse)
			rm_required_qty = (allocation.fg_quantity * item.stock_qty) / bom_doc.quantity

			if key not in rm_aggregate:
				rm_aggregate[key] = {
					"item_code": item.item_code,
					"stock_uom": item.stock_uom,
					"source_warehouse": item.source_warehouse,
					"rm_required_qty_in_stock_uom": 0,
					"required_datetime": allocation.expected_production_start_datetime
				}

			rm_aggregate[key]["rm_required_qty_in_stock_uom"] += rm_required_qty

	# Step 3: Track batch consumption across all items
	batch_availability = {}

	for key, data in rm_aggregate.items():
		item_code = data["item_code"]
		warehouse = data["source_warehouse"]
		required_qty = data["rm_required_qty_in_stock_uom"]
		production_date = data["required_datetime"]

		# Get stock in hand
		stock_in_hand = frappe.db.get_value("Bin", {"item_code": item_code, "warehouse": warehouse}, "actual_qty") or 0

		# Find eligible batches
		batches = frappe.get_all(
			"Batch",
			filters={
				"item": item_code,
				"expiry_date": [">", production_date]
			},
			fields=["name", "batch_qty", "expiry_date"],
			order_by="expiry_date asc"
		)

		remaining_qty = required_qty
		batch_allocation = []

		for batch in batches:
			# Initialize availability
			available_qty = batch_availability.get(batch.name, batch.batch_qty or 0)

			if available_qty <= 0:
				continue

			allocated_qty = min(available_qty, remaining_qty)

			batch_allocation.append({
				"batch_no": batch.name,
				"allocated_qty": allocated_qty,
				"available_qty_before": available_qty,
				"expiry_date": batch.expiry_date
			})

			# Reduce from batch_availability
			batch_availability[batch.name] = available_qty - allocated_qty
			remaining_qty -= allocated_qty

			if remaining_qty <= 0:
				break

		primary_batch_no = batch_allocation[0]["batch_no"] if batch_allocation else None

		mrp_doc.append("mrp_bom_exploded_items", {
			"item_code": item_code,
			"stock_uom": data["stock_uom"],
			"warehouse": warehouse,
			"required_qty_in_stock_uom": required_qty,
			"stock_in_hand": stock_in_hand,
			"available_for_use": stock_in_hand,
			"batch_allocation": frappe.as_json(batch_allocation),
			"batch_no": primary_batch_no  # ✅ store the primary batch
		})


	# Step 4: Save
	mrp_doc.save(ignore_permissions=True)
	frappe.msgprint("Exploded BOM items updated in `mrp_bom_exploded_items` with batch allocation.")
