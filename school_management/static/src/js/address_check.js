/** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from "@web/core/network/rpc_service";


publicWidget.registry.registrationAddress = publicWidget.Widget.extend({
    selector: '.registration_form_template',
    events: {
        'click .is_same': '_is_sameChange',
        'change #dob': '_is_DobChange',
        'change #tc': '_tc_Change',
        'click #submit_btn': '_btn_Click'
    },
    init() {
        this._super(...arguments);
        this.result = 0;
    },

     _is_sameChange() {
        var $checkbox = $('#is_same');
        var $communicationAddress = $('#communication_addr');
        var $permanentAddress = $('#permanent_addr');

        if ($checkbox.is(':checked')) {
            console.log("checked");
            var communicationAddressValue = $communicationAddress.val();
            $permanentAddress.val(communicationAddressValue);
            $('#permanent_addr').hide();
            $('#permanent_addr_span').hide();
            }

        else {
            $permanentAddress.val("");
            $('#permanent_addr').show();
            $('#permanent_addr_span').show();
            console.log('else');
            }
     },

     _is_DobChange() {
        var dob = new Date($('#dob').val());
        var today = new Date();
        console.log(today.getFullYear(), 'today year');
        var $age = $('#age');
        if (dob) {
            $age.val(today.getFullYear() - dob.getFullYear());
            console.log($age.val());
            }
    },

     _tc_Change() {
            console.log("function");
            var fileInput = $('#tc')[0]; // Get the DOM element
            var file = fileInput.files[0];
            var $fileError = $('#tc_error');
            if (file) {
                var fileType = file.type;
                if (fileType !== 'application/pdf') {
                    console.log('not pdf');
                    $fileError.text('**Please upload a PDF file.');
                    this.result += 1;
                    console.log(this.result, 'incre');
                }
                else {
                    this.result = 0;
                    $fileError.text('');
                }
            }
         },

     _btn_Click() {
            console.log('btn');
            var $form = $('#form_id');
            var $SubmitError = $('#submit_error');
            var first_name = $('#first_name').val();
            var communication_addr = $('#communication_addr').val();
            var email = $('#email').val();
            var dob = $('#dob').val();
            var aadhaar = $('#aadhaar_number').val();
            var cls = $('#current_class').val();
            if (this.result == 0) {
                console.log(this.result, 'decr');
                if (first_name == "" || communication_addr == "" || email == "" || dob == "" || aadhaar == "" || cls == "") {
                    $SubmitError.text('Fill all required fields');
                }
                else {
                    $form.submit();
                    $SubmitError.text('');
                }
            }
            else {
                $SubmitError.text('**Correct the Errors');
            }
        },

});

publicWidget.registry.studentCheck = publicWidget.Widget.extend({
    selector: '.student_table',
    events: {
        'click .clickable_row': '_on_row_Click',
        'click .confirm_btn': '_confirm_btn_Click',
        'click .close_btn': '_close_btn_Click',
    },

     async _on_row_Click(ev) {
        console.log(ev,'ev')
        var studentId = $(ev.currentTarget).parent().children().html();
        const token = await jsonrpc('/registration/student_id', {
            studentId
        })
        .then(function(student){
            var id = student['student']
            window.location = `/registration/details/${id}`;
        })
     },

     async _confirm_btn_Click(ev) {
//        console.log(ev.currentTarget.id,'ev');
        var buttonId = (ev.currentTarget.id);
        const token = await jsonrpc('/registration/button_id', {
            buttonId
        })
        .then(function(student){
//            console.log(student)
            $('#student_id').val(student['student']);
            $('#confirm_student').val(student['student']);
            $('#student_name').val(student['student_name']);
            $('#student_email').val(student['student_email']);
            $('#student_phone').val(student['student_phone']);
            $('#student_class').val(student['student_class']); // Show the modal
            $('#confirmModal').modal('show');
         })

     },

     _close_btn_Click(){
        window.location = '/registration';
     }

});

