# -*- coding: utf-8 -*-
from odoo import models, fields


class ManageSaleOrder(models.Model):
    """To add a new state in the status bar"""
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[('admitted', 'Admitted')])