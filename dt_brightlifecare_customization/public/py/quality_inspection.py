import frappe
from frappe.utils import flt


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


def get_warehouse_address(warehouse):
    """Fetch linked Address for a Warehouse from Address → Dynamic Link"""
    if not warehouse:
        return ""
    return frappe.db.get_value(
        "Dynamic Link",
        {"link_doctype": "Warehouse", "link_name": warehouse, "parenttype": "Address"},
        "parent"
    ) or ""


def _create_stock_entry(qi, stock_entry_type, qty, source_wh=None, target_wh=None, draft=False, to_address=None, parameters=None, batch_no=None):
    """Create a Stock Entry document linked to QI and set addresses + GST"""
    if not source_wh:
        source_wh = _get_source_warehouse(qi)

    se = frappe.new_doc("Stock Entry")
    se.company = qi.company
    se.stock_entry_type = stock_entry_type
    se.quality_inspection = qi.name

    # Item row
    item_row = se.append("items", {})
    item_row.item_code = qi.item_code
    item_row.qty = qty
    item_row.uom = frappe.db.get_value("Item", qi.item_code, "stock_uom")
    item_row.s_warehouse = source_wh
    item_row.t_warehouse = target_wh
    item_row.quality_inspection = qi.name
    item_row.batch_no = batch_no or qi.batch_no
    item_row.use_serial_batch_fields = 1

    # -----------------------
    # Address Mapping
    # -----------------------
    if stock_entry_type == "Sample Internal Transfer":
        # Bill From / Ship From → Source WH company address
        se.bill_from_address = frappe.db.get_value("Warehouse", source_wh, "custom_company_address") or ""
        se.ship_from_address = get_warehouse_address(source_wh)

        # Bill To / Ship To → Target WH company address
        se.bill_to_address = get_warehouse_address(target_wh)
        se.ship_to_address = se.bill_to_address

    elif stock_entry_type == "Internal NRGP":
        # Source WH → Warehouse Address (linked in Address table)
        se.bill_from_address = frappe.db.get_value("Warehouse", source_wh, "custom_company_address") or ""
        se.ship_from_address = get_warehouse_address(source_wh)

        # Target WH → Warehouse Address
        se.bill_to_address = get_warehouse_address(target_wh)
        se.ship_to_address = se.bill_to_address

    elif stock_entry_type == "External QC NRGP":
        se.bill_from_address = frappe.db.get_value("Warehouse", source_wh, "custom_company_address") or ""
        se.ship_from_address = get_warehouse_address(source_wh)

        # Bill To / Ship To → External Party Address (passed in)
        se.bill_to_address = to_address or ""
        se.ship_to_address = to_address or ""

    # -----------------------
    # GST Categories
    # -----------------------
    # for field, addr in {
    #     "bill_from_gst_category": se.bill_from_address,
    #     "bill_to_gst_category": se.bill_to_address,
    # }.items():
    #     if addr:
    #         se.set(field, frappe.db.get_value("Address", addr, "gst_category") or "Unregistered")

     # ✅ Add custom parameters before submission
    if parameters:
        for p in parameters:
            se.append("custom_parameters", {
                "parameter": p.get("parameter"),
                "total_cost": p.get("total_cost") or 0
            })


    se.insert()

    if not draft:
        se.submit()

    return se.name




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
    """Determine source warehouse for External QC NRGP dynamically"""
    internal_nrgp_entries = _existing_stock_entry(qi.name, types=["Internal NRGP"])
    if internal_nrgp_entries:
        se_items = frappe.get_all(
            "Stock Entry Detail",
            filters={"parent": internal_nrgp_entries[0].name},
            fields=["t_warehouse"]
        )
        if se_items:
            return se_items[0].t_warehouse

    if qi.get("custom_mt_target_warehouse"):
        return qi.custom_mt_target_warehouse

    return None


# -------------------------------
# Whitelisted Methods
# -------------------------------

# @frappe.whitelist()
# def make_internal_transfer(qi_name, sample_qty=None):
#     """Collect Sample → creates a Sample Internal Transfer"""
#     if _existing_stock_entry(qi_name, types=["Sample Internal Transfer"]):
#         frappe.throw(f"Sample Internal Transfer already exists for this QI: {qi_name}")

