/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from "@web/core/network/rpc_service";


publicWidget.registry.leaveCheck = publicWidget.Widget.extend({
    selector: '.leave_form_template',
    events: {
        'change #students_name': '_students_nameChange',
        'click #half_day': '_half_dayChange',
        'change #end_date': '_end_dateChange',
        'change #start_date': '_start_dateChange',

    },

    async _students_nameChange() {
        console.log("function");
        var test_variable = $("#students_name").val();
        var class_name = $("#current_class").val();
        console.log(test_variable, 'test');
        const token = await jsonrpc('/leave/class_id', {
            test_variable
        })
        .then(function(class_name) {
            $("#current_class").val(class_name.class_name);
        });
    },

    _half_dayChange() {
        var $checkbox = $('#half_day');
        var $end_date = $('#end_date');
        var $start_date = $('#start_date');
        var $total_days = $('#total_days');
        if ($checkbox.is(':checked')) {
            $end_date.hide(); $('#end_date_span').hide();
            $total_days.val("0.5");
        }
        else {
            $end_date.val("");
            $total_days.val("");
            $end_date.show();
             $('#end_date_span').show();
             console.log('else');
         }
    },

    _start_dateChange() {
        var $start_date = $('#start_date').val();
        var $end_date = $('#end_date').val();
        var $checkbox = $('#half_day');
        var $total_days = $('#total_days');
        if (start_date && end_date) {
            this.CustomFunction();
        }
        if ($start_date && !$end_date && !$checkbox.is(':checked')) {
            $total_days.val(1);
        }
     },

    _end_dateChange(ev){
        this.CustomFunction();
    },

    CustomFunction() {
        var start_date = new Date($('#start_date').val());
        var end_date = new Date($('#end_date').val());
        var $total_days = $('#total_days');
        var $DateError = $('#date_error');
        var days = 0;
        var new_date = start_date;
        if (new_date && end_date) {
            if (new_date > end_date) {
                $DateError.text('Start date should be lower than End date');
            }
            else {
                while (new_date <= end_date) {
                    if (new_date.getDay() !== 0 && new_date.getDay() !== 6) {
                        days += 1;
                        console.log(days, 'days');
                        $total_days.val(days);
                    }
                    new_date.setDate(new_date.getDate() + 1);
                }
            }
        }
    },
});

