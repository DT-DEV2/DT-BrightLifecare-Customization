frappe.listview_settings['Job Card'] = {
    onload(listview) {
        // Bulk Start + Complete + Submit in sequence_id order
        listview.page.add_inner_button('Auto Process Sequence', () => {
            const selected = listview.get_checked_items();

            if (!selected.length) {
                frappe.msgprint("Please select at least one Job Card.");
                return;
            }

            const job_cards = selected.map(d => d.name);

            frappe.call({
                method: "dt_brightlifecare_customization.public.py.job_card.bulk_process_job_cards",
                args: { job_cards },
                freeze: true,
                freeze_message: "Processing Job Cards in sequence...",
                callback(r) {
                    if (!r.exc) {
                        frappe.msgprint("All Job Cards processed successfully.");
                        listview.refresh();
                    }
                }
            });
        });
    }
};
