# Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class BMRBatchManufacturingReport(Document):
    def before_insert(self):
        user = frappe.session.user if frappe.session.user and frappe.session.user != "Guest" else self.owner
        if not self.requisition_given_by:
            self.requisition_given_by = user

        # --- Auto populate blend_output table from Work Order ---
        if self.reference_name:
            work_order = frappe.get_doc("Work Order", self.reference_name)

            item_batch_size = flt(work_order.custom__item_batch_size)
            lot_size = flt(work_order.custom_lot_size)
            lot_count = int(flt(work_order.custom_lot_count))

            if item_batch_size and lot_count:
                self.blend_output = []  # clear existing rows
                total_batch_size = item_batch_size
                remaining = total_batch_size

                for i in range(lot_count):
                    row = self.append("blend_output", {})

                    if lot_size:  # Case 1: custom lot size defined
                        if remaining >= lot_size and i < lot_count - 1:
                            std_weight = round(lot_size, 3)
                        else:
                            std_weight = round(remaining, 3)
                        remaining -= std_weight
                    else:  # Case 2: equal division
                        std_weight = round(total_batch_size / lot_count, 3)
                        if i == lot_count - 1:
                            std_weight = round(remaining, 3)
                        remaining -= std_weight

                    row.std_lot_weight = std_weight

            # Fetch and set item batch size
            self.item_batch_size = item_batch_size or 0.00

            # --- Fetch and set Theoretical Yield from BOM ---
            if work_order.bom_no:
                theoretical_yield = frappe.db.get_value(
                    "BOM",
                    work_order.bom_no,
                    "custom_theoretical_yield_"
                )
                self.theoretical_yield_batch = flt(theoretical_yield or 0.00)

        # Initialize previous product + selected_bom to safe defaults
        self.previous_product = None
        self.previous_product_line = None
        self.previous_product_1 = None
        self.previous_product_powder = None
        selected_bom = None  # <---- ensure this is always defined

        if self.reference_name:
            wo_bom = frappe.db.get_value("Work Order", self.reference_name, "bom_no")
            if wo_bom:
                nut_boms = frappe.db.sql("""
                    SELECT DISTINCT parent
                    FROM `tabBOM Item`
                    WHERE bom_no = %s
                """, (wo_bom,), as_dict=True)

                if nut_boms:
                    nut_bom_names = [n["parent"] for n in nut_boms]
                    bom_details = frappe.db.sql(f"""
                        SELECT
                            name,
                            custom_source_warehouse,
                            quantity,
                            custom_priority,
                            is_default
                        FROM `tabBOM`
                        WHERE name IN ({', '.join(['%s'] * len(nut_bom_names))})
                    """, tuple(nut_bom_names), as_dict=True)

                    # decide selected_bom robustly
                    if len(bom_details) == 1:
                        selected_bom = bom_details[0]["name"]
                    else:
                        default_boms = [b for b in bom_details if b.get("is_default")]
                        if default_boms:
                            selected_bom = default_boms[0]["name"]
                        else:
                            sorted_boms = sorted(
                                bom_details,
                                key=lambda b: (
                                    -(b.get("custom_priority") or 0),
                                    -(b.get("quantity") or 0)
                                )
                            )
                            if sorted_boms:
                                selected_bom = sorted_boms[0]["name"]

                    if selected_bom:
                        previous_product_item = frappe.db.get_value(
                            "BOM",
                            selected_bom,
                            "item"
                        )
                        if previous_product_item:
                            self.previous_product = previous_product_item
                            self.previous_product_line = previous_product_item
                            self.previous_product_1 = previous_product_item
                            self.previous_product_powder = previous_product_item

        # Fetch Batch No from latest Work Order for the same BOM as used in previous_product
        self.batch_no = None
        self.batch_no_line = None
        self.b_no = None
        self.batch_no_powder = None
        if self.reference_name:
            # Step 1: Use the same BOM selected for previous_product
            if selected_bom:
                # Step 2: Find latest Work Order using this BOM
                latest_wo = frappe.db.sql("""
                    SELECT name
                    FROM `tabWork Order`
                    WHERE bom_no = %s
                    ORDER BY creation DESC
                    LIMIT 1
                """, (selected_bom,), as_dict=True)

                if latest_wo:
                    latest_wo_name = latest_wo[0].get("name")

                    # Step 3: Fetch Batch linked to that Work Order
                    batch_doc = frappe.db.get_value(
                        "Batch",
                        {
                            "reference_doctype": "Work Order",
                            "reference_name": latest_wo_name,
                        },
                        "name",
                    )

                    if batch_doc:
                        self.batch_no = batch_doc
                        self.batch_no_line = batch_doc
                        self.b_no = batch_doc
                        self.batch_no_powder = batch_doc

        # -------------------------------------------------------------------
        # ADDITION 1: Theoretical Yield → Theoretical Yield Reconcile
        # -------------------------------------------------------------------
        self.theoretical_yield_reconcile = self.theoretical_yield or 0.00

        # -------------------------------------------------------------------
        # ADDITION 2: Fetch area_used from Work Order
        # -------------------------------------------------------------------
        if self.reference_name:
            area_used = frappe.db.get_value(
                "Work Order",
                self.reference_name,
                "custom_area_used"
            )
            self.area_used = area_used or 0.00
        
        if not self.created_by_line_clearance:
            self.created_by_line_clearance = self.owner

        if not self.created_by_bill_of_material:
            self.created_by_bill_of_material = self.owner

        if not self.created_by_rm:
            self.created_by_rm = self.owner

        if not self.created_by_powder:
            self.created_by_powder = self.owner

        if not self.created_by_sieve:
            self.created_by_sieve = self.owner
        
        if not self.created_by_manufacture:
            self.created_by_manufacture = self.owner
        
        if not self.created_by_blend:
            self.created_by_blend = self.owner
        
        if not self.created_by_label:
            self.created_by_label = self.owner
        
        if not self.created_by_enclosure:
            self.created_by_enclosure = self.owner
        
        if not self.created_by_reconcile:
            self.created_by_reconcile = self.owner
    def before_save(self):
        # 1️⃣ Fetch item_batch_size from Work Order
        if self.reference_name:
            item_batch_size = frappe.db.get_value(
                "Work Order",
                self.reference_name,
                "custom__item_batch_size"
            )
            self.item_batch_size = float(item_batch_size or 0)
        else:
            self.item_batch_size = 0

        # 2️⃣ Calculate bulk weight and actual yield after manufacturing
        total_weight = sum(float(d.net_weight_kg or 0) for d in self.blend_output)
        self.bulk_weight_found_after_manufacturing = total_weight

        if self.item_batch_size:
            try:
                actual_yield = (
                    float(self.bulk_weight_found_after_manufacturing)
                    / float(self.item_batch_size)
                ) * 100
                self.actual_yield_after_manufacturing = actual_yield
            except ZeroDivisionError:
                self.actual_yield_after_manufacturing = 0
        else:
            self.actual_yield_after_manufacturing = 0

        # 3️⃣ Fetch QC Sample Quantity (in gm)
        self.quantity_of_qc_sample_gm = 0
        if self.reference_name:
            manufacture_entry = frappe.db.get_value(
                "Stock Entry",
                {
                    "work_order": self.reference_name,
                    "stock_entry_type": "Manufacture",
                    "docstatus": ["<", 2],
                },
                "name",
            )

            if manufacture_entry:
                quality_inspection = frappe.db.get_value(
                    "Quality Inspection",
                    {
                        "reference_type": "Stock Entry",
                        "reference_name": manufacture_entry,
                    },
                    "name",
                )

                if quality_inspection:
                    sample_transfer = frappe.db.get_value(
                        "Stock Entry",
                        {"stock_entry_type": "Sample Internal Transfer"},
                        "name",
                    )

                    if sample_transfer:
                        qty = frappe.db.get_value(
                            "Stock Entry Detail",
                            {"parent": sample_transfer},
                            "qty",
                        )
                        self.quantity_of_qc_sample_gm = float(qty or 0)

        # 4️⃣ Calculate Process Loss
        self.processloss_during_manufacturing = (
            float(self.item_batch_size or 0)
            - float(self.bulk_weight_found_after_manufacturing or 0)
            - float(self.quantity_of_qc_sample_gm or 0)
        )

        # 5️⃣ Calculate Actual Yield for Packing
        try:
            self.actual_yield_for_packing = (
                (float(self.bulk_weight_found_after_manufacturing or 0)
                - float(self.quantity_of_qc_sample_gm or 0))
                / float(self.item_batch_size or 1)
            ) * 100
        except ZeroDivisionError:
            self.actual_yield_for_packing = 0
