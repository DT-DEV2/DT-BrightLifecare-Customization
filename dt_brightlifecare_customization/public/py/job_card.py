# import frappe
# from frappe.utils import add_to_date, get_datetime

# @frappe.whitelist()
# def bulk_process_job_cards(job_cards):
#     """
#     job_cards = list of job card names
#     Process:
#     - Sort by sequence_id
#     - Start job card
#     - Add time_logs from_time, to_time
#     - Set completed qty
#     - Submit
#     """

#     if isinstance(job_cards, str):
#         job_cards = frappe.parse_json(job_cards)

#     # Sort job cards by sequence_id
#     job_cards = sorted(
#         job_cards,
#         key=lambda jc: frappe.db.get_value("Job Card", jc, "sequence_id") or 0
#     )

#     last_end_time = None

#     for jc_name in job_cards:
#         doc = frappe.get_doc("Job Card", jc_name)

#         # Quantity to complete
#         qty = doc.for_quantity or doc.total_completed_qty or 1

#         # TIME MANAGEMENT → NO OVERLAP
#         if last_end_time:
#             from_time = last_end_time
#         else:
#             from_time = get_datetime()

#         # Calculate to_time
#         time_required_mins = doc.time_required or 1
#         to_time = add_to_date(from_time, minutes=time_required_mins)

#         # Create / update time log row
#         if not doc.time_logs:
#             row = doc.append("time_logs", {})
#         else:
#             row = doc.time_logs[0]

#         row.from_time = from_time
#         row.to_time = to_time
#         row.completed_qty = qty  # CHILD TABLE

#         # Set completed qty in parent
#         doc.total_completed_qty = qty

#         # Update required statuses
#         doc.status = "Completed"
#         doc.completed_on = to_time

#         doc.save()
#         doc.submit()

#         last_end_time = to_time

#     return "All Job Cards processed successfully in sequence."












import frappe
from frappe.utils import add_to_date, get_datetime

@frappe.whitelist()
def bulk_process_job_cards(job_cards):
    """
    Process Job Cards in sequence_id order:
    - Start
    - Add time logs
    - Set completed quantity
    - Submit
    - Auto-shift time if ERPNext reports overlap
    """

    if isinstance(job_cards, str):
        job_cards = frappe.parse_json(job_cards)

    # Sort by sequence_id
    job_cards = sorted(
        job_cards,
        key=lambda jc: frappe.db.get_value("Job Card", jc, "sequence_id") or 0
    )

    last_end_time = None

    for jc_name in job_cards:
        doc = frappe.get_doc("Job Card", jc_name)

        # Quantity to complete
        qty = doc.for_quantity or 1

        # Get last valid end time from database
        if last_end_time:
            from_time = last_end_time
        else:
            # Check last submitted job card BEFORE this one
            prev_jc = frappe.db.sql("""
                SELECT jc.name, tl.to_time
                FROM `tabJob Card` jc
                LEFT JOIN `tabJob Card Time Log` tl ON tl.parent = jc.name
                WHERE jc.docstatus = 1 AND tl.to_time IS NOT NULL
                ORDER BY tl.to_time DESC LIMIT 1
            """, as_dict=True)

            if prev_jc:
                from_time = add_to_date(prev_jc[0].to_time, minutes=1)
            else:
                from_time = get_datetime()

        time_required_mins = doc.time_required or 1
        to_time = add_to_date(from_time, minutes=time_required_mins)

        # ------- TIME LOG WRITING WITH SAFETY --------
        if not doc.time_logs:
            row = doc.append("time_logs", {})
        else:
            row = doc.time_logs[0]

        row.from_time = from_time
        row.to_time = to_time
        row.completed_qty = qty

        doc.total_completed_qty = qty
        doc.status = "Completed"
        doc.completed_on = to_time

        try:
            doc.save()
        except Exception as e:
            # If the error is time overlap → FIX automatically
            if "overlapping" in str(e).lower():
                from_time = add_to_date(from_time, minutes=2)
                to_time = add_to_date(from_time, minutes=time_required_mins)

                row.from_time = from_time
                row.to_time = to_time
                doc.completed_on = to_time

                # retry save
                doc.save()
            else:
                raise e  # real error → stop execution

        doc.submit()

        last_end_time = to_time  # update for next job card

    return "Job Cards processed sequentially without overlap."
