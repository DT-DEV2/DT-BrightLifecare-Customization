# Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
from frappe import _
from frappe.utils import now_datetime, flt, get_time, getdate, nowdate, add_days
from datetime import datetime, timedelta
import time

from erpnext.manufacturing.doctype.work_order.work_order import make_stock_entry


def _get_wip_warehouse(fg_warehouse):
    """Return custom WIP warehouse configured on the finished good warehouse."""
    if not fg_warehouse:
        return None

    return frappe.db.get_value(
        "Warehouse",
        fg_warehouse,
        "custom_workinprogress_warehouse",
    )

class MRP(Document):
    def on_submit(self):
        create_mrp_reservation_entries(self)
    
    def validate(self):
        validate_qty(self)
        get_sub_assembly_items(self)
        explode_bom(self)



def validate_qty(mrp_doc):

	if not mrp_doc.material_request_items:
		return

	errors = []

	for item in mrp_doc.material_request_items:
		# skip rows without proper MR linkage
		if not item.material_request or not item.material_request_item_detail:
			continue

		# get original qty from Material Request Item
		mr_item = frappe.db.get_value(
			"Material Request Item",
			item.material_request_item_detail,
			["qty", "name", "idx"],
			as_dict=True
		)

		if not mr_item:
			errors.append(f"Material Request Item {item.material_request_item_detail} not found for MR {item.material_request}")
			continue

		mr_item_qty = flt(mr_item.qty)

		# sum material_requested_qty from OTHER MRPs (docstatus < 2), exclude current MRP
		already_created = frappe.db.sql("""
			SELECT COALESCE(SUM(material_requested_qty), 0) AS s
			FROM `tabMRP Material Request Item`
			WHERE material_request = %s
				AND material_request_item_detail = %s
				AND parent != %s
				AND docstatus < 2
		""", (item.material_request, item.material_request_item_detail, mrp_doc.name), as_dict=True)

		already_created_qty = flt(already_created[0].s) if already_created else 0.0

		this_row_qty = flt(item.material_requested_qty or 0.0)
		total_after_this_mrp = already_created_qty + this_row_qty

		if total_after_this_mrp > mr_item_qty:
			errors.append(
				_(
					"Material Request <b>{mr}</b>, Item <b>{mr_item}</b>: "
					"Allowed Qty = <b>{mr_q}</b>, "
					"Already Requested = <b>{already}</b>, "
					"This MRP Qty = <b>{this}</b>, "
					"Total = <b>{total}</b>"
				).format(
					mr=item.material_request,
					mr_item=item.material_request_item_detail,
					mr_q=mr_item_qty,
					already=already_created_qty,
					this=this_row_qty,
					total=total_after_this_mrp,
				)
			)


	if errors:
		frappe.throw("Some MRP rows would exceed their Material Request item quantities:\n\n" + "\n".join(errors))


	if mrp_doc.material_request_items:
		for i in mrp_doc.material_request_items:
			if flt(i.material_requested_qty) and i.uom_conversion_factor:
				qty_in_stock_uom = flt(i.material_requested_qty) * flt(i.uom_conversion_factor)
				i.qty_in_stock_uom = qty_in_stock_uom


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
            reservation.batch_no = row.batch_no

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




def _get_reserved_lookup(item_wh_pairs):
    """Return a dict keyed by (item_code, warehouse) -> sum(balance_reserved_qty) of submitted MRP reservations."""
    if not item_wh_pairs:
        return {}

    items = list({i for i, _ in item_wh_pairs})
    whs = list({w for _, w in item_wh_pairs})

    rows = frappe.get_all(
        "MRP Reservation Entry",
        filters={
            "docstatus": 1,
            "item_code": ["in", items],
            "warehouse": ["in", whs],
        },
        fields=["item_code", "warehouse", "sum(balance_reserved_qty) as reserved"],
        group_by="item_code, warehouse",
    )

    out = {}
    for r in rows:
        out[(r.get("item_code"), r.get("warehouse"))] = flt(r.get("reserved") or 0)
    return out



