# -*- coding: utf-8 -*-
import logging
import pprint

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class MultisafepayController(http.Controller):
    _return_url = '/payment/multisafepay/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False
    )
    def multisafepay_return_from_checkout(self, **data):
        """ Process the notification data sent by multisafepay after redirection from checkout"""
        _logger.info("handling redirection from Multisafepay with data:\n%s", pprint.pformat(data))
        transaction = request.env['payment.transaction'].search([('reference','=',data.get('transactionid'))])
        transaction._handle_notification_data('multisafepay', data)
        return request.redirect('/payment/status')


