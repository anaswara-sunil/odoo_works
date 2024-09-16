# -*- coding: utf-8 -*-
from odoo import models, fields, Command, api, _
from odoo.exceptions import ValidationError


class MaterialRequest(models.Model):
    _name = "material.request"
    _description = 'Material Request'
    _inherit = 'mail.thread'

    name = fields.Char('',default=lambda self: _('New'), copy=False, readonly=True, tracking=True)
    request_owner_id = fields.Many2one('res.partner', required=True, string="Request Owner")
    request_date = fields.Date(default=fields.Datetime.now, string="Date")
    request_line_ids = fields.One2many('request.line', 'request_id',required=True)
    purchase_count = fields.Integer(string="Purchase",  compute='_compute_purchase_count',default=0)
    transfer_count = fields.Integer(string="Transfer", compute='_compute_transfer_count', default=0)

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('first_approval', 'First Approval'),
        ('second_approval', 'Second Approval'),
        ('rejected', 'Rejected')
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='draft')

    @api.model_create_multi
    def create(self, vals_list):
        print(vals_list)
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'request.reference')
        return super().create(vals_list)

    @api.constrains('request_line_ids')
    def _check_locations(self):
        """Field Validation checking"""
        for rec in self.request_line_ids:
            if rec.type == "transfer" and (not rec.location_src_id or not rec.location_dest_id):
                raise ValidationError("Internal Transfer needs location ids")

    def action_button_request(self):
        """Change state to Submitted"""
        if not self.request_line_ids:
            raise ValidationError("Fill the Product lines")
        else:
            self.write({
                'state': "submitted"
            })
            # self.same_product_on_purchase()

    def action_button_first_approval(self):
        """Change state to First Approval"""
        if not self.request_line_ids:
            raise ValidationError("Fill the Product lines")
        self.write({
            'state': "first_approval"
        })

    def action_button_second_approval(self):
        """Create new Purchase Order and Change state to Second approval"""
        if not self.request_line_ids:
            raise ValidationError("Fill the Product lines")
        self.write({
            'state': "second_approval"
        })

        lines = self.env['request.line'].search([('request_id', '=', self.id)])
        for record in lines:
            if record.type == 'purchase':
                vendors = record.product_id.seller_ids
                for rec in vendors:
                    self.env['purchase.order'].create({"partner_id": rec.partner_id.id,'material_request_id': self.id,
                        "order_line": [
                            (Command.create({
                                'product_id': record.product_id.product_variant_id.id,
                                'product_qty': record.quantity,
                                'price_unit': rec.price,
                            }))] })
            if record.type == 'transfer':
                    picking = self.env['stock.picking'].create({"partner_id": self.request_owner_id.id,
                        'picking_type_id': self.env.ref('stock.picking_type_internal').id,
                        'material_request_id': self.id,
                        "move_ids": [
                            (Command.create({
                                'name': 'material request',
                                'product_id': record.product_id.product_variant_id.id,
                                'product_uom_qty': record.quantity,
                                'location_id': record.location_src_id.id,
                                'location_dest_id': record.location_dest_id.id,
                                'product_uom': record.uom.id,
                            }))] })
                    picking.action_confirm()

    def action_button_reject(self):
        self.write({
            'state': "rejected"
        })

    def _compute_purchase_count(self):
        """Computing the Purchasing Order count"""
        for record in self:
            record.purchase_count = self.env['purchase.order'].search_count([('material_request_id', '=', self.id)])

    def action_get_purchase_record(self):
        """Purchase Order records """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Purchase',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('material_request_id', '=', self.id)],
            'context': {'create': False}
        }

    def _compute_transfer_count(self):
        """Computing the Internal Transfer count"""
        for record in self:
            record.transfer_count = self.env['stock.picking'].search_count([('material_request_id', '=', self.id)])

    def action_get_transfer_record(self):
        """Internal Transfer records """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transfer',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('material_request_id', '=', self.id)],
            'context': {'create': False}
        }

    def same_product_on_purchase(self):
        products_val = {}
        purchase_item = (self.request_line_ids.filtered(lambda x: x.type == 'purchase'))
        for i in purchase_item:
            if i.product_id in products_val:
                products_val[i.product_id] += i.quantity
            else:
                products_val[i.product_id] = i.quantity
        for key in products_val.keys():
            vendors = key.seller_ids
            for i in vendors:
                self.env['purchase.order'].create({"partner_id": i.partner_id.id,'material_request_id': self.id,
                        "order_line": [
                        (Command.create({'name': 'material request',
                            'product_id': key.product_variant_id.id,
                            'product_qty': products_val[key] ,
                             'price_unit': i.price,
                        }))] })



# Adding same product to same purchase order using list functionalities
        # request_line = []
        # for record in self.request_line_ids:
        #     if record.type == 'purchase':
        #         request_line.append(record)
        #
        # for i in request_line:
        #     order = self.env['purchase.order'].search([('material_request_id', '=', self.id),
        #                    ('order_line.product_id', '=', i.product_id.product_variant_id.id)])
        #     if order:
        #         order.write({
        #             "order_line": [
        #                 (Command.update(order.order_line.id, {
        #                                 'product_qty': order.order_line.product_qty + i.quantity}))]
        #         })
        #     else:
        #         vendors = i.product_id.seller_ids
        #         for rec in vendors:
        #              self.env['purchase.order'].create({"partner_id": rec.partner_id.id,'material_request_id': self.id,
        #                       "order_line": [
        #                         (Command.create({'product_id': i.product_id.product_variant_id.id,
        #                             'product_qty': i.quantity ,'price_unit': rec.price,
        #                         }))] })

