# -*- coding: utf-8 -*-
import json
import logging
import pprint
import requests
from odoo import fields, models, api, _
from urllib.parse import parse_qs
from odoo.exceptions import ValidationError, UserError, AccessDenied
from odoo.tools import hmac

_logger = logging.getLogger(__name__)
UNPREDICTABLE_MONERIS_DATA = object() # sentinel

class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    def _get_payment_terminal_selection(self):
        return super(PosPaymentMethod, self)._get_payment_terminal_selection() + [('moneris', 'Moneris')]

    # Moneris
    moneris_api_key = fields.Char(string="Moneris API key", help='Used when connecting to Moneris', copy=False)
    moneris_terminal_identifier = fields.Char(help='[Terminal model]-[Serial number], for example: P400Plus-123456789', copy=False)
    # moneris_store_id = fields.Char(help='Store ID', copy=False)
    moneris_test_mode = fields.Boolean(help='Run transactions in the test environment.')

    moneris_latest_response = fields.Char(copy=False) # used to buffer the latest asynchronous notification from moneris.
    moneris_latest_diagnosis = fields.Char(copy=False) # used to determine if the terminal is still connected.

    def _is_write_forbidden(self, fields):
        return super(PosPaymentMethod, self)._is_write_forbidden(fields - {'moneris_latest_response'})

    def get_latest_moneris_status(self):
        self.ensure_one()
        latest_response = self.sudo().moneris_latest_response
        latest_response = json.loads(latest_response) if latest_response else False
        return latest_response

    def proxy_moneris_request(self, data, operation=False):
        ''' Necessary because Moneris's endpoints don't have CORS enabled '''
# py.1
        print(2)
        print(_logger,'_logger')
        print(data,'data')
        # print(data['SaleToPOIRequest']['MessageHeader']['SaleID'],'SaleID')
        print(operation,'operation')
        self.ensure_one()
        if not data:
            raise UserError(_('Invalid Moneris request'))

        if 'SaleToPOIRequest' in data and data['SaleToPOIRequest']['MessageHeader']['MessageCategory'] == 'Payment' and 'PaymentRequest' in data['SaleToPOIRequest']:  # Clear only if it is a payment request
            self.sudo().moneris_latest_response = ''  # avoid handling old responses multiple times

        if not operation:
            operation = 'terminal_request'

        # These checks are not optimal. This RPC method should be changed.
        is_capture_data = operation == 'capture' and hasattr(self, 'moneris_merchant_account') and self._is_valid_moneris_request_data(data, {
            'originalReference': UNPREDICTABLE_MONERIS_DATA,
            'modificationAmount': {
                'value': UNPREDICTABLE_MONERIS_DATA,
                'currency': UNPREDICTABLE_MONERIS_DATA,
            },
            # 'merchantAccount': self.moneris_merchant_account,
            'merchantAccount': 'moneris',
        })
        is_adjust_data = operation == 'adjust' and hasattr(self, 'moneris_merchant_account') and self._is_valid_moneris_request_data(data, {
            'originalReference': UNPREDICTABLE_MONERIS_DATA,
            'modificationAmount': {
                'value': UNPREDICTABLE_MONERIS_DATA,
                'currency': UNPREDICTABLE_MONERIS_DATA,
            },
            # 'merchantAccount': self.moneris_merchant_account,
            'merchantAccount': 'moneris',
            'additionalData': {
                'industryUsage': 'DelayedCharge',
            },
        })
        is_cancel_data = operation == 'terminal_request' and self._is_valid_moneris_request_data(data, {
            'SaleToPOIRequest': {
                'MessageHeader': self._get_expected_message_header('Abort'),
                'AbortRequest': {
                    'AbortReason': 'MerchantAbort',
                    'MessageReference': {
                        'MessageCategory': 'Payment',
                        'SaleID': UNPREDICTABLE_MONERIS_DATA,
                        'ServiceID': UNPREDICTABLE_MONERIS_DATA,
                    },
                },
            },
        })
        is_payment_request_with_acquirer_data = operation == 'terminal_request' and self._is_valid_moneris_request_data(data, self._get_expected_payment_request(True))
        # print(is_capture_data,'is_capture_data')
        # print(is_adjust_data,'is_adjust_data')
        # print(is_cancel_data,'is_cancel_data')

        if is_payment_request_with_acquirer_data:
            parsed_sale_to_acquirer_data = parse_qs(data['SaleToPOIRequest']['PaymentRequest']['SaleData']['SaleToAcquirerData'])
            valid_acquirer_data = self._get_valid_acquirer_data()
            is_payment_request_with_acquirer_data = len(parsed_sale_to_acquirer_data.keys()) <= len(valid_acquirer_data.keys())
            if is_payment_request_with_acquirer_data:
                for key, values in parsed_sale_to_acquirer_data.items():
                    if len(values) != 1:
                        is_payment_request_with_acquirer_data = False
                        break
                    value = values[0]
                    valid_value = valid_acquirer_data.get(key)
                    if valid_value == UNPREDICTABLE_MONERIS_DATA:
                        continue
                    if value != valid_value:
                        is_payment_request_with_acquirer_data = False
                        break
        is_payment_request_without_acquirer_data = operation == 'terminal_request' and self._is_valid_moneris_request_data(data, self._get_expected_payment_request(False))

        if not is_payment_request_without_acquirer_data and not is_payment_request_with_acquirer_data and not is_adjust_data and not is_cancel_data and not is_capture_data:
            raise UserError(_('Invalid Monerissss request'))

        if is_payment_request_with_acquirer_data or is_payment_request_without_acquirer_data:
            acquirer_data = data['SaleToPOIRequest']['PaymentRequest']['SaleData'].get('SaleToAcquirerData')
            msg_header = data['SaleToPOIRequest']['MessageHeader']
            metadata = 'metadata.pos_hmac=' + self._get_hmac(msg_header['SaleID'], msg_header['ServiceID'], msg_header['POIID'], data['SaleToPOIRequest']['PaymentRequest']['SaleData']['SaleTransactionID']['TransactionID'])

            data['SaleToPOIRequest']['PaymentRequest']['SaleData']['SaleToAcquirerData'] = acquirer_data + '&' + metadata if acquirer_data else metadata

        return self._proxy_moneris_request_direct(data, operation)

    @api.model
    def _is_valid_moneris_request_data(self, provided_data, expected_data):
