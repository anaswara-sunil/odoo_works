# -*- coding: utf-8 -*-
from odoo import models, fields


class ManageSubject(models.Model):
    """Manage Subject"""
    _name = "manage.subject"
    _description = "Manage Subject"
    _inherit = 'mail.thread'


    name = fields.Char('Name', required=True)
    dept_id = fields.Many2one('manage.department', string="Department", required=True)
    pass_mark = fields.Integer()
    max_mark = fields.Integer()