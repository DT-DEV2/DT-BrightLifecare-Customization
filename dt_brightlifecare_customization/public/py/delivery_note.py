import frappe
from frappe import _
from frappe.utils import flt


def before_submit(doc, method):
    validate_reserve_stock_against_delivery_note(doc, method)



def validate_reserve_stock_against_delivery_note(doc, method):

    mrp_settings = frappe.get_single("MRP Settings")
    if mrp_settings.validate_reserve_stock_against_delivery_note == 0:
        return

    msg_list = []

    for item in doc.items:

        if not item.item_code or not item.warehouse:
            continue

        bin_data = frappe.db.get_value(
            "Bin",
            {
                "item_code": item.item_code,
                "warehouse": item.warehouse
            },
            [
                "actual_qty",
                "custom_reserved_stock_for_mrp"
            ],
            as_dict=True
        ) or {}

        actual_qty = flt(bin_data.get("actual_qty"))
        reserved_qty = flt(bin_data.get("custom_reserved_stock_for_mrp"))
        available_qty = actual_qty - reserved_qty
        requested_qty = flt(item.qty)

        if requested_qty > available_qty:

            msg = _(
                "Requested {0} units of {1} from {2}, but only {3} units are available "
                "after reserving {4} units for MRP."
            ).format(
                frappe.bold(frappe.format_value(requested_qty)),
                frappe.get_desk_link("Item", item.item_code),
                frappe.get_desk_link("Warehouse", item.warehouse),
                frappe.bold(frappe.format_value(available_qty)),
                frappe.bold(frappe.format_value(reserved_qty)),
            )

            if available_qty > 0:
                msg += " " + _(
                    "As stock is reserved for MRP, you are allowed to deliver only {0} units."
                ).format(
                    frappe.bold(frappe.format_value(available_qty))
                )
            else:
                msg += " " + _(
                    "As the full stock is reserved for MRP, you're not allowed to deliver the stock."
                )

            msg_list.append(msg)

    if msg_list:
        frappe.throw(
            "<br><br>".join(msg_list),
            title=_("Insufficient Stock for Delivery")
        )