# -*- coding: utf-8 -*-
from odoo import models


class ProductTemplate(models.Model):
    """To add a new state in the status bar"""
    _inherit = "product.template"

    def action_button_purchase_order(self):
        """Create new Purchase Order """
        return {'type': 'ir.actions.act_window',
           'name': 'Purchase Order',
           'res_model': 'purchase.order.wizard',
           'target': 'new',
           'view_mode': 'form',
           'view_type': 'form',
           'context': {'default_vendor_id': self.seller_ids[0].partner_id.id,
                       'default_price': self.seller_ids[0].price,
                       'default_product_id': self.id
                      }
            }
