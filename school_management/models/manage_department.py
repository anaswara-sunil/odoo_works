# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ManageDepartment(models.Model):
    """Manage Department"""
    _name = "manage.department"
    _description = "Manage Department"
    _inherit = 'mail.thread'


    name = fields.Char(' Name', required=True)
    hod_id = fields.Many2one('res.partner', string="Head Of the Dept.")
    school_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    class_ids = fields.One2many('manage.class','department_id')



