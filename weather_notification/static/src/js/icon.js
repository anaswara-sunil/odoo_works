/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import {Dropdown} from '@web/core/dropdown/dropdown';
import {DropdownItem} from '@web/core/dropdown/dropdown_item';
import { useState } from "@odoo/owl";
import { session } from '@web/session';


class SystrayIcon extends Component {
    async setup() {
       super.setup(...arguments);
       this.action = useService("action");
       this.rpc = useService("rpc");
       this.orm = useService("orm");

       this.state=useState(
            {weatherData: null ,
             date: new Date().toDateString(),
             icon_code:null,
             icon_url:null,
             temp:null,
             boolean : session.is_weather_boolean,
             stage:true,
             api_loc:false,
            })
    }

    async getApiKey() {
        const res= await this.orm.call('ir.config_parameter', 'get_param', ['api']);
        return res;
    }

    async getLocation() {
         const res= await this.orm.call('ir.config_parameter', 'get_param', ['location']);
         return res;
    }

    async _openWeather()  {
        const apiKey = await this.getApiKey();
        const location = await this.getLocation();
        console.log(apiKey,location,'api,loc')

        if (apiKey && !location){
            console.log('api only')
            this.state.stage = true;
            console.log(this.state.stage,'stage')
        }
        else if (!apiKey && location){
            console.log('location only')
            this.state.stage = false;
            console.log(this.state.stage,'stage')
        }
        else if (apiKey && location) {
            const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${location}&appid=${apiKey}`);
            if (response.ok) {
                const data = await response.json();
                this.state.weatherData = data;
                this.state.icon_code = this.state.weatherData.weather[0].icon;
                    this.state.icon_url = "http://openweathermap.org/img/w/" + this.state.icon_code + ".png";
                this.state.temp = (this.state.weatherData.main.temp/10).toFixed(2);
                console.log(this.state.boolean,'state boolean')}
        }
        else{
            this.state.api_loc = true;
        }
    }

}
   SystrayIcon.template = "systray_icon";
   SystrayIcon.components = {Dropdown, DropdownItem };
   export const systrayItem = { Component: SystrayIcon,};
   registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });


