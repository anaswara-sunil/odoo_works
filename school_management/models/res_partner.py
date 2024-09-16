# -*- coding: utf-8 -*-
from odoo import models, fields


class ManageResPartner(models.Model):
    """To add a new state in the status bar"""
    _inherit = "res.partner"

    contact_type = fields.Selection(selection=[('student','Student'),('teacher','Teacher'),('office_staff','Office Staff')])