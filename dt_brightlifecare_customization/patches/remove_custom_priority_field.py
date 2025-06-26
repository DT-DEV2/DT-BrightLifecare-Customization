import frappe

def execute():
    table = "BOM"
    column = "custom_priority"
    tablename = f"tab{table}"

    try:
        if column in frappe.db.get_table_columns(table):
            # Step 1: Clean non-numeric values to prevent cast errors
            frappe.db.sql(f"""
                UPDATE `{tablename}`
                SET `{column}` = 0
                WHERE `{column}` IS NOT NULL AND `{column}` NOT REGEXP '^[0-9]+$'
            """)
            frappe.db.commit()

            # Step 2: Drop the column
            frappe.db.sql(f"ALTER TABLE `{tablename}` DROP COLUMN `{column}`")
            frappe.db.commit()
        else:
            frappe.logger().info(f"[PATCH] Column `{column}` not found in `{table}`, skipping drop.")

        # Step 3: Clean up lingering Custom Field metadata (if exists)
        if frappe.db.exists("Custom Field", f"{table}-{column}"):
            frappe.delete_doc("Custom Field", f"{table}-{column}", force=True)
            frappe.db.commit()

    except Exception as e:
        raise
