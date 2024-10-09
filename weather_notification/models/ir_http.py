# -*- coding: utf-8 -*-
from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        """Adding boolean field value into session info"""
        result = super(IrHttp, self).session_info()
        weather_boolean = self.env['ir.config_parameter'].sudo().get_param('weather')
        result['is_weather_boolean'] = weather_boolean
        return result
