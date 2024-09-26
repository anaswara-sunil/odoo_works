/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToFragment  } from "@web/core/utils/render";


function chunkArray(arr, size) {
        const result = [];
        for (let i = 0; i < arr.length; i += size)
            { result.push(arr.slice(i, i + size)); }
        return result;
    }
var LatestEvents = PublicWidget.Widget.extend({
        selector: '.latest_events_snippet',
        events: {
        'click .card-body': '_onEventClick',
        },
        async _onEventClick(ev) {
           var eventId = $(ev.currentTarget).children().html();
           const token = await jsonrpc('/latest_events/event_id', {
            eventId
           })
            .then(function(event){
            console.log(event,'event')
            var id = event['event']
            console.log(id,'id')

            window.location = `/event/detail/${id}`;
            })
        },

         willStart: async function () {
            const data = await jsonrpc('/latest_events', {})
            const events = data
            console.log(data,'data')
            Object.assign(this, {
                events
            })
//            this.events = chunkArray(events, 4);
            console.log(this.events, ' events');
        },

        start: function () {
            const refEl = this.$el.find("#latest_events_carousel");
            console.log(this, 'this');
            const { events } = this;
            const unique_id = `event_carousel-${Math.floor(Math.random() * 1000)}`;
            console.log(unique_id,'unique_id')
            const chunkData = chunkArray(events, 4);
            chunkData[0].is_active = true
            console.log(chunkData, 'chunkData');
            refEl.html(renderToFragment ("school_management.latest_event", { events,chunkData,unique_id }));
        },
    });
PublicWidget.registry.latest_event_snippet = LatestEvents;
return LatestEvents;
