# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_set_due_limit = fields.Boolean(related='pos_config_id.set_due_limit', readonly=False)
    pos_customer_due_limit = fields.Integer(related='pos_config_id.customer_due_limit', readonly=False)

class PosConfig(models.Model):
    _inherit = 'pos.config'

    set_due_limit = fields.Boolean(string="Set Due Limit")
    customer_due_limit = fields.Integer(string="Customer Due Limit")
