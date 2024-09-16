# -*- coding: utf-8 -*-
from datetime import date
from reportlab.lib.validators import isNumber
from odoo import models, fields, api, _, Command
from odoo.api import ondelete
from odoo.exceptions import ValidationError


class StudentRegistration(models.Model):
    """Student Registration"""
    _name = "student.reg"
    _description = "Student Registration"
    _inherit = 'mail.thread'
    _rec_name = "full_name"

    club_ids = fields.Many2many('manage.club', string="Clubs")
    name = fields.Char(default=_('New'), copy=False, readonly=True, tracking=True, string='Sequence')

    full_name = fields.Char(string='Full Name', compute='_compute_full_name', store=True)
    first_name = fields.Char('First Name', required=True)
    last_name = fields.Char('Last Name')

    father_name = fields.Char('Father Name')
    mother_name = fields.Char('Mother Name')

    communication_addr = fields.Text(string="Communication address")
    is_same = fields.Boolean('Same as Communication Address?')
    permanent_addr = fields.Text('Permanent address')

    email = fields.Char('Email',required=True)
    phone = fields.Char('Phone Number')
    dob = fields.Date(copy=False, string="Date of Birth")

    student_age = fields.Integer('Age', compute='_compute_student_age', store=True)
    gender = fields.Selection(selection=[('female', 'Female'), ('male', 'Male'), ('others', 'Others')], string='Gender')
    registration_date = fields.Date(default=fields.Datetime.now,copy=False, string="Reg. Date")

    image = fields.Image()

    previous_department_id = fields.Many2one('manage.department', string="Previous academic department ")
    previous_class_id = fields.Many2one('manage.class', string="Previous class ")
    current_class_id = fields.Many2one('manage.class')

    school_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    tc = fields.Binary(string='TC', attachment=True)
    file_name = fields.Char("File Name")

    aadhaar_number = fields.Char(required=False)
    exam_ids = fields.Many2many('manage.exam', string="Exams")

    # login = fields.Char()
    user_id = fields.Many2one('res.users', string="User", readonly=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string="Partner", readonly=True, ondelete='cascade')

    attendance_status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
    ], string="Attendance Status")

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('registered', 'Registered')
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='draft')

    website_created = fields.Boolean("Created from Website", default=False)

    _sql_constraints = [
        ('aadhaar_number_unique', 'unique(aadhaar_number)', "An Aadhaar can only be assigned to one person !")]



    #  sequence generating while button action
    def action_button_done(self):
        """draft-done button"""
        if self.name == _('New') and self.state == 'draft':
            self.write({
                'state': "registered",
                'name': self.env['ir.sequence'].next_by_code('reg.reference'),
            })
        else:
            raise ValidationError("Already registered")
        if not self.dob:
            raise ValidationError("DOB Required")

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        """Full name from first and last names"""
        # print("compute full name")
        for record in self:
            # if record.first_name and record.last_name:
            #     record.full_name = record.first_name + ' ' + record.last_name
            record.full_name = f"{record.first_name or ''} {record.last_name or ''}"
            # print(record.full_name)

    @api.constrains('tc')
    def _check_tc(self):
        """TC file checking"""
        # print(self.file_name, type(self.file_name))
        if self.file_name:
            if str(self.file_name.split(".")[1]) != 'pdf':
                # print('hi')
                raise ValidationError("Cannot upload file different from .pdf file")

    @api.onchange('is_same')
    def address_change(self):
        """Communication address and Permanent address"""
        self.permanent_addr = self.communication_addr if self.is_same else False

    # Age calculation on save
    @api.depends("dob")
    def _compute_student_age(self):
        """Age calculation"""
        # print(self.state)
        if self.state == 'draft':
            for record in self:
                current_date = date.today()
                if record.dob:
                    record.student_age = current_date.year - record.dob.year
                else:
                    record.student_age = 0

    @api.constrains('student_age')
    def _check_student_age(self):
        """Age error message"""
        for record in self:
            if record.dob:
            # print("hi", record.student_age)
                if record.student_age < 5:
                    # print("l.")
                    raise ValidationError("Minimum allowed age to register is 5")

    @api.constrains('aadhaar_number')
    def _check_aadhaar_number(self):
        """Aadhaar number validation"""
        for record in self:
            if record.aadhaar_number:
                if isNumber(record.aadhaar_number):
                    digit_count = len(str(record.aadhaar_number)) # Count digits excluding the sign
                    if digit_count > 3:
                        raise ValidationError('Aadhaar number cannot have more than 3 digits.')
                else:
                    raise ValidationError('Aadhaar number should be numbers ')

    def attendance_check(self):
        """Updates attendance status based on leave requests"""
        today = date.today()
        # print(today)
        students = self.env['student.reg'].search(
            [('state', '=', 'registered')])
        for student in students:
            leave_requests = self.env['manage.leave'].search([
                ('student_id', '=', student.id), ('start_date', '<=', today), ('end_date', '>=', today)
            ])
            # print(leave_requests)
            if leave_requests:
                student.attendance_status = 'absent' if leave_requests else 'present'

    def create_user(self):
        """Creates a user upon Student registration"""
        print(self)
        if self.state == 'registered':
            partner_vals = {
                'name': self.full_name,
                'email': self.email,
                'contact_type': 'student'
            }
            partner = self.env['res.partner'].search([('email', '=', self.email )],limit=1)
            if not partner:
                partner = self.env['res.partner'].create(partner_vals)


            user_name = self.env['res.users'].search([('login', '=', self.email)],limit=1)
            if not user_name:
                user_values = {
                    'login': self.email,
                    'name': self.full_name,
                    'partner_id' : partner.id,
                    'groups_id': [Command.set([self.env.ref('school_management.school_management_student').id])]
                }
                user = self.env['res.users'].create(user_values)
                self.user_id = user.id
                # user.groups_id =
















# ,('name', '=', self.full_name )

 # <record id="property_rule" model="ir.rule">
 #            <field name="name">Property multi-company</field>
 #            <field name="model_id" ref="model_ir_property"/>
 #            <field eval="True" name="global"/>
 #            <field name="domain_force">[('company_id', 'in', company_ids + [False])]</field>
 #        </record>




# @api.onchange('email')
# def login_change(self):
#     """Communication address and Permanent address"""
#     if self.email:
#         self.login = self.email
#     else:
#         self.login = ""


#  sequence generating while saving
# @api.model_create_multi
# def create(self, vals_list):
#     """sequence for each registration"""
#     print(self, 'create')
#     for vals in vals_list:
#         if vals.get('name', _('New')) == _('New'):
#             vals['name'] = self.env['ir.sequence'].next_by_code(
#                 'reg.reference')
#     return super().create(vals_list)
