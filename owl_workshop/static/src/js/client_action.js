/** @odoo-module */
import { registry } from "@web/core/registry";
import { InputBox} from "./input_box";
import {
    Component,
 } from "@odoo/owl";

class AdvancedDashboard extends Component {


}
AdvancedDashboard.template = "owl_workshop.advanced_dashboard"
AdvancedDashboard.components = {
    InputBox
}
registry.category("actions").add("advanced_dashboard",AdvancedDashboard)