# py.3, 4 ,7-11 ,14-21
        print('3')
        # print(provided_data,expected_data,'jkgh')
        if not isinstance(provided_data, dict) or set(provided_data.keys()) != set(expected_data.keys()):
            return False

        for provided_key, provided_value in provided_data.items():
            expected_value = expected_data[provided_key]
            if expected_value == UNPREDICTABLE_MONERIS_DATA:
                continue
            if isinstance(expected_value, dict):
                if not self._is_valid_moneris_request_data(provided_value, expected_value):
                    return False
            else:
                if provided_value != expected_value:
                    return False
        return True

    def _get_expected_message_header(self, expected_message_category):
# py.2 , 6 , 13
        print(self,'4')
        return {
            'ProtocolVersion': '3.0',
            'MessageClass': 'Service',
            'MessageType': 'Request',
            'MessageCategory': expected_message_category,
            'SaleID': UNPREDICTABLE_MONERIS_DATA,
            'ServiceID': UNPREDICTABLE_MONERIS_DATA,
            # 'POIID': self.moneris_terminal_identifier     #The unique ID of the terminal to send this request to.
            'POIID': 'moneris'     #The unique ID of the terminal to send this request to.
        }
    
    def _get_expected_payment_request(self, with_acquirer_data):
# py.5 , 12
        print(self,'5')
        res = {
            'SaleToPOIRequest': {
                'MessageHeader': self._get_expected_message_header('Payment'),
                'PaymentRequest': {
                    'SaleData': {
                        'SaleTransactionID': {
                            'TransactionID': UNPREDICTABLE_MONERIS_DATA,
                            'TimeStamp': UNPREDICTABLE_MONERIS_DATA,
                        },
                    },
                    'PaymentTransaction': {
                        'AmountsReq': {
                            'Currency': UNPREDICTABLE_MONERIS_DATA,
                            'RequestedAmount': UNPREDICTABLE_MONERIS_DATA,
                        },
                    },
                },
            },
        }

        if with_acquirer_data:
            res['SaleToPOIRequest']['PaymentRequest']['SaleData']['SaleToAcquirerData'] = UNPREDICTABLE_MONERIS_DATA
        return res

    @api.model
    def _get_valid_acquirer_data(self):
        print(self,'6')
        return {
            'tenderOption': 'AskGratuity',
            'authorisationType': 'PreAuth'
        }

    @api.model
    def _get_hmac(self, sale_id, service_id, poi_id, sale_transaction_id):
# py.22
        print(self,'7')
        return hmac(
            env=self.env(su=True),
            scope='pos_moneris_payment',
            message=(sale_id, service_id, poi_id, sale_transaction_id)
        )

    def _proxy_moneris_request_direct(self, data, operation):
# py.23
        print(self,'8')
        self.ensure_one()
        TIMEOUT = 10

        _logger.info('Request to Moneris by user #%d:\n%s', self.env.uid, pprint.pformat(data))

        environment = 'test' if self.sudo().moneris_test_mode else 'live'
        print(environment, "eeeee")
        print(operation, "eeeee")
        print(self._get_moneris_endpoints(), "eeeee")
        endpoint = self._get_moneris_endpoints()[operation]
        print(endpoint, 'eee[[')
        headers = {
            'x-api-key': self.sudo().moneris_api_key,
            # 'x-api-key': 'yesguy',
        }
        print(data,'api')
        req = requests.post(endpoint, json=data, headers=headers, timeout=TIMEOUT)
        print(req.text)
        # Authentication error doesn't return JSON
        if req.status_code == 401:
            return {
                'error': {
                    'status_code': req.status_code,
                    'message': req.text
                }
            }

        if req.text == 'ok':
            return True

        return req.json()

    def _get_moneris_endpoints(self):
        # py.24
        print(self, '1')
        return {
            # 'terminal_request': 'https://gatewayt.moneris.com/chktv2/request/request.php',
            'terminal_request': 'https://gatewayt.moneris.com/chktv2/request/request.php',
            # 'terminal_request': 'https://gatewayt.moneris.com/chkt/js/chkt_v1.00.js',
        }












    # @api.constrains('moneris_terminal_identifier')
    # def _check_moneris_terminal_identifier(self):
    #     for payment_method in self:
    #         if not payment_method.moneris_terminal_identifier:
    #             continue
    #         # sudo() to search all companies
    #         existing_payment_method = self.sudo().search([('id', '!=', payment_method.id),
    #                                                       ('moneris_terminal_identifier', '=',
    #                                                        payment_method.moneris_terminal_identifier)],
    #                                                      limit=1)
    #         if existing_payment_method:
    #             if existing_payment_method.company_id == payment_method.company_id:
    #                 raise ValidationError(_('Terminal %s is already used on payment method %s.',
    #                                         payment_method.moneris_terminal_identifier,
    #                                         existing_payment_method.display_name))
    #             else:
    #                 raise ValidationError(_('Terminal %s is already used in company %s on payment method %s.',
    #                                         payment_method.moneris_terminal_identifier,
    #                                         existing_payment_method.company_id.name,
    #                                         existing_payment_method.display_name))