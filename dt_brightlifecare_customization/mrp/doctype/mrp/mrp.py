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
	def on_submit(self):
		create_mrp_reservation_entries(self)


def create_mrp_reservation_entries(mrp_doc):
    for row in mrp_doc.raw_materials:
        plan_to_reserve = row.get("plan_to_reserve") or 0

        if plan_to_reserve > 0:
            reservation = frappe.new_doc("MRP Reservation Entry")
            reservation.item_code = row.item_code
            reservation.warehouse = row.warehouse
            reservation.voucher_type = "MRP"
            reservation.voucher_no = mrp_doc.name
            reservation.voucher_detail_no = row.name

            reservation.stock_uom = row.stock_uom
            reservation.available_qty_to_reserve = row.get("available_for_use") or 0
            reservation.voucher_qty = row.required_qty_in_stock_uom
            reservation.reserved_qty = plan_to_reserve
            reservation.issued_qty = 0
            reservation.transferred_qty = 0
            reservation.balance_reserved_qty = plan_to_reserve
            reservation.company = mrp_doc.company
            reservation.status = "Reserved"

            reservation.save()
            reservation.submit()





@frappe.whitelist()
def explode_bom(mrp_name):
	mrp_doc = frappe.get_doc("MRP", mrp_name)

	# Step 1: Clear previously exploded rows
	mrp_doc.set("mrp_bom_exploded_items", [])

	rm_aggregate = {}
	missing_bom_rows = []

	# Step 2: Explode all BOMs and aggregate RM needs
	for mr_item in mrp_doc.material_request_items:
		if not mr_item.bom_no:
			missing_bom_rows.append(mr_item.item_code or mr_item.name)
			continue

		bom_doc = frappe.get_doc("BOM", mr_item.bom_no)

		for bom_item in bom_doc.exploded_items:
			key = (bom_item.item_code, bom_item.source_warehouse)
			required_qty = (flt(mr_item.material_requested_qty) * flt(bom_item.stock_qty)) / flt(bom_doc.quantity)

			if key not in rm_aggregate:
				rm_aggregate[key] = {
					"item_code": bom_item.item_code,
					"stock_uom": bom_item.stock_uom,
					"source_warehouse": bom_item.source_warehouse,
					"rm_required_qty_in_stock_uom": 0
				}

			rm_aggregate[key]["rm_required_qty_in_stock_uom"] += required_qty

	# Step 3: Throw error if any rows were missing BOM
	if missing_bom_rows:
		frappe.throw(_("BOM not found for items: {0}").format(", ".join(missing_bom_rows)))

	# Step 4: Preload batch availability for all items across all warehouses
	all_item_codes = list({item["item_code"] for item in rm_aggregate.values()})
	batch_availability = {}

	batches = frappe.get_all(
		"Batch",
		filters={
			"item": ["in", all_item_codes],
			"expiry_date": [">", mrp_doc.expected_start_date]
		},
		fields=["name", "item", "batch_qty", "expiry_date"],
		order_by="expiry_date asc"
	)

	for batch in batches:
		batch_availability[batch.name] = flt(batch.batch_qty)

	# 🔁 Step 4.5: Subtract previously allocated batch qtys from submitted MRP documents
	mrp_batch_consumed_qty = frappe.db.sql("""
		SELECT
			allocated_batch.batch_no AS batch_no,
			SUM(CAST(allocated_batch.allocated_qty AS DECIMAL(18,6))) AS total_used
		FROM
			`tabMRP` mrp
		JOIN
			`tabMRP BOM Exploded Item` item ON item.parent = mrp.name
		JOIN
			JSON_TABLE(item.batch_allocation,
				'$[*]' COLUMNS (
					batch_no VARCHAR(140) PATH '$.batch_no',
					allocated_qty DECIMAL(18,6) PATH '$.allocated_qty'
				)
			) AS allocated_batch
		WHERE
			mrp.docstatus = 1
			AND allocated_batch.batch_no IS NOT NULL
		GROUP BY
			allocated_batch.batch_no
	""", as_dict=True)


	for row in mrp_batch_consumed_qty:
		batch_no = row.batch_no
		used_qty = flt(row.total_used)
		if batch_no in batch_availability:
			batch_availability[batch_no] = max(batch_availability[batch_no] - used_qty, 0)

	# Step 5: Process each RM and perform batch allocation
	for key, data in rm_aggregate.items():
		item_code = data["item_code"]
		warehouse = data["source_warehouse"]
		required_qty = flt(data["rm_required_qty_in_stock_uom"])

		# Get stock and reserved (custom)
		bin_data = frappe.db.get_value(
			"Bin",
			{"item_code": item_code, "warehouse": warehouse},
			["actual_qty", "custom_reserved_stock_for_mrp"],
			as_dict=True
		) or {}

		stock_in_hand = flt(bin_data.get("actual_qty", 0))
		reserved_qty = flt(bin_data.get("custom_reserved_stock_for_mrp", 0))
		available_for_use = max(stock_in_hand - reserved_qty, 0)

		plan_to_reserve = min(available_for_use, required_qty)
		plan_to_purchase = required_qty - plan_to_reserve

		# Allocate batch quantities safely from global availability
		remaining_qty = required_qty
		batch_allocation = []

		for batch in batches:
			if batch.item != item_code:
				continue

			available_qty = batch_availability.get(batch.name, 0)

			if available_qty <= 0:
				continue

			# Only use batch if it can fulfill the required_qty
			if available_qty >= required_qty:
				batch_allocation.append({
					"batch_no": batch.name,
					"allocated_qty": required_qty,
					"available_qty_before": available_qty,
					"expiry_date": batch.expiry_date
				})
				# Reduce from global availability
				batch_availability[batch.name] = available_qty - required_qty
				remaining_qty = 0
				break  # ✅ stop after assigning one batch


		primary_batch_no = batch_allocation[0]["batch_no"] if batch_allocation else None

		mrp_doc.append("mrp_bom_exploded_items", {
			"item_code": item_code,
			"stock_uom": data["stock_uom"],
			"warehouse": warehouse,
			"required_qty_in_stock_uom": required_qty,
			"stock_in_hand": stock_in_hand,
			"reserved_stock_for_mrp": reserved_qty,
			"available_for_use": available_for_use,
			"plan_to_reserve": plan_to_reserve,
			"plan_to_purchase": plan_to_purchase,
			"batch_allocation": frappe.as_json(batch_allocation),
			"batch_no": primary_batch_no,
			"material_request_type": "Purchase" if plan_to_purchase > 0 else "Material Transfer"
		})

	# Step 6: Save and confirm
	mrp_doc.save()
	frappe.msgprint(_("BOM Exploded Successfully"))






