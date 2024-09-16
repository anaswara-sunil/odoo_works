from odoo import models, fields


class HospitalDoctors(models.Model):
    _inherit = "hr.employee"

    qualification = fields.Char()
    fee = fields.Float()

