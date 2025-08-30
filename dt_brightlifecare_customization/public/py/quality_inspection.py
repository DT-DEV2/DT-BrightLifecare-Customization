import frappe

def _existing_stock_entry(qi_name, types=None):
    """
    Returns True if any Draft/Submitted Stock Entry exists for this QI.
    Optionally filter by stock_entry_type.
    """
    filters = {
        "quality_inspection": qi_name,
        "docstatus": ["in", [0, 1]]
    }
    if types:
        filters["stock_entry_type"] = ["in", types]

    existing_se = frappe.get_all("Stock Entry", filters=filters, fields=["name"])
    return bool(existing_se)


def _get_source_warehouse(qi):
    """
    Fetch source warehouse from reference document (PR or DN).
    """
    if not qi.reference_name:
        frappe.throw(f"Reference document not found for QI {qi.name}")

    warehouse = frappe.db.get_value(qi.reference_type, qi.reference_name, "set_warehouse")
    if not warehouse:
        frappe.throw(f"Cannot find source warehouse for QI {qi.name} in {qi.reference_name}")

    return warehouse


def _create_stock_entry(qi, purpose, qty, source_wh=None):
    """
    Create one Stock Entry linked to QI.
    If purpose = NRGP → only s_warehouse
    If purpose = MT → s_warehouse + t_warehouse
    """
    if not source_wh:
        source_wh = _get_source_warehouse(qi)

    se = frappe.new_doc("Stock Entry")
    se.company = qi.company

    if purpose == "NRGP":
        se.stock_entry_type = "NRGP"
        target_wh = None
    else:
        se.stock_entry_type = "Material Transfer"
        target_wh = frappe.db.get_value("Warehouse", source_wh, "custom_qc_warehouse") or "FG LUHARI - BL"

    se.append("items", {
        "item_code": qi.item_code,
        "qty": qty,
        "uom": frappe.db.get_value("Item", qi.item_code, "stock_uom"),
        "s_warehouse": source_wh,
        "t_warehouse": target_wh,
        "quality_inspection": qi.name,
        "batch_no": qi.batch_no,
        "use_serial_batch_fields": 1
    })

    se.quality_inspection = qi.name
    se.insert()
    se.submit()

    return se.name, target_wh


@frappe.whitelist()
def make_internal_transfer(qi_name):
    """
    First button → Create one Stock Entry (Internal Transfer) with full sample qty.
    """
    if _existing_stock_entry(qi_name, types=["Material Transfer"]):
        frappe.throw(f"Material Transfer already exists for this Quality Inspection: {qi_name}")

    qi = frappe.get_doc("Quality Inspection", qi_name)
    sample_size = qi.sample_size or 1
    se_name, target_wh = _create_stock_entry(qi, "Material Transfer", sample_size)

    # Save target warehouse
    qi.db_set("custom_mt_target_warehouse", target_wh)

    # ✅ Update status field
    qi.db_set("custom_sample_status", "Sample Collected")

    return {"stock_entries": [se_name]}


@frappe.whitelist()
def make_external_nrgp(qi_name):
    """
    Second button → Create one NRGP Stock Entry (half sample qty).
    Source warehouse = target warehouse from first MT entry.
    """
    if _existing_stock_entry(qi_name, types=["NRGP"]):
        frappe.throw(f"NRGP already exists for this Quality Inspection: {qi_name}")

    qi = frappe.get_doc("Quality Inspection", qi_name)
    sample_size = qi.sample_size or 1
    half_qty = sample_size / 2

    # Get source warehouse from the target warehouse of MT entry
    source_wh = qi.get("custom_mt_target_warehouse")
    if not source_wh:
        frappe.throw(f"No MT Target Warehouse found. Please run 'Collect Sample Approval' first.")

    se_name, _ = _create_stock_entry(qi, "NRGP", half_qty, source_wh=source_wh)
    return {"stock_entries": [se_name]}