#     qi = frappe.get_doc("Quality Inspection", qi_name)

#     # use user-entered qty or fall back to sample_size or 1
#     qty = float(sample_qty) if sample_qty else (qi.sample_size or 1)

#     # ✅ Ensure total qty of all Internal NRGP < reference doc qty
#     ref_type = qi.reference_type
#     ref_name = qi.reference_name
#     if not (ref_type and ref_name):
#         frappe.throw("Missing reference document in Quality Inspection.")

#     # Get the reference document’s total quantity
#     ref_doc = frappe.get_doc(ref_type, ref_name)
#     ref_qty = 0
#     if hasattr(ref_doc, "items"):
#         ref_qty = sum(flt(i.qty) for i in ref_doc.items if i.item_code == qi.item_code)
#     else:
#         frappe.throw(f"Reference document {ref_type} has no items table to compare quantity.")


#     if not ref_qty:
#         frappe.throw(f"No 'qty' found in reference document {qi.reference_name}")

#     if qty > ref_qty:
#         frappe.throw(
#             f"Sample quantity ({qty}) cannot exceed reference document qty ({ref_qty})."
#         )


#     target_wh = frappe.db.get_value("Warehouse", _get_source_warehouse(qi), "custom_qc_warehouse") \
#                  or "FG LUHARI - BL"

#     se_name = _create_stock_entry(
#         qi,
#         "Sample Internal Transfer",
#         qty,
#         source_wh=_get_source_warehouse(qi),
#         target_wh=target_wh,
#         draft=False
#     )

#     qi.db_set("custom_mt_target_warehouse", target_wh)
#     _sync_sample_status(qi.name)

#     return {"stock_entry": se_name}





@frappe.whitelist()
def make_internal_transfer(qi_name, sample_qty=None):
    """Collect Sample → Split batch → Create Sample Internal Transfer."""
    

    if _existing_stock_entry(qi_name, types=["Sample Internal Transfer"]):
        frappe.throw(f"Sample Internal Transfer already exists for this QI: {qi_name}")

    qi = frappe.get_doc("Quality Inspection", qi_name)
    qty = float(sample_qty) if sample_qty else (qi.sample_size or 1)

    # --- Validate reference document ---
    ref_type, ref_name = qi.reference_type, qi.reference_name
    if not (ref_type and ref_name):
        frappe.throw("Missing reference document in Quality Inspection.")

    ref_doc = frappe.get_doc(ref_type, ref_name)
    ref_qty = sum(flt(i.qty) for i in getattr(ref_doc, "items", []) if i.item_code == qi.item_code)

    if not ref_qty:
        frappe.throw(f"No 'qty' found in reference document {qi.reference_name}")

    if qty > ref_qty:
        frappe.throw(f"Sample quantity ({qty}) cannot exceed reference document qty ({ref_qty}).")

    # --- Batch split logic ---
    if not qi.batch_no:
        frappe.throw("No batch number found in Quality Inspection.")

    source_wh = _get_source_warehouse(qi)
    if not source_wh:
        frappe.throw("No source warehouse found for this Quality Inspection.")

    # Generate new batch ID
    new_batch_id = f"Sample{qi.batch_no}"

    # Check if a sample batch already exists
    existing_sample_batch = frappe.db.exists("Batch", {"batch_id": new_batch_id, "item": qi.item_code})
    if existing_sample_batch:
        frappe.msgprint(f"Reusing existing sample batch: <b>{new_batch_id}</b>")
        new_batch_name = existing_sample_batch
    else:
        # ✅ Use ERPNext’s built-in batch split function
        new_batch_name = split_batch_custom(
            batch_no=qi.batch_no,
            item_code=qi.item_code,
            warehouse=source_wh,
            qty=qty,
            new_batch_id=new_batch_id
        )
        frappe.msgprint(f"Created new sample batch: <b>{new_batch_name}</b>")

    # --- Create Stock Entry using new batch ---
    target_wh = frappe.db.get_value("Warehouse", source_wh, "custom_qc_warehouse")

    se_name = _create_stock_entry(
        qi,
        "Sample Internal Transfer",
        qty,
        source_wh=source_wh,
        target_wh=target_wh,
        draft=False,
        batch_no=new_batch_name,  # 👈 assign the split batch
    )

    qi.db_set("custom_mt_target_warehouse", target_wh)
    _sync_sample_status(qi.name)

    return {"stock_entry": se_name}





