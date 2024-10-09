# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    weather_sync = fields.Boolean(string="Enable Weather Sync",config_parameter='weather')
    api_key = fields.Char(string="API Key", config_parameter='api')
    location = fields.Char(string="Location", config_parameter='location')

    @api.onchange('weather_sync')
    def _onchange_weather_sync(self):
        """ Clearing the fields on changing boolean field """
        if not self.weather_sync :
            self.api_key = False
            self.location = False