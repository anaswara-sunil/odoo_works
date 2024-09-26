# -*- coding: utf-8 -*-
from odoo import models, api


class OwlModel(models.Model):
    """Owl workshop"""
    _name = "owl.model"

    @api.model
    def orm_call_method(self):
        return self.env['sale.order'].search([],limit=10)

