# -*- coding: utf-8 -*-
from odoo import models


class PosSession(models.Model):
    """Extends the `pos.session` model"""
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """Loading field to an existing model in POS"""
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('discount_price_tag')
        # print(result,'result')
        return result


