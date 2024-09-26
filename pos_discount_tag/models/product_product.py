# -*- coding: utf-8 -*-
from odoo import models,fields


class ProductProduct(models.Model):
    """To add  new fields inside the products"""
    _inherit = "product.product"

    discount_price_tag = fields.Char(string="Discount Price")
