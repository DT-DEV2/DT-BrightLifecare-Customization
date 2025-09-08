import frappe

# -------------------------------
# Helpers
# -------------------------------

def _existing_stock_entry(qi_name, types=None, include_draft=True, include_submitted=True):
    """Return stock entries for a QI filtered by type and docstatus"""
    filters = {"quality_inspection": qi_name}
    docstatus = []
    if include_draft:
        docstatus.append(0)
    if include_submitted:
        docstatus.append(1)
    if docstatus:
        filters["docstatus"] = ["in", docstatus]
    if types:
        filters["stock_entry_type"] = ["in", types]

    return frappe.get_all("Stock Entry", filters=filters, fields=["name", "docstatus"])


def _get_source_warehouse(qi):
    """Find source warehouse from reference document"""
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


def _create_stock_entry(qi, stock_entry_type, qty, source_wh=None, target_wh=None, is_external=False):
    """Create a Stock Entry document linked to QI"""
    if not source_wh:
        source_wh = _get_source_warehouse(qi)

    se = frappe.new_doc("Stock Entry")
    se.company = qi.company
    se.stock_entry_type = stock_entry_type
    se.quality_inspection = qi.name

    item_row = se.append("items", {})
    item_row.item_code = qi.item_code
    item_row.qty = qty
    item_row.uom = frappe.db.get_value("Item", qi.item_code, "stock_uom")
    item_row.s_warehouse = source_wh
    item_row.t_warehouse = target_wh
    item_row.quality_inspection = qi.name
    item_row.batch_no = qi.batch_no
    item_row.use_serial_batch_fields = 1

    se.insert()

    # Submit only if NOT external
    if not is_external:
        se.submit()

    return se.name, target_wh


def _sync_sample_status(qi_name):
    """Update custom_sample_status field depending on whether a Sample Internal Transfer exists"""
    entries = _existing_stock_entry(
        qi_name,
        types=["Sample Internal Transfer"],
        include_draft=False,
        include_submitted=True
    )
    has_active = any(se.docstatus == 1 for se in entries)

    frappe.db.set_value(
        "Quality Inspection",
        qi_name,
        "custom_sample_status",
        "Sample Collected" if has_active else ""
    )
    frappe.db.commit()
    return has_active


def _get_source_for_external_nrgp(qi):
    """Determine source warehouse for External NRGP dynamically"""
    # Check if Internal NRGP exists
    internal_nrgp_entries = _existing_stock_entry(qi.name, types=["Internal NRGP"])
    if internal_nrgp_entries:
        # Get target warehouse from the first Internal NRGP's items
        se_items = frappe.get_all(
            "Stock Entry Detail",
            filters={"parent": internal_nrgp_entries[0].name},
            fields=["t_warehouse"]
        )
        if se_items:
            return se_items[0].t_warehouse

    # Otherwise, use Sample Internal Transfer target warehouse
    if qi.get("custom_mt_target_warehouse"):
        return qi.custom_mt_target_warehouse

    # Fallback
    return None


# -------------------------------
# Whitelisted Methods
# -------------------------------

@frappe.whitelist()
def make_internal_transfer(qi_name):
    """Collect Sample → creates a Sample Internal Transfer"""
    if _existing_stock_entry(qi_name, types=["Sample Internal Transfer"]):
        frappe.throw(f"Sample Internal Transfer already exists for this QI: {qi_name}")

    qi = frappe.get_doc("Quality Inspection", qi_name)
    sample_size = qi.sample_size or 1

    target_wh = frappe.db.get_value("Warehouse", _get_source_warehouse(qi), "custom_qc_warehouse") \
                 or "FG LUHARI - BL"

    se_name, target_wh = _create_stock_entry(
        qi,
        "Sample Internal Transfer",
        sample_size,
        source_wh=_get_source_warehouse(qi),
        target_wh=target_wh,
    )

    qi.db_set("custom_mt_target_warehouse", target_wh)

    # Sync status to "Sample Collected"
    _sync_sample_status(qi.name)

    return {"stock_entries": [se_name]}


@frappe.whitelist()
def make_external_nrgp(qi_name):
    """Create an External NRGP (half qty)"""
    if _existing_stock_entry(qi_name, types=["External NRGP"]):
        frappe.throw(f"External NRGP already exists for this QI: {qi_name}")

    qi = frappe.get_doc("Quality Inspection", qi_name)
    sample_size = qi.sample_size or 1
    half_qty = sample_size / 2  # External → half qty

    # Determine source warehouse dynamically
    source_wh = _get_source_for_external_nrgp(qi)
    if not source_wh:
        frappe.throw("No source warehouse found. Please run 'Collect Sample' or create Internal NRGP first.")

    se_name, _ = _create_stock_entry(
        qi,
        "External NRGP",
        half_qty,
        source_wh=source_wh,
        is_external=True
    )
    return {"stock_entries": [se_name]}


@frappe.whitelist()
def make_internal_nrgp(qi_name, target_warehouse=None):
    """Create an Internal NRGP (full qty)"""
    if _existing_stock_entry(qi_name, types=["Internal NRGP"]):
        frappe.throw(f"Internal NRGP already exists for this QI: {qi_name}")

    if not target_warehouse:
        frappe.throw("Please select a Target Warehouse for Internal NRGP")

    qi = frappe.get_doc("Quality Inspection", qi_name)
    sample_size = qi.sample_size or 1

    # Source warehouse = Sample Internal Transfer target
    source_wh = qi.get("custom_mt_target_warehouse")
    if not source_wh:
        frappe.throw("No MT Target Warehouse found. Please run 'Collect Sample' first.")

    se_name, _ = _create_stock_entry(
        qi,
        "Internal NRGP",
        sample_size,
        source_wh=source_wh,
        target_wh=target_warehouse,
    )
    return {"stock_entries": [se_name]}


@frappe.whitelist()
def has_sample_stock_entry(qi_name):
    """Return stock entry status for 'Sample Internal Transfer'"""
    entries = frappe.get_all(
        "Stock Entry",
        filters={
            "quality_inspection": qi_name,
            "stock_entry_type": "Sample Internal Transfer"
        },
        fields=["name", "docstatus"]
    )

    if not entries:
        # No entry at all
        return {"active": False, "all_cancelled": True, "status": ""}

    active = any(e.docstatus in [0, 1] for e in entries)
    all_cancelled = all(e.docstatus == 2 for e in entries)

    status = "Sample Collected" if active else ""

    return {
        "active": active,
        "all_cancelled": all_cancelled,
        "status": status
    }


# -------------------------------
# Batch Status Updates
# -------------------------------

def update_batch_status(batch_no, new_status):
    if not batch_no:
        return
    if frappe.db.exists("Batch", batch_no):
        frappe.db.set_value("Batch", batch_no, "custom_status", new_status)
        frappe.db.commit()


def on_qi_validate(doc, method=None):
    if doc.docstatus == 0:
        update_batch_status(doc.batch_no, "Testing")


def on_qi_submit(doc, method=None):
    if doc.batch_no:
        batch = frappe.get_doc("Batch", doc.batch_no)
        for row in batch.custom_quality_check_schedule:
            row.ar_number = doc.name
        batch.save()

    if doc.status == "Accepted":
        update_batch_status(doc.batch_no, "Approved")
    elif doc.status == "Rejected":
        update_batch_status(doc.batch_no, "Rejected")
