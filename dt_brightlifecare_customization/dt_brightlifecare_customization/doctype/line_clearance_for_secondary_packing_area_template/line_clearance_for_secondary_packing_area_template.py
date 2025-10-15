# Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LineClearanceforSecondaryPackingAreaTemplate(Document):
	def validate(self):
		if self.is_default:
			frappe.db.sql("""
			UPDATE `tabLine Clearance for Secondary Packing Area Template`
			SET is_default = 0
			WHERE name != %s
			""", (self.name,))
