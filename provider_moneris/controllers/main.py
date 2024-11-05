# controllers/main.py
from odoo import http
from odoo.http import request

class MonerisPController(http.Controller):
    @http.route('/payment/moneris/return', type='http', auth='public', csrf=False)
    def moneris_return(self, **post):
        request.env['payment.transaction'].sudo()._handle_notification_data('moneris', post)
        return request.redirect('/payment/status')

    @http.route('/payment/moneris/cancel', type='http', auth='public', csrf=False)
    def moneris_cancel(self, **post):
        return request.redirect('/payment/status')

    @http.route('/payment/moneris/error', type='http', auth='public', csrf=False)
    def moneris_error(self, **post):
        return request.redirect('/payment/status')