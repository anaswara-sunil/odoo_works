/** @odoo-module */
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";

export class ProductVideoPopup extends AbstractAwaitablePopup{
    static template = "point_of_sale.ProductVideoPopup";
    static defaultProps ={
//        closePopup: _t("Cancel"),
        title: _t("Product Details"),
        cancelKey: false,
    };
}