/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosBus } from "@point_of_sale/app/bus/pos_bus_service";

patch(PosBus.prototype, {
    // Override
    dispatch(message) {
//        console.log('dispatch(message)')
        super.dispatch(...arguments);

        if (message.type === "MONERIS_LATEST_RESPONSE" && message.payload === this.pos.config.id) {
            this.pos
                .getPendingPaymentLine("moneris")
                .payment_method.payment_terminal.handleMonerisStatusResponse();
        }
    },
});
