# -*- coding: utf-8 -*-
from odoo import models


class PosSession(models.Model):
    """Extends the `pos.session` model"""
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        """Loading field to an existing model in POS"""
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].append('total_due')
        result['search_params']['fields'].append('customer_due_limit')
        # print(result,'result')
        return result