@frappe.whitelist()
def get_raw_materials_for_transfer(mrp_name):
    mrp = frappe.get_doc("MRP", mrp_name)

    # Clear existing raw_materials
    mrp.set("raw_materials", [])

    for row in mrp.mrp_bom_exploded_items:
        item_code = row.item_code
        required_qty = flt(row.required_qty_in_stock_uom)
        original_warehouse = row.warehouse
        remaining_qty = required_qty

        # Always copy the row as-is first
        if row.material_request_type != "Purchase":
            # For non-purchase rows, copy directly without alternate warehouse logic
            mrp.append("raw_materials", {
                "item_code": row.item_code,
                "stock_uom": row.stock_uom,
                "warehouse": row.warehouse,
                "required_qty_in_stock_uom": row.required_qty_in_stock_uom,
                "stock_in_hand": row.stock_in_hand,
                "reserved_stock_for_mrp": row.reserved_stock_for_mrp,
                "available_for_use": row.available_for_use,
                "plan_to_reserve": row.plan_to_reserve,
                "plan_to_purchase": row.plan_to_purchase,
                "batch_allocation": row.batch_allocation,
                "batch_no": row.batch_no,
                "material_request_type": row.material_request_type
            })
            continue

        # For rows with type "Purchase", check alternate warehouses
        feeding_warehouses = frappe.get_all(
            "Feeding Warehouse",
            filters={"parenttype": "Warehouse"},
            fields=["warehouse"]
        )

        for fw in feeding_warehouses:
            alt_wh = fw.warehouse
            if alt_wh == original_warehouse:
                continue

            bin_data = frappe.db.get_value(
                "Bin",
                {"item_code": item_code, "warehouse": alt_wh},
                ["actual_qty", "custom_reserved_stock_for_mrp"],
                as_dict=True
            ) or {}

            stock_in_hand = flt(bin_data.get("actual_qty", 0))
            reserved_qty = flt(bin_data.get("custom_reserved_stock_for_mrp", 0))
            available = max(stock_in_hand - reserved_qty, 0)

            if available <= 0:
                continue

            alloc_qty = min(available, remaining_qty)

            # Add row for this warehouse with allocated quantity
            mrp.append("raw_materials", {
                "item_code": item_code,
                "stock_uom": row.stock_uom,
                "warehouse": alt_wh,
                "required_qty_in_stock_uom": required_qty,
                "stock_in_hand": stock_in_hand,
                "reserved_stock_for_mrp": reserved_qty,
                "available_for_use": available,
                "plan_to_reserve": alloc_qty,
                "plan_to_purchase": 0,
                "batch_allocation": row.batch_allocation,
                "batch_no": row.batch_no,
                "material_request_type": "Material Transfer"
            })

            remaining_qty -= alloc_qty

            if remaining_qty <= 0:
                break

        # If there is still some quantity left, mark for Purchase
        if remaining_qty > 0:
            mrp.append("raw_materials", {
                "item_code": item_code,
                "stock_uom": row.stock_uom,
                "warehouse": original_warehouse,
                "required_qty_in_stock_uom": required_qty,
                "stock_in_hand": row.stock_in_hand,
                "reserved_stock_for_mrp": row.reserved_stock_for_mrp,
                "available_for_use": row.available_for_use,
                "plan_to_reserve": 0,
                "plan_to_purchase": remaining_qty,
                "batch_allocation": row.batch_allocation,
                "batch_no": row.batch_no,
                "material_request_type": "Purchase"
            })

    mrp.save()
    frappe.msgprint("Raw materials updated with stock split from alternate warehouses.")