@frappe.whitelist()
def explode_bom(doc):
	from erpnext.stock.doctype.batch.batch import get_batch_qty

	mrp_doc = doc

	# Step 1: Clear previously rows
	mrp_doc.set("raw_materials", [])
	# new_raw_materials = []

	rm_aggregate = {}
	missing_bom_rows = []

	# Step 2: Explode all BOMs and aggregate RM needs
	for mr_item in mrp_doc.material_request_items:
		if not mr_item.bom_no:
			missing_bom_rows.append(mr_item.item_code or mr_item.name)
			continue

		bom_doc = frappe.get_doc("BOM", mr_item.bom_no)

		for bom_item in bom_doc.exploded_items:
			# Preserve both source and destination so transfers can be grouped correctly
			for_warehouse = getattr(mr_item, "warehouse", None)
			key = (bom_item.item_code, bom_item.source_warehouse, for_warehouse)
			required_qty = (flt(mr_item.material_requested_qty) * flt(bom_item.stock_qty)) / flt(bom_doc.quantity)

			if key not in rm_aggregate:
				rm_aggregate[key] = {
					"item_code": bom_item.item_code,
					"stock_uom": bom_item.stock_uom,
					"source_warehouse": bom_item.source_warehouse,
					"for_warehouse": for_warehouse,
					"rm_required_qty_in_stock_uom": 0,
				}

			rm_aggregate[key]["rm_required_qty_in_stock_uom"] += required_qty

	# Step 3: Throw error if any rows were missing BOM
	if missing_bom_rows:
		frappe.throw(_("BOM not found for items: {0}").format(", ".join(missing_bom_rows)))

	# Step 4: Preload batch expiry info
	all_item_codes = list({item["item_code"] for item in rm_aggregate.values()})
	batch_expiry_lookup = {
		b.name: b.expiry_date for b in frappe.get_all(
			"Batch",
			filters={"item": ["in", all_item_codes]},
			fields=["name", "expiry_date"]
		)
	}

	# Step 4.1: Reserved lookup from submitted MRP reservations per (item, source_warehouse)
	item_wh_pairs = {(d["item_code"], d["source_warehouse"]) for d in rm_aggregate.values() if d.get("source_warehouse")}
	reserved_lookup = _get_reserved_lookup(item_wh_pairs)

	# Step 4.5: Subtract previously allocated batch qtys from submitted MRP documents
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

	consumed_qty_by_batch = {row.batch_no: flt(row.total_used) for row in mrp_batch_consumed_qty}

	# Step 5: Process each RM and perform batch allocation
	for key, data in rm_aggregate.items():
		item_code = data["item_code"]
		original_warehouse = data["source_warehouse"]
		for_warehouse = data.get("for_warehouse")
		required_qty = flt(data["rm_required_qty_in_stock_uom"])

		# Get stock and reserved (derive reserved from submitted MRP Reservation Entries)
		bin_data = frappe.db.get_value(
			"Bin",
			{"item_code": item_code, "warehouse": original_warehouse},
			["actual_qty"],
			as_dict=True
		) or {}

		stock_in_hand = flt(bin_data.get("actual_qty", 0))
		reserved_qty = flt(reserved_lookup.get((item_code, original_warehouse), 0))
		available_for_use = max(stock_in_hand - reserved_qty, 0)

		# Determine if item is batch-tracked; non-batch items should still transfer from stock
		has_batch_no = frappe.db.get_value("Item", item_code, "has_batch_no")

		batch_allocation = []
		allocated_from_stock = 0.0
		primary_batch_no = None

		if has_batch_no and original_warehouse:
			# --- Batch availability (exclude batches already consumed by submitted MRPs) ---
			batchwise_qty = get_batch_qty(item_code=item_code, warehouse=original_warehouse)
			if isinstance(batchwise_qty, list):
				batchwise_qty = {b.get("batch_no"): b.get("qty") for b in batchwise_qty if b.get("batch_no")}
			else:
				batchwise_qty = batchwise_qty or {}

			if consumed_qty_by_batch:
				batchwise_qty = {
					batch_no: qty
					for batch_no, qty in batchwise_qty.items()
					if batch_no not in consumed_qty_by_batch
				}

			sorted_batches = sorted(
				batchwise_qty.items(),
				key=lambda b: batch_expiry_lookup.get(b[0]) or frappe.utils.getdate("2999-12-31")
			)

			# --- Allocate from stock only if a single batch can satisfy the need ---
			need_from_stock = min(required_qty, available_for_use)
			if need_from_stock > 0:
				selected_batch = None
				for batch_no, available_qty in sorted_batches:
					if flt(available_qty) >= need_from_stock:
						selected_batch = (batch_no, available_qty)
						break

				if selected_batch:
					batch_no, available_qty = selected_batch
					take = flt(need_from_stock)
					batch_allocation.append({
						"batch_no": batch_no,
						"allocated_qty": take,
						"available_qty_before": flt(available_qty),
						"expiry_date": batch_expiry_lookup.get(batch_no)
					})
					allocated_from_stock += take
					primary_batch_no = batch_no
		else:
			# Non-batch or no source warehouse → simple allocation up to available_for_use
			allocated_from_stock = min(required_qty, available_for_use)
			batch_allocation = []
			primary_batch_no = None

		# Compute remaining qty and round to field precision to avoid 0-qty Purchase rows
		qty_precision = frappe.get_precision("MRP Raw Material", "plan_to_purchase") or 6
		remaining_qty = flt(max(required_qty - allocated_from_stock, 0.0), qty_precision)
		allocated_from_stock = flt(allocated_from_stock, qty_precision)

		# --- Row 1: Material Transfer for the qty satisfied from stock ---
		if allocated_from_stock > 0:
			mrp_doc.append("raw_materials", {
				"item_code": item_code,
				"stock_uom": data["stock_uom"],
				"warehouse": original_warehouse,
				"for_warehouse": for_warehouse,
				"required_qty_in_stock_uom": required_qty,
				"stock_in_hand": stock_in_hand,
				"reserved_stock_for_mrp": reserved_qty,
				"available_for_use": available_for_use,
				"plan_to_reserve": allocated_from_stock,
				"plan_to_purchase": 0,
				"batch_allocation": frappe.as_json(batch_allocation),
				"batch_no": primary_batch_no,
				"material_request_type": "Material Transfer",
			})

		# --- Row 2: Purchase for the remaining qty ---
		if remaining_qty > 0:
			mrp_doc.append("raw_materials", {
				"item_code": item_code,
				"stock_uom": data["stock_uom"],
				"warehouse": None,  # purchase has no from-warehouse
				"for_warehouse": for_warehouse,
				"required_qty_in_stock_uom": required_qty,
				"stock_in_hand": stock_in_hand,
				"reserved_stock_for_mrp": reserved_qty,
				"available_for_use": available_for_use,
				"plan_to_reserve": 0,
				"plan_to_purchase": remaining_qty,
				"batch_allocation": "[]",
				"batch_no": None,
				"material_request_type": "Purchase",
			})

	# Step 6: Save and confirm
	# mrp_doc.save()
	frappe.msgprint(_("BOM Exploded Successfully"))




