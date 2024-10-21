# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    set_idle_time = fields.Float(string="set Idle Time",config_parameter='idle_time')
    set_timer_time = fields.Float(string="set timer time-out Time",config_parameter='timer_time')



