import frappe
from frappe.utils import flt
from frappe import _
from dt_brightlifecare_customization.mrp.doctype.mrp.mrp import (
    explode_bom,
    get_sub_assembly_items,
)
from frappe.utils import flt, cint


# @frappe.whitelist()
# def create_mrp(material_request, use_defaults=False):
#     material_request_doc = frappe.get_doc('Material Request', material_request)
#     missing_items = []
#     for item in material_request_doc.items:
#         if not item.item_code:
#             missing_items.append({
#                 "Row no in Items": item.idx,
#                 "Item Code": item.item_code or "Missing",
#                 "Bom No": item.bom_no or "Missing"
#             })

#     if missing_items and not frappe.utils.cint(use_defaults):
#         frappe.throw(
#             ("Some fields are missing in items: {0}.").format(missing_items)
#         )

#     new_mrp_doc = frappe.new_doc("MRP")
#     new_mrp_doc.company = material_request_doc.company
#     new_mrp_doc.posting_date = material_request_doc.transaction_date
#     new_mrp_doc.expected_start_date = material_request_doc.transaction_date
    
#     new_mrp_doc.append('material_requests', {
#         'material_request': material_request_doc.name,
#         'material_request_date': material_request_doc.transaction_date,
#         'required_by' : material_request_doc.schedule_date,
#     })

#     for item in material_request_doc.items:
#         # bom_and_warehouse = get_best_bom(item.item_code, item.warehouse)

#         # fallback to item.bom_no if available
#         # best_bom = bom_and_warehouse.get("bom")
#         # best_warehouse = bom_and_warehouse.get("warehouse")

#         new_mrp_doc.append('material_request_items', {
#             'item_code': item.item_code,
#             'material_requested_qty': item.qty,
#             'required_by': item.schedule_date,
#             'warehouse': item.warehouse,
#             'uom': item.uom,
#             'material_request': material_request_doc.name,
#             'material_request_item_detail': item.name,
#             'qty_in_stock_uom': item.stock_qty,
#             'uom_conversion_factor': item.conversion_factor,
#             'stock_uom': item.stock_uom,
#             'description': item.description,
#             'bom_no': item.bom_no
#         })

#     new_mrp_doc.insert()
#     # Populate sub-assemblies and raw materials automatically for the new MRP
#     get_sub_assembly_items(new_mrp_doc.name)
#     explode_bom(new_mrp_doc.name)

#     return new_mrp_doc.as_dict()





# def get_best_bom(item_code, warehouse):
#     result = frappe.db.sql("""
#         SELECT name AS bom, custom_source_warehouse AS warehouse
#         FROM `tabBOM`
#         WHERE item = %s AND custom_source_warehouse = %s AND is_active = 1 AND docstatus = 1
#         ORDER BY custom_fg_batch_size DESC, custom_priority ASC
#         LIMIT 1
#     """, (item_code, warehouse,), as_dict=True)

#     return result[0] if result else {}




@frappe.whitelist()
def create_mrp(material_request, use_defaults=False):
    

    material_request_doc = frappe.get_doc('Material Request', material_request)
    missing_items = []

    # 1) Validate item_code presence
    for item in material_request_doc.items:
        if not item.item_code:
            missing_items.append({
                "Row no in Items": item.idx,
                "Item Code": item.item_code or "Missing",
                "Bom No": item.bom_no or "Missing"
            })

    if missing_items and not cint(use_defaults):
        frappe.throw(("Some fields are missing in items: {0}.").format(missing_items))

    # 2) build list of items with remaining qty to create MRPs for
    items_with_remaining = []
    for item in material_request_doc.items:
        # Sum any already-created requested qty for this material request item across MRPs
        already_created = frappe.db.sql("""
            SELECT COALESCE(SUM(material_requested_qty), 0) AS s
            FROM `tabMRP Material Request Item`
            WHERE material_request=%s AND material_request_item_detail=%s and docstatus < 2
        """, (material_request_doc.name, item.name), as_dict=True)
        already_created_qty = flt(already_created[0].s) if already_created else 0.0

        remaining_qty = flt(item.qty) - already_created_qty
        # If remaining is positive, we want to create MRP for that remaining amount
        if remaining_qty > 0:
            items_with_remaining.append((item, remaining_qty))

    # 3) if nothing remaining -> throw error
    if not items_with_remaining:
        frappe.msgprint(
            "All items in this Material Request already have their quantities covered by existing MRPs.",
            title="No Remaining Quantity"
        )
        return
    
    # 4) create new MRP and append only remaining-qty items
    new_mrp_doc = frappe.new_doc("MRP")
    new_mrp_doc.company = material_request_doc.company
    new_mrp_doc.posting_date = material_request_doc.transaction_date
    new_mrp_doc.expected_start_date = material_request_doc.transaction_date

    new_mrp_doc.append('material_requests', {
        'material_request': material_request_doc.name,
        'material_request_date': material_request_doc.transaction_date,
        'required_by' : material_request_doc.schedule_date,
    })

    for item, remaining_qty in items_with_remaining:
        new_mrp_doc.append('material_request_items', {
            'item_code': item.item_code,
            'material_requested_qty': remaining_qty,
            'required_by': item.schedule_date or material_request_doc.schedule_date,
            'warehouse': item.warehouse,
            'uom': item.uom,
            'material_request': material_request_doc.name,
            'material_request_item_detail': item.name,
            'qty_in_stock_uom': item.stock_qty,
            'uom_conversion_factor': item.conversion_factor,
            'stock_uom': item.stock_uom,
            'description': item.description,
            'bom_no': item.bom_no
        })

    new_mrp_doc.insert()
    # Populate sub-assemblies and raw materials automatically for the new MRP
    # get_sub_assembly_items(new_mrp_doc.name)
    # explode_bom(new_mrp_doc.name)

    return new_mrp_doc.as_dict()