@frappe.whitelist()
def get_raw_materials_for_transfer(mrp_name, warehouses=None):
	from erpnext.stock.doctype.batch.batch import get_batch_qty
	from frappe.utils import getdate, nowdate
	import json
	

	if isinstance(warehouses, str):
		try:
			warehouses = json.loads(warehouses)
		except Exception:
			warehouses = []

	mrp = frappe.get_doc("MRP", mrp_name)
	explode_bom(mrp)

	# Precompute submitted MRP batch consumption so we don't double-allocate the same batch
	mrp_batch_consumed_qty = frappe.db.sql(
		"""
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
		""",
		as_dict=True,
	)

	consumed_qty_by_batch = {row.batch_no: flt(row.total_used) for row in mrp_batch_consumed_qty}

	# Precision for rounding
	reserve_precision = frappe.get_precision("MRP Raw Material", "plan_to_reserve") or 6
	purchase_precision = frappe.get_precision("MRP Raw Material", "plan_to_purchase") or 6

	# Build reserved lookup for selected warehouses and items in Purchase rows
	purchase_items = {r.item_code for r in mrp.raw_materials if r.material_request_type == 'Purchase'}
	selected_whs = set(warehouses or [])
	reserved_pairs = {(i, w) for i in purchase_items for w in selected_whs}
	reserved_lookup = _get_reserved_lookup(reserved_pairs)

	for row in mrp.raw_materials[:]:	# iterate safely over a copy
		if row.material_request_type == 'Purchase':
			item_code = row.item_code
			required_qty = flt(row.required_qty_in_stock_uom)
			remaining_qty = required_qty
			total_transferred_qty = 0
			has_batch_no = frappe.db.get_value("Item", item_code, "has_batch_no")

			# Get expiry dates of all batches for the item
			batch_expiry_lookup = {
				b.name: b.expiry_date for b in frappe.get_all(
					"Batch",
					filters={"item": item_code},
					fields=["name", "expiry_date"]
				)
			}

			# Iterate over warehouses selected by user
			for alt_wh in warehouses:
				if remaining_qty <= 0:
					break

				# Compute availability in this warehouse (actual - reserved)
				bin_data = frappe.db.get_value(
					"Bin",
					{"item_code": item_code, "warehouse": alt_wh},
					["actual_qty"],
					as_dict=True,
				) or {}

				stock_in_hand = flt(bin_data.get("actual_qty", 0))
				reserved_qty = flt(reserved_lookup.get((item_code, alt_wh), 0))
				available_for_use = max(stock_in_hand - reserved_qty, 0)

				if flt(available_for_use) <= 0:
					continue

				if has_batch_no:
					# Batch-wise allocation mirroring explode_bom
					batchwise_qty = get_batch_qty(item_code=item_code, warehouse=alt_wh)
					if isinstance(batchwise_qty, list):
						batchwise_qty = {
							b.get("batch_no"): flt(b.get("qty")) for b in batchwise_qty if b.get("batch_no")
						}
					else:
						batchwise_qty = batchwise_qty or {}

					# Drop batches already consumed by submitted MRPs entirely
					if consumed_qty_by_batch:
						batchwise_qty = {
							batch_no: qty
							for batch_no, qty in batchwise_qty.items()
							if batch_no not in consumed_qty_by_batch
						}

					# Filter out expired batches
					batchwise_qty = {
						batch_no: qty
						for batch_no, qty in batchwise_qty.items()
						if (not batch_expiry_lookup.get(batch_no))
						or getdate(batch_expiry_lookup[batch_no]) >= getdate(nowdate())
					}

					# Sort batches by expiry date (FEFO)
					sorted_batches = sorted(
						batchwise_qty.items(),
						key=lambda b: batch_expiry_lookup.get(b[0]) or getdate("2999-12-31"),
					)

					need_from_stock = min(remaining_qty, available_for_use)
					if need_from_stock <= 0:
						continue

					batch_allocation = []
					allocated_from_wh = 0
					selected_batch = None
					for batch_no, available_qty in sorted_batches:
						if flt(available_qty) >= need_from_stock:
							selected_batch = (batch_no, available_qty)
							break

					if not selected_batch:
						continue

					batch_no, available_qty = selected_batch
					take = flt(need_from_stock, reserve_precision)
					batch_allocation.append(
						{
							"batch_no": batch_no,
							"allocated_qty": take,
							"available_qty_before": flt(available_qty),
							"expiry_date": batch_expiry_lookup.get(batch_no),
						}
					)

					allocated_from_wh = take

					if allocated_from_wh > 0:
						new_row = mrp.append("raw_materials", {})
						for field in row.as_dict():
							if field not in [
								"name",
								"idx",
								"required_qty_in_stock_uom",
								"warehouse",
								"material_request_type",
								"plan_to_reserve",
								"plan_to_purchase",
								"batch_no",
								"batch_allocation",
							]:
								new_row.set(field, row.get(field))

						new_row.required_qty_in_stock_uom = required_qty
						new_row.warehouse = alt_wh
						new_row.stock_in_hand = stock_in_hand
						new_row.reserved_stock_for_mrp = reserved_qty
						new_row.available_for_use = available_for_use
						new_row.plan_to_reserve = allocated_from_wh
						new_row.plan_to_purchase = 0
						new_row.batch_allocation = frappe.as_json(batch_allocation)
						new_row.batch_no = batch_allocation[0]["batch_no"] if batch_allocation else None
						new_row.material_request_type = "Material Transfer"

						remaining_qty = flt(remaining_qty - allocated_from_wh, purchase_precision)
						total_transferred_qty += allocated_from_wh
				else:
					# Non-batch item: simple allocation up to available_for_use
					alloc_qty = flt(min(remaining_qty, available_for_use), reserve_precision)
					if alloc_qty <= 0:
						continue

					new_row = mrp.append("raw_materials", {})
					for field in row.as_dict():
						if field not in [
							"name",
							"idx",
							"required_qty_in_stock_uom",
							"warehouse",
							"material_request_type",
							"plan_to_reserve",
							"plan_to_purchase",
							"batch_no",
							"batch_allocation",
						]:
							new_row.set(field, row.get(field))

					new_row.required_qty_in_stock_uom = required_qty
					new_row.warehouse = alt_wh
					new_row.stock_in_hand = stock_in_hand
					new_row.reserved_stock_for_mrp = reserved_qty
					new_row.available_for_use = available_for_use
					new_row.plan_to_reserve = alloc_qty
					new_row.plan_to_purchase = 0
					new_row.batch_allocation = frappe.as_json([])
					new_row.batch_no = None
					new_row.material_request_type = "Material Transfer"

					remaining_qty = flt(remaining_qty - alloc_qty, purchase_precision)
					total_transferred_qty += alloc_qty

			# ✅ Adjust the original Purchase row
			if total_transferred_qty > 0:
				# Round remaining qty to field precision to avoid 0-qty purchase rows
				remaining_qty = flt(remaining_qty, purchase_precision)

				if remaining_qty > 0:
					# Keep purchase row but reflect balance
					row.required_qty_in_stock_uom = required_qty   # keep full
					row.plan_to_reserve = 0
					row.plan_to_purchase = remaining_qty
					row.material_request_type = "Purchase"
					# keep original destination warehouse on row.for_warehouse
				else:
					# Fully satisfied → remove the original Purchase row
					mrp.raw_materials.remove(row)


	mrp.save()
	frappe.msgprint("Raw materials updated with selected warehouses")


