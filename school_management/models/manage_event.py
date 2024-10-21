# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date
from datetime import timedelta
from odoo.exceptions import ValidationError

class ManageEvent(models.Model):
    """Manage Events"""
    _name = "manage.event"
    _description = "Manage Events"
    _inherit = 'mail.thread'

    name = fields.Char('Event')
    start_date = fields.Date(default=fields.Datetime.now, copy=False, string="Start Date")
    end_date = fields.Date(default=fields.Datetime.now, copy=False, string="End Date")
    club_ids = fields.Many2many('manage.club', string="Clubs")
    active = fields.Boolean(default=True)
    event_poster = fields.Binary(string='Upload Poster')
    event_description = fields.Html()
    website_created = fields.Boolean("Created from Website", default=False)
    # image=fields.Image()

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('announced', 'Announced'),
        ('done','Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', required=True, readonly=True, copy=False,
        tracking=True, default='draft')



    def action_button_confirm(self):
        """Confirm button action"""
        self.write({
            'state': "announced"
        })
        # self.status = dict(self._fields['state'].selection).get(self.state)
        # print(self.status)

    def action_button_cancel(self):
        """Cancel button action"""
        self.write({
            'state': "cancelled"
        })

    def action_button_done(self):
        """Done button action"""
        current_date = date.today()
        if self.end_date <= current_date:
            self.write({'state': 'done'})
        else:
            raise ValidationError('Event is not yet over!!!')
        # var = dict(self._fields['state'].selection).get(self.state)
        # print(var)

    def archive_event(self):
        """Scheduled Archiving Action"""
        # print(self)
        # print(self.name)
        today = date.today()
        events = self.search(
            ['|',('state', '=', 'done'),('end_date', '<', today)])
        # events = self.env['manage.event'].search(
        #     ['|', ('state', '=', 'done'), ('end_date', '<', today)])
        # print(events)
        if  events:
            # print('done state')
            events.write({
                'active': False,
            })

    def send_email(self):
        """Automated Email """
        today = date.today()
        reminder_date = today + timedelta(days=2)
        # print(reminder_date)
        events = self.search([('start_date', '=', reminder_date)])
        employees = self.env['res.partner'].search(
            [('contact_type', 'in' , ['office_staff','teacher'])])
        # print(employees.id)
        # print(employees)
        # print(events)
        for rec in events:
            email_values = {
                'email_cc': False,
                'email_to': [employee.email for employee in employees],
            }
            # print(email_values)

            mail_template = self.env.ref('school_management.email_template_name')

            mail_template.send_mail(rec.id,email_values = email_values, force_send=True)




    # @api.constrains('state')
    # def _check_state(self):
    #     print(self.state)
    #     var ={
    #         'state_value' : dict(self._fields['state'].selection).get(self.state)
    #     }
    #     print(var)
    #     # return self.env..ref('report.school_management.report_event')(None,var=var)
    #     return {
    #          'var' :  var,
    #         'res_model':'report.school_management.report_event',
    #             }
    #
