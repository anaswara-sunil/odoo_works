# -*- coding: utf-8 -*-
from email.policy import default

from odoo import models,fields


class RequestLine(models.Model):
    _name = "request.line"
    _description = 'Request Lines'

    product_id = fields.Many2one('product.product',string='Product',required=True)
    type = fields.Selection(selection=[('purchase','Purchase Order'),('transfer','Internal Transfer')],
                            string='Get by',required=True)
    quantity = fields.Integer(default=1)
    uom = fields.Many2one(related='product_id.uom_id')
    request_id = fields.Many2one('material.request')
    location_src_id = fields.Many2one('stock.location', 'Source Location',
                                      domain="[('usage','=','internal')]")
    location_dest_id = fields.Many2one('stock.location', 'Destination Location',
                                       domain="[('usage','=','internal')]")

