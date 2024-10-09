# -*- coding: utf-8 -*-
import logging
import pprint
from werkzeug import urls
from odoo import _, models
from odoo.exceptions import ValidationError
from ..controllers.main import MultisafepayController

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'


    def _get_specific_rendering_values(self, processing_values):
         """ Override of payment to return multisafepay-specific rendering values(POST Method)"""
         res = super()._get_specific_rendering_values(processing_values)
         if self.provider_code != 'multisafepay':
             return res
         payload = self._multisafepay_prepare_payment_request_payload()
         _logger.info("sending '/payments' request for link creation:\n%s", pprint.pformat(payload))
         api_key = self.provider_id.multisafepay_api_key
         payment_data = self.provider_id._multisafepay_make_request(api_key=api_key, data=payload,method='POST')
         data_url = payment_data['data']
         return {'api_url': data_url['payment_url']}

    def _multisafepay_prepare_payment_request_payload(self):
        """ Create the payload for the payment request based on the transaction values"""
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.url_join(base_url, MultisafepayController._return_url)

        multisafepay_values = {
            "type": "redirect",
            "order_id": self.id,
            "gateway": "",
            "currency": self.currency_id.name,
            "amount": round(self.amount),
            "description": "Test order description",
            "payment_options": {
                "notification_url": "https://www.example.com/client/notification?type=notification",
                "notification_method": "POST",
                "redirect_url": f'{redirect_url}?ref={self.reference}',
            },
            "customer": {
                "first_name": self.partner_name,
                "locale": "nl_NL",
                "ip_address": "123.123.123.123",
                "last_name": "Doe",
                "company_name": "Test Company Name",
                "address1": "Kraanspoor",
                "house_number": "39C",
                "zip_code": "1033SC",
                "city": "Amsterdam",
                "country": "NL",
                "phone": "0208500500",
                "email": "jdoe@example.com",
            }
        }
        return  multisafepay_values

    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override of payment to find the transaction based on Multisafepay data"""
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)

        if provider_code != 'multisafepay' or len(tx) == 1:
            return tx
        tx = self.search(
            [('reference', '=', notification_data.get('ref')), ('provider_code', '=', 'multisafepay')]
        )

        if not tx:
            raise ValidationError("Multisafepay: " + _(
                "No transaction found matching reference %s.", notification_data.get('ref')
            ))
        tx._process_notification_data(notification_data)
        return tx

    def _process_notification_data(self, notification_data):
        """ Override of payment to process the transaction based on Mollie data (GET Method)"""
        super()._process_notification_data(notification_data)
        if self.provider_code != 'multisafepay':
            return
        transaction_id = notification_data['transactionid']
        api_key = self.provider_id.multisafepay_api_key
        payment_data = self.provider_id._multisafepay_make_request(api_key=api_key, data=transaction_id, method='GET')

#if transaction is declined(paypal-initially declined),transaction will be in 'Initialized' state.
        if payment_data['data']['costs']:
            self.provider_reference = payment_data['data']['costs'][0]['transaction_id']
        payment_status = payment_data['data']['status']

#Update the transactions' state to according to the payment status.
        if payment_status in ['initialized', 'uncleared']:
            self._set_pending()
        elif payment_status in ['completed', 'shipped']:
            self._set_done()
        elif payment_status in ['void', 'cancel', 'declined']:
            self._set_canceled("MultiSafePay: " + _("Canceled payment with status: %s", payment_status))
        else:
            self._set_error('Error')





