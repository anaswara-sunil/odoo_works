# -*- coding: utf-8 -*-
import logging
import requests
from odoo import _, fields, models, service

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('multisafepay', 'Multisafepay')], ondelete={'multisafepay': 'set default'}
    )
    multisafepay_api_key = fields.Char(
        string="Multisafepay API Key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider="multisafepay",
        groups="base.group_system"
    )

    def _multisafepay_make_request(self, api_key, data=None, method=None):
        """ Make a request at multisafepay endpoint."""
        self.ensure_one()
        if method == 'POST':
            url = f'https://testapi.multisafepay.com/v1/json/orders?api_key={api_key}'
            headers = {
                'Content-Type': 'application/json',
                'accept': 'application/json',
            }
            response = requests.request(method, url, json=data, headers=headers, timeout=60)
        else:
            url = f'https://testapi.multisafepay.com/v1/json/orders/{data}/?api_key={api_key}'
            headers = {
                'accept': 'application/json',
            }
            response = requests.request(method, url, headers=headers, timeout=60)
        return response.json()



