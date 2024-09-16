/**@odoo-module*/
import { InputBox } from "./input_box"
import { patch } from "@web/core/utils/patch";

patch(InputBox.prototype, {
    setup() {
        super.setup()

    },
    demofu(){
        console.log("hii")
    }
});