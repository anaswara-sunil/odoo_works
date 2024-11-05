/** @odoo-module */
import { register_payment_method } from "@point_of_sale/app/store/pos_store";
import { Payment } from "@point_of_sale/app/store/models";
import { PaymentMoneris } from "@moneris_payment/app/payment_moneris";
import { patch } from "@web/core/utils/patch";

register_payment_method("moneris", PaymentMoneris);

patch(Payment.prototype, {
    setup() {
// 2nd
        super.setup(...arguments);
        console.log(this.terminalServiceId,'setup')
        this.terminalServiceId = this.terminalServiceId || null;
    },
//3rd  -  @override
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.terminalServiceId = json.terminal_service_id;
        console.log('init_from_JSON',this.terminalServiceId,json.terminal_service_id)
    },
//4th  12th  16th  -  @override
    export_as_JSON() {
        console.log('export_as_JSON',this)
        const json = super.export_as_JSON(...arguments);
        if (json) {
            json.terminal_service_id = this.terminalServiceId;
        }
        console.log(json,json.terminal_service_id,'json moneris')
        return json;
    },

//10th
    setTerminalServiceId(id) {
        console.log('setTerminalServiceId')
        this.terminalServiceId = id;
    },
});
