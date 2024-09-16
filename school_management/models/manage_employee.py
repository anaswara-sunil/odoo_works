# -*- coding: utf-8 -*-
from odoo import models, fields, Command
# from odoo.exceptions import ValidationError


class ManageEmployee(models.Model):
    """Manage Office Staffs"""
    _name = "manage.employee"
    _description = "Employees"
    _inherit = 'mail.thread'

    partner_id = fields.Many2one('res.partner', required=True)
    email = fields.Char(related='partner_id.email',required=True)
    contact_type = fields.Selection(related='partner_id.contact_type',store=True)
    school_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    user_id = fields.Many2one('res.users', string="User", readonly=True, )
    _sql_constraints = [
        ('employee_uniq', 'unique(name)', "This person already exists in the records !")]


    def create_user(self):
        """Creates a user upon employee registration"""
        # print(self)
        user_name = self.env['res.users'].search([('login', '=', self.email)])
        # print(user_name)
        if not user_name:
            # if self.email:
            # print('if loop')
            user_values = {
                'login': self.email,
                'name': self.partner_id.name,
                'partner_id' : self.partner_id.id
            }
            user = self.env['res.users'].create(user_values)
            if self.contact_type == 'teacher':
                user.groups_id = [Command.set([self.env.ref('school_management.school_management_teacher').id])]
            if self.contact_type == 'office_staff':
                user.groups_id = [Command.set([self.env.ref('school_management.school_management_staff').id])]
            self.user_id = user.id

