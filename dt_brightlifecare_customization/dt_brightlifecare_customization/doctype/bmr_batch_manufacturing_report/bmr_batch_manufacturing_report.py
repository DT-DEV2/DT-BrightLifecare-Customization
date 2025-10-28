# Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BMRBatchManufacturingReport(Document):
    def before_insert(self):
        # Get the user creating the Work Order or fallback to owner
        user = frappe.session.user if frappe.session.user and frappe.session.user != "Guest" else self.owner

        # Set 'requisition_given_by' automatically if not already set
        if not self.requisition_given_by:
            self.requisition_given_by = user
