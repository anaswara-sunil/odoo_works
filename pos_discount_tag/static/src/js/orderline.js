/** @odoo-module */
import { Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";


patch(Orderline.prototype, {
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            discount_price_tag: this.get_product().discount_price_tag,
        };
    },
});
