# -*- coding: utf-8 -*-
from odoo import models


class PurchaseOrder(models.Model):
    """Purchase Orders"""
    _inherit = "purchase.order"
