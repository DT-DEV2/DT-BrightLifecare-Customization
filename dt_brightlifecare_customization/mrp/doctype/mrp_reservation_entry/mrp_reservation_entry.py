# Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class MRPReservationEntry(Document):
	def on_submit(self):
		# Increment reserved stock directly without recalculating available qty
		custom_reserved_stock = frappe.db.get_value(
			"Bin",
			{"item_code": self.item_code, "warehouse": self.warehouse},
			"custom_reserved_stock_for_mrp"
		) or 0

		frappe.db.set_value(
			"Bin",
			{"item_code": self.item_code, "warehouse": self.warehouse},
			"custom_reserved_stock_for_mrp",
			flt(custom_reserved_stock) + flt(self.balance_reserved_qty)
		)

		self.db_set("status", "Reserved")




	def on_cancel(self):
		if self.balance_reserved_qty and self.balance_reserved_qty > 0:
			custom_reserved_stock = frappe.db.get_value(
				"Bin",
				{"item_code": self.item_code, "warehouse": self.warehouse},
				"custom_reserved_stock_for_mrp"
			) or 0

			custom_reserved_stock = flt(custom_reserved_stock)
			balance_reserved = flt(self.balance_reserved_qty)

			new_reserved = custom_reserved_stock - balance_reserved if custom_reserved_stock >= balance_reserved else 0

			frappe.db.set_value(
				"Bin",
				{"item_code": self.item_code, "warehouse": self.warehouse},
				"custom_reserved_stock_for_mrp",
				new_reserved
			)

		self.db_set("status", "Cancelled")
