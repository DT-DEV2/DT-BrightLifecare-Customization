import frappe

def _existing_stock_entry(qi_name):
   """
   Returns True if any Draft/Submitted Stock Entry exists for this QI.
   """
   existing_se = frappe.get_all(
       "Stock Entry",
       filters={
           "quality_inspection": qi_name,
           "docstatus": ["in", [0, 1]]  # 0=Draft, 1=Submitted
       },
       fields=["name"]
   )
   return bool(existing_se)


def _get_source_warehouse(qi):
   """
   Fetch source warehouse from reference document (PR or DN).
   """
   if not qi.reference_name:
       frappe.throw(f"Reference document not found for QI {qi.name}")

   # Fetch warehouse from the reference document's field 'set_warehouse'
   warehouse = frappe.db.get_value(qi.reference_type, qi.reference_name, "set_warehouse")
   if not warehouse:
       frappe.throw(f"Cannot find source warehouse for QI {qi.name} in {qi.reference_name}")

   return warehouse


def _create_stock_entry(qi, purpose, qty):
   """
   Create one Stock Entry linked to QI.
   """
   source_wh = _get_source_warehouse(qi)

   se = frappe.new_doc("Stock Entry")
   se.company = qi.company

   if purpose == "NRGP":
       se.stock_entry_type = "NRGP"
       target_wh = None
   else:
       se.stock_entry_type = "Material Transfer"
       # Fetch the custom QC warehouse from the source warehouse
       target_wh = frappe.db.get_value("Warehouse", source_wh, "custom_qc_warehouse")
       if not target_wh:
           # fallback if custom field is empty
           target_wh = "FG LUHARI - BL"

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

   # Link Stock Entry to Quality Inspection
   se.quality_inspection = qi.name

   se.insert()   # Insert first
   se.submit()                          # Auto-submit for both NRGP & MT

   return se.name




@frappe.whitelist()
def make_internal_transfer(qi_name):
   """
   Create one Stock Entry (Internal Transfer) with full sample qty.
   """
   if _existing_stock_entry(qi_name):
       frappe.throw(f"Stock Entry already exists for this Quality Inspection: {qi_name}")

   qi = frappe.get_doc("Quality Inspection", qi_name)
   sample_size = qi.sample_size or 1
   se_name = _create_stock_entry(qi, "Material Transfer", sample_size)
   return {"stock_entries": [se_name]}


@frappe.whitelist()
def make_internal_external_transfer(qi_name):
   """
   Create two Stock Entries (NRGP + Internal Transfer) split half-half.
   """
   if _existing_stock_entry(qi_name):
       frappe.throw(f"Stock Entry already exists for this Quality Inspection: {qi_name}")

   qi = frappe.get_doc("Quality Inspection", qi_name)
   sample_size = qi.sample_size or 1

   half_qty = sample_size / 2
   remaining_qty = sample_size - half_qty

   se1 = _create_stock_entry(qi, "NRGP", half_qty)
   se2 = _create_stock_entry(qi, "Material Transfer", remaining_qty)

   return {"stock_entries": [se1, se2]}

