import frappe
from frappe.model.document import Document

class BatchPackagingRecordBPR(Document):
    def before_insert(self):
        """
        Set performed_by_setup as the creator of the BPR
        """
        if not self.performed_by_setup:
            self.performed_by_setup = self.owner

        if not self.performed_by_line:
            self.performed_by_line = self.owner

        if not self.performed_by_packing:
            self.performed_by_packing = self.owner

        if not self.performed_by_rh:
            self.performed_by_rh = self.owner

        if not self.performed_by_primary:
            self.performed_by_primary = self.owner
        
        if not self.performed_by_coding:
            self.performed_by_coding = self.owner
        
        if not self.performed_by_defects:
            self.performed_by_defects = self.owner
        
        if not self.performed_by_secondary:
            self.performed_by_secondary = self.owner
        
        if not self.performed_by_online:
            self.performed_by_online = self.owner
        
        if not self.performed_by_sample:
            self.performed_by_sample = self.owner
        
        if not self.performed_by_reconcile:
            self.performed_by_reconcile = self.owner
        
        if not self.performed_by_excess:
            self.performed_by_excess = self.owner
        
        if not self.performed_by_shipper:
            self.performed_by_shipper = self.owner
        
        if not self.performed_by_finished:
            self.performed_by_finished = self.owner

        if not self.performed_by_bar:
            self.performed_by_bar = self.owner
        
        if not self.performed_by_deviation:
            self.performed_by_deviation = self.owner

    def before_save(self):
        """
        Fetch BOM items and populate child table
        """
        bom_no = self.revision_no  # BOM name from your field

        if not bom_no:
            return

        # fetch BOM items in idx order
        bom_items = frappe.get_all(
            "BOM Item",
            filters={"parent": bom_no},
            fields=["item_code", "item_name", "idx"],
            order_by="idx asc"
        )

        # clear child table safely
        self.machinery_setup_dispensing_request_detail.clear()

        # append rows
        for item in bom_items:
            row = self.append("machinery_setup_dispensing_request_detail", {})
            row.item_code = item.item_code
            row.item_name = item.item_name
