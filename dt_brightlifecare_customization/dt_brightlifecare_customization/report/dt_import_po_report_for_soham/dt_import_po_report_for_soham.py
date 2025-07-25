import frappe

def execute(filters=None):
    columns = [
        {"label": "Warehouse", "fieldname": "warehouse", "fieldtype": "Link", "options": "Warehouse"},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company"},
        {"label": "Item Group", "fieldname": "item_group", "fieldtype": "Link", "options": "Item Group"},
        {"label": "Sub-Item-group", "fieldname": "sub_item_group", "fieldtype": "Data"},
        {"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date"},
        {"label": "Sno. for line items", "fieldname": "name", "fieldtype": "Link", "options": "Purchase Order"},
        {"label": "Supplier Code", "fieldname": "supplier_code", "fieldtype": "Link", "options": "Supplier"},
        {"label": "Supplier Name", "fieldname": "supplier_name", "fieldtype": "Data"},
        {"label": "Address type", "fieldname": "address_type", "fieldtype": "Data"},
        {"label": "BLC F/W Code", "fieldname": "fw_code", "fieldtype": "Data"},
        {"label": "Bright life care", "fieldname": "bright_life_care", "fieldtype": "Data"},
        {"label": "BLC Address", "fieldname": "blc_address", "fieldtype": "Data"},
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item"},
        {"label": "Item Name", "fieldname": "item_name", "fieldtype": "Data"},
        {"label": "PO Qty", "fieldname": "qty", "fieldtype": "Float"},
        {"label": "PO Rate", "fieldname": "rate", "fieldtype": "Currency"},
        {"label": "Required By Date", "fieldname": "schedule_date", "fieldtype": "Date"},
        {"label": "Manufacturer name", "fieldname": "manufacturer", "fieldtype": "Data"},
        {"label": "Internal Remarks", "fieldname": "internal_remarks", "fieldtype": "Data"},
        {"label": "Supplier Quotation No", "fieldname": "supplier_quotation", "fieldtype": "Link", "options": "Supplier Quotation"},
        {"label": "Quotation Date", "fieldname": "quotation_date", "fieldtype": "Date"},
        {"label": "Dispatch Date", "fieldname": "dispatch_date", "fieldtype": "Date"},
        {"label": "HSN Code", "fieldname": "hsn_code", "fieldtype": "Data"},
        {"label": "Item Tax Rate", "fieldname": "item_tax_rate", "fieldtype": "Percent"},
        {"label": "Taxable Amount", "fieldname": "taxable_amount", "fieldtype": "Currency"},
        {"label": "Net/Gross Amount", "fieldname": "amount", "fieldtype": "Currency"},
        {"label": "Net Rate", "fieldname": "net_rate", "fieldtype": "Currency"},
        {"label": "Description Field1", "fieldname": "description", "fieldtype": "Data"},
        {"label": "Description Field2", "fieldname": "description_2", "fieldtype": "Data"},
        {"label": "Purchase Specification", "fieldname": "purchase_specification", "fieldtype": "Data"},
        {"label": "Material Remark", "fieldname": "material_remark", "fieldtype": "Data"},
        {"label": "Packing Instruction", "fieldname": "packing_instruction", "fieldtype": "Data"},
        {"label": "External Note", "fieldname": "external_note", "fieldtype": "Data"},
        {"label": "Payment Terms", "fieldname": "payment_terms", "fieldtype": "Data"},
    ]

    data = frappe.db.sql("""
        SELECT
            po.set_warehouse AS warehouse,
            po.company AS company,             
            po.transaction_date AS posting_date,
            po.name,
            po.supplier AS supplier_code,
            po.supplier_name AS supplier_name,
            poi.item_code AS item_code,
			poi.item_name AS item_name,
            poi.qty AS qty,
            poi.rate AS rate,
            po.schedule_date AS schedule_date,
            poi.gst_hsn_code AS hsn_code,
			poi.taxable_value AS taxable_amount,
            poi.base_net_amount AS amount,
            poi.base_net_rate AS net_rate,
            poi.description AS description,
            po.tc_name AS payment_terms

        FROM `tabPurchase Order` po
		JOIN `tabPurchase Order Item` poi ON po.name = poi.parent
        WHERE po.docstatus != 2
    """, as_dict=1)

    return columns, data