from erpnext.stock.doctype.batch.batch import make_batch_bundle

@frappe.whitelist()
def split_batch_custom(batch_no: str, item_code: str, warehouse: str, qty: float, new_batch_id: str | None = None):
    """Custom Batch Split that creates a Stock Entry with stock_entry_type='Batch Split'"""

    qty = flt(qty)
    if not all([batch_no, item_code, warehouse, qty]):
        frappe.throw("Missing required parameters for batch split")

    # --- Create new batch ---
    batch = frappe.get_doc({
        "doctype": "Batch",
        "item": item_code,
        "batch_id": new_batch_id
    }).insert()

    # --- Get company ---
    company = frappe.db.get_value("Warehouse", warehouse, "company")
    if not company:
        frappe.throw(f"Company not found for warehouse {warehouse}")

    # --- Create Outward bundle from old batch ---
    from_bundle_id = make_batch_bundle(
        item_code=item_code,
        warehouse=warehouse,
        batches=frappe._dict({batch_no: qty}),
        company=company,
        type_of_transaction="Outward",
        qty=qty,
    )

    # --- Create Inward bundle for new batch ---
    to_bundle_id = make_batch_bundle(
        item_code=item_code,
        warehouse=warehouse,
        batches=frappe._dict({batch.name: qty}),
        company=company,
        type_of_transaction="Inward",
        qty=qty,
    )

    # --- Create Stock Entry of type 'Batch Split' ---
    stock_entry = frappe.get_doc({
        "doctype": "Stock Entry",
        "stock_entry_type": "Batch Split",  # 👈 Custom type
        "purpose": "Repack",
        "company": company,
        "items": [
            {
                "item_code": item_code,
                "qty": qty,
                "s_warehouse": warehouse,
                "serial_and_batch_bundle": from_bundle_id,
            },
            {
                "item_code": item_code,
                "qty": qty,
                "t_warehouse": warehouse,
                "serial_and_batch_bundle": to_bundle_id,
            },
        ],
    })

    # 👇 Do NOT call set_stock_entry_type() — it will override your custom type
    stock_entry.insert()
    stock_entry.submit()

    return batch.name








# @frappe.whitelist()
# def make_external_nrgp(qi_name, ship_to_address=None, draft=False, custom_test_cost=None):
#     """Create External NRGP (asks only Ship To Address + Test Cost)"""
#     draft = frappe.utils.cint(draft) == 1 or str(draft).lower() == "true"

#     if _existing_stock_entry(qi_name, types=["External NRGP"]):
#         frappe.throw(f"External NRGP already exists for this QI: {qi_name}")

#     qi = frappe.get_doc("Quality Inspection", qi_name)
#     sample_size = qi.sample_size or 1
#     half_qty = sample_size / 2

#     source_wh = _get_source_for_external_nrgp(qi)
#     if not source_wh:
#         frappe.throw("No source warehouse found. Run 'Collect Sample' or create Internal NRGP first.")

#     se_name = _create_stock_entry(
#         qi,
#         "External NRGP",
#         half_qty,
#         source_wh=source_wh,
#         target_wh=None,
#         draft=draft,
#         to_address=ship_to_address
#     )

#     # ✅ Save test cost into Stock Entry
#     if custom_test_cost:
#         frappe.db.set_value("Stock Entry", se_name, "custom_test_cost", custom_test_cost)

#     return {"stock_entry": se_name}



