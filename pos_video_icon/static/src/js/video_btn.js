/** @odoo-module */
import { ProductsWidget } from "@point_of_sale/app/screens/product_screen/product_list/product_list";
import { patch } from "@web/core/utils/patch";
import { ProductVideoPopup } from "./product_video_popup"

patch(ProductsWidget.prototype, {
     async onProductVideoClick(product) {
       this.popup.add(ProductVideoPopup, { product: product });
    }
});
