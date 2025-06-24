# Copyright (c) 2025, Digitalis Technologies Pvt Ltd and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class BOMAllocationLog(Document):
	def validate(doc):
		if doc.operation_time_per_batch_size and doc.required_qty:
			doc.total_number_of_batches = doc.required_qty / doc.operation_time_per_batch_size
	    
		if doc.total_number_of_batches and doc.operation_time_per_batch_size:
   			doc.total_operation_time = doc.total_number_of_batches * doc.operation_time_per_batch_size