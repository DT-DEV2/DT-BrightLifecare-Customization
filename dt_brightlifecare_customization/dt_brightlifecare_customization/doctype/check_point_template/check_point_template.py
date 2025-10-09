# Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CheckPointTemplate(Document):
    def validate(self):
        # If this record is marked as default
        if self.is_default:
            # Uncheck 'is_default' in all other Check Point Templates
            frappe.db.sql("""
                UPDATE `tabCheck Point Template`
                SET is_default = 0
                WHERE name != %s
            """, (self.name,))
