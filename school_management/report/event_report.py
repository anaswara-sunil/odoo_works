# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError


class EventReport(models.AbstractModel):
    _name = 'report.school_management.report_event'

    @api.model
    def _get_report_values(self,docids,data=None):
        """Setting datas to the template"""
        # print(data,'data')
        # docs = self.env['manage.event'].browse(docids)
        query = """select mc.name as club,
                            me.start_date,me.end_date,me.name,me.state from manage_event as me
                            inner join manage_club_manage_event_rel as mce on mce.manage_event_id = me.id
							inner join manage_club as mc on mc.id = mce.manage_club_id
                            where 1=1"""
    # club based
        if data.get('club_id'):
            query += """ and mce.manage_club_id = '%s'""" % (data.get('club_id'))
    # month based
        if data.get('month_week_day') == 'month':
            query += """ and me.start_date >= '%s' """ % (
                fields.Date.to_string(fields.Date.today().replace(day=1)))
    # week based
        if data.get('month_week_day') == 'week':
            start = fields.Date.today() - timedelta(days=fields.Date.today().weekday())
            end = start + timedelta(days=6)
            query += """ and me.start_date >= '%s' and me.start_date <= '%s' """ % (start,end)
    #Day based
        if data.get('month_week_day') == 'day':
            query += """ and me.start_date <= '%s' and me.end_date >= '%s' """ % (fields.Date.today(),fields.Date.today())
    # custom date based
        if data.get('start_date'):
            query += (""" and me.start_date >= '%s' and me.end_date <= '%s'"""
                      % (data.get('start_date'), data.get('end_date')))

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        # print(report,'report')
        if not report:
            raise UserError(_('No Data Found'))

        state_dict = dict(self.env['manage.event']._fields['state'].selection)

        return {
            'doc_ids': docids,
            'doc_model': 'event_wizard',
            # 'docs': docs,
            'data': data,
            'report' : report,
            'date': fields.Date.today(),
            'state_dict':state_dict,
        }


