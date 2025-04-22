import frappe

@frappe.whitelist(allow_guest=True)
def uom_filter_condition(doctype, txt, searchfield, start, page_len, filters):
    item_code = filters.get('item_code')
    print("Item Code:", item_code) 

    data = frappe.db.sql("""
        SELECT u.uom
        FROM `tabItem` i, `tabUOM Conversion Detail` u
        WHERE u.parent = i.name AND i.name = %s
    """, (item_code,), as_dict=1)
    print("Data:", data)
    
    uom_values = [(item['uom'], item['uom']) for item in data]

    return uom_values