# -*- coding: utf-8 -*-
from odoo import fields, models, Command
from odoo.addons.test_convert.tests.test_env import field


class CreatePurchaseOrder(models.TransientModel):
   """This model is used for sending WhatsApp messages through Odoo."""
   _name = 'purchase.order.wizard'
   _description = "Purchase Order Wizard"

   vendor_id = fields.Many2one( 'res.partner',string="Vendor", readonly=True)
   quantity = fields.Integer(required=True)
   price = fields.Float(required=True, readonly=True)
   product_id = fields.Many2one( 'product.template',readonly=True)


   def action_create_po(self):
         """Create new Purchase Order """
         vendor = self.vendor_id.name
         purchase_order = self.env['purchase.order'].search([('partner_id', 'in',vendor),
                                                             ('state', '=', 'draft')],limit=1)
         if purchase_order:
             purchase_order.order_line = [Command.create ( {
                     'product_id': self.product_id.product_variant_id.id,
                     'price_unit': self.price,
                     'product_qty': self.quantity,
                  })]
         else:
            purchase_order = self.env['purchase.order'].create({
               "partner_id" : self.vendor_id.id,
               "order_line": [
                  (Command.create({
                     'product_id': self.product_id.product_variant_id.id,
                     'price_unit': self.price,
                     'product_qty': self.quantity,
                  }))]
            })
         purchase_order.button_confirm()

