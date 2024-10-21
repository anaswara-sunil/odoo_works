/** @odoo-module */
import { register_payment_method } from "@point_of_sale/app/store/pos_store";
import { Payment } from "@point_of_sale/app/store/models";
import { PaymentMoneris } from "@moneris_payment/app/payment_moneris";
import { patch } from "@web/core/utils/patch";

register_payment_method("moneris", PaymentMoneris);

patch(Payment.prototype, {
    setup() {
        super.setup(...arguments);
        this.terminalServiceId = this.terminalServiceId || null;
    },
    //@override
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        if (json) {
            json.terminal_service_id = this.terminalServiceId;
        }
        console.log(json,'json moneris')
        return json;
    },
    //@override
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.terminalServiceId = json.terminal_service_id;
    },
    setTerminalServiceId(id) {
        this.terminalServiceId = id;
    },
});
