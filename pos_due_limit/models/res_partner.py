# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.populate import compute


class ManageResPartner(models.Model):
    """To add Total due amount field in partner"""
    _inherit = "res.partner"

    total_due = fields.Integer('Total Due pending',compute='_compute_due_amount',store=True)
    set_due_limit = fields.Boolean(string="Set Due Limit")
    customer_due_limit = fields.Integer(string="Customer Due Limit")

    @ api.depends('invoice_ids.state','invoice_ids.payment_state')
    def _compute_due_amount(self):
        """Calculating due from unpaid orders"""
        for partner in self:
            print(partner,'partner')
            unpaid_orders = self.env['account.move'].search([ ('partner_id', '=', partner.id), ('state', 'in', ['draft','posted']), ('payment_state', 'in', ['not_paid','in_payment','partial']) ])
            print(unpaid_orders,'order')
            total_due_amt = 0.0
            if unpaid_orders:
                for order in unpaid_orders:
                    print(order)
                    # partner.total_due += round(order.amount_residual,2)
                    total_due_amt += order.amount_residual
                    partner.total_due = total_due_amt
            else:
                partner.total_due = 0.0
            print(partner.total_due,'t due')

