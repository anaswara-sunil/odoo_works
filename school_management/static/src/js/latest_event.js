/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";

var LatestEvents = PublicWidget.Widget.extend({
        selector: '.latest_events_snippet',
        willStart: async function () {
            const data = await jsonrpc('/latest_events', {})
            const events = data
            console.log(data,'data')
            Object.assign(this, {
                events
            })
        },
        start: function () {
            const refEl = this.$el.find("#latest_events_carousel")
            console.log(this,'this')
            const {events} = this
            console.log(events,'event')
            refEl.html(renderToElement("school_management.latest_event",{events}))
        },
    });
PublicWidget.registry.latest_event_snippet = LatestEvents;
return LatestEvents;
