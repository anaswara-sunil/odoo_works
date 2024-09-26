# -*- coding: utf-8 -*-
from odoo import models,fields, api


class ResPartner(models.Model):
    """To add  new fields inside the customer profile"""
    _inherit = "res.partner"

    based_on = fields.Selection(selection=[
        ('allowed_products', 'Allowed Products'),
        ('allowed_categories', 'Allowed Categories')
    ], string='Website View Based on', required=True, default='allowed_products')
    allowed_product_ids = fields.Many2many('product.template', string="Allowed Products")
    allowed_category_ids = fields.Many2many('product.public.category', string="Allowed Category")

    @api.onchange('based_on')
    def _onchange_department_id(self):
        """when 'based on' field changes"""
        if self.based_on == 'allowed_products':
            self.allowed_category_ids = False
        if self.based_on == 'allowed_categories':
            self.allowed_product_ids = False
