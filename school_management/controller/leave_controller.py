# -*- coding: utf-8 -*-
from odoo.http import request, Controller, route
from dateutil.parser import parse

class LeaveController(Controller):
    @route('/leave', auth='public', website=True)
    def leaves_list_view(self, **kwargs):
        """List view of Leaves created from website"""
        leaves = request.env['manage.leave'].sudo().search([('website_created', '=', True)])
        return request.render('school_management.leave_list_template', {'leaves': leaves})

    @route('/leave/create_leave', auth='public', website=True)
    def leave_form_view(self, **kwargs):
        """Form view for creating new leaves"""
        students = request.env['student.reg'].sudo().search([])
        # print(students)
        return request.render('school_management.leave_form_template', {'students': students})

    @route('/leave/submit', type='http', auth='public', website=True, methods=['POST'])
    def submit_form(self, **post):
        """Submit action of Leave form"""
        # print(post, 'post')
        if(post['end_date'] == ''):
            post['end_date'] = post['start_date']
        message = "Your Leave registration has been received successfully"
        url = "/leave"
        request.env['manage.leave'].sudo().create({
            'student_id': post.get('students_name'),
            'class_id': post.get('current_class'),
            'start_date':parse(post.get('start_date'), parserinfo=None) ,
            'end_date':parse(post.get('end_date'), parserinfo=None),
            'total_days': post.get('total_days'),
            'half_day': post.get('half_day'),
            'reason': post.get('reason'),
            'website_created': True,
        })
        return request.render('school_management.thank_you_page',{'message': message, 'url': url})


    # jsonrpc
    @route('/leave/class_id', type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def student_class_details(self, **kwargs):
        """jsonrpc for showing the class of the selected student"""
        # print(kwargs['test_variable'],'fun')
        students = request.env['student.reg'].sudo().search([('id','=',kwargs['test_variable'])])
        # print(students.current_class_id.name,'students')
        # class_id = students.current_class_id
        return {
            'class_name': students.current_class_id.name
        }
