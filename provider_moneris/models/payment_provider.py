# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import hashlib
import hmac
import logging
import requests
from werkzeug import urls

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('moneris', 'Moneris')],
        ondelete={'moneris': 'set default'}
    )

    moneris_store_id = fields.Char(
        string="Store ID",
        help="The Store ID provided by Moneris",
        required_if_code='moneris'
    )
    moneris_api_token = fields.Char(
        string="API Token",
        help="The API Token provided by Moneris",
        required_if_code='moneris'
    )
    moneris_check_avs = fields.Boolean(
        string="Verify Address (AVS)",
        help="Enable Address Verification Service",
        default=True
    )
    moneris_check_cvv = fields.Boolean(
        string="Verify CVV",
        help="Enable Card Verification Value check",
        default=True
    )

    def _compute_feature_support_fields(self):
        """Specify supported features for Moneris"""
        super()._compute_feature_support_fields()
        for provider in self:
            if provider.code != 'moneris':
                continue
            provider.support_tokenization = True
            # provider.support_refund = True
            # provider.support_capture_method = True

    @api.model
    def _get_moneris_api_url(self):
        """Get the appropriate Moneris API URL based on environment"""
        print('self')
        if self.state == 'test':
            # return 'https://gateway.moneris.com/'
            return 'https://gatewayt.moneris.com/chktv2/request/request.php'
        return 'https://esqa.moneris.com/'