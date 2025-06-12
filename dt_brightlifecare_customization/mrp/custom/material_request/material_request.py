import frappe
from frappe.utils import flt
from frappe import _


@frappe.whitelist()
def create_mrp(material_request, use_defaults=False):
    material_request_doc = frappe.get_doc('Material Request', material_request)
    missing_items = []
    for item in material_request_doc.items:
        if not item.item_code or not item.bom_no:
            missing_items.append({
                "Row no in Items": item.idx,
                "Item Code": item.item_code or "Missing",
                "Bom No": item.bom_no or "Missing"
            })

    if missing_items and not frappe.utils.cint(use_defaults):
        frappe.throw(
            ("Some fields are missing in items: {0}.").format(missing_items)
        )

    new_mrp_doc = frappe.new_doc("MRP")
    new_mrp_doc.get_items_from = "Material Request"
    # if material_request_doc.set_warehouse:
    #     branch = frappe.get_value("Warehouse", material_request_doc.set_warehouse, "custom_branch")
    #     if branch:
    #         new_mrp_doc.custom_branch = branch

    new_mrp_doc.append('material_requests', {
        'material_request': material_request_doc.name,
        'material_request_date': material_request_doc.transaction_date
    })

    for item in material_request_doc.items:
        new_mrp_doc.append('assembly_items', {
            'item_code': item.item_code,
            'planned_qty': item.qty,
            'schedule_date': item.schedule_date,
            'warehouse': item.warehouse,
            'uom': item.uom,
            'material_request': material_request_doc.name,
            'bom_no': item.bom_no or 0,
            'quantity': item.qty
        })

    new_mrp_doc.insert()

    return new_mrp_doc.as_dict()






