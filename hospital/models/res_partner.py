from odoo import models, fields


class HospitalPatient(models.Model):
    _inherit = "res.partner"

    blood_group = fields.Selection(selection=[('A+', 'A+'), ('B+', 'B+'), ('AB+', 'AB+'), ('O+', 'O+')], string='Blood Group')
    dob = fields.Date(copy=False)
    age = fields.Integer()