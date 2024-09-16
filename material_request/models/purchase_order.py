# -*- coding: utf-8 -*-
from odoo import models, fields


class PurchaseOrder(models.Model):
    """To add a new field in the purchase order"""
    _inherit = "purchase.order"

    material_request_id = fields.Many2one('material.request')


class InternalTransfer(models.Model):
    """To add a new field in the internal transfer"""
    _inherit = "stock.picking"

    material_request_id = fields.Many2one('material.request')
