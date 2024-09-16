from odoo import models, fields


class RealEstate(models.Model):
    _name = "real.estate"
    _description = "Real Estate"

    name = fields.Char('Customer Name', required=True)
    description = fields.Char()
    postcode = fields.Integer(limit=6)
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    phone = fields.Integer(required=True)
    booking_date = fields.Datetime(default=fields.Datetime.now, copy=False)
    active = fields.Boolean()
    status = fields.Selection(selection=[('new','New'), ('offer received', 'Offer Received')], string='Status')