@frappe.whitelist()
def get_sub_assembly_items(doc):
    """Populate `sub_assembly_items` from BOMs of Material Request Items.
    Logic:
    - For each Material Request Item with a BOM, find BOM Item rows that reference a sub-BOM (bom_no set).
    - Compute required sub-assembly qty in stock UOM using: 
      required_stock_qty = fg_qty_in_stock_uom * (child.stock_qty / parent_bom.quantity)
    - Append rows into `sub_assembly_items` with key fields (item, parent FG, qty, BOM, warehouses, UOMs).
    """
    mrp = doc

    # Clear existing sub-assembly rows
    mrp.set("sub_assembly_items", [])

    for mr_item in mrp.get("material_request_items", []):
        bom_no = mr_item.get("bom_no")
        if not bom_no:
            # skip rows without BOM
            continue

        try:
            bom_doc = frappe.get_doc("BOM", bom_no)
        except Exception:
            continue

        parent_bom_qty = flt(bom_doc.quantity) or 1.0

        # Finished good qty in stock UOM on the MR row
        fg_qty_stock = flt(mr_item.get("qty_in_stock_uom"))
        if not fg_qty_stock:
            # fallback to material_requested_qty * uom_conversion_factor
            fg_qty_stock = flt(mr_item.get("material_requested_qty")) * flt(mr_item.get("uom_conversion_factor") or 1.0)

        # Fetch direct BOM items that have a sub-BOM reference (i.e., sub-assemblies)
        bom_items = frappe.get_all(
            "BOM Item",
            filters={"parent": bom_no},
            fields=["item_code", "uom", "stock_qty", "qty", "bom_no"],
            order_by="idx asc",
        )

        for bi in bom_items:
            if not bi.get("bom_no"):
                # only consider items that are themselves assemblies (i.e., point to another BOM)
                continue

            item_code = bi.get("item_code")
            try:
                item_doc = frappe.get_cached_doc("Item", item_code)
            except Exception:
                continue

            stock_uom = item_doc.stock_uom
            # child.stock_qty is per parent BOM's quantity
            child_stock_per_parent = flt(bi.get("stock_qty") or 0)
            if child_stock_per_parent <= 0:
                # fall back to qty (in item's UOM) if stock_qty missing
                child_stock_per_parent = flt(bi.get("qty") or 0)

            required_stock_qty = 0.0
            if parent_bom_qty > 0:
                required_stock_qty = fg_qty_stock * (child_stock_per_parent / parent_bom_qty)

            # Append to child table
            mrp.append("sub_assembly_items", {
                "production_item": item_code,
                "item_name": item_doc.item_name,
                "parent_item_code": mr_item.get("item_code"),
                "fg_warehouse": mr_item.get("warehouse"),
                "qty": flt(required_stock_qty),
                "bom_no": bi.get("bom_no"),
                "uom": bi.get("uom") or stock_uom,
                "stock_uom": stock_uom,
                "mrp_item": mr_item.get("name"),
                "type_of_manufacturing": "In House",
            })

    # mrp.save()
    frappe.msgprint(_("Sub-assembly items updated from BOMs"))
    # return True

