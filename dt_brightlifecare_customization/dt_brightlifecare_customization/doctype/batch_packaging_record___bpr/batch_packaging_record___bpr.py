import frappe
from frappe.model.document import Document

class BatchPackagingRecordBPR(Document):
    
    def before_save(self):
        bom_no = self.revision_no     # BOM name from your field

        if not bom_no:
            return

        # fetch BOM items in the same order (idx order)
        bom_items = frappe.get_all(
            "BOM Item",
            filters={"parent": bom_no},
            fields=["item_code", "item_name", "idx"],
            order_by="idx asc"
        )

        # clear child table first
        self.machinery_setup_dispensing_request_detail = []

        # append in the same order
        for item in bom_items:
            row = self.append("machinery_setup_dispensing_request_detail", {})
            row.item_code = item.item_code
            row.item_name = item.item_name
