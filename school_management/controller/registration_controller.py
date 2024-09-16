# -*- coding: utf-8 -*-
from odoo.http import request, Controller, route
from odoo import _

class RegistrationController(Controller):
    @route('/registration', auth='public', website=True)
    def students_view(self, **kwargs):
        """List view of Students created from website"""
        students = request.env['student.reg'].sudo().search([('website_created', '=', True)])
        return request.render('school_management.students_list_template', {'students': students})

    @route('/registration/details/<int:id>', auth='public', website=True)
    def individual_view(self, id):
        """Detailed view of each student"""
        student = request.env['student.reg'].browse([id])
        return request.render('school_management.student_details_template', {'student': student})

    @route('/registration/register', auth='public', website=True)
    def registration_form(self, **kwargs):
        """Form for registering new students"""
        current_class = request.env['manage.class'].search([])
        return request.render('school_management.registration_form_template',{'current_class': current_class})

    @route('/registration/submit', type='http', auth='public', website=True, methods=['POST'])
    def submit_form(self, **post):
        """Submit action of Student Registration form"""
        # print(post,'post')
        tc = ".join(format(ord(x), '08b') for x in post.get('tc')" #to convert string into binary
        message = "Your Student registration has been received successfully"
        url = "/registration"
        request.env['student.reg'].sudo().create({
                    'first_name': post.get('first_name'),
                    'last_name': post.get('last_name'),
                    'email': post.get('email'),
                    'communication_addr': post.get('communication_addr'),
                    'permanent_addr': post.get('permanent_addr'),
                    'dob': post.get('dob'),
                    'student_age': post.get('age'),
                    'tc': tc,
                    'aadhaar_number': post.get('aadhaar_number'),
                    'website_created': True,
                    'current_class_id': post.get('current_class'),
                })
        return request.render('school_management.thank_you_page',{'message': message, 'url': url})

    @route('/registration/delete/<int:id>', type='http', auth='public', website=True)
    def delete_student(self, id, **kwargs):
        """Delete action for student list row"""
        student = request.env['student.reg'].browse([id])
        student.sudo().unlink()
        return request.redirect('/registration')

    @route('/registration/confirm_student', type='http',methods=['POST'], auth='public',website=True)
    def confirm_student(self, **kwargs):
        """Confirm action for Student list row"""
        # print(kwargs,kwargs['student_id'])
        student = request.env['student.reg'].sudo().search([('id', '=',kwargs['student_id'])])
        # print(student)
        if student.name == _('New') and student.state == 'draft':
            if student: student.write({
                'state': 'registered',
                'name': student.env['ir.sequence'].next_by_code('reg.reference'),
                'full_name': kwargs.get('name'),
                'email': kwargs.get('email'),
                'phone': kwargs.get('phone'),
                'current_class_id': kwargs.get('class'),
            })
        return request.redirect('/registration')


# jsonrpc
    @route('/registration/student_id', type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def student_details(self, **kwargs):
        """ jsonrpc for passing id along with url"""
        # print(kwargs,'fun')
        students = request.env['student.reg'].sudo().search([('id', '=', kwargs['studentId'])])
        # print(students,'students')

        return ({
            'student': students.id
        })

    @route('/registration/button_id', type='json', auth='public', methods=['POST'], website=True,csrf=False)
    def button_details(self, **kwargs):
        """jsonrpc for showing modal along with the details of the particular student"""
        students = request.env['student.reg'].sudo().search([('id', '=', kwargs['buttonId'])])
        return {
            'student': students.id,
            'student_name': students.full_name,
            'student_email': students.email,
            'student_class': students.current_class_id.name,
            'student_phone': students.phone,
        }
