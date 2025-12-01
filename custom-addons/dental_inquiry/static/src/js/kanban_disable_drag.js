/** @odoo-module **/

import { KanbanController } from "@web/views/kanban/kanban_controller";
import { patch } from "@web/core/utils/patch";

patch(KanbanController.prototype, {
    get canDragAndDrop() {
        // Disable drag and drop for crm.lead kanban (dental inquiries)
        if (this.props.resModel === 'crm.lead') {
            return false;
        }
        return super.canDragAndDrop;
    },
});

