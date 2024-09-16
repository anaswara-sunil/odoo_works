# -*- coding: utf-8 -*-
# from dateutil.rrule import weekday
from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class ManageLeave(models.Model):
    """Manage Leaves"""
    _name = "manage.leave"
    _description = "Manage Leaves"
    _inherit = 'mail.thread'
    _rec_name = "student_id"

    student_id = fields.Many2one('student.reg', ondelete='cascade', required=True, string="Student Name")
    class_id = fields.Many2one(related='student_id.current_class_id')

    start_date = fields.Date( required=True)
    end_date = fields.Date()
    total_days = fields.Float(compute='_compute_total_days',store=True)
    # delta = timedelta(days=1)

    half_day = fields.Boolean()
    fn_an = fields.Selection(selection=[('fn', 'FN'), ('an', 'AN')])
    reason = fields.Text(required=True)

    website_created = fields.Boolean("Created from Website", default=False)

    @api.depends('start_date','end_date','half_day')
    def _compute_total_days(self):
        """Total days of leave calculating"""
        for rec in self:
            rec.total_days = 0
            new_date = rec.start_date
            if new_date and rec.end_date:
                if new_date > rec.end_date:
                    raise ValidationError("Check the Start date and End date")
                else:
                    while new_date <= rec.end_date:
                        new_date += timedelta(days=1)
                        if new_date.weekday() not in [0,6]:  #6 is sat, 0 is sun
                            rec.total_days += 1
            if rec.half_day:
                rec.end_date = rec.start_date
                rec.total_days = 0.5

    @api.constrains('total_days')
    def _check_days(self):
        """Total Days checking"""
        if self.total_days < 0.5:
            raise ValidationError("Total days must be a positive integer")






    # @api.onchange('student_id')
    # def _onchange_student_id(self):
    #     """Students in the selected class only"""
    #     self.write({
    #         'class_id': self.student_id.current_class_id
    #     })


  # @api.onchange('half_day')
    # def half_day_change(self):
    #     """Half Day leave"""
    #     if self.half_day:
    #         self.end_date = self.start_date
    #         self.total_days = '0.5'
    #
    #     else:
    #         self.end_date = self.start_date = ""
    #         self.total_days = ""