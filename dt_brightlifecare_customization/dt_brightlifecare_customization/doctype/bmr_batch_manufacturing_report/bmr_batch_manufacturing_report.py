# Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BMRBatchManufacturingReport(Document):
    def before_insert(self):
        user = frappe.session.user if frappe.session.user and frappe.session.user != "Guest" else self.owner
        if not self.requisition_given_by:
            self.requisition_given_by = user

        # --- Auto populate blend_output table ---
        if self.reference_name:
            work_order = frappe.get_doc("Work Order", self.reference_name)
            item_batch_size = work_order.custom__item_batch_size
            lot_size = work_order.custom_lot_size
            lot_count = work_order.custom_lot_count

            if item_batch_size and lot_count:
                self.blend_output = []  # clear existing rows
                total_batch_size = float(item_batch_size)
                lot_count = int(lot_count)
                lot_size = float(lot_size) if lot_size else None

                remaining = total_batch_size

                for i in range(lot_count):
                    row = self.append("blend_output", {})

                    # Case 1: Lot size is defined
                    if lot_size:
                        if remaining >= lot_size and i < lot_count - 1:
                            row.std_lot_weight = round(lot_size, 3)
                            remaining -= lot_size
                        else:
                            # Last or smaller remaining amount
                            row.std_lot_weight = round(remaining, 3)
                            remaining = 0

                    # Case 2: Lot size not defined → equal division
                    else:
                        std_lot_weight = total_batch_size / lot_count
                        if i < lot_count - 1:
                            row.std_lot_weight = round(std_lot_weight, 3)
                            remaining -= std_lot_weight
                        else:
                            row.std_lot_weight = round(remaining, 3)
                            remaining = 0
            else:
                frappe.msgprint("⚠️ Missing Item Batch Size or Lot Count in Work Order.")