@frappe.whitelist()
def make_material_request(mrp_name):
    """Create Material Request(s) from MRP.raw_materials similar to Production Plan.
    - Creates up to two Material Requests: one for Purchase, one for Material Transfer.
    - Aggregates by item + target warehouse for cleaner docs.
    Returns list of created docs.
    """
    mrp = frappe.get_doc("MRP", mrp_name)

    created = []
    work_orders_created = []
    stock_entries_created = []


    # Build per-row entries so we can set custom_mrp_raw_material_item accurately
    purchase_entries = []
    transfer_entries = []

    for row in mrp.get("raw_materials", []):
        # Only consider positive planned quantities
        ptp = flt(row.get("plan_to_purchase") or 0)
        ptr = flt(row.get("plan_to_reserve") or 0)
        if row.material_request_type == "Purchase" and ptp > 0:
            purchase_entries.append({
                "item_code": row.item_code,
                "warehouse": row.for_warehouse,
                "stock_uom": row.stock_uom,
                "qty": ptp,
                "source_row": row.name,
            })
        elif row.material_request_type == "Material Transfer" and ptr > 0:
            # For transfer, set source as row.warehouse and target as row.for_warehouse
            transfer_entries.append({
                "item_code": row.item_code,
                "from_warehouse": row.warehouse,
                "warehouse": row.for_warehouse,
                "stock_uom": row.stock_uom,
                "qty": ptr,
                "source_row": row.name,
            })

    # Create Purchase Material Request
    if purchase_entries:
        mr = frappe.new_doc("Material Request")
        mr.material_request_type = "Purchase"
        mr.company = mrp.company
        mr.schedule_date = add_days(nowdate(), 7)
        # Ensure no supplier/from warehouse is set on Purchase MR to avoid conflicts
        mr.set_from_warehouse = None
        mr_item_has_link = bool(frappe.get_meta("Material Request Item").get_field("custom_mrp"))
        mr_item_has_rm_link = bool(frappe.get_meta("Material Request Item").get_field("custom_mrp_raw_material_item"))
        for data in purchase_entries:
            item_row = {
                "item_code": data["item_code"],
                "schedule_date": mr.schedule_date,
                "qty": flt(data["qty"]),
                "uom": data.get("stock_uom"),
                "stock_uom": data.get("stock_uom"),
                "warehouse": data["warehouse"],
            }
            if mr_item_has_link:
                item_row["custom_mrp"] = mrp.name
            if mr_item_has_rm_link and data.get("source_row"):
                item_row["custom_mrp_raw_material_item"] = data["source_row"]
            mr.append("items", item_row)
        mr.insert()
        created.append({"doctype": "Material Request", "name": mr.name})

    # Create Material Transfer Material Request
    if transfer_entries:
        mr_t = frappe.new_doc("Material Request")
        mr_t.material_request_type = "Material Transfer"
        mr_t.company = mrp.company
        mr_t.schedule_date = add_days(nowdate(), 3)
        mr_item_has_link = bool(frappe.get_meta("Material Request Item").get_field("custom_mrp"))
        mr_item_has_rm_link = bool(frappe.get_meta("Material Request Item").get_field("custom_mrp_raw_material_item"))
        for data in transfer_entries:
            # Skip invalid or same-warehouse transfers
            if not data.get("from_warehouse") or not data.get("warehouse"):
                continue
            if data["from_warehouse"] == data["warehouse"]:
                continue
            item_row = {
                "item_code": data["item_code"],
                "schedule_date": mr_t.schedule_date,
                "qty": flt(data["qty"]),
                "uom": data.get("stock_uom"),
                "stock_uom": data.get("stock_uom"),
                "warehouse": data["warehouse"],          # target
                "from_warehouse": data["from_warehouse"], # source
            }
            if mr_item_has_link:
                item_row["custom_mrp"] = mrp.name
            if mr_item_has_rm_link and data.get("source_row"):
                item_row["custom_mrp_raw_material_item"] = data["source_row"]
            mr_t.append("items", item_row)
        if mr_t.get("items"):
            mr_t.insert()
            created.append({"doctype": "Material Request", "name": mr_t.name})

    frappe.msgprint(_(f"Created {len(created)} Material Request(s)."))
    return {"created": created}


