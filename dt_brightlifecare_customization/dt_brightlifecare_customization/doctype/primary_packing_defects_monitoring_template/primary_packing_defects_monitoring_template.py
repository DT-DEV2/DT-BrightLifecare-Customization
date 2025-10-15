# Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PrimaryPackingDefectsMonitoringTemplate(Document):
    def validate(self):
        if self.is_default:
            frappe.db.sql("""
				UPDATE `tabPrimary Packing Defects Monitoring Template`
				SET is_default = 0
                WHERE name != %s
			""", (self.name,))
