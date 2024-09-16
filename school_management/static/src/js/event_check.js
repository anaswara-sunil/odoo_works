/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from "@web/core/network/rpc_service";


publicWidget.registry.eventCheck = publicWidget.Widget.extend({
    selector: '.event_table',
    events: {
        'click .clickable_raw': '_onEventClick',
    },

     async _onEventClick(ev) {
        console.log($(ev.currentTarget).children().html(),'ev')
        var eventId = $(ev.currentTarget).children().html();
        console.log(eventId,'eventId')
        console.log(eventId,'id')
        const token = await jsonrpc('/event/event_id', {
            eventId
        })
        .then(function(event){
            console.log(event,'event')
            var id = event['event']
            console.log(id,'id')

            window.location = `/event/detail/${id}`;
        })
},

});

////event reg form-date check
publicWidget.registry.dateCheck = publicWidget.Widget.extend({
    selector: '.event_form_template',
    events: {
        'change #start_date': '_start_dateChange',
        'change #end_date': '_end_dateChange',
    },
    _start_dateChange() {
        console.log('start')
        var $start_date = new Date($('#start_date').val());
        var $end_date = new Date($('#end_date').val());
        var $SubmitError = $('#submit_error');
        if ($start_date && $end_date) {
            this.CustomFunction();
        }
    },

    _end_dateChange() {
        console.log('end')
        var $start_date = new Date($('#start_date').val());
        var $end_date = new Date($('#end_date').val());
        var $SubmitError = $('#submit_error');
        if ($start_date && $end_date) {
            this.CustomFunction();
        }
    },

    CustomFunction() {
        var $start_date = new Date($('#start_date').val());
        var $end_date = new Date($('#end_date').val());
        var $SubmitError = $('#submit_error');
        if ($start_date && $end_date) {
            if ($start_date > $end_date) {
                $SubmitError.text('Start date should be lower than End date');
            }
            else{
             $SubmitError.text("")
            }
        }

    }

});

//clubs as many-2-many - tags
var CustomForm = publicWidget.Widget.extend({
    selector: '.clubs_name',
    start: function () {
    $('.multiple-selection').select2();
    },
    });
publicWidget.registry.Many2many_tag = CustomForm;
return CustomForm;