@frappe.whitelist()
def make_work_orders(mrp_name):
    """Create Work Orders per material_request_items, mirroring Production Plan flow.
    Expects each row to have a valid BOM and requested qty.
    """
    mrp = frappe.get_doc("MRP", mrp_name)

    created = []
    work_orders_created = []
    # stock_entries_created = []
    for row in mrp.get("material_request_items", []):
        if not row.get("bom_no") or flt(row.get("material_requested_qty") or 0) <= 0:
            continue

        wo = frappe.new_doc("Work Order")
        wo.company = mrp.company
        wo.production_item = row.item_code
        wo.bom_no = row.bom_no
        wo.qty = flt(row.material_requested_qty)
        # Use destination warehouse on the MR row as FG warehouse if available
        fg_warehouse = row.get("warehouse")
        wo.fg_warehouse = fg_warehouse
        if not fg_warehouse:
            frappe.throw(_(f"Finished Goods Warehouse is mandatory for Work Order of item {row.item_code}."))

        wip_warehouse = _get_wip_warehouse(fg_warehouse)
        if not wip_warehouse:
            frappe.throw(_(f"Configure Custom Work In Progress Warehouse for {fg_warehouse} to create Work Orders."))
        wo.wip_warehouse = wip_warehouse
        # Planned dates
        wo.planned_start_date = nowdate()
        wo.use_multi_level_bom = 0

        # Link back to MRP if custom field exists
        if frappe.get_meta("Work Order").get_field("custom_mrp"):
            wo.set("custom_mrp", mrp.name)
        wo.insert()
        # wo.submit()
        work_orders_created.append({"doctype": "Work Order", "name": wo.name})

        # stock_entry_data = make_stock_entry(wo.name, "Material Transfer for Manufacture")
        # stock_entry_doc = frappe.get_doc(stock_entry_data)
        # stock_entry_doc.insert()
        # stock_entries_created.append({"doctype": "Stock Entry", "name": stock_entry_doc.name})

    # Also create Work Orders for Sub Assembly Items where manufacturing type is In House
    for srow in mrp.get("sub_assembly_items", []):
        mf_type = (srow.get("type_of_manufacturing") or "").strip()
        if mf_type != "In House":
            continue
        if not srow.get("bom_no") or flt(srow.get("qty") or 0) <= 0:
            continue

        wo = frappe.new_doc("Work Order")
        wo.company = mrp.company
        wo.production_item = srow.production_item
        wo.bom_no = srow.bom_no
        wo.qty = flt(srow.qty)
        fg_warehouse = srow.get("fg_warehouse")
        wo.fg_warehouse = fg_warehouse
        if not fg_warehouse:
            frappe.throw(_(f"Finished Goods Warehouse is mandatory for Work Order of item {srow.production_item}."))

        wip_warehouse = _get_wip_warehouse(fg_warehouse)
        if not wip_warehouse:
            frappe.throw(_(f"Configure Custom Work In Progress Warehouse for {fg_warehouse} to create Work Orders."))
        wo.wip_warehouse = wip_warehouse
        wo.planned_start_date = nowdate()
        # wo.use_multi_level_bom = 0
        if frappe.get_meta("Work Order").get_field("custom_mrp"):
            wo.set("custom_mrp", mrp.name)
        wo.insert()
        # wo.submit()
        work_orders_created.append({"doctype": "Work Order", "name": wo.name})

        # stock_entry_data = make_stock_entry(wo.name, "Material Transfer for Manufacture")
        # stock_entry_doc = frappe.get_doc(stock_entry_data)
        # stock_entry_doc.insert()
        # stock_entries_created.append({"doctype": "Stock Entry", "name": stock_entry_doc.name})

    created.extend(work_orders_created)
    # created.extend(stock_entries_created)

    if work_orders_created:
        summary_parts = []
        if work_orders_created:
            summary_parts.append(_("{0} Work Order(s)").format(len(work_orders_created)))
        # if stock_entries_created:
        #     summary_parts.append(_("{0} Stock Entry(s)").format(len(stock_entries_created)))
        frappe.msgprint(_("Created {0}.").format(" and ".join(summary_parts)))
    else:
        frappe.msgprint(_("No Work Orders created."))

    return {"created": created}