@frappe.whitelist()
def make_external_nrgp(qi_name, ship_to_address=None, draft=False, custom_qty=None, parameters=None):
    """Create External NRGP (asks for Ship To Address + Parameters + Quantity)"""
    import json

    draft = frappe.utils.cint(draft) == 1 or str(draft).lower() == "true"
    parameters = frappe.parse_json(parameters) if parameters else []

    qi = frappe.get_doc("Quality Inspection", qi_name)

    # ✅ Determine quantity
    try:
        qty = flt(custom_qty) if custom_qty else flt((qi.sample_size or 1) / 2)
    except Exception:
        frappe.throw("Invalid quantity value provided for External QC NRGP.")

    # ✅ Get source warehouse
    source_wh = _get_source_for_external_nrgp(qi)
    if not source_wh:
        frappe.throw("No source warehouse found. Run 'Collect Sample' or create Internal NRGP first.")

    # ✅ Validate against reference document qty
    ref_type = qi.reference_type
    ref_name = qi.reference_name
    if not (ref_type and ref_name):
        frappe.throw("Missing reference document in Quality Inspection.")

    ref_doc = frappe.get_doc(ref_type, ref_name)
    ref_qty = 0
    if hasattr(ref_doc, "items"):
        ref_qty = sum(flt(i.qty) for i in ref_doc.items if i.item_code == qi.item_code)
    else:
        frappe.throw(f"Reference document {ref_type} has no items table to compare quantity.")

    existing_qty = frappe.db.sql(
        """
        SELECT SUM(sei.qty)
        FROM `tabStock Entry Detail` sei
        JOIN `tabStock Entry` se ON se.name = sei.parent
        WHERE se.stock_entry_type = 'External QC NRGP'
          AND sei.quality_inspection = %s
          AND se.docstatus < 2
        """,
        qi_name
    )[0][0] or 0

    total_after_new = existing_qty + qty
    if total_after_new > ref_qty:
        frappe.throw(
            f"Cannot create External QC NRGP of qty {qty}. "
            f"Total NRGP qty ({total_after_new}) exceeds reference qty ({ref_qty})."
        )

    # ✅ Create Stock Entry
    se_name = _create_stock_entry(
        qi,
        "External QC NRGP",
        qty,
        source_wh=source_wh,
        target_wh=None,
        draft=draft,
        to_address=ship_to_address,
        parameters=parameters
    )

    # ✅ Add selected parameters
    # if parameters:
    #     se = frappe.get_doc("Stock Entry", se_name)
    #     for p in parameters:
    #         se.append("custom_parameters", {
    #             "parameter": p.get("parameter"),
    #             "total_cost": p.get("total_cost") or 0
    #         })
    #     se.save(ignore_permissions=True)
    #     frappe.db.commit()

    return {"stock_entry": se_name}


# @frappe.whitelist()
# def make_internal_nrgp(qi_name, target_warehouse=None, draft=False):
#     draft = frappe.utils.cint(draft) == 1 or str(draft).lower() == "true"
#     """Create an Internal NRGP (full qty)"""
#     if _existing_stock_entry(qi_name, types=["Internal NRGP"]):
#         frappe.throw(f"Internal NRGP already exists for this QI: {qi_name}")

#     if not target_warehouse:
#         frappe.throw("Please select a Target Warehouse for Internal NRGP")

#     qi = frappe.get_doc("Quality Inspection", qi_name)
#     sample_size = qi.sample_size or 1

#     # Source warehouse = Sample Internal Transfer target
#     source_wh = qi.get("custom_mt_target_warehouse")
#     if not source_wh:
#         frappe.throw("No MT Target Warehouse found. Run 'Collect Sample' first.")

#     se_name = _create_stock_entry(
#         qi,
#         "Internal NRGP",
#         sample_size,
#         source_wh=source_wh,
#         target_wh=target_warehouse,
#         draft=draft
#     )

#     return {"stock_entry": se_name}



