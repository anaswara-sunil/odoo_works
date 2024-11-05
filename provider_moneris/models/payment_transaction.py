# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import hashlib
import hmac
import logging
import requests
from werkzeug import urls

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """Return Moneris-specific rendering values"""
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'moneris':
            return res

        # Prepare base transaction data
        base_url = self.provider_id.get_base_url()
        tx_values = {
            'store_id': self.provider_id.moneris_store_id,
            'order_id': self.reference,
            'amount': str(self.amount),
            'currency': self.currency_id.name,
            'txn_type': 'purchase',
            'crypt_type': '7',  # SSL enabled transaction
        }

        # Add customer information
        partner = self.partner_id
        if partner:
            tx_values.update({
                'cust_id': partner.id,
                'email': partner.email or '',
                'bill_first_name': partner.name.split()[0] if partner.name else '',
                'bill_last_name': ' '.join(partner.name.split()[1:]) if partner.name else '',
                'bill_address1': partner.street or '',
                'bill_city': partner.city or '',
                'bill_state': partner.state_id.code if partner.state_id else '',
                'bill_country': partner.country_id.code if partner.country_id else '',
                'bill_zip': partner.zip or '',
                'bill_phone': partner.phone or ''
            })

        # Add callback URLs
        tx_values.update({
            'rtn_url': urls.url_join(base_url, '/payment/moneris/return'),
            'failure_url': urls.url_join(base_url, '/payment/moneris/error'),
            'cancel_url': urls.url_join(base_url, '/payment/moneris/cancel')
        })

        # Generate hash for security
        tx_values['hash'] = self._moneris_generate_hash(tx_values)

        return tx_values

    def _moneris_generate_hash(self, values):
        """Generate security hash for transaction"""
        data = f"{values['store_id']}{values['order_id']}{values['amount']}"
        secret = self.provider_id.moneris_api_token
        return hmac.new(
            secret.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _process_notification_data(self, data):
        """Handle the notification data sent by Moneris"""
        super()._process_notification_data(data)

        if self.provider_code != 'moneris':
            return

        # Verify hash
        received_hash = data.get('hash')
        computed_hash = self._moneris_generate_hash({
            'store_id': self.provider_id.moneris_store_id,
            'order_id': self.reference,
            'amount': str(self.amount)
        })

        if not hmac.compare_digest(received_hash, computed_hash):
            _logger.warning('Received invalid Moneris notification')
            raise ValidationError('Invalid notification received from Moneris')

        # Process response codes
        response_code = data.get('response_code')
        if response_code == '1':  # Approved
            self._set_done()
        elif response_code == '2':  # Declined
            self._set_canceled('Transaction declined by Moneris')
        elif response_code == '3':  # Error
            self._set_error('Technical error during processing')
        else:
            _logger.error('Received unrecognized Moneris response code: %s', response_code)
            self._set_error('Unknown response code received')

    def _send_refund_request(self, amount_to_refund):
        """Handle refund request to Moneris"""
        if self.provider_code != 'moneris':
            return super()._send_refund_request(amount_to_refund)

        refund_data = {
            'store_id': self.provider_id.moneris_store_id,
            'api_token': self.provider_id.moneris_api_token,
            'txn_type': 'refund',
            'order_id': self.reference,
            'amount': str(amount_to_refund),
            'txn_number': self.provider_reference,
            'crypt_type': '7'
        }

        try:
            response = requests.post(
                self.provider_id._get_moneris_api_url() + 'refund',
                json=refund_data,
                timeout=10
            )
            response.raise_for_status()

            result = response.json()
            if result.get('response_code') == '1':
                _logger.info('Refund successful for transaction %s', self.reference)
                return True
            else:
                _logger.error(
                    'Moneris refund failed for transaction %s: %s',
                    self.reference,
                    result.get('message')
                )
                return False

        except (requests.exceptions.RequestException, ValueError) as e:
            _logger.error('Error processing refund: %s', str(e))
            return False


