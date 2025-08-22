import frappe
from frappe.utils import flt
from frappe import _


@frappe.whitelist()
def create_mrp(material_request, use_defaults=False):
    material_request_doc = frappe.get_doc('Material Request', material_request)
    missing_items = []
    for item in material_request_doc.items:
        if not item.item_code:
            missing_items.append({
                "Row no in Items": item.idx,
                "Item Code": item.item_code or "Missing",
                # "Bom No": item.bom_no or "Missing"
            })

    if missing_items and not frappe.utils.cint(use_defaults):
        frappe.throw(
            ("Some fields are missing in items: {0}.").format(missing_items)
        )

    new_mrp_doc = frappe.new_doc("MRP")
    new_mrp_doc.company = material_request_doc.company
    new_mrp_doc.posting_date = material_request_doc.transaction_date
    new_mrp_doc.expected_start_date = material_request_doc.transaction_date
    
    new_mrp_doc.append('material_requests', {
        'material_request': material_request_doc.name,
        'material_request_date': material_request_doc.transaction_date,
        'required_by' : material_request_doc.schedule_date,
    })

    for item in material_request_doc.items:
        bom_and_warehouse = get_best_bom(item.item_code, item.warehouse)

        # fallback to item.bom_no if available
        best_bom = bom_and_warehouse.get("bom")
        # best_warehouse = bom_and_warehouse.get("warehouse")

        new_mrp_doc.append('material_request_items', {
            'item_code': item.item_code,
            'material_requested_qty': item.qty,
            'required_by': item.schedule_date,
            'warehouse': item.warehouse,
            'uom': item.uom,
            'material_request': material_request_doc.name,
            'material_request_item_detail': item.name,
            'qty_in_stock_uom': item.stock_qty,
            'uom_conversion_factor': item.conversion_factor,
            'stock_uom': item.stock_uom,
            'description': item.description,
            'bom_no': best_bom
        })

    new_mrp_doc.insert()

    return new_mrp_doc.as_dict()





def get_best_bom(item_code, warehouse):
    result = frappe.db.sql("""
        SELECT name AS bom, custom_source_warehouse AS warehouse
        FROM `tabBOM`
        WHERE item = %s AND custom_source_warehouse = %s AND is_active = 1 AND docstatus = 1
        ORDER BY custom_fg_batch_size DESC, custom_priority DESC
        LIMIT 1
    """, (item_code, warehouse,), as_dict=True)

    return result[0] if result else {}