@frappe.whitelist()
def make_internal_nrgp(qi_name, target_warehouse=None, draft=False, custom_qty=None, parameters=None):
    """Create an Internal NRGP (uses entered Quantity or full sample size)"""
    import json

    # ✅ Handle the draft flag and JSON input
    draft = frappe.utils.cint(draft) == 1 or str(draft).lower() == "true"
    parameters = frappe.parse_json(parameters) if parameters else []

    if not target_warehouse:
        frappe.throw("Please select a Target Warehouse for Internal NRGP")

    qi = frappe.get_doc("Quality Inspection", qi_name)

    try:
        qty = float(custom_qty) if custom_qty else float(qi.sample_size or 1)
    except Exception:
        frappe.throw("Invalid quantity value provided for Internal NRGP.")

    source_wh = qi.get("custom_mt_target_warehouse")
    if not source_wh:
        frappe.throw("No MT Target Warehouse found. Run 'Collect Sample' first.")

    ref_type = qi.reference_type
    ref_name = qi.reference_name
    if not (ref_type and ref_name):
        frappe.throw("Missing reference document in Quality Inspection.")

    ref_doc = frappe.get_doc(ref_type, ref_name)
    ref_qty = 0
    if hasattr(ref_doc, "items"):
        ref_qty = sum(flt(i.qty) for i in ref_doc.items if i.item_code == qi.item_code)
    else:
        frappe.throw(f"Reference document {ref_type} has no items table to compare quantity.")

    existing_qty = frappe.db.sql(
        """
        SELECT SUM(sei.qty)
        FROM `tabStock Entry Detail` sei
        JOIN `tabStock Entry` se ON se.name = sei.parent
        WHERE se.stock_entry_type = 'Internal NRGP'
          AND sei.quality_inspection = %s
          AND se.docstatus < 2
        """,
        qi_name
    )[0][0] or 0

    total_after_new = existing_qty + qty
    if total_after_new > ref_qty:
        frappe.throw(
            f"Cannot create Internal NRGP of qty {qty}. "
            f"Total NRGP qty ({total_after_new}) exceeds reference qty ({ref_qty})."
        )

    # ✅ Create the Stock Entry
    se_name = _create_stock_entry(
        qi,
        "Internal NRGP",
        qty,
        source_wh=source_wh,
        target_wh=target_warehouse,
        draft=draft,
        parameters=parameters
    )

    # ✅ Add selected parameters into SE.custom_parameters
    # if parameters:
    #     se = frappe.get_doc("Stock Entry", se_name)
    #     for p in parameters:
    #         se.append("custom_parameters", {
    #             "parameter": p.get("parameter"),
    #             "total_cost": p.get("total_cost") or 0
    #         })
    #     se.save()
    #     frappe.db.commit()

    return {"stock_entry": se_name}




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
        return {"active": False, "all_cancelled": True, "status": ""}

    active = any(e.docstatus in [0, 1] for e in entries)
    all_cancelled = all(e.docstatus == 2 for e in entries)

    status = "Sample Collected" if active else ""

    return {"active": active, "all_cancelled": all_cancelled, "status": status}


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
    # 🔒 Block submission if any linked Stock Entries are not submitted
    pending_entries = frappe.get_all(
        "Stock Entry",
        filters={
            "quality_inspection": doc.name,
            "docstatus": ["!=", 1]  # anything not submitted
        },
        pluck="name"
    )

    if pending_entries:
        frappe.throw(
            f"Quality Inspection {doc.name} cannot be submitted until all Stock Entries "
            f"({', '.join(pending_entries)}) are submitted."
        )
    if doc.batch_no:
        batch = frappe.get_doc("Batch", doc.batch_no)
        for row in batch.custom_quality_check_schedule:
            row.ar_number = doc.name
        batch.save()

    if doc.status == "Accepted":
        update_batch_status(doc.batch_no, "Approved")
    elif doc.status == "Rejected":
        update_batch_status(doc.batch_no, "Rejected")



@frappe.whitelist()
def check_stock_entries(qi_name):
    """Return if internal/external stock entries exist for this QI (via Stock Entry Detail)."""
    parents = frappe.get_all(
        "Stock Entry Detail",
        filters={"quality_inspection": qi_name},
        pluck="parent"
    )
    if not parents:
        return {"internal_exists": False, "external_exists": False}

    internal_exists = frappe.db.exists("Stock Entry", {
        "name": ["in", parents],
        "stock_entry_type": ["in", ["Sample Internal Transfer", "Internal NRGP"]],
        "docstatus": 1
    })

    external_exists = frappe.db.exists("Stock Entry", {
        "name": ["in", parents],
        "stock_entry_type": "External QC NRGP",
    })

    return {
        "internal_exists": bool(internal_exists),
        "external_exists": bool(external_exists)
    }

@frappe.whitelist()
def get_external_qc_stock_entries(qi_name):
    """
    Fetch all Stock Entries of type "External QC NRGP" linked to this Quality Inspection.
    Returns: list of dicts with stock_entry name and stock_entry_type
    """
    return frappe.db.get_all(
        "Stock Entry",
        filters={
            "stock_entry_type": "External QC NRGP",
            "quality_inspection": qi_name  # replace with your actual link field
        },
        fields=["name", "stock_entry_type"]
    )
