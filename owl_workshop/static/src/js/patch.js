/**@odoo-module*/
import { InputBox } from "./input_box"
import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";
import {useEffect } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { useRef } from "@odoo/owl";


patch(InputBox.prototype, {
    setup() {
        super.setup()
        this.orm = useService("orm");
        this.InputFieldInputRef = useRef("InputFieldInInputBox");
        this.state=useState(
        {
        value: 0,
        next_val:0
        }
        )
     useEffect(
        (Output) => {
               this.state.next_val += Output
               console.log(Output,'Output')
            },
         () => [this.state.value]


        )
    },
    demofu(e){
        console.log(e)
        this.state.value += e
        console.log(this.state.value,'state val')
    },
    click_btn(){
        console.log(this.InputFieldInputRef.el.value)
    },
    async fetch_orm(){
//        this.sale_orders = await this.orm.call('owl.model', 'orm_call_method', []);
//        this.sale_orders= await this.orm.search("sale.order", []);
        this.sale_orders= await this.orm.searchRead("sale.order",[],['name','partner_id'],{limit:10});
        console.log(this.sale_orders,'sale orders')
    }
});
