import frappe

# -------------------------------
# Helpers
# -------------------------------

def _existing_stock_entry(qi_name, types=None):
    """
    Returns True if any Draft/Submitted Stock Entry exists for this QI.
    Optionally filter by stock_entry_type.
    """
    filters = {
        "quality_inspection": qi_name,
        "docstatus": ["in", [0, 1]],  # check Draft + Submitted
    }
    if types:
        filters["stock_entry_type"] = ["in", types]

    existing_se = frappe.get_all("Stock Entry", filters=filters, fields=["name"])
    return bool(existing_se)


def _get_source_warehouse(qi):
    """
    Fetch source warehouse from reference document (Purchase Receipt / Delivery Note / Stock Entry).
    """
    if not qi.reference_name or not qi.reference_type:
        frappe.throw(f"Reference document not found for QI {qi.name}")

    warehouse = None

    if qi.reference_type == "Purchase Receipt":
        warehouse = frappe.db.get_value(
            "Purchase Receipt Item",
            {"parent": qi.reference_name, "item_code": qi.item_code},
            "warehouse"
        )

    elif qi.reference_type == "Delivery Note":
        warehouse = frappe.db.get_value(
            "Delivery Note Item",
            {"parent": qi.reference_name, "item_code": qi.item_code},
            "warehouse"
        )

    elif qi.reference_type == "Stock Entry":
        warehouse = frappe.db.get_value(
            "Stock Entry Detail",
            {"parent": qi.reference_name, "item_code": qi.item_code},
            "t_warehouse"
        )

    else:
        frappe.throw(f"Unsupported reference type {qi.reference_type} for QI {qi.name}")

    if not warehouse:
        frappe.throw(
            f"Cannot find source warehouse for QI {qi.name} "
            f"in {qi.reference_type} {qi.reference_name}"
        )

    return warehouse


def _create_stock_entry(qi, stock_entry_type, qty, source_wh=None, target_wh=None):
    """
    Generic Stock Entry creator.
    """
    if not source_wh:
        source_wh = _get_source_warehouse(qi)

    se = frappe.new_doc("Stock Entry")
    se.company = qi.company
    se.stock_entry_type = stock_entry_type

    item_row = se.append("items", {})
    item_row.item_code = qi.item_code
    item_row.qty = qty
    item_row.uom = frappe.db.get_value("Item", qi.item_code, "stock_uom")
    item_row.s_warehouse = source_wh
    item_row.t_warehouse = target_wh
    item_row.quality_inspection = qi.name
    item_row.batch_no = qi.batch_no
    item_row.use_serial_batch_fields = 1

    se.quality_inspection = qi.name
    se.insert()
    se.submit()

    return se.name, target_wh


# -------------------------------
# Whitelisted Methods (Buttons)
# -------------------------------

@frappe.whitelist()
def make_internal_transfer(qi_name):
    """
    First button → Create one Sample Internal Transfer with full sample qty.
    """
    if _existing_stock_entry(qi_name, types=["Sample Internal Transfer"]):
        frappe.throw(f"Sample Internal Transfer already exists for this QI: {qi_name}")

    qi = frappe.get_doc("Quality Inspection", qi_name)
    sample_size = qi.sample_size or 1

    # fetch target wh (custom field or fallback)
    target_wh = frappe.db.get_value("Warehouse", _get_source_warehouse(qi), "custom_qc_warehouse") \
                 or "FG LUHARI - BL"

    se_name, target_wh = _create_stock_entry(
        qi,
        "Sample Internal Transfer",
        sample_size,
        source_wh=_get_source_warehouse(qi),
        target_wh=target_wh,
    )

    # Save target warehouse for later NRGP
    qi.db_set("custom_mt_target_warehouse", target_wh)
    qi.db_set("custom_sample_status", "Sample Collected")

    return {"stock_entries": [se_name]}


@frappe.whitelist()
def make_external_nrgp(qi_name):
    """
    Second button → External NRGP (half sample qty).
    """
    if _existing_stock_entry(qi_name, types=["External NRGP"]):
        frappe.throw(f"External NRGP already exists for this QI: {qi_name}")

    qi = frappe.get_doc("Quality Inspection", qi_name)
    sample_size = qi.sample_size or 1
    half_qty = sample_size / 2

    source_wh = qi.get("custom_mt_target_warehouse")
    if not source_wh:
        frappe.throw(f"No MT Target Warehouse found. Please run 'Collect Sample' first.")

    se_name, _ = _create_stock_entry(qi, "External NRGP", half_qty, source_wh=source_wh)
    return {"stock_entries": [se_name]}


@frappe.whitelist()
def make_internal_nrgp(qi_name, target_warehouse=None):
    """
    Internal NRGP (half sample qty).
    """
    if _existing_stock_entry(qi_name, types=["Internal NRGP"]):
        frappe.throw(f"Internal NRGP already exists for this QI: {qi_name}")

    if not target_warehouse:
        frappe.throw("Please select a Target Warehouse for Internal NRGP")

    qi = frappe.get_doc("Quality Inspection", qi_name)
    sample_size = qi.sample_size or 1
    half_qty = sample_size / 2

    source_wh = qi.get("custom_mt_target_warehouse")
    if not source_wh:
        frappe.throw("No MT Target Warehouse found. Please run 'Collect Sample' first.")

    se_name, _ = _create_stock_entry(
        qi,
        "Internal NRGP",
        half_qty,
        source_wh=source_wh,
        target_wh=target_warehouse,
    )
    return {"stock_entries": [se_name]}


# -------------------------------
# Batch Status Updates
# -------------------------------

def update_batch_status(batch_no, new_status):
    """Update the batch status field (use exact fieldname)"""
    if not batch_no:
        return
    if frappe.db.exists("Batch", batch_no):
        frappe.db.set_value("Batch", batch_no, "custom_status", new_status)
        frappe.db.commit()


def on_qi_validate(doc, method=None):
    """When QI is in draft → Batch = Testing"""
    if doc.docstatus == 0:
        update_batch_status(doc.batch_no, "Testing")


def on_qi_submit(doc, method=None):
    """When QI is submitted → Batch = Approved / Rejected"""
    if doc.status == "Accepted":
        update_batch_status(doc.batch_no, "Approved")
    elif doc.status == "Rejected":
        update_batch_status(doc.batch_no, "Rejected")
