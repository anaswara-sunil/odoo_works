from odoo import models, fields, api, _


class OpTicket(models.Model):
    _name = "op.ticket"


    name = fields.Char('',default=lambda self: _('New'), copy=False, readonly=True, tracking=True)
    patient_id = fields.Many2one('res.partner', string="Patient", required=True)
    booking_date = fields.Datetime(default=fields.Datetime.now, copy=False,string="Date")
    patient_age = fields.Char()
    phone = fields.Char(required=True)
    doctor_id = fields.Many2one('hr.employee', string="Doctor")
    department_id = fields.Many2one('hr.department', string="Department")

    @api.model_create_multi
    def create(self, vals_list):
        print(vals_list)
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'ticket.reference')
        return super().create(vals_list)


    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        self.write({
            'patient_age': self.patient_id.age
        })


    @api.onchange('doctor_id')
    def _onchange_partner_id(self):
        self.write({
            'department_id': self.doctor_id.department_id
        })


    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='draft')

    def button_done(self):
        self.write({
            'state': "done",

        })


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        self.partner_id.country_id.currency_id.symbol = '$'
        print(self.partner_id.country_id.currency_id.symbol)