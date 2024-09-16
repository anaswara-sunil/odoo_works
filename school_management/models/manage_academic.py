# -*- coding: utf-8 -*-
from odoo import models, fields


class ManageAcademicYear(models.Model):
    """Manage academic year"""
    _name = "manage.academic"
    _description = "Academic Year"

    academic_name = fields.Char(' Name', required=True)
    school_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
