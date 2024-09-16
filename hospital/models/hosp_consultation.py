from odoo import models, fields, api


class ConsultationForm(models.Model):
    _name = "consultation.form"

    name = fields.Many2one('op.ticket', string="Ticket")
    consultation_no = fields.Char()
    patient_id = fields.Many2one('res.partner', string="Patient", required=True)
    doctor_id = fields.Many2one('hr.employee', string="Doctor")
    department_id = fields.Many2one('hr.department', string="Department")
    date = fields.Datetime(default=fields.Datetime.now, copy=False)
    prescription = fields.Text()

    @api.onchange('doctor_id')
    def _onchange_partner_id(self):
        self.write({
            'department_id': self.doctor_id.department_id
        })

    # @api.onchange('name')
    # def _onchange_patient_id(self):
    #     self.write({
    #         'patient_id': self.
    #